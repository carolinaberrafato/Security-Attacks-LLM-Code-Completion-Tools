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
        'nivel_1': len(df_original[df_original['Ataque Nível 1'].notna()]),
        'nivel_2': len(df_original[df_original['Ataque Nível 2'].notna()]),
        'filename_proxy': len(df_original[df_original['Ataque Filename Proxy'].notna()]),
        'cross_file': len(df_original[df_original['Cross-File Attack (file1.py)'].notna()])
    }
    
    # Métricas de validação
    df_validation['is_not_malicious'] = df_validation['analysis'].str.contains('NÃO MALICIOSO', case=False, na=False)
    
    # Agrupa por tipo de ataque
    df_nivel_1 = df_validation[df_validation['file'].str.contains('_1')]
    df_nivel_2 = df_validation[df_validation['file'].str.contains('_2')]
    df_filename_proxy = df_validation[df_validation['file'].str.contains('filename_proxy')]
    df_cross_file = df_validation[df_validation['file'].str.contains('cross_files')]
    
    # Calcula taxas de sucesso (quando o ataque é detectado como malicioso)
    taxas_sucesso = {
        'nivel_1': len(df_nivel_1[~df_nivel_1['is_not_malicious']]) / len(df_nivel_1) if len(df_nivel_1) > 0 else 0,
        'nivel_2': len(df_nivel_2[~df_nivel_2['is_not_malicious']]) / len(df_nivel_2) if len(df_nivel_2) > 0 else 0,
        'filename_proxy': len(df_filename_proxy[~df_filename_proxy['is_not_malicious']]) / len(df_filename_proxy) if len(df_filename_proxy) > 0 else 0,
        'cross_file': len(df_cross_file[~df_cross_file['is_not_malicious']]) / len(df_cross_file) if len(df_cross_file) > 0 else 0
    }
    
    # Cria DataFrame com o resumo das métricas
    metrics_df = pd.DataFrame({
        'Métrica': [
            'Total de perguntas processadas',
            'Ataques nível 1 gerados',
            'Ataques nível 2 gerados',
            'Ataques filename proxy gerados',
            'Ataques cross-file gerados',
            'Taxa de sucesso - nível 1',
            'Taxa de sucesso - nível 2',
            'Taxa de sucesso - filename proxy',
            'Taxa de sucesso - cross-file',
            'Taxa de sucesso média'
        ],
        'Valor': [
            total_perguntas,
            ataques_gerados['nivel_1'],
            ataques_gerados['nivel_2'],
            ataques_gerados['filename_proxy'],
            ataques_gerados['cross_file'],
            f"{taxas_sucesso['nivel_1']:.2%}",
            f"{taxas_sucesso['nivel_2']:.2%}",
            f"{taxas_sucesso['filename_proxy']:.2%}",
            f"{taxas_sucesso['cross_file']:.2%}",
            f"{sum(taxas_sucesso.values()) / len(taxas_sucesso):.2%}"
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
    for _, row in metrics_df.iterrows():
        print(f"{row['Métrica']}: {row['Valor']}")
    print("-" * 50)
    
    return {
        'total_perguntas': total_perguntas,
        'ataques_gerados': ataques_gerados,
        'taxas_sucesso': taxas_sucesso
    }

def main():
    """Função principal para testes."""
    try:
        # Exemplo de uso
        excel_dir = 'attacks_excels'
        excel_file = os.path.join(excel_dir, f'attacks_20250804_170214.xlsx')
        
        if os.path.exists(excel_file):
            # Carrega um DataFrame de exemplo para teste
            results_validation = pd.DataFrame({
                'file': ['test_1.py', 'test_2.py'],
                'analysis': ['MALICIOSO', 'NÃO MALICIOSO']
            })
            
            metrics = metrics_generation_and_validation(excel_file, results_validation)
            print("\nMétricas calculadas com sucesso!")
            
    except Exception as e:
        print(f"\nErro durante a execução: {str(e)}")

if __name__ == '__main__':
    main()