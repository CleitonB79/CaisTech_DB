# corrigir_banco.py
import sqlite3

print("🔧 CORRIGINDO ESTRUTURA DO BANCO CAIS TECH")
print("=" * 50)

conexao = sqlite3.connect('caistech.db')
cursor = conexao.cursor()

# 1. VERIFICAR A ESTRUTURA ATUAL DA TABELA 'clientes'
print("\n📋 ESTRUTURA ATUAL DA TABELA 'clientes':")
cursor.execute("PRAGMA table_info(clientes)")
colunas = cursor.fetchall()

for col in colunas:
    print(f"  • {col[1]} ({col[2]})")

# 2. ADICIONAR COLUNAS FALTANTES
print("\n➕ ADICIONANDO COLUNAS FALTANTES...")

# Lista de colunas que deveriam existir
colunas_necessarias = [
    ('valor_mensal', 'DECIMAL(10,2) DEFAULT 0'),
    ('telefone', 'TEXT'),
    ('data_cadastro', 'DATE DEFAULT (date("now"))')
]

colunas_existentes = [col[1] for col in colunas]

for coluna, tipo in colunas_necessarias:
    if coluna not in colunas_existentes:
        try:
            cursor.execute(f"ALTER TABLE clientes ADD COLUMN {coluna} {tipo}")
            print(f"✅ Coluna '{coluna}' adicionada")
        except sqlite3.OperationalError as e:
            print(f"⚠️  Erro ao adicionar '{coluna}': {e}")
    else:
        print(f"✅ Coluna '{coluna}' já existe")

# 3. ATUALIZAR VALORES PARA OS CLIENTES EXISTENTES
print("\n💰 ATRIBUINDO VALORES MENSAL PARA CLIENTES:")

# Atualizar com valores baseados no plano atual
cursor.execute('''
    UPDATE clientes 
    SET valor_mensal = CASE 
        WHEN plano = 'Básico' THEN 297.00
        WHEN plano = 'Profissional' THEN 497.00  
        WHEN plano = 'Enterprise' THEN 997.00
        ELSE 0
    END
    WHERE valor_mensal IS NULL OR valor_mensal = 0
''')

linhas_atualizadas = cursor.rowcount
print(f"✅ {linhas_atualizadas} clientes atualizados com valores")

# 4. VERIFICAR OS VALORES ATRIBUÍDOS
print("\n📊 VALORES ATUAIS DOS CLIENTES:")
cursor.execute('''
    SELECT nome_empresa, plano, valor_mensal 
    FROM clientes 
    ORDER BY valor_mensal DESC
''')

print(f"{'Empresa':30} {'Plano':15} {'Valor':>10}")
print("-" * 60)
for nome, plano, valor in cursor.fetchall():
    print(f"{nome[:30]:30} {plano:15} R$ {valor:>7.2f}")

# 5. CRIAR TABELA DE SERVIÇOS SE NÃO EXISTIR
print("\n🛠️  VERIFICANDO TABELA 'servicos_contratados':")
cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='servicos_contratados'")
if not cursor.fetchone():
    print("⚠️  Tabela 'servicos_contratados' não encontrada. Criando...")
    cursor.execute('''
        CREATE TABLE servicos_contratados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            servico TEXT NOT NULL,
            status TEXT DEFAULT 'Ativo',
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    ''')

    # Inserir serviços de exemplo
    cursor.executemany('''
        INSERT INTO servicos_contratados (cliente_id, servico) 
        VALUES (?, ?)
    ''', [
        (1, 'Automação de Relatórios de Fretes'),
        (1, 'Integração Planilha x Sistema'),
        (2, 'Dashboard Financeiro Mensal')
    ])
    print("✅ Tabela 'servicos_contratados' criada com dados de exemplo")

# 6. RESUMO FINAL
print("\n📈 RESUMO DA ESTRUTURA ATUAL:")
cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tabelas = cursor.fetchall()

print(f"Total de tabelas: {len(tabelas)}")
for tabela in tabelas:
    cursor.execute(f"SELECT COUNT(*) FROM {tabela[0]}")
    total = cursor.fetchone()[0]
    print(f"  • {tabela[0]}: {total} registros")

# Calcular MRR total
cursor.execute("SELECT SUM(valor_mensal) FROM clientes")
mrr_total = cursor.fetchone()[0] or 0

conexao.commit()
conexao.close()

print("\n" + "=" * 50)
print(f"💰 MRR TOTAL (Receita Mensal Recorrente): R$ {mrr_total:.2f}")
print("✅ Banco de dados corrigido e pronto para uso!")
print("=" * 50)
