# %%
# Automação de Whatsapp - Encaminhamento de mensagens
# Encaminhar para uma lista de contatos ou de grupos
# Encaminhar de 5 em 5 contatos/grupos

# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyperclip
import time

# Inicializar o navegador
service = Service(ChromeDriverManager().install())
nav = webdriver.Chrome(service=service)
nav.get("https://web.whatsapp.com")

# %%
mensagem = """Mensagem a ser enviada
"""

lista_contatos = ["Meu Numero", "Grupo1", "Grupo2", "Grupo3", "Grupo4", "Grupo5"]

# enviar a mensagem para o Meu Numero para poder depois encaminhar
def enviar_mensagem(contato, mensagem):
    # clicar na lupa e buscar o contato
    nav.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div/button/div[2]/span').click()
    search_box = nav.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p')
    search_box.send_keys(contato)
    search_box.send_keys(Keys.ENTER)
    
    # esperar o chat carregar
    WebDriverWait(nav, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')))
    
    # escrever a mensagem para nós mesmos
    pyperclip.copy(mensagem)
    nav.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p').send_keys(Keys.CONTROL + "v")
    nav.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p').send_keys(Keys.ENTER)
    time.sleep(2)

enviar_mensagem("Meu Numero", mensagem)

# %%
# encaminhar a mensagem para a lista de contatos
qtde_contatos = len(lista_contatos)
qtde_blocos = (qtde_contatos + 4) // 5  # Calcula a quantidade de blocos de 5 contatos

for i in range(qtde_blocos):
    # rodar o código de encaminhar
    i_inicial = i * 5
    i_final = (i + 1) * 5
    lista_enviar = lista_contatos[i_inicial:i_final]

    # selecionar a mensagem para enviar e abre a caixa de encaminhar
    lista_elementos = nav.find_elements(By.CLASS_NAME, '_2AOIt')
    for item in lista_elementos:
        mensagem_sanitizada = mensagem.replace("\n", "").strip()
        texto = item.text.replace("\n", "").strip()
        if mensagem_sanitizada in texto:
            elemento = item
            break
    else:
        print("Mensagem não encontrada!")
        continue
    
    ActionChains(nav).move_to_element(elemento).perform()
    elemento.find_element(By.CLASS_NAME, '_3u9t-').click()
    time.sleep(0.5)
    nav.find_element(By.XPATH, '//*[@id="app"]/div/span[4]/div/ul/div/li[4]/div').click()
    nav.find_element(By.XPATH, '//*[@id="main"]/span[2]/div/button[4]/span').click()
    time.sleep(1)

    for nome in lista_enviar:
        # selecionar os 5 contatos para enviar
        # escrever o nome do contato
        search_box = nav.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div[1]/p')
        search_box.send_keys(nome)
        time.sleep(1)
        # dar enter
        search_box.send_keys(Keys.ENTER)
        time.sleep(1)
        # apagar o nome do contato
        search_box.clear()

    nav.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/span/div/div/div/span').click()
    time.sleep(3)



