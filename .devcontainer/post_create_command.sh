#!/bin/bash

# Criar o ambiente virtual
python -m venv .venv

# Ativar o ambiente virtual
# Para sistemas Unix (Linux, macOS):
source .venv/bin/activate

# Para sistemas Windows, use:
# .\.venv\Scripts\activate

# Atualizar pip
pip install --upgrade pip

# Instalar as dependências do arquivo requirements.txt
pip install -r requirements.txt
