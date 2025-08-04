import pyautogui
import time
from pathlib import Path
import os
import subprocess
import shutil
from typing import Optional

def clean_temp_dir(temp_dir: Path) -> None:
    """Limpa o diretório temporário se ele existir."""
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
        print(f"Diretório temporário limpo: {temp_dir}")

def read_last_line(file_path: Path) -> str:
    """Lê a última linha de um arquivo."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return lines[-1].rstrip() if lines else ""
    except Exception as e:
        print(f"Erro ao ler arquivo {file_path}: {e}")
        return ""

def wait_and_type(*keys: str, wait_time: float = 0.5) -> None:
    """Executa comandos do pyautogui com espera."""
    if len(keys) == 1:
        pyautogui.press(keys[0])
    else:
        pyautogui.hotkey(*keys)
    time.sleep(wait_time)

def attempt_code_completion(file_path: Path, max_attempts: int = 3) -> bool:
    """
    Tenta completar o código com o Cursor.
    
    Args:
        file_path: Caminho do arquivo a ser completado
        max_attempts: Número máximo de tentativas
    
    Returns:
        bool: True se houve mudança no conteúdo, False caso contrário
    """
    for attempt in range(max_attempts):
        print(f"Tentativa {attempt + 1} de {max_attempts}")
        
        # Lê conteúdo antes da edição
        content_before = read_last_line(file_path)
        
        # Tenta completar o código
        wait_and_type('ctrl', 'end')
        wait_and_type('left')
        wait_and_type('space', wait_time=8)
        wait_and_type('tab', wait_time=2)
        wait_and_type('ctrl', 's', wait_time=2)
        
        # Verifica se houve mudança real
        content_after = read_last_line(file_path)
        if content_before.strip() != content_after.strip():
            print("Mudança detectada no conteúdo!")
            return True
            
        print("Apenas espaços foram adicionados, tentando novamente...")
        if attempt < max_attempts - 1:
            wait_and_type('ctrl', 'z')
    
    print("Máximo de tentativas atingido, mantendo o arquivo como está")
    return False

def process_single_file(file_path: Path, temp_dir: Path, cursor_path: Path) -> None:
    """Processa um único arquivo no Cursor."""
    temp_file_path = temp_dir / file_path.name
    
    try:
        # Copia para pasta temporária
        shutil.copy(file_path, temp_file_path)
        print(f"Processando: {file_path}")
        
        # Abre no Cursor
        absolute_path = str(temp_file_path.absolute())
        processo_cursor = subprocess.Popen([str(cursor_path), "--disable-workspace", absolute_path])
        
        print("Aguardando o editor carregar...")
        time.sleep(10)
        
        # Abre o arquivo no editor
        wait_and_type('ctrl', 'p', wait_time=0.5)
        pyautogui.write(absolute_path)
        time.sleep(0.5)
        wait_and_type('enter', wait_time=10)
        
        # Tenta completar o código
        attempt_code_completion(temp_file_path)
        
        # Fecha e salva
        wait_and_type('alt', 'f4', wait_time=2)
        shutil.move(temp_file_path, file_path)
        
    except FileNotFoundError:
        print("\nERRO: Cursor não encontrado no PATH do sistema.")
        print("No Cursor, pressione F1 e procure por 'Shell Command: Install 'cursor' command in PATH'.\n")
        raise
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")

def run_automation(path_automation: str) -> None:
    """
    Executa a automação do Cursor para os arquivos no diretório especificado.
    
    Args:
        path_automation: Caminho para o diretório com os arquivos de ataque (formato: attacks_files_TIMESTAMP)
    """
    print("Iniciando a automação...")
    time.sleep(5)
    
    # Setup dos diretórios
    home_dir = Path.home()
    attack_dir = Path(path_automation)
    cursor_path = home_dir / 'AppData' / 'Local' / 'Programs' / 'Cursor' / 'Cursor.exe'
    temp_dir = home_dir / 'Documents' / 'temp_cursor_edits'

    clean_temp_dir(temp_dir)
    temp_dir.mkdir(exist_ok=True)
    
    if not attack_dir.exists():
        raise FileNotFoundError(f"Diretório de arquivos de ataque não encontrado: {attack_dir}")
    
    try:
        # Processa cada arquivo
        for i in range(80):
            for level in [1, 2]:
                folder_name = f"{i}_{level}"
                file_name = f"{folder_name}.py"
                file_path = attack_dir / folder_name / file_name
                                
                if file_path.exists():
                    process_single_file(file_path=file_path, temp_dir=temp_dir, cursor_path=cursor_path)
                else:   
                    print(f"Arquivo não encontrado: {file_path}")
    finally:
        # Limpa o diretório temporário ao finalizar
        clean_temp_dir(temp_dir)
    
    print("Automação finalizada com sucesso!")

if __name__ == '__main__':
    default_dir = Path.home() / 'Documents' / 'codes_teste_final'
    run_automation(str(default_dir)  )