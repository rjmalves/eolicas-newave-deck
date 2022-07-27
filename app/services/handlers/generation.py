from app.models.settings import Settings
import app.domain.commands as commands
import pathlib
from app.services.unitofwork.newave import factory
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


class GenerationHandler:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._zippath = (
            pathlib.Path(self._settings.basedir)
            .resolve()
            .joinpath(self._settings.newave_deck_zip)
        )
        self._uow = factory("FS", self._zippath.parent)

    def extract_files_from_deck(self):
        # Extracts "arquivos.dat"
        with self._uow:
            arquivos_filename = self._uow.newave.caso.arquivos
        command = commands.ExtractZipFile(
            self._zippath, self._settings.tmpdir, arquivos_filename
        )
        extract_file(command)
        # Extracts the other necessary files
        with self._uow:
            files_to_extract = [
                self._uow.newave.arquivos.dger,
                self._uow.newave.arquivos.sistema,
                self._uow.newave.arquivos.patamar,
            ]
        for f in files_to_extract:
            command = commands.ExtractZipFile(
                self._zippath, self._settings.tmpdir, f
            )
            extract_file(command)

    def process_deck_data(self):
        dger_command = commands.ProcessDgerData(
            self._settings.generatewind, self._settings.windcutpenalty
        )
        patamar_command = commands.ProcessPatamarData(
            self._settings.nonsimulatedblock
        )
        sistema_command = commands.ProcessSistemaData(
            self._settings.nonsimulatedblock
        )
        self._dger_data = process_dger_data(dger_command, self._uow)
        self._patamar_data = process_patamar_data(patamar_command, self._uow)
        self._sistema_data = process_sistema_data(sistema_command, self._uow)

    def __generate_eolicacadastro(self):
        comando = commands.GenerateEolicaCadastro(
            self._dger_data.month,
            self._dger_data.year,
            self._dger_data.pre_study_horizon,
            self._dger_data.study_horizon,
            self._dger_data.post_study_horizon,
            self._settings.clustersdir,
            self._settings.clusters_file,
            self._settings.installed_capacity_file,
            self._settings.tmpdir,
            self._settings.eolicacadastro_file,
        )
        generate_eolicacadastro(comando, self._uow)

    def __generate_eolicasubmercado(self):
        comando = commands.GenerateEolicaSubmercado(
            self._settings.clustersdir,
            self._settings.clusters_file,
            self._settings.tmpdir,
            self._settings.eolicacadastro_file,
            self._settings.eolicasubmercado_file,
        )
        generate_eolicasubmercado(comando, self._uow)

    def __generate_eolicaconfig(self):
        comando = commands.GenerateEolicaConfig(
            self._dger_data.month,
            self._dger_data.year,
            self._dger_data.pre_study_horizon,
            self._dger_data.study_horizon,
            self._dger_data.post_study_horizon,
            self._settings.clustersdir,
            self._settings.clusters_file,
            self._settings.tmpdir,
            self._settings.eolicacadastro_file,
            self._settings.eolicaconfig_file,
        )
        generate_eolicaconfig(comando, self._uow)

    def __generate_eolicafte(self):
        comando = commands.GenerateEolicaFTE(
            self._dger_data.month,
            self._dger_data.year,
            self._dger_data.pre_study_horizon,
            self._dger_data.study_horizon,
            self._dger_data.post_study_horizon,
            self._settings.clustersdir,
            self._settings.ftm_file,
            self._settings.tmpdir,
            self._settings.eolicacadastro_file,
            self._settings.eolicafte_file,
        )
        generate_eolicafte(comando, self._uow)

    def __generate_eolicahistorico(self):
        comando = commands.GenerateEolicaHistorico(
            self._settings.clustersdir,
            self._settings.average_wind_file,
            self._settings.tmpdir,
            self._settings.eolicacadastro_file,
            self._settings.histventos_file,
        )
        generate_eolicahistorico(comando, self._uow)

    def __generate_eolicageracao(self):
        comando = commands.GenerateEolicaGeracao(
            self._dger_data.month,
            self._dger_data.year,
            self._dger_data.pre_study_horizon,
            self._dger_data.study_horizon,
            self._dger_data.post_study_horizon,
            self._patamar_data.blocks,
            self._settings.tmpdir,
            self._settings.eolicacadastro_file,
            self._settings.eolicasubmercado_file,
            self._settings.eolicageracao_file,
        )
        generate_eolicageracao(comando, self._uow)

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
        with self._uow:
            files_to_compress = [
                self._uow.newave.arquivos.dger,
                self._uow.newave.arquivos.sistema,
                self._uow.newave.arquivos.patamar,
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
        # Extracts files from the deck zip
        self.extract_files_from_deck()
        # Reads essential information
        # Edits existing files
        self.process_deck_data()
        # Generates each of the new deck files
        self.generate_deck_newfiles()
        # Adds new deck files to the zip
        self.compress_files_to_deck()


def generate():
    settings = Settings()
    handler = GenerationHandler(settings)
    handler.generate()
