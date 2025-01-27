#!/bin/bash

# Remover pasta downloads se existir
if [ -d "downloads" ]; then
    echo "Removendo pasta 'downloads' existente..."
    rm -rf downloads
fi

# Criar pasta downloads
echo "Criando pasta downloads..."
mkdir downloads

# Remover o ambiente virtual se existir
if [ -d "selenium_env" ]; then
    echo "Removendo ambiente virtual existente..."
    rm -rf selenium_env
fi

# Criar um novo ambiente virtual
echo "Criando ambiente virtual..."
python3 -m venv selenium_env

# Ativar o ambiente virtual
source selenium_env/bin/activate

# Atualizar pip e instalar dependências
echo "Instalando dependências no ambiente virtual..."
pip install --upgrade pip
pip install selenium
pip install pandas

# Instalar o Google Chrome (caso não esteja instalado)
if ! command -v google-chrome &> /dev/null
then
    echo "Instalando Google Chrome..."
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
    sudo apt update
    sudo apt install -y google-chrome-stable
fi

# Obter a versão do Chrome instalada
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d. -f1)

# Baixar e instalar o ChromeDriver compatível dentro do ambiente virtual
echo "Baixando ChromeDriver para versão $CHROME_VERSION..."
wget -O selenium_env/chromedriver.zip "https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION)/chromedriver_linux64.zip"

unzip selenium_env/chromedriver.zip -d selenium_env/
chmod +x selenium_env/chromedriver

# Testar instalação
echo "Verificando instalação..."
selenium_env/chromedriver --version
python -c "import selenium; print('Selenium instalado com sucesso!')"

echo "Setup concluído! 🚀"
echo "Para ativar o ambiente virtual, use: source selenium_env/bin/activate"
