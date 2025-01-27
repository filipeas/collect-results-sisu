from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Função para ler o valor de 'i' do arquivo
def ler_valor_i():
    try:
        with open("i.txt", "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0  # Se o arquivo não existir, começa do início

# Função para salvar o valor de 'i' no arquivo
def salvar_valor_i(i):
    with open("i.txt", "w") as f:
        f.write(str(i))

diretorio_projeto = os.path.dirname(os.path.abspath(__file__))
diretorio_downloads = os.path.join(diretorio_projeto, "downloads")

# Configuração do WebDriver
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": diretorio_downloads}  # Define o diretório de download
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)

try:
    # Acessar a página
    url = "https://sisu.mec.gov.br/#/selecionados"
    driver.get(url)

    wait = WebDriverWait(driver, 8)

    # Clicar no combobox para abrir a lista
    combobox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ng-select")))
    combobox.click()
    time.sleep(2)  # Esperar a lista carregar

    # Obter todos os itens da lista
    options = driver.find_elements(By.CSS_SELECTOR, ".ng-option")
    # print(options)

    # Começar o loop a partir do índice salvo (ou 0, se não houver índice salvo)
    inicio = ler_valor_i()

    # Iterar sobre os itens e clicar em cada um
    for i in range(inicio, len(options)):
        try:
            # time.sleep(5)
            # Clicar no combobox para abrir a lista
            combobox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ng-select")))
            combobox.click()
            time.sleep(2)  # Esperar a lista carregar

            # Selecionar o item da lista
            options_tmp = driver.find_elements(By.CSS_SELECTOR, ".ng-option")
            options_tmp[i].click()

            # Confirmar se um item foi selecionado
            selected_value = combobox.text
            print(f"Instituição selecionada: {selected_value}")

            # Agora, podemos clicar no botão "Pesquisar"
            search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-botao")))
            search_button.click()
            
            # Aguardar a página carregar
            time.sleep(5)

            # Buscar o link do CSV
            csv_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href$='.csv']")))
            csv_url = csv_link.get_attribute("href")

            print(f"Arquivo CSV encontrado: {csv_url}")

            # Baixar o arquivo CSV
            driver.get(csv_url)
            print("Download iniciado...")

            # Salvar o índice 'i' após cada iteração para continuar depois
            salvar_valor_i(i + 1)  # Salva o próximo índice a ser processado
        except Exception as e:
            print(f"Erro ao processar o item {i}: {e}")
            continue  # Em caso de erro, continua o loop
finally:
    time.sleep(10)
    driver.quit()
