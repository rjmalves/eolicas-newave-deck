from app.models.settings import Settings
import app.domain.commands as commands
from app.utils.log import Log
from typing import Optional
import pathlib
from app.services.unitofwork.newave import factory as nw_factory
from app.services.unitofwork.clusters import factory as clusters_factory
from app.services.handlers.files import compress_file, extract_file
from app.services.handlers.processing import (
    process_dger_data,
    process_patamar_data,
    process_sistema_data,
    generate_eolicacadastro,
    generate_eolicasubmercado,
    generate_eolicaconfig,
    generate_eolicafte,
    generate_eolicahistorico,
    generate_eolicageracao,
)
from app.services.handlers.validation import (
    validate_patamar_data,
    validate_sistema_data,
    validate_cluster_files,
)


class GenerationHandler:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._scriptpath = (
            pathlib.Path(self._settings.installdir)
            .resolve()
            .joinpath(self._settings.encoding_convert_script)
        )
        self._zippath = (
            pathlib.Path(self._settings.basedir)
            .resolve()
            .joinpath(self._settings.newave_deck_zip)
        )
        self._tmppath = pathlib.Path(self._settings.tmpdir)
        self._clusterspath = pathlib.Path(self._settings.clustersdir)
        # Extracts "caso.dat"
        command = commands.ExtractZipFile(
            str(self._zippath), self._settings.tmpdir, self._settings.caso_file
        )
        extract_file(command)
        # Instantiates UoW
        self._uow = nw_factory(
            "FS",
            self._zippath.parent,
            self._settings.caso_file,
            self._scriptpath,
        )
        self._tmpuow = nw_factory(
            "FS", self._tmppath, self._settings.caso_file, self._scriptpath
        )
        self._clustersuow = clusters_factory(
            "FS",
            self._clusterspath,
            self._settings.clusters_file,
            self._settings.installed_capacity_file,
            self._settings.ftm_file,
            self._settings.average_wind_file,
        )

    def extract_files_from_deck(self):
        # Extracts "arquivos.dat"
        with self._tmpuow:
            arquivos_filename = self._tmpuow.newave.caso.arquivos
        command = commands.ExtractZipFile(
            str(self._zippath), self._settings.tmpdir, arquivos_filename
        )
        extract_file(command)
        # Extracts the other necessary files
        with self._tmpuow:
            files_to_extract = [
                self._tmpuow.newave.arquivos.dger,
                self._tmpuow.newave.arquivos.sistema,
                self._tmpuow.newave.arquivos.patamar,
            ]
        for f in files_to_extract:
            command = commands.ExtractZipFile(
                str(self._zippath), self._settings.tmpdir, f
            )
            extract_file(command)

    def process_deck_data(self):
        dger_command = commands.ProcessDgerData(
            self._settings.parpmodel,
            self._settings.orderreduction,
            self._settings.generatewind,
            self._settings.windcutpenalty,
            self._settings.crosscorrelation,
            self._settings.swirlingconstraints,
            self._settings.defluenceconstraints,
        )
        patamar_command = commands.ProcessPatamarData(
            self._settings.nonsimulatedblock
        )
        sistema_command = commands.ProcessSistemaData(
            self._settings.nonsimulatedblock
        )
        self._dger_data = process_dger_data(dger_command, self._tmpuow)
        self._patamar_count, self._patamar_data = process_patamar_data(
            patamar_command, self._tmpuow
        )
        self._sistema_data = process_sistema_data(
            sistema_command, self._tmpuow
        )

    def __generate_eolicacadastro(self):
        comando = commands.GenerateEolicaCadastro(
            self._dger_data.month,
            self._dger_data.year,
            self._dger_data.pre_study_horizon,
            self._dger_data.study_horizon,
            self._dger_data.post_study_horizon,
        )
        generate_eolicacadastro(comando, self._tmpuow, self._clustersuow)

    def __generate_eolicasubmercado(self):
        comando = commands.GenerateEolicaSubmercado()
        generate_eolicasubmercado(comando, self._tmpuow, self._clustersuow)

    def __generate_eolicaconfig(self):
        comando = commands.GenerateEolicaConfig(
            self._dger_data.month,
            self._dger_data.year,
            self._dger_data.pre_study_horizon,
            self._dger_data.study_horizon,
            self._dger_data.post_study_horizon,
        )
        generate_eolicaconfig(comando, self._tmpuow, self._clustersuow)

    def __generate_eolicafte(self):
        comando = commands.GenerateEolicaFTE(
            self._dger_data.month,
            self._dger_data.year,
            self._dger_data.pre_study_horizon,
            self._dger_data.study_horizon,
            self._dger_data.post_study_horizon,
        )
        generate_eolicafte(comando, self._tmpuow, self._clustersuow)

    def __generate_eolicahistorico(self):
        comando = commands.GenerateEolicaHistorico()
        generate_eolicahistorico(comando, self._tmpuow, self._clustersuow)

    def __generate_eolicageracao(self):
        comando = commands.GenerateEolicaGeracao(
            self._dger_data.month,
            self._dger_data.year,
            self._dger_data.pre_study_horizon,
            self._dger_data.study_horizon,
            self._dger_data.post_study_horizon,
            self._patamar_count,
            self._patamar_data.blocks,
        )
        generate_eolicageracao(comando, self._tmpuow, self._clustersuow)

    def generate_deck_newfiles(self):
        self.__generate_eolicacadastro()
        self.__generate_eolicasubmercado()
        self.__generate_eolicaconfig()
        self.__generate_eolicafte()
        self.__generate_eolicahistorico()
        self.__generate_eolicageracao()

    def compress_files_to_deck(self):
        # Static
        installdir = pathlib.Path(self._settings.installdir).resolve()
        command = commands.AddFileToZip(
            self._zippath,
            installdir.joinpath(self._settings.static_file_path),
            self._settings.indice_file,
        )
        compress_file(command)
        # Generated during execution
        with self._tmpuow:
            files_to_compress = [
                self._tmpuow.newave.arquivos.dger,
                self._tmpuow.newave.arquivos.sistema,
                self._tmpuow.newave.arquivos.patamar,
                self._settings.eolicacadastro_file,
                self._settings.eolicasubmercado_file,
                self._settings.eolicaconfig_file,
                self._settings.eolicafte_file,
                self._settings.histventos_file,
                self._settings.eolicageracao_file,
            ]
        for f in files_to_compress:
            command = commands.AddFileToZip(
                self._zippath, self._settings.tmpdir, f
            )
            compress_file(command)

    def generate(self):
        if not self.validate():
            return
        # Reads essential information
        # Edits existing files
        Log.log().info(" ## PROCESSAMENTO DOS ARQUIVOS  ##")
        self.process_deck_data()
        # Generates each of the new deck files
        self.generate_deck_newfiles()
        # Adds new deck files to the zip
        self.compress_files_to_deck()

    def validate(self) -> bool:
        Log.log().info(" ## VALIDAÇÃO DOS ARQUIVOS  ##")
        valid_patamar = validate_patamar_data(
            commands.ValidatePatamarData(self._settings.nonsimulatedblock),
            self._tmpuow,
        )
        valid_sistema = validate_sistema_data(
            commands.ValidateSistemaData(self._settings.nonsimulatedblock),
            self._tmpuow,
        )
        valid_clusters = validate_cluster_files(self._clustersuow)
        valid = all([valid_patamar, valid_sistema, valid_clusters])
        if not valid:
            Log.log().error(
                "Validação dos arquivos não" + " concluída com sucesso."
            )
        else:
            Log.log().info("Arquivos validados com sucesso")
        return valid


def __construct_handler() -> Optional[GenerationHandler]:
    handler: Optional[GenerationHandler] = None
    try:
        settings = Settings()
        Log.configure_logging(settings.basedir)
        handler = GenerationHandler(settings)
    except Exception as e:
        print(f"Erro na leitura das configurações: {e}")
    return handler


def __greet():
    Log.log().info(
        " #### APLICAÇÃO PARA PROCESSAMENTO DO "
        + "DECK DE NEWAVE - GERAÇÃO EÓLICA ####"
    )


def __farewell():
    Log.log().info(" #### FIM DO PROCESSAMENTO ####")


def validate():
    handler = __construct_handler()
    if handler is not None:
        __greet()
        handler.extract_files_from_deck()
        handler.validate()
        __farewell()


def generate():
    handler = __construct_handler()
    if handler is not None:
        __greet()
        handler.extract_files_from_deck()
        handler.generate()
        __farewell()
