import app.domain.commands as commands
import pathlib
from zipfile import ZipFile, ZIP_DEFLATED


def extract_file(command: commands.ExtractZipFile):
    with ZipFile(command.zippath) as localzipfile:
        localzipfile.extract(command.filename, command.targetdir)


def compress_file(command: commands.AddFileToZip):
    with ZipFile(
        command.zippath, "w", compression=ZIP_DEFLATED
    ) as localzipfile:
        srcpath = (
            pathlib.Path(command.srcdir).resolve().joinpath(command.filename)
        )
        localzipfile.write(srcpath, command.filename)
