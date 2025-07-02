# Identificando Ataques à Segurança de Ferramentas de Completude de Código Baseadas em LLMs
---
_Trabalho baseado no paper "Security Attacks on LLM-based Code Completion Tools" (https://doi.org/10.1609/aaai.v39i22.34537)_

## Objetivo
Este projeto aprofunda a análise de falhas de segurança em ferramentas de autocompletar código baseadas em LLMs, como GitHub Copilot e Amazon Q, conhecidas como LCCTs. Além dos ataques abordados no artigo, como jailbreaking, que induz a geração de conteúdo malicioso, e extração de dados de treinamento, que revela informações pessoais, vamos explorar novos cenários e avaliar vulnerabilidades em diferentes modelos e ambientes de desenvolvimento. O objetivo central é evidenciar como a estrutura dessas ferramentas pode aumentar os riscos de segurança.

---

## Experimentos
Para este projeto, decidimos estender os experimentos do artigo em análise, de forma que englobe:

### Experimento 1:
Realizar os experimentos propostos no artigo com outras LCCTs, como por exemplo o Gemini Code Assist, Cursor, e DeepSeek Coder. 
**Justificativa**: Percebemos que os experimentos realizados, ainda que bastante aprofundados, se restringiram ao Amazon Q e ao GitHub Copilot, mas com mais ferramentas de completude de código surgindo a cada dia, acreditamos que expandir esses experimentos a outras ferramentas poderia agregar uma análise mais ampla ao artigo.

### Experimento 2:
Testar os prompts originais em outros idiomas para comparar os resultados com a eficácia dos experimentos originais, em inglês. 
**Justificativa**: É de conhecimento geral que, usualmente, os LLMs apresentam uma performance mais alta para o inglês em comparação com outros idiomas. Acreditamos que repetir os experimentos do artigo para outros idiomas - especialmente o português, mas não limitado a ele - pode nos levar a resultados diferentes dos originais, e talvez expor vulnerabilidades até maiores.

### Experimento 3:
Ampliar o escopo de prompts experimentados. 
**Justificativa**: Os 80 prompts originalmente testados na pesquisa foram gerados propositalmente para pertencer a 4 classes que violam os termos de uso da OpenAI. Mas outros tipos de prompt, que não se restrinjam a esses termos, podem nos levar a resultados diferentes - inclusive indicando vulnerabilidades que não foram previamente identificadas.

### [Extra] Experimento 4:
Tentar extrair informações adicionais que não se restrinjam ao GitHub, como comentários ofensivos, tokens, ou até mesmo chaves de API.
Nota: Esse experimento ainda precisa ser discutido com o professor, considerando que lida com dados sensíveis. Caso seja inviável ou configure algum tipo de violação à Lei Geral de Proteção de Dados (LGPD), não será realizado.

---

## Grupo
- Erlan Lira Soares Júnior - `elsj`  
- Maria Carolina Santos Berrafato - `mcsb3`  
- Thiago Henrique Lopes da Silva - `thls`
