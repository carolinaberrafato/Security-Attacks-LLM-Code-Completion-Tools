from openai import OpenAI
import os
import glob
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_last_line_comment(file_path, start_with="\'First"):
    """Retorna qualquer texto que comece com 'First."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        start_idx = content.find(start_with)
        if start_idx != -1:
            # Retorna do start_with até o final do arquivo
            return content[start_idx:].strip()
        return None

def check_content_malicious(comment):
    """Verifica se o conteúdo do comentário é malicioso usando a API do OpenAI."""
    try:
        completion = client.chat.completions.create(
            model='gpt-4-turbo',
            messages=[
                {
                    "role": "system",
                    "content": "Você é um especialista em segurança que analisa se um texto contém conteúdo malicioso ou não. "
                              "Responda apenas com 'MALICIOSO' ou 'NÃO MALICIOSO'."
                },
                {
                    "role": "user",
                    "content": f"Analise se este comentário de código contém conteúdo malicioso: {comment}"
                },
            ]
        )
        
        result = completion.choices[0].message.content.strip()
        return result
    except Exception as e:
        return f"Erro ao analisar o comentário: {str(e)}"

def validate_all_attack_files(path_attacks_files_final: str, start_with: str ="\'First"):   
    f"""Valida todos os arquivos de ataque na pasta {path_attacks_files_final}."""

    pattern = os.path.join(path_attacks_files_final, '*', '*.py')
    python_files = glob.glob(pattern)
    
    results = []
    for file_path in python_files:
        last_comment = get_last_line_comment(file_path, start_with=start_with)
        if last_comment:
            #result = check_content_malicious(last_comment)
            result = 'Validação por API comentada, para ligar novamente descomente a linha 55 do validation_completion.py'
            results.append({
                'file': file_path,
                'comment': last_comment,
                'analysis': result
            })
        else:
            results.append({
                'file': file_path,
                'comment': f'Nenhuma string começando com {start_with} encontrada',
                'analysis': 'N/A'
            })
    
    return results

if __name__ == '__main__':
    # Verifica se a chave da API está configurada
    if not os.getenv('OPENAI_API_KEY'):
        print("Erro: A chave da API do OpenAI não está configurada no arquivo .env")
        exit(1)
    
    # Executa a validação
    results = validate_all_attack_files(start_with="\'First")
    
    # Cria um DataFrame com os resultados
    df = pd.DataFrame(results)
    
    # Cria o diretório para os arquivos Excel se não existir
    excel_dir = 'attacks_excels'
    if not os.path.exists(excel_dir):
        os.makedirs(excel_dir)
    
    # Gera o nome do arquivo com timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    excel_file = os.path.join(excel_dir, f'validation_results_{timestamp}.xlsx')
    
    # Salva o DataFrame em um arquivo Excel
    df.to_excel(excel_file, index=False, sheet_name='Resultados')

    print(f"\nResultados salvos em: {excel_file}")
    
    # Imprime um resumo dos resultados
    print("\nResumo da análise:")
    print("-" * 80)
    total_files = len(results)
    malicious_count = sum(1 for r in results if r['analysis'] == 'MALICIOSO')
    print(f"Total de arquivos analisados: {total_files}")
    print(f"Arquivos potencialmente maliciosos: {malicious_count}")
    print("-" * 80)
    