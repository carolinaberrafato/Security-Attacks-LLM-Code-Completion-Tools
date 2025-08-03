import pyautogui
import time
from pathlib import Path

print("Iniciando a automação... ")
time.sleep(5)

for i in range(80):
    for level in [1, 2]:
        # Monta o nome do diretório e do arquivo dinamicamente
        sub_dir_name = f"{i}_level{level}"
        file_name = f"{sub_dir_name}.py"
        
        # Constrói o caminho completo para o arquivo
        file_path = Path(str(i)) / sub_dir_name / file_name

        # Verifica se o arquivo realmente existe antes de tentar abri-lo
        if file_path.exists():
            print(f"Processando o arquivo: {file_path}")

            # Simula o atalho para abrir um arquivo (Ctrl+O)
            pyautogui.hotkey('ctrl', 'o')
            time.sleep(0.5)

            # Escreve o caminho absoluto do arquivo e pressiona Enter
            # Usar .resolve() garante que o caminho completo seja passado
            pyautogui.write(str(file_path.resolve()))
            pyautogui.press('enter')
            
            # Espera o arquivo carregar
            time.sleep(1)

            # Move o cursor para o final da linha
            pyautogui.hotkey('ctrl', 'end')
            time.sleep(0.5)

            # Move um caractere para a esquerda
            pyautogui.press('left')
            time.sleep(0.5)

            pyautogui.press('space')
            time.sleep(2)
            pyautogui.press('tab')
            time.sleep(2)

            # Adicionado: Salva o arquivo (Ctrl+S)
            pyautogui.hotkey('ctrl', 's')
            time.sleep(0.5)

            # Adicionado: Fecha o arquivo (Ctrl+W) para evitar muitas abas abertas
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(0.5)

        else:
            print(f"Arquivo não encontrado, pulando: {file_path}")

print("Automação finalizada com sucesso!")