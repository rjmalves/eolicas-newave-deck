#! /bin/bash


# Checks if Python 3 is installed
command -v python3 >/dev/null 2>&1
PYTHON3_INSTALLED=$?
if [ $PYTHON3_INSTALLED -ne 0 ]; then
    echo "Python 3 não foi encontrado!"
    exit $PYTHON3_INSTALLED
fi

# Creates installation directory in /tmp 
TMPDIR=$(dirname $(mktemp -u))
INSTALLDIR=${TMPDIR}/eolicas-newave-deck
[ ! -d $INSTALLDIR ] && mkdir $INSTALLDIR

# Copies necessary files
cp -r app/ $INSTALLDIR
cp main.py $INSTALLDIR
cp requirements.txt $INSTALLDIR
cp run.sh $INSTALLDIR

# Creates venv is not exists
[ ! -d $INSTALLDIR/venv ] && python3 -m venv $INSTALLDIR/venv

# Activates venv and installs requirements
CURDIR=pwd
cd $INSTALLDIR
source venv/bin/Activates
pip install -r requirements.txt

# Deactivates venv
deactivate
cd $CURDIR
