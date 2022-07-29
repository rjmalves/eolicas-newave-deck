from typing import List, Tuple, Optional
import time
import subprocess
import sys

TIMEOUT_DEFAULT = 10


def run_terminal(
    cmds: List[str], timeout: float = TIMEOUT_DEFAULT
) -> Tuple[Optional[int], List[str]]:
    cmd = " ".join(cmds)
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, shell=True, universal_newlines=True
    )
    start_t = time.time()
    out_lines: List[str] = []
    while True:
        std = process.stdout
        if std is None:
            raise ValueError("Erro no subprocess")
        out = std.readline()
        out_lines.append(out.strip())
        code = process.poll()
        if code is not None:
            for out in std.readlines():
                out_lines.append(out.strip())
            break
        current_t = time.time()
        if current_t - start_t > timeout:
            break
        time.sleep(0.5)
    process.terminate()
    return code, out_lines


def __convert_encoding_windows(path: str) -> Optional[int]:
    converting_command = (
        f"Get-Content {path} | Out-File -encoding utf8 -filepath {path}"
    )
    c, _ = run_terminal(["powershell", "-Command", converting_command])
    return c


def __convert_encoding_unix(path: str, script: str) -> Optional[int]:
    _, out = run_terminal([f"file -i {path}"])
    cod = out[0].split("charset=")[1].strip()
    c: Optional[int] = 0
    if all([cod != "utf-8", cod != "us-ascii", cod != "binary"]):
        cod = cod.upper()
        c, _ = run_terminal([f"{script}" + f" {path} {cod}"])
        return c
    return c


def convert_encoding(path: str, script: str) -> int:
    platform = sys.platform
    ret: Optional[int] = 0
    if platform in ["cygwin", "linux"]:
        ret = __convert_encoding_unix(path, script)
    elif platform in ["win32"]:
        ret = __convert_encoding_windows(path)
    return ret if ret is not None else 255
