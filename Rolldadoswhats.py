#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Para simular a tecla "Enter"
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Caminho do seu WebDriver
service = Service(executable_path=r'C:\Users\kezin\Downloads\edgedriver_win64\webdriver\msedgedriver.exe')
driver = webdriver.Edge(service=service)  # Usando o Service para o WebDriver

driver.get('https://web.whatsapp.com')  # Acesse o WhatsApp Web

print("📲 Escaneie o QR Code no WhatsApp Web para continuar...")
time.sleep(15)  # Atraso para escanear o QR Code e carregar o WhatsApp Web

# Função para encontrar e abrir o grupo
def abrir_grupo(nome_do_grupo):
    try:
        # Espera até que o grupo esteja visível
        group_xpath = f"//span[@title='{nome_do_grupo}']"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, group_xpath)))
        
        group = driver.find_element(By.XPATH, group_xpath)
        group.click()  # Clica no grupo
        print(f"🔍 Grupo '{nome_do_grupo}' encontrado e aberto!")
    except Exception as e:
        print(f"Erro ao abrir o grupo '{nome_do_grupo}': {e}")

# Função para enviar uma mensagem
def enviar_mensagem(mensagem):
    try:
        # Aguarda a caixa de entrada estar disponível
        input_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//footer//div[@contenteditable="true"]'))
        )
        input_box.click()  # Clica para ativar
        input_box.send_keys(mensagem)  # Digita a mensagem
        time.sleep(1)  # Dá um tempo para o WhatsApp processar
        
        # Pressiona Enter para enviar
        input_box.send_keys(Keys.ENTER)
        
        print(f"✅ Mensagem enviada: {mensagem}")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
# Função para monitorar novas mensagens no grupo
def monitorar_mensagens():
    last_message = ""
    while True:
        try:
            # Espera até que o container de mensagens esteja visível
            message_container_xpath = '//div[contains(@class, "copyable-text")]'
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, message_container_xpath))
            )

            # Pega todas as mensagens visíveis
            messages = driver.find_elements(By.XPATH, message_container_xpath)

            if messages:
                # Pega a última mensagem
                current_message = messages[-1].text
                if current_message != last_message:
                    print(f"🔄 Nova mensagem detectada: {current_message}")
                    last_message = current_message
                    
                    # Se a mensagem contiver um comando para rolar o dado
                    if "rolar 1d20" in current_message or "rolar_d20" in current_message or "rolar _d20" in current_message:
                        # Rola o dado e envia a resposta
                        dado_resultado = random.randint(1, 20)
                        enviar_mensagem(f"O resultado do dado é: {dado_resultado}")
                else:
                    print("🔄 Nenhuma mensagem nova detectada.")
            else:
                print("🔄 Nenhuma mensagem nova detectada.")

            time.sleep(3)  # Espera 3 segundos antes de verificar novamente
        except Exception as e:
            print(f"Erro ao monitorar mensagens: {e}")
            break

# Abrir o grupo com o nome '#HATAROS'
abrir_grupo('#HATAROS')

# Monitorar as mensagens e responder automaticamente
monitorar_mensagens()


# In[ ]:





# In[ ]:




