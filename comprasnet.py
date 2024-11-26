from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Função para destacar elementos
def highlight_element(driver, element):
    """Destaca um elemento na página."""
    driver.execute_script("arguments[0].style.border='3px solid red'", element)
    time.sleep(1)
    driver.execute_script("arguments[0].style.border=''", element)

# Função para adicionar mensagem na página
def add_message(driver, message):
    """Adiciona uma mensagem na página."""
    # Usando aspas duplas para evitar problemas com f-string
    script = (
        "var msg = document.createElement('div');"
        "msg.innerHTML = '" + message.replace("'", "\\'") + "';"  # Escapando aspas simples
        "msg.style.position = 'fixed';"
        "msg.style.top = '10px';"
        "msg.style.left = '10px';"
        "msg.style.backgroundColor = 'white';"
        "msg.style.border = '1px solid black';"
        "msg.style.padding = '10px';"
        "msg.style.zIndex = 10000;"
        "document.body.appendChild(msg);"
    )
    driver.execute_script(script)

# Função para ensinar a acessar ComprasNet
def guide():
    # Navega para a página do Google
    driver = webdriver.Firefox()
    
    # Maximiza a janela do navegador
    driver.maximize_window()

    driver.get("https://www.google.com")

    # Espera a página carregar
    time.sleep(2)

    # Destaca a barra de pesquisa
    search_box = driver.find_element(By.NAME, "q")
    highlight_element(driver, search_box)
    add_message(driver, "1. Use a barra de pesquisa e digite 'comprasnet'.")
    print("1. Use a barra de pesquisa e digite 'comprasnet'.")

    # Espera o usuário interagir
    user_completed = False
    while not user_completed:
        if search_box.get_attribute("value"):  # Se o campo de pesquisa tiver valor
            user_completed = True
        time.sleep(1)

    add_message(driver, "Ótimo! Agora, pressione a tecla 'Enter' ou clique no botão 'Pesquisa Google'.")
    print("Ótimo! Agora, pressione a tecla 'Enter' ou clique no botão 'Pesquisa Google'.")

    # Destaca o botão de pesquisa
    search_button = driver.find_element(By.NAME, "btnK")
    highlight_element(driver, search_button)

    # Espera o usuário clicar no botão de pesquisa
    user_clicked = False
    while not user_clicked:
        try:
            if driver.find_element(By.ID, "result-stats"):  # Se os resultados aparecerem
                user_clicked = True
        except:
            pass
        time.sleep(1)

    # Destaca o próximo conjunto de resultados
    results = driver.find_elements(By.CSS_SELECTOR, "h3")
    if results:
        add_message(driver, "Aqui está o site do comprasnet. Clique no link para acessar.")
        print("Aqui está o site do comprasnet. Clique no link para acessar.")
        highlight_element(driver, results[0])

    # Espera o usuário clicar no resultado
    user_clicked_result = False
    while not user_clicked_result:
        try:
            if driver.current_url.startswith("http://www.comprasnet.gov.br/"):  # Se o usuário acessou o site
                user_clicked_result = True
        except:
            pass
        time.sleep(1)

    add_message(driver, "Ótimo! Agora você sabe como procurar e acessar o site comprasnet.")
    print("Ótimo! Agora você sabe como procurar e acessar o site comprasnet.")

    # Espera antes de fechar
    time.sleep(5)

    # Fecha o navegador
    driver.quit()

if __name__ == "__main__":
    guide()