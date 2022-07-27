command -v python3 >/dev/null 2>&1
PYTHON3_INSTALLED=$?
if [ $PYTHON3_INSTALLED -ne 0 ]; then
    echo "Python 3 não foi encontrado!"
    exit $PYTHON3_INSTALLED
fi

printf "import tempfile\nprint(tempfile.gettempdir())" | python3