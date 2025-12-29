-- Consulta 1: Todos os clientes
SELECT * FROM clientes;

-- Consulta 2: Apenas clientes Enterprise
SELECT nome_empresa, email FROM clientes WHERE plano = 'Enterprise';

-- Consulta 3: Contar clientes por plano
SELECT plano, COUNT(*) as total FROM clientes GROUP BY plano;