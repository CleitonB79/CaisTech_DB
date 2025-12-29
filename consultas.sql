-- 1. Listar todas as tabelas
SELECT name FROM sqlite_master WHERE type='table';

-- 2. Ver estrutura das tabelas
.schema clientes
.schema servicos_contratados
.schema enderecos

-- 3. Contar registros em cada tabela
SELECT 'clientes' as tabela, COUNT(*) as total FROM clientes
UNION ALL
SELECT 'servicos_contratados', COUNT(*) FROM servicos_contratados
UNION ALL
SELECT 'enderecos', COUNT(*) FROM enderecos;

-- 4. Ver TODOS os dados combinados
SELECT 
    c.id as cliente_id,
    c.nome_empresa,
    c.plano,
    c.valor_mensal,
    e.cep,
    e.cidade,
    e.estado,
    e.data_consulta,
    GROUP_CONCAT(s.servico, ', ') as servicos
FROM clientes c
LEFT JOIN enderecos e ON c.id = e.cliente_id
LEFT JOIN servicos_contratados s ON c.id = s.cliente_id
GROUP BY c.id
ORDER BY c.id;