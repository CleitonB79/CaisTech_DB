-- ============================================
-- BANCO DE DADOS DA CAIS TECH - VERSÃO 1.0
-- ============================================

-- 1. CRIAR TABELA DE CLIENTES
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_empresa TEXT NOT NULL,
    email TEXT UNIQUE,
    plano TEXT CHECK (plano IN ('Básico', 'Profissional', 'Enterprise'))
);

-- 2. INSERIR PRIMEIROS CLIENTES (DADOS DE TESTE)
INSERT INTO clientes (nome_empresa, email, plano) VALUES
('Transportadora Expresso SC', 'joao@expressosc.com.br', 'Profissional'),
('Contabilidade Total', 'maria@contabilidadetotal.com', 'Básico'),
('Loja Tech Sul', 'carlos@techsul.com.br', 'Enterprise');

-- 3. VERIFICAR SE DEU CERTO
SELECT * FROM clientes;

-- 4. TABELA DE SERVIÇOS
CREATE TABLE IF NOT EXISTS servicos_contratados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    servico TEXT NOT NULL,
    status TEXT DEFAULT 'Ativo',
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- 5. INSERIR SERVIÇOS
INSERT INTO servicos_contratados (cliente_id, servico) VALUES
(1, 'Automação de Relatórios de Fretes'),
(1, 'Integração Planilha x Sistema'),
(2, 'Dashboard Financeiro Mensal');

-- 6. CONSULTA COM JOIN (AVANÇADA)
SELECT 
    c.nome_empresa,
    c.plano,
    GROUP_CONCAT(s.servico, ', ') as servicos
FROM clientes c
LEFT JOIN servicos_contratados s ON c.id = s.cliente_id
GROUP BY c.id;