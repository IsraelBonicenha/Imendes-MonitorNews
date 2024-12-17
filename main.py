# !!! COMANDOS PARA BUILDAR O PROJETO !!!

# py -m venv venv (powershell)
# venv\Scripts\Activate
# pip install requests colorama termcolor pyfiglet plyer pyinstaller
# pyinstaller -n MonitorNews --onefile --hidden-import=pyfiglet --hidden-import=plyer.platforms.win --hidden-import=plyer.platforms.win.notification --add-data "C:\\Users\\israe\\Documents\\Desenvolvimento\\Imendes-MonitorNews\\venv\\Lib\\site-packages\\pyfiglet\\fonts;pyfiglet/fonts" main.py

import os
import sys
import time
import requests
import warnings
from colorama import Fore, Back
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
from termcolor import colored
from pyfiglet import figlet_format
from plyer import notification

# Mensagens Padronizadas
def msg_sucesso(msg):
    print(colored(f"✅          {msg}", "green"))
    time.sleep(2)

def msg_erro(msg):
    print(colored(f"❌           {msg}", "red"))
    time.sleep(2)

def msg_info(msg):
    print(colored(f"{msg}", "blue"))
    time.sleep(2)

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")
    print(colored(figlet_format("MONITOR   NEWS", font="Standard"), "white"))
    print("=" * 75)

# Função para salvar dados no arquivo
def salvar_dados(arqvo_data, data_dict):
    msg_sucesso("Dados salvos no arquivo com sucesso")
    with open(arqvo_data, "w") as arquivo:
        for chave, valor in data_dict.items():
            arquivo.write(f"{chave}:{valor}\n")

# Função para carregar dados do arquivo
def carregar_dados(arqvo_data):
    if not os.path.exists(arqvo_data):
        return {}
    with open(arqvo_data, "r") as arquivo:
        linhas = arquivo.readlines()
        return {linha.split(":")[0]: int(linha.split(":")[1].strip()) for linha in linhas}

# Função para verificar alterações
def verificar_alteracoes(url, chave, data_dict):
    warnings.simplefilter("ignore", InsecureRequestWarning)
    resposta = requests.get(url, verify=False)
    time.sleep(2)

    if resposta.status_code == 200:
        html_page = resposta.text
        numero_atual = html_page.count("</tr>") - 1  # -1 por causa do cabeçalho
        numero_antigo = data_dict.get(chave, 0)

        # Exibir comparações detalhadas
        print(f"\n{chave.capitalize().upper()}")
        print(f"    Número antigo: {numero_antigo}")
        print(f"    Número  atual: {numero_atual}")
        time.sleep(2)

        if numero_atual > numero_antigo:
            data_dict[chave] = numero_atual
            msg_sucesso(f"Alteração detectada em {chave}")
            return True
        print(f"            Nenhuma alteração detectada em {chave}")
        return False
    else:
        msg_erro(f"Erro ao acessar {url}. Status Code: {resposta.status_code}")
        return False

# Função para enviar notificação para o usuário com mensagem personalizada
def enviar_notificacao(titulo, mensagem):
    notification.notify(
        title=titulo,
        message=mensagem,
        timeout=30  # 10 segundos para exibir a notificação
    )
    msg_info("            Notificação enviada ao usuário")


# Função para solicitar confirmação do usuário
def confirmar_usuario():
    input(colored("Pressione ENTER para continuar após visualizar a notificação", "white"))


def verificar_nova_versao(versao_atual):
    url = "https://raw.githubusercontent.com/IsraelBonicenha/Installers-Updates/main/MonitorNews/version.txt"

    try:
        # Faz a requisição HTTP
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve erros na requisição

        # Obtém o conteúdo do arquivo
        version = response.text.strip()

        print(f"Versão atual: {versao_atual}")
        print(f"Versão disponível: {version}")

        if versao_atual == version:
            msg_sucesso("O usuário já está atualizado")
            time.sleep(1.5)
        else:
            print("Inciando o donwload das atualiações...")
            time.sleep(1.5)
            os.startfile("C:\\MonitorNews\\Update - MonitorNews.exe")
            sys.exit()

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar o arquivo: {e}")

# Função principal modificada
def monitorar():
    while True:
        clear_terminal()
        print()
        print()
        msg_info("MONITORANDO SITES")

        ano_atual = datetime.now().year
        pasta_data = "data"
        arqvo_data = f"{pasta_data}/data{ano_atual}.txt"
        urls = {
            "protocolos": f"https://www.confaz.fazenda.gov.br/legislacao/protocolos/{ano_atual}",
            "convenios": f"https://www.confaz.fazenda.gov.br/legislacao/convenios/{ano_atual}"
        }

        # Criar pasta de dados se não existir
        if not os.path.exists(pasta_data):
            os.makedirs(pasta_data)

        # Carregar ou inicializar arquivo de dados
        data_dict = carregar_dados(arqvo_data)
        if not data_dict:
            for chave in urls:
                warnings.simplefilter("ignore", InsecureRequestWarning)
                resposta = requests.get(urls[chave], verify=False)
                if resposta.status_code == 200:
                    html_page = resposta.text
                    numero_atual = html_page.count("</tr>") - 1  # -1 por causa do cabeçalho
                    data_dict[chave] = numero_atual
                else:
                    data_dict[chave] = 0  # caso o número não possa ser obtido
            salvar_dados(arqvo_data, data_dict)

        print()

        time.sleep(2)

        # Variáveis para detectar alterações específicas
        alteracoes_protocolos = False
        alteracoes_convenios = False

        # Verificar alterações nos protocolos e convenios
        for chave, url in urls.items():
            if verificar_alteracoes(url, chave, data_dict):
                if chave == "protocolos":
                    alteracoes_protocolos = True
                elif chave == "convenios":
                    alteracoes_convenios = True

        print()
        print()

        # Atualizar o arquivo de dados se houver alterações
        if alteracoes_protocolos or alteracoes_convenios:
            salvar_dados(arqvo_data, data_dict)
            msg_sucesso("Alterações detectadas e atualizadas no arquivo")
            
            # Personalizar a notificação de acordo com as alterações
            if alteracoes_protocolos and alteracoes_convenios:
                enviar_notificacao("⚠️ Alterações Encontradas!", "Foram encontradas alterações nos protocolos e convenios")
            elif alteracoes_protocolos:
                enviar_notificacao("⚠️ Alterações Encontradas!", "Foram encontradas alterações nos protocolos")
            elif alteracoes_convenios:
                enviar_notificacao("⚠️ Alterações Encontradas!", "Foram encontradas alterações nos convênios")
                
            print()
            print()
            print("=" * 75)
            print()
            print()
            confirmar_usuario()  # Aguarda confirmação do usuário
        else:
            msg_info("Nenhuma alteração detectada")
        
        print()
        print()

        print("=" * 75)
        print()
        print()
        # Aguarde antes de realizar a próxima verificação
        msg_info("Aguardando 1 minuto para a próxima verificação")
        time.sleep(60)  # 5 minutos


if __name__ == "__main__":

    
    versao_atual = "1.0.0"
    verificar_nova_versao(versao_atual)

    try:
        monitorar()
    except Exception as excecao:
        print(f"Ocorreu um erro: {excecao}")
    finally:
        input("Pressione Enter para sair...")