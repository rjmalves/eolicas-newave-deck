#! /bin/bash

USERINSTALLDIR=/usr/lib
INSTALLDIR=${USERINSTALLDIR}/eolicas-newave/deck
echo "Removendo arquivos da instalação em ${INSTALLDIR}" 
[ -d $INSTALLDIR ] && rm -r $INSTALLDIR

EXECPATH=/usr/bin/eolicas-newave-deck
echo "Removendo executável em ${EXECPATH}" 
[ -f $EXECPATH ] && rm $EXECPATH
echo "Finalizando..."

