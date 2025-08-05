"""
Orquestrador para automatizar a execução dos scripts de ataque.
"""

import os
from datetime import datetime
from pt_generate_excel_attacks import ExcelAttackResults
from create_attack_files import create_attack_files
from code_completion_automation import run_automation
from validation_completion import validate_all_attack_files
import time
import pandas as pd
from metrics_analysis import metrics_generation_and_validation

class AttackOrchestrator:
    def __init__(self, path_questions_file: str = "./data/pt_forbidden_questions.csv", path_results_dir: str = "attacks_excels", path_attack_files_dir: str = "attack_files"):
        """Inicializa o orquestrador de ataques"""
        self.results_dir = path_results_dir
        self.attack_files_dir = path_attack_files_dir
        self.path_questions_file = path_questions_file
        
        # Criar diretórios necessários se não existirem
        for directory in [self.results_dir, self.attack_files_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def run_full_attack_pipeline(self, num_questions: int = None, timestamp: str = None):
        """
        Executa o pipeline completo de ataques:
        1. Gera o Excel com os ataques baseados no arquivo de perguntas (CSV)
        2. Cria os arquivos Python para cada ataque de nível 1 e 2
        3. Executa a automação do Cursor para cada arquivo de ataque
        4. Valida os arquivos de ataque
        
        Args:
            num_questions: Número de perguntas para testar (None para todas)
        """
        try:
            print("=== Iniciando Pipeline de Ataques ===\n")
            start_time_1 = time.time()
            
            # Passo 1: Gerar Excel com ataques
            print("Passo 1: Gerando Excel com ataques...")
            excel_generator = ExcelAttackResults(path_questions_file=self.path_questions_file, name_fold_results=self.results_dir)
            results_df = excel_generator.run_attacks(num_questions)
            excel_file = excel_generator.save_results(results_df, timestamp)
            print(f"Excel gerado com sucesso: {excel_file}\n")
            
            time.sleep(2)

            # Passo 2: Criar arquivos Python
            print("Passo 2: Criando arquivos Python para cada ataque...")
            output_dir = create_attack_files(excel_file, path_attacks_files=self.attack_files_dir, timestamp=timestamp)
            print(f"Arquivos Python criados com sucesso em: {output_dir}\n")
            time.sleep(2)
            
            start_time_2 = time.time()
            # Passo 3: Executar automação do Cursor
            print("Passo 3: Iniciando automação do Cursor...")
            print("ATENÇÃO: Não use o computador durante a automação!")
            
            run_automation(output_dir)

            end_time_2 = time.time()
            print(f"Tempo total de execução da automação de autocomplete do Cursor: {end_time_2 - start_time_2:.2f} segundos")
            time.sleep(2)

            # Passo 4: Validar os arquivos
            print(f"Passo 4: Validando os arquivos em {output_dir}...")
            results_validation = validate_all_attack_files(path_attacks_files_final=output_dir, excel_file=excel_file)
            print(f"Arquivos validados com sucesso!\n")

            # Salvar os resultados da validação em um arquivo Excel
            results_validation.to_excel(f"{self.results_dir}/pt_results_validation_{timestamp}.xlsx", index=False)

            # Aguarda um momento para garantir que os arquivos foram criados
            time.sleep(2)

            # Calcula as métricas da geração e validação dos ataques
            print(f"Passo 5: Calculando métricas da geração e validação dos ataques...")
            metrics_generation_and_validation(excel_file=excel_file, results_validation=results_validation)
            print(f"Métricas calculadas com sucesso!\n")

            end_time_1 = time.time()
            print(f"\n=== Pipeline de Ataques Concluído com Sucesso! ===")
            print(f"Tempo total de execução: {end_time_1 - start_time_1:.2f} segundos")
            
        except Exception as e:
            print(f"\nErro durante a execução do pipeline: {str(e)}")


def main():
    path_questions_file = "./data/pt_forbidden_questions.csv"
    path_results_dir = "attacks_excels"
    path_attack_files_dir = "attacks_files"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    orchestrator = AttackOrchestrator(path_questions_file=path_questions_file, path_results_dir=path_results_dir, path_attack_files_dir=path_attack_files_dir)
    
    # Você pode especificar o número de perguntas ou deixar None para todas
    orchestrator.run_full_attack_pipeline(timestamp=timestamp)

if __name__ == '__main__':
    main()