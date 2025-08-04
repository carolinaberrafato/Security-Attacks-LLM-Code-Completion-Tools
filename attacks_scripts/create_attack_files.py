"""
Script para criar arquivos Python separados para cada ataque do Excel.
"""

import pandas as pd
import os
from datetime import datetime

def create_attack_files(excel_file: str, path_attacks_files: str ="attacks_files", timestamp: str = None):
    """
    Cria arquivos Python separados para cada ataque do Excel.
    
    Args:
        excel_file: Caminho para o arquivo Excel com os ataques
    """
    output_dir = path_attacks_files
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if not os.path.exists(output_dir + '//' + output_dir + f"_{timestamp}"):
        os.makedirs(output_dir + '//' + output_dir + f"_{timestamp}")

    output_dir = output_dir + '//' + output_dir + f"_{timestamp}"
    
    # Ler o Excel
    df = pd.read_excel(excel_file)
    
    # Criar arquivos para cada linha
    for idx, row in df.iterrows():
        os.makedirs(os.path.join(output_dir, f"{idx}_1"))
        os.makedirs(os.path.join(output_dir, f"{idx}_2"))
        os.makedirs(os.path.join(output_dir, f"{idx}_filename_proxy"))
        os.makedirs(os.path.join(output_dir, f"{idx}_cross_files"))

        # Arquivo para ataque nível 1 
        with open(os.path.join(output_dir, f"{idx}_1", f"{idx}_1.py"), 'w', encoding='utf-8') as f:
            f.write(row["Ataque Nível 1"])
        
        # Arquivo para ataque nível 2
        with open(os.path.join(output_dir, f"{idx}_2", f"{idx}_2.py"), 'w', encoding='utf-8') as f:
            f.write(row["Ataque Nível 2"])

        # Arquivo para ataque filename proxy
        filename = row["Ataque Filename Proxy"].split("\n")[0]
        output_path = os.path.join(output_dir, f"{idx}_filename_proxy", f"{filename}")

        with open(output_path, 'w', encoding='utf-8') as f:
            lines = row["Ataque Filename Proxy"].splitlines()[1:]
            f.write("\n".join(lines))
    
        # Arquivo para ataque nível 2
        with open(os.path.join(output_dir, f"{idx}_cross_files", f"file1.py"), 'w', encoding='utf-8') as f:
            f.write(row["Cross-File Attack (file1.py)"])

        with open(os.path.join(output_dir, f"{idx}_cross_files", f"file2.py"), 'w', encoding='utf-8') as f:
            f.write(row["Cross-File Attack (file2.py)"])
    
    return output_dir

def main():
    excel_file = "attacks_excels/attacks_20250803_150922.xlsx"
    
    try:
        output_dir = create_attack_files(excel_file)
        print(f"\nArquivos criados com sucesso na pasta: {output_dir}")
        print(f"Total de arquivos criados: {len(pd.read_excel(excel_file)) * 2}")
        
    except Exception as e:
        print(f"\nErro durante a execução: {str(e)}")

if __name__ == '__main__':
    main()