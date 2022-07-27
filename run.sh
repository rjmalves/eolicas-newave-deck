# Variaveis importantes

WORKDIR=$PWD
DIR_ENCADEADOR=~/rotinas/encadeador-pem
ENCADEIA=$DIR_ENCADEADOR/main.py

echo Ativando o ambiente virtual
source $DIR_ENCADEADOR/venv/bin/activate

echo Mudando o diretorio para $WORKDIR
cd $WORKDIR

echo Executando o Encadeador
python3 $ENCADEIA

echo Desativando o ambiente virtual
deactivate
