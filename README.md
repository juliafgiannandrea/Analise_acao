# Analise_acao
Prova da disciplina Projeto em Ciência de Dados. Foi feita uma comparação de retornos de 2 carteiras de ações, com base no ROE e na Magic Formula de Joel Greenblatt. 
Este projeto realiza uma análise financeira de ações brasileiras utilizando dados da *API do Laboratório de Finanças(https://laboratoriodefinancas.com/home). O foco principal é calcular o retorno das ações em comparação com o índice **Ibovespa* e aplicar a *Fórmula Mágica de Joel Greenblatt* para a seleção de ações.


## Objetivo

O projeto tem dois objetivos principais:

1. *Analisar o retorno das ações com base no ROE* (Retorno sobre o Patrimônio Líquido) e compará-las com o desempenho do Ibovespa.
2. *Aplicar a Fórmula Mágica* de Joel Greenblatt para selecionar as ações mais promissoras, com base em métricas como *Earning Yield* e *ROIC*, e calcular o retorno dessas ações.

## Funcionalidades

- *Recuperação de Dados*: Utilização da API para obter informações financeiras detalhadas das ações.
- *Seleção de Ações por ROE*: As ações com o maior ROE são selecionadas para a análise.
- *Cálculo do Retorno das Ações*: O retorno de cada ação é calculado com base nos preços de abertura e fechamento, corrigidos ao longo do período especificado.
- *Comparação com o Ibovespa*: As ações são comparadas com o índice Ibovespa para determinar se "ganham", "perdem" ou "empatam" em termos de retorno.
- *Aplicação da Fórmula Mágica*: As ações são classificadas e filtradas com base nas métricas de Earning Yield e ROIC, e as 10 melhores são selecionadas.

## Pré-requisitos

Para executar este projeto, você precisará das seguintes bibliotecas Python:

- requests
- pandas
- numpy

## Colaboradores: 
Ludmila Guedes (https://github.com/LudmilaGuedes/Analise_acao.git)

Isabella Aguiar (https://github.com/isabellaaguiarr/Analise_acao.git)

Júlia Félix Giannandrea ()
