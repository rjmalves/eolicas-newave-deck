#!/bin/bash

arq=$1
enc=$2

# Converte o arquivo para UTF-8
iconv -f $enc -t "UTF-8" $arq -o $arq.tmp
mv $arq.tmp $arq