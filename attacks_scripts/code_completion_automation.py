import pyautogui
import time
from pathlib import Path
import os
import subprocess
import shutil
from typing import Optional
import pandas as pd
from datetime import datetime

def clean_temp_dir(temp_dir: Path) -> None:
    """Limpa o diretório temporário se ele existir."""
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
        print(f"Diretório temporário limpo: {temp_dir}")

def read_last_line(file_path: Path) -> tuple[str, str]:
    """
    Lê a última linha não vazia de um arquivo.
    Remove linhas que contêm apenas quebras de linha ou espaços.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.rstrip() for line in f.readlines() if line.strip()]
            return (lines[-1], lines[-1].split(" ")[-1]) if lines else ("", "")
    except Exception as e:
        print(f"Erro ao ler arquivo {file_path}: {e}")
        return "", ""

def get_last_line_comment(file_path, start_with="'First"):
    f"""Retorna todo o conteúdo do arquivo a partir da primeira linha que contenha {start_with}."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        start_idx = None
        for idx, line in enumerate(lines):
            if start_with in line:
                start_idx = idx
                break
        if start_idx is not None:
            return ''.join(lines[start_idx:]).strip()
        return None


def wait_and_type(*keys: str, wait_time: float = 0.5) -> None:
    """Executa comandos do pyautogui com espera."""
    if len(keys) == 1:
        pyautogui.press(keys[0])
    else:
        pyautogui.hotkey(*keys)
    time.sleep(wait_time)

def attempt_code_completion(file_path: Path, max_attempts: int = 3, cross_file: bool = False) -> bool:
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
        content_before_line, guide_word = read_last_line(file_path)
        print(f"Linha completa antes: {content_before_line}")
        print(f"Guide word: {guide_word}")

        # Tenta completar o código
        wait_and_type('ctrl', 'end')
        wait_and_type('left')
        wait_and_type('space', wait_time=8)
        wait_and_type('tab', wait_time=2)
        wait_and_type('ctrl', 's', wait_time=3)
        
        # Lê o conteúdo após a edição
        content_after_line, _ = read_last_line(file_path)
        print(f"Linha completa depois: {content_after_line}")

        # Remove espaços em branco e compara as linhas completas
        content_before_clean = content_before_line.replace(" ", "").replace("\t", "")
        content_after_clean = content_after_line.replace(" ", "").replace("\t", "")
        
        if content_before_clean != content_after_clean:
            print("Mudança detectada no conteúdo!")
            return True
            
        print("Apenas espaços foram adicionados ou nenhuma mudança, tentando novamente...")
        if attempt < max_attempts - 1:
            wait_and_type('ctrl', 'z')
    
    print("Máximo de tentativas atingido, mantendo o arquivo como está")
    return False

def process_single_file(file_path: Path, temp_dir: Path, cursor_path: Path, cross_file: bool = False) -> None:
    """
    Processa um único arquivo no Cursor.
    
    Args:
        file_path: Caminho do arquivo a ser processado
        temp_dir: Diretório temporário para cópia dos arquivos
        cursor_path: Caminho do executável do Cursor
        cross_file: Se True, processa todos os arquivos do diretório
    """
    
    temp_file_path = temp_dir / file_path.name
    
    try:
        # Copia para pasta temporária
        if cross_file:
            temp_dir = temp_file_path.parent
            source_dir = file_path.parent

            temp_dir.mkdir(parents=True, exist_ok=True)

            for item in source_dir.iterdir():
                if item.is_file():
                    shutil.copy(item, temp_dir)
        else:
            shutil.copy(file_path, temp_file_path)

        print(f"Processando: {file_path}")

        absolute_path = str(temp_file_path.absolute())

        if cross_file:
            parent_absolute_path = str(temp_file_path.parent.absolute())
            processo_cursor = subprocess.Popen([str(cursor_path), parent_absolute_path])
        else:
            processo_cursor = subprocess.Popen([str(cursor_path), "--disable-workspace", absolute_path])
                    
        print("Aguardando o editor carregar...")
        time.sleep(10)

        if cross_file:
            absolute_path_file2 = str(temp_file_path.parent.absolute()) + "/file2.py"
            print(absolute_path_file2)
            wait_and_type('ctrl', 'p', wait_time=0.5)
            pyautogui.write(absolute_path_file2)  
            time.sleep(0.5)
            wait_and_type('enter')
            processo_cursor = subprocess.Popen([str(cursor_path), parent_absolute_path])
            time.sleep(0.5)
            wait_and_type('ctrl', 'alt', 'b')
            time.sleep(0.1)

        # Abre o arquivo no editor
        wait_and_type('ctrl', 'p', wait_time=0.5)
        pyautogui.write(absolute_path)  
        time.sleep(0.5)
        wait_and_type('enter', wait_time=10)
        
        # Tenta completar o código
        attempt_code_completion(temp_file_path, cross_file=cross_file)
        
        # Fecha e salva
        wait_and_type('alt', 'f4', wait_time=2)
        shutil.move(temp_file_path, file_path)
        
        if cross_file:
            clean_temp_dir(temp_dir)

    except FileNotFoundError:
        print("\nERRO: Cursor não encontrado no PATH do sistema.")
        print("No Cursor, pressione F1 e procure por 'Shell Command: Install 'cursor' command in PATH'.\n")
        raise
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")

def run_automation(path_automation: str, num_questions: int = 80) -> None:
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
        for i in range(num_questions):
            for level in [1, 2]:
                folder_name = f"{i}_{level}"
                file_name = f"{folder_name}.py"
                file_path = attack_dir / folder_name / file_name
                                
                if file_path.exists():
                    process_single_file(file_path=file_path, temp_dir=temp_dir, cursor_path=cursor_path)
                else:   
                    print(f"Arquivo não encontrado: {file_path}")
        
            # Processa o ataque filename proxy
            folder_name = f"{i}_filename_proxy"
            folder_path = attack_dir / folder_name

            # Procura pelo primeiro arquivo .py dentro da pasta
            py_files = list(folder_path.glob("*.py"))
            if py_files:
                file_path = py_files[0]  # pega o primeiro arquivo .py encontrado
            else:
                raise FileNotFoundError(f"Nenhum arquivo .py encontrado em {folder_path}")
            
            if file_path.exists():
                process_single_file(file_path=file_path, temp_dir=temp_dir, cursor_path=cursor_path)
            else:
                print(f"Arquivo não encontrado: {file_path}")

            # Processa o ataque cross-file
            folder_name = f"{i}_cross_files"
            folder_path = attack_dir / folder_name 
            file_path = attack_dir / folder_name / "file1.py"

            process_single_file(file_path=file_path, temp_dir=temp_dir, cursor_path=cursor_path, cross_file=True)
            
    finally:
        clean_temp_dir(temp_dir)
    
    print("Automação finalizada com sucesso!")

if __name__ == '__main__':
    default_dir = Path.home() / 'Documents' / '2' / 'Security-Attacks-LLM-Code-Completion-Tools' / 'attacks_files' / 'attacks_files_20250805_222025_1'
    run_automation(str(default_dir))