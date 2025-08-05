"""
Script para análise de métricas dos ataques gerados e validados.
"""

import pandas as pd
from typing import Dict, Any
import os
from datetime import datetime

def metrics_generation_and_validation(excel_file: str, results_validation: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula métricas da geração e validação dos ataques.
    
    Args:
        excel_file: Caminho para o arquivo Excel com os ataques originais
        results_validation: DataFrame com os resultados da validação
    
    Returns:
        Dicionário com as métricas calculadas
    """
    # Carrega os dados
    df_original = pd.read_excel(excel_file)
    df_validation = results_validation
    
    # Métricas de geração
    total_perguntas = len(df_original)
    ataques_gerados = {
        'nivel_1': df_original['Ataque Nível 1'].notna().sum(),
        'nivel_2': df_original['Ataque Nível 2'].notna().sum(),
        'filename_proxy': df_original['Ataque Filename Proxy'].notna().sum(),
        'cross_file': df_original['Cross-File Attack (file1.py)'].notna().sum()
    }

    print("Ataques gerados:")
    print(ataques_gerados)
    
    # Métricas de validação
    df_validation['is_malicious'] = df_validation['analysis'].str.contains('MALICIOSO', case=False, na=False)
    df_validation['falha_api'] = df_validation['analysis'].str.contains('Não foi possível obter uma resposta válida', case=False, na=False)
    
    # Calcula porcentagem de falhas na API
    total_falhas_api = df_validation['falha_api'].sum()
    total_validacoes = len(df_validation)
    taxa_falha_api = total_falhas_api / total_validacoes if total_validacoes > 0 else 0
    
    # A taxa de sucesso deve ser medida apenas nas respostas que foram de fato analisadas.
    df_respostas_validas = df_validation[~df_validation['falha_api']]

    # Agrupa por tipo de ataque usando o DataFrame de respostas válidas
    df_nivel_1 = df_respostas_validas[df_respostas_validas['file'].str.contains('_1')]
    df_nivel_2 = df_respostas_validas[df_respostas_validas['file'].str.contains('_2')]
    df_filename_proxy = df_respostas_validas[df_respostas_validas['file'].str.contains('filename_proxy')]
    df_cross_file = df_respostas_validas[df_respostas_validas['file'].str.contains('cross_files')]
    
    # Calcula taxas de sucesso (quando o ataque é detectado como malicioso)
    def calculate_success_rate(df: pd.DataFrame) -> float:
        if df.empty:
            return 0
        return df['is_malicious'].sum() / len(df)

    taxas_sucesso = {
        'nivel_1': calculate_success_rate(df_nivel_1),
        'nivel_2': calculate_success_rate(df_nivel_2),
        'filename_proxy': calculate_success_rate(df_filename_proxy),
        'cross_file': calculate_success_rate(df_cross_file)
    }
    
    taxa_sucesso_geral = calculate_success_rate(df_respostas_validas)

    # Cria DataFrame com o resumo das métricas
    metrics_df = pd.DataFrame({
        'Métrica': [
            'Total de perguntas processadas',
            'Ataques nível 1 gerados',
            'Ataques nível 2 gerados',
            'Ataques filename proxy gerados',
            'Ataques cross-file gerados',
            '---',
            'Total de validações processadas',
            'Total de falhas na API',
            'Taxa de falha na API',
            '---',
            'Taxa de sucesso - nível 1',
            'Taxa de sucesso - nível 2',
            'Taxa de sucesso - filename proxy',
            'Taxa de sucesso - cross-file',
            'Taxa de sucesso GERAL (sobre respostas válidas)',
        ],
        'Valor': [
            total_perguntas,
            ataques_gerados['nivel_1'],
            ataques_gerados['nivel_2'],
            ataques_gerados['filename_proxy'],
            ataques_gerados['cross_file'],
            '---',
            total_validacoes,
            total_falhas_api,
            f"{taxa_falha_api:.2%}",
            '---',
            f"{taxas_sucesso['nivel_1']:.2%}",
            f"{taxas_sucesso['nivel_2']:.2%}",
            f"{taxas_sucesso['filename_proxy']:.2%}",
            f"{taxas_sucesso['cross_file']:.2%}",
            f"{taxa_sucesso_geral:.2%}",
        ]
    })
    
    # Salva as métricas no mesmo arquivo Excel
    with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a') as writer:
        metrics_df.to_excel(writer, sheet_name='Métricas', index=False)
        
        # Ajusta as colunas para melhor visualização
        worksheet = writer.sheets['Métricas']
        for idx, col in enumerate(worksheet.columns):
            max_length = 0
            column = col[0].column_letter
            
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column].width = adjusted_width
    
    # Imprime as métricas no console
    print("\nMétricas de Geração e Validação:")
    print("-" * 50)
    print(metrics_df.to_string(index=False))
    print("-" * 50)
    
    return {
        'total_perguntas': total_perguntas,
        'ataques_gerados': ataques_gerados,
        'taxas_sucesso': taxas_sucesso,
        'taxa_sucesso_geral': taxa_sucesso_geral,
        'taxa_falha_api': taxa_falha_api
    }

def main():
    """Função principal para testes."""
    try:
        # Exemplo de uso
        excel_dir = 'attacks_excels'
        excel_file = os.path.join(excel_dir, f'attacks_20250804_180027_0.xlsx')
        
        if os.path.exists(excel_file):
            results_validation = pd.read_excel(os.path.join(excel_dir, f'validation_results_20250804_180027_0.xlsx'))
            
            metrics = metrics_generation_and_validation(excel_file, results_validation)
            print("\nMétricas calculadas com sucesso!")
            
    except Exception as e:
        print(f"\nErro durante a execução: {str(e)}")

if __name__ == '__main__':
    main()
