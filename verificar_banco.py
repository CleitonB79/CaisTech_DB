import sqlite3
import os

print("🔍 ANALISANDO BANCO DE DADOS CAIS TECH")
print("=" * 50)

# Verificar se o arquivo existe
if not os.path.exists('caistech.db'):
    print("❌ Arquivo caistech.db não encontrado!")
    exit()

# Conectar ao banco
conexao = sqlite3.connect('caistech.db')
cursor = conexao.cursor()

# 1. Listar tabelas
cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tabelas = cursor.fetchall()

print(f"📁 TABELAS ENCONTRADAS ({len(tabelas)}):")
for tabela in tabelas:
    print(f"   • {tabela[0]}")

print("\n" + "=" * 50)

# 2. Mostrar conteúdo de cada tabela
for tabela in tabelas:
    nome_tabela = tabela[0]

    # Contar registros
    cursor.execute(f"SELECT COUNT(*) FROM {nome_tabela}")
    total = cursor.fetchone()[0]

    print(f"\n📊 TABELA: {nome_tabela} ({total} registros)")

    # Mostrar estrutura (colunas)
    cursor.execute(f"PRAGMA table_info({nome_tabela})")
    colunas = cursor.fetchall()
    nomes_colunas = [col[1] for col in colunas]
    print(f"   Colunas: {', '.join(nomes_colunas)}")

    # Mostrar primeiros registros
    if total > 0:
        cursor.execute(f"SELECT * FROM {nome_tabela} LIMIT 3")
        registros = cursor.fetchall()
        for reg in registros:
            print(f"   → {reg}")

print("\n" + "=" * 50)

# 3. Consulta especial: verificar integração CEP
print("\n📍 VERIFICAÇÃO DE INTEGRAÇÃO (Tabela 'enderecos'):")
try:
    cursor.execute('''
        SELECT c.nome_empresa, e.cep, e.cidade, e.estado, e.data_consulta
        FROM enderecos e
        JOIN clientes c ON e.cliente_id = c.id
    ''')
    resultados = cursor.fetchall()

    if resultados:
        print("✅ Integração funcionou! Dados encontrados:")
        for linha in resultados:
            print(
                f"   • {linha[0]}: {linha[1]} - {linha[2]}/{linha[3]} ({linha[4]})")
    else:
        print("⚠️  Tabela 'enderecos' existe mas está vazia.")
except sqlite3.OperationalError as e:
    print(f"❌ Tabela 'enderecos' não encontrada: {e}")

conexao.close()
print("\n" + "=" * 50)
print("✅ Análise concluída!")
