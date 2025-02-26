import requests

# URL base do repositório no GitHub
BASE_URL = "https://raw.githubusercontent.com/Luamateus2/Repositorio-de-Imagens/main/imagens/repositorio-imagens"

# Função para verificar uma pasta específica
def verificar_pasta(numero_pasta):
    # Caminho para o metadata.json
    url_metadata = f"{BASE_URL}/{numero_pasta}/metadata.json"
    
    # Verifica se o metadata.json está disponível
    response_metadata = requests.get(url_metadata)
    if response_metadata.status_code == 200:
        metadata = response_metadata.json()
        id_individuo = metadata.get("id")
        print(f"Pasta {numero_pasta}: metadata.json encontrado. ID do indivíduo: {id_individuo}")
    else:
        print(f"Pasta {numero_pasta}: metadata.json não encontrado.")
        return

    # Lista os arquivos da pasta usando a API do GitHub
    url_pasta = f"https://api.github.com/repos/Luamateus2/Repositorio-de-Imagens/contents/imagens/repositorio-imagens/{numero_pasta}"
    response_pasta = requests.get(url_pasta)
    if response_pasta.status_code != 200:
        print(f"Pasta {numero_pasta}: Erro ao acessar a pasta.")
        return

    # Encontra o nome da imagem (qualquer arquivo que não seja metadata.json)
    arquivos = response_pasta.json()
    nome_imagem = None
    for arquivo in arquivos:
        if arquivo["name"] != "metadata.json" and arquivo["name"].lower().endswith((".jpg", ".jpeg")):
            nome_imagem = arquivo["name"]
            break

    if nome_imagem:
        # Verifica se a imagem está disponível
        url_imagem = f"{BASE_URL}/{numero_pasta}/{nome_imagem}"
        response_imagem = requests.get(url_imagem)
        if response_imagem.status_code == 200:
            print(f"Pasta {numero_pasta}: Imagem '{nome_imagem}' encontrada.")
        else:
            print(f"Pasta {numero_pasta}: Imagem '{nome_imagem}' não encontrada.")
    else:
        print(f"Pasta {numero_pasta}: Nenhuma imagem válida encontrada.")

# Loop para verificar todas as pastas de 1 a 15
for numero_pasta in range(1, 16):
    verificar_pasta(numero_pasta)