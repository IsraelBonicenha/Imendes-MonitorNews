import os
import sys
import time
import shutil
import zipfile
import requests
import subprocess
from tqdm import tqdm





def clear_terminal_and_exibirReescrever():
    os.system("cls" if os.name == "nt" else "clear")

    print(f"{BLUE}{'=' * 100}")
    print(f"{BLUE}{' ' * 40}INSTALADOR MONITORNEWS")
    print(f"{BLUE}{'=' * 100}{RESET}")
    print(f"\n{YELLOW}Termos de Uso e Privacidade:{RESET} Ao utilizar este instalador, você concorda que o programa será")
    print(f"instalado no diretório padrão {YELLOW}C:\\MonitorNews{RESET}. Certifique-se de que você possui os direitos")
    print("necessários para instalar o software neste local.\n")
    print(f"Deseja aceitar os termos e continuar? [S/N]")

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def criar_pasta(caminho):
    """
    Cria uma pasta no caminho especificado, caso ela não exista.
    """
    if not os.path.exists(caminho):
        try:
            os.makedirs(caminho)
            print(f"\033[92mPasta '{caminho}' criada com sucesso!\033[0m")
        except Exception as e:
            print(f"\033[91mErro ao criar a pasta '{caminho}': {e}\033[0m")
    else:
        print(f"\033[93mA pasta '{caminho}' já existe.\033[0m")

def baixar_arquivo(url, caminho_destino):
    """
    Baixa o arquivo da URL para o caminho especificado com uma barra de progresso.
    """
    # Enviar solicitação para a URL
    resposta = requests.get(url, stream=True)
    resposta.raise_for_status()  # Levanta erro se a solicitação falhar

    # Obter o tamanho do arquivo
    total_tamanho = int(resposta.headers.get('content-length', 0))

    # Abrir o arquivo para escrita binária
    with open(caminho_destino, 'wb') as f, tqdm(
        desc=caminho_destino,
        total=total_tamanho,
        unit='B',
        unit_scale=True
    ) as barra:
        for dados in resposta.iter_content(chunk_size=1024):
            f.write(dados)
            barra.update(len(dados))  # Atualiza a barra de progresso

def descompactar_zip(caminho_zip, caminho_destino):
    """
    Descompacta o arquivo ZIP para a pasta destino e remove o arquivo ZIP.
    """
    try:
        with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
            zip_ref.extractall(caminho_destino)
            print(f"\033[92mArquivo descompactado com sucesso em: {caminho_destino}\033[0m")
        # Excluir o arquivo ZIP após descompactação
        os.remove(caminho_zip)
        print(f"\033[92mArquivo ZIP '{caminho_zip}' excluído com sucesso.\033[0m")
    except Exception as e:
        print(f"\033[91mErro ao descompactar ou excluir o arquivo ZIP: {e}\033[0m")

def instalar_monitornews(caminho_destino, url_zip):
    """
    Função para instalar o MonitorNews:
    1. Baixar o arquivo ZIP.
    2. Descompactar na pasta.
    3. Excluir o ZIP após a descompactação.
    """
    nome_arquivo_zip = os.path.join(caminho_destino, "MonitorNews.zip")
    
    # Passo 1: Baixar o arquivo ZIP
    print("\033[96mBaixando o arquivo MonitorNews...\033[0m")
    baixar_arquivo(url_zip, nome_arquivo_zip)
    
    # Passo 2: Descompactar o arquivo ZIP
    descompactar_zip(nome_arquivo_zip, caminho_destino)

def executar_aplicativo(caminho_aplicativo):
    """
    Executa um aplicativo a partir do caminho especificado em um novo terminal.
    """
    try:
        # Obter o diretório onde o aplicativo está localizado
        diretorio_aplicativo = os.path.dirname(caminho_aplicativo)
        
        # Comando para abrir o cmd no diretório do aplicativo e executar o aplicativo
        comando = f'cmd /K "cd /d {diretorio_aplicativo} && {caminho_aplicativo}"'
        
        # Executa o comando no novo terminal
        subprocess.run(comando, shell=True, check=True)
        
        print(f"\033[92mAplicativo '{caminho_aplicativo}' executado com sucesso!\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[91mErro ao executar o aplicativo: {e}\033[0m")
    except FileNotFoundError:
        print(f"\033[91mO aplicativo '{caminho_aplicativo}' não foi encontrado!\033[0m")

def copiar_e_renomear_arquivo_update(caminho_destino):
    """
    Cria uma cópia do arquivo executável atual na pasta destino, renomeando-o para 'Update - MonitorNews.exe'.
    """
    # Caminho do arquivo executável atual
    arquivo_atual = sys.argv[0]
    
    # Caminho do novo arquivo renomeado
    novo_arquivo = os.path.join(caminho_destino, "MonitorNewsUpdate.exe")  # Renomeando para .exe
    
    try:
        # Copiar o arquivo para o novo destino com o novo nome
        shutil.copy(arquivo_atual, novo_arquivo)
        print(f"\033[92mCópia do arquivo criada com sucesso: {novo_arquivo}\033[0m")
    except Exception as e:
        print(f"\033[91mErro ao copiar e renomear o arquivo: {e}\033[0m")



# Definindo cores para o terminal
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Caminho da pasta
caminho = r"C:\MonitorNews"

# Verificar se a pasta existe
if os.path.exists(caminho):
    instalar_monitornews(caminho, "https://github.com/IsraelBonicenha/Installers-Updates/raw/main/MonitorNews/Release/MonitorNews.zip")
    executar_aplicativo(caminho + "\MonitorNews.exe")
else:
    # Exibir título e Termos de Uso
    print(f"{BLUE}{'=' * 100}")
    print(f"{BLUE}{' ' * 40}INSTALADOR MONITORNEWS")
    print(f"{BLUE}{'=' * 100}{RESET}")
    print(f"\n{YELLOW}Termos de Uso e Privacidade:{RESET} Ao utilizar este instalador, você concorda que o programa será")
    print(f"instalado no diretório padrão {YELLOW}C:\\MonitorNews{RESET}. Certifique-se de que você possui os direitos")
    print("necessários para instalar o software neste local.\n")
    print(f"Deseja aceitar os termos e continuar? [S/N]")
    
    # Capturar resposta do usuário
    resposta = input("> ").strip().upper()
    if resposta == "S":
        clear_terminal_and_exibirReescrever()
        print(f"{GREEN}Continuando com a instalação...{RESET}")
        time.sleep(2)
        clear_terminal()
        criar_pasta(caminho)
        
        instalar_monitornews(caminho, "https://github.com/IsraelBonicenha/Installers-Updates/raw/main/MonitorNews/Release/MonitorNews.zip")
        copiar_e_renomear_arquivo_update(caminho)
        executar_aplicativo(caminho + "\MonitorNews.exe")

    else:
        clear_terminal_and_exibirReescrever()
        print(f"{RED}Termos recusados.{RESET}")

print(f"\n{BLUE}{'=' * 100}{RESET}")
print("\nProcesso encerrado. Fechando programa em 5 segundo...")
time.sleep(3)
