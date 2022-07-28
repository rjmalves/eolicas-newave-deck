import app.domain.commands as commands
from app.utils.log import Log
import pathlib
import tempfile
import os
from zipfile import ZipFile, ZIP_DEFLATED


def extract_file(command: commands.ExtractZipFile):
    Log.log().info(
        f"Extraindo {command.filename} em"
        + f" {command.zippath} para {command.targetdir}"
    )
    with ZipFile(command.zippath) as localzipfile:
        localzipfile.extract(command.filename, command.targetdir)


def compress_file(command: commands.AddFileToZip):
    Log.log().info(
        f"Comprimindo {command.filename} em"
        + f" {command.srcdir} para {command.zippath}"
    )
    tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(command.zippath))
    os.close(tmpfd)

    with ZipFile(command.zippath, "r") as zin:
        with ZipFile(tmpname, "w") as zout:
            zout.comment = zin.comment
            for item in zin.infolist():
                if item.filename != command.filename:
                    zout.writestr(item, zin.read(item.filename))

    os.remove(command.zippath)
    os.rename(tmpname, command.zippath)

    with ZipFile(command.zippath, mode="a", compression=ZIP_DEFLATED) as zf:
        srcpath = (
            pathlib.Path(command.srcdir).resolve().joinpath(command.filename)
        )
        zf.write(srcpath, command.filename)
