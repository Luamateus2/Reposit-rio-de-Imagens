import os
import shutil
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Diretório atual onde as imagens estão armazenadas
DIRETORIO_ATUAL = "/home/luana/Documentos/GitHub/Repositorio-de-Imagens/imagens"
# Diretório onde o repositório de imagens será criado
DIRETORIO_REPOSITORIO = os.path.join(DIRETORIO_ATUAL, "repositorio-imagens")

# Inicializa o contador de IDs
contador_id = 1

def processar_imagem(caminho_arquivo, arquivo):
    """
    Processa uma imagem: cria uma pasta com ID sequencial, move a imagem
    para a pasta e gera um arquivo JSON com metadados.
    """
    global contador_id

    # Gera um ID sequencial para a imagem
    imagem_id = str(contador_id)

    # Cria a pasta para a imagem
    pasta_imagem = os.path.join(DIRETORIO_REPOSITORIO, imagem_id)
    os.makedirs(pasta_imagem, exist_ok=True)

    # Move a imagem para a pasta
    destino_imagem = os.path.join(pasta_imagem, arquivo)
    shutil.move(caminho_arquivo, destino_imagem)

    # Coleta metadados da imagem
    metadados = {
        "id": imagem_id,
        "nome_arquivo": arquivo,
        "tamanho_bytes": os.path.getsize(destino_imagem),
        "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "caminho_imagem": destino_imagem
    }

    # Salva os metadados em um arquivo JSON
    caminho_metadata = os.path.join(pasta_imagem, "metadata.json")
    with open(caminho_metadata, "w", encoding="utf-8") as f:
        json.dump(metadados, f, indent=4)

    print(f"Imagem '{arquivo}' processada e salva em '{pasta_imagem}' com ID {imagem_id}")

    # Incrementa o contador de IDs
    contador_id += 1

class ManipuladorDeEventos(FileSystemEventHandler):
    """
    Classe para manipular eventos no diretório monitorado.
    """
    def on_created(self, event):
        """
        Executado quando um novo arquivo é criado no diretório.
        """
        if not event.is_directory:  # Ignora pastas
            arquivo = os.path.basename(event.src_path)
            if arquivo.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                print(f"Novo arquivo detectado: {arquivo}")
                processar_imagem(event.src_path, arquivo)

def monitorar_diretorio():
    """
    Monitora o diretório de imagens e processa novos arquivos automaticamente.
    """
    # Verifica se o diretório atual existe
    if not os.path.exists(DIRETORIO_ATUAL):
        print(f"Diretório atual não encontrado: {DIRETORIO_ATUAL}")
        return

    # Cria o diretório do repositório, se não existir
    if not os.path.exists(DIRETORIO_REPOSITORIO):
        os.makedirs(DIRETORIO_REPOSITORIO)

    # Configura o monitoramento do diretório
    manipulador = ManipuladorDeEventos()
    observador = Observer()
    observador.schedule(manipulador, path=DIRETORIO_ATUAL, recursive=False)
    observador.start()

    print(f"Monitorando o diretório '{DIRETORIO_ATUAL}' para novas imagens...")

    try:
        while True:
            # Mantém o script em execução
            pass
    except KeyboardInterrupt:
        # Encerra o monitoramento ao pressionar Ctrl+C
        observador.stop()
        print("Monitoramento interrompido.")

    observador.join()

# Executa a função principal
if __name__ == "__main__":
    monitorar_diretorio()