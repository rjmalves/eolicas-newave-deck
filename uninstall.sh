#! /bin/bash

echo "Removendo arquivos da instalação..." 
TMPDIR=$(dirname $(mktemp -u))
INSTALLDIR=${TMPDIR}/eolicas-newave-deck
[ -d $INSTALLDIR ] && rm -r $INSTALLDIR

echo "Finalizando..."

