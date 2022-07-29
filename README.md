# eolicas-newave-deck
Módulo de geração de decks, parte da aplicação responsável por processar dados provenientes de bases de dados das usinas eólicas e preparar casos do NEWAVE.


## Instalação

Este módulo deve ser instalado a partir dos scripts fornecidos no repositório. Este é copiado para um diretório temporário do sistema, onde o ambiente é configurado e as dependências são instaladas. Para isto, basta executar:
```sh
./install.sh
```

O script de instalação é aberto e pode ser modificado para atender as necessidades do usuário.

## Requisitos

Para o uso da aplicação é necessário ter uma instalação local do `python3` em versão superior ou igual à 3.7 e também do pacote para criação de ambientes virtuais. Na maioria das distribuições linux este recebe o nome de `python3-venv`.

Caso o script de instalação não detecte a instalação do Python, este irá interromper sua execução. Caso haja problemas com o pacote de criação de ambientes virtuais, será exibido o erro, que na maioria das distribuições orienta o comando necessário para instalação.

Uma das etapas finais do script é copiar o executável que serve de atalho para a aplicação para um diretório no `PATH` do sistema. Isto pode ser personalizado por cada usuário final, sendo que o valor default é em `$HOME/bin`.

```bash
# Copies the executable to a folder in the system's PATH
[ ! -d $HOME/bin ] && mkdir $HOME/bin
EXECPATH=$HOME/bin/eolicas-newave-deck
echo "Copiando executável para ${EXECPATH}" 
cp eolicas-newave-deck $EXECPATH
```

**IMPORTANTE:** O diretório `$HOME/bin` foi escolhido por padrão. Para que a aplicação funcione plenamente é necessário que este seja adicionado ao `PATH` do sistema, ou que o script de instalação seja editado para que o executável seja posicionado em um diretório que esteja no `PATH`. Caso a primeira opção seja escolhida, isto pode ser feito editando o arquivo `~/.bashrc`, como mostrado [neste link](https://askubuntu.com/questions/60218/how-to-add-a-directory-to-the-path).

## Exemplos de Uso

Uma vez instalada a aplicação, esta faz uso de informações provenientes da aplicação de clusterização de dados de usinas eólicas. A localização destes dados deve ser informada no momento de execução da aplicação, por meio de um parâmetro opcional. Caso contrário, a aplicação irá assumir que estão no próprio diretório de chamada.

Quando a aplicação é chamada, ela exibe a tela de ajuda inicial:

```
eolicas-newave-deck
Gerência de Metodologias e Modelos Energéticos - PEM / ONS
Versão 1.0.0 - 29/07/2022
Ativando o ambiente virtual
Executando
------------------
python3 /tmp/eolicas-newave-deck/main.py
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  Aplicação CLI para geração de decks de NEWAVE com informações de clusters de
  usinas eólicas.

Options:
  --help  Show this message and exit.

Commands:
  geradeck        Processa o deck, realiza as alterações necessárias e...
  validaarquivos  Valida o deck para o processamento.
------------------
Desativando o ambiente virtual
```

### Comando **validaarquivos**

O primeiro modo de execução da aplicação é responsável por validar os arquivos do NEWAVE existentes dentro do ZIP e os arquivos com dados da clusterização das usinas eólicas, existentes ou no próprio diretório de chamada da aplicação ou em caminho especificado com a opção `--clusters`. Um exemplo de chamada da aplicação é:

```bash
➜  teste_app_eolica ls
deck_newave_base.zip  eolicas-newave-deck.cfg  ne1s1
➜  eolicas-newave-deck validaarquivos --clusters ne1s1 deck_newave_base.zip
```

O comando também possui uma tela de ajuda com `--help`:

```
➜  teste_app_eolica eolicas-newave-deck validaarquivos --help
eolicas-newave-deck
Gerência de Metodologias e Modelos Energéticos - PEM / ONS
Versão 1.0.0 - 29/07/2022
Ativando o ambiente virtual
Executando
------------------
python3 /tmp/eolicas-newave-deck/main.py validaarquivos --help
Usage: main.py validaarquivos [OPTIONS] DECK

  Valida o deck para o processamento. Confere se os arquivos necessários estão
  no ZIP e se contém as informações necessárias no processamento.

  DECK: arquivos de entrada do NEWAVE comprimidos em um .zip

Options:
  --clusters TEXT  diretório com os arquivos resultantes da clusterização
  --help           Show this message and exit.
------------------
Desativando o ambiente virtual
```


### Comando **geradeck**

O segundo modo de execução da aplicação é responsável por realizar as alterações no deck do NEWAVE fornecido dentro do ZIP a partir das configurações escolhidas e dos arquivos com dados da clusterização das usinas eólicas. Um exemplo de chamada da aplicação é:

```bash
➜  teste_app_eolica ls
deck_newave_base.zip  eolicas-newave-deck.cfg  ne1s1
➜  eolicas-newave-deck geradeck --clusters ne1s1 deck_newave_base.zip
```

O comando também possui uma tela de ajuda com `--help`:

```
➜  teste_app_eolica eolicas-newave-deck geradeck --help
eolicas-newave-deck
Gerência de Metodologias e Modelos Energéticos - PEM / ONS
Versão 1.0.0 - 29/07/2022
Ativando o ambiente virtual
Executando
------------------
python3 /tmp/eolicas-newave-deck/main.py geradeck --help
Usage: main.py geradeck [OPTIONS] DECK

  Processa o deck, realiza as alterações necessárias e gera os arquivos novos
  para consideração da geração eólica.

  DECK: arquivos de entrada do NEWAVE comprimidos em um .zip

Options:
  --clusters TEXT  diretório com os arquivos resultantes da clusterização
  --help           Show this message and exit.
------------------
Desativando o ambiente virtual
➜  teste_app_eolica
```

## Manual de Uso

Informações mais detalhadas sobre o uso da aplicação podem ser encontradas no manual, disponível [aqui](https://github.com/rjmalves/eolicas-newave-deck/wiki/Manual-da-Aplica%C3%A7%C3%A3o).

## Desinstalação

Caso seja desejado eliminar os arquivos de instalação do módulo, pode ser usado o script de desinstalação, existente no mesmo repositório:
```sh
./uninstall.sh
```