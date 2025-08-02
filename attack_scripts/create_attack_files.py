"""
Script para criar arquivos Python separados para cada ataque do Excel.
"""

import pandas as pd
import os
from datetime import datetime

def create_attack_files(excel_file: str):
    """
    Cria arquivos Python separados para cada ataque do Excel.
    
    Args:
        excel_file: Caminho para o arquivo Excel com os ataques
    """
    # Criar pasta para os arquivos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"attack_files"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if not os.path.exists(output_dir + '//' +output_dir + f"_{timestamp}"):
        os.makedirs(output_dir + '//' + output_dir + f"_{timestamp}")

    output_dir = output_dir + '//' + output_dir + f"_{timestamp}"
    
    # Ler o Excel
    df = pd.read_excel(excel_file)
    
    # Criar arquivos para cada linha
    for idx, row in df.iterrows():
        # Arquivo para ataque nível 1
        with open(os.path.join(output_dir, f"{idx}_level1.py"), 'w', encoding='utf-8') as f:
            f.write(row["Ataque Nível 1"])
        
        # Arquivo para ataque nível 2
        with open(os.path.join(output_dir, f"{idx}_level2.py"), 'w', encoding='utf-8') as f:
            f.write(row["Ataque Nível 2"])
    
    return output_dir

def main():
    # Modificar o nome do arquivo de acordo com o nome do arquivo de resultados
    excel_file = "attacks_excels/attacks_20250802_191141.xlsx"
    
    try:
        output_dir = create_attack_files(excel_file)
        print(f"\nArquivos criados com sucesso na pasta: {output_dir}")
        print(f"Total de arquivos criados: {len(pd.read_excel(excel_file)) * 2}")
        
    except Exception as e:
        print(f"\nErro durante a execução: {str(e)}")

if __name__ == '__main__':
    main()