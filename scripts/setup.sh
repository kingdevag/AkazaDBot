#!/bin/bash

echo "Creando lo nesesario...";
echo "Creando carpetas"
mkdir json
ls -l json
mkdir server
ls -l server
echo "Creando archivos"
cd json
touch prefixes.json
ls -l prefixes.json
echo "{}" > prefixes.json
cd ..
cd json
touch database.json
ls -l database.json
echo "{}" > database.json
ls
echo Instalando Dependencias
pip install -r docs/requirements.txt
pip list
echo Para mas Ayuda consulta instructions.md