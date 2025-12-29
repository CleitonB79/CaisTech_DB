# CaisTech_DB

# 🚀 Cais Tech - Repositório de Estudos & Projetos

**De Diretor a Tech Lead: Minha Jornada de 90 Dias**  
*Repositório principal da minha transição de carreira e construção da startup Cais Tech*

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow) 
![GitHub Last Commit](https://img.shields.io/github/last-commit/CleitonB79/meus-estudos)

## 📖 Sobre este Repositório

Este repositório documenta minha jornada de **transição de carreira** após 15 anos na área financeira/logística para a tecnologia, com foco em:
- **Desenvolvimento Back-end com Python**
- **Automação de Processos com N8N**
- **Análise de Dados e SQL**
- **Cibersegurança aplicada a automações**
- **Empreendedorismo Tech**

O nome **"Cais Tech"** representa as iniciais da minha família (Cleiton, Aline, Isabela, Sophia) e simboliza uma **base sólida para inovação**.

## 🏗️ Estrutura do Projeto

meus-estudos/
├── 📁 banco_caistech/ # Projeto: Banco de Dados da Cais Tech
│ ├── banco_caistech.sql # Script completo do BD com dados simulados
│ └── consultas_avancadas.sql # Consultas SQL para análise de negócio
├── 📁 scripts-python/ # Scripts de automação e análise
│ ├── analise_negocio.py # Análise financeira da startup
│ └── api_integration.py # Exemplos de integração com APIs
├── 📁 documentacao/ # Documentos da empresa
│ ├── pitch_caistech.md # Pitch de apresentação
│ └── plano_negocios.md # Plano de negócios inicial
├── 📁 n8n-workflows/ # Fluxos de automação exportados
│ └── google-sheets-to-email.json
└── 📁 estudos/ # Materiais de estudo organizados
├── sql/
├── python/
├── n8n/
└── cybersecurity/


## 🎯 Projeto em Destaque: Banco de Dados Cais Tech

### 📊 Objetivo
Sistema de banco de dados relacional simulando o **CRM interno da Cais Tech**, com:
- Cadastro de clientes e serviços
- Análise de receita recorrente (MRR)
- Relacionamentos entre tabelas (JOINs)
- Consultas estratégicas para tomada de decisão

### 🛠️ Tecnologias Utilizadas
- **SQLite** (banco de dados)
- **Python** (para futuras integrações)
- **Git/GitHub** (controle de versão)

### 📈 Consultas Principais
```sql
-- Receita mensal por plano
SELECT plano, SUM(valor_mensal) as receita_total 
FROM clientes 
GROUP BY plano;

-- Clientes com múltiplos serviços
SELECT c.nome_empresa, COUNT(s.id) as qtd_servicos
FROM clientes c
JOIN servicos_contratados s ON c.id = s.cliente_id
GROUP BY c.id
HAVING qtd_servicos > 1;

## 🔗 Integração com APIs Externas

### 📍 Consulta de CEPs Automatizada
Script Python que consulta a API ViaCEP, salva em JSON e integra com banco SQLite.

**Funcionalidades:**
- Consulta de CEP individual e em massa
- Salvamento automático em JSON e integração com SQLite
- Tratamento de erros e timeout

**Tecnologias:** Python, Requests, SQLite, JSON
