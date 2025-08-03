import pyautogui
import time
from pathlib import Path
import os
import subprocess
import shutil

print("Iniciando a automação... ")
time.sleep(5)

# Guarda o diretório original
diretorio_home = Path.home()
diretorio_original = diretorio_home / 'Documents' / 'codes_teste_final'
caminho_cursor_app = diretorio_home / 'AppData' / 'Local' / 'Programs' / 'Cursor' / 'Cursor.exe'
temp_dir = diretorio_home / 'Documents' / 'temp_cursor_edits'
temp_dir.mkdir(exist_ok=True)


for i in range(80):
    for level in [1, 2]:
        pasta_level = f"{i}_{level}"
        file_name = f"{pasta_level}.py"
        
        # Constrói o caminho completo para o diretório e arquivo
        file_path = diretorio_original / pasta_level / file_name

        # Verifica se o arquivo existe
        if file_path.exists():
            # Copia o arquivo para a pasta temporária
            temp_file_path = temp_dir / file_name
            shutil.copy(file_path, temp_file_path)

            print(f"Processando o arquivo: {file_path}")
            
            try:
                absolute_path = str(temp_file_path.absolute())
                processo_cursor = subprocess.Popen([caminho_cursor_app, "--disable-workspace", absolute_path])

                print("Aguardando o editor carregar...")
                time.sleep(10)

                print("Editor carregado!")

                # Abre o arquivo no editor
                pyautogui.hotkey('ctrl', 'p')
                time.sleep(0.5)
                pyautogui.write(absolute_path)
                time.sleep(0.5)
                pyautogui.press('enter')
                time.sleep(10)

                # Move o cursor até a última linha, move o cursor para a esquerda, e adiciona um espaço e um tab
                print("Editando o arquivo...")
                pyautogui.hotkey('ctrl', 'end')
                time.sleep(0.5)
                pyautogui.press('left')
                time.sleep(0.5)
                pyautogui.press('space')
                time.sleep(5)
                pyautogui.press('tab')
                time.sleep(5)

                # Salva o arquivo (Ctrl+S)
                pyautogui.hotkey('ctrl', 's')
                time.sleep(0.5)

                # Fecha o arquivo (Ctrl+F4)
                pyautogui.hotkey('alt', 'f4')
                time.sleep(2)

                # Move o arquivo temporário de volta para o diretório original
                shutil.move(temp_file_path, file_path)

            except FileNotFoundError:
                print("\nERRO: O comando 'cursor' não foi encontrado.")
                print("Verifique se o Cursor está no PATH do seu sistema.")
                print("No Cursor, pressione F1 e procure por 'Shell Command: Install 'cursor' command in PATH'.\n")
                exit()
            except Exception as e:
                print(f"!!! Erro inesperado ao processar {pasta_level}: {str(e)}")
        else:
            print(f"Arquivo não encontrado, pulando: {file_path}")


'''
                # Simul'a o atalho para abrir um arquivo (Ctrl+O)
                pyautogui.hotkey('ctrl', 'o')
                time.sleep(0.5)

                # Escreve apenas o nome do arquivo, já que estamos no diretório correto
                pyautogui.write(str(file_path))
                pyautogui.press('enter')
                
                # Espera o arquivo carregar
                time.sleep(30)

                # Move o cursor para o final da linha
                pyautogui.hotkey('ctrl', 'end')
                time.sleep(0.5)

                # Move um caractere para a esquerda
                pyautogui.press('left')
                time.sleep(0.5)
                
                pyautogui.press('space')
                time.sleep(5)
                pyautogui.press('tab')
                time.sleep(5)

                # Salva o arquivo (Ctrl+S)
                pyautogui.hotkey('ctrl', 's')
                time.sleep(0.5)

                # Fecha o arquivo (Ctrl+W)
                pyautogui.hotkey('ctrl', 'w')
                time.sleep(0.5)

                # Volta para o diretório original
                os.chdir(diretorio_original)

            except Exception as e:
                print(f"Erro ao processar {file_path}: {str(e)}")
                # Garante que voltamos ao diretório original mesmo em caso de erro
                os.chdir(diretorio_original)
        else:
            print(f"Arquivo não encontrado, pulando: {file_path}")'''

print("Automação finalizada com sucesso!")