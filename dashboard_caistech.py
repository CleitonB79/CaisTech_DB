# dashboard_caistech.py
import time
import schedule
import sqlite3
from datetime import datetime

print("📈 DASHBOARD CAIS TECH - VISÃO COMPLETA DO NEGÓCIO")
print("=" * 60)

conexao = sqlite3.connect('caistech.db')
cursor = conexao.cursor()

# 1. VERIFICAR E CRIAR ESTRUTURA SE NECESSÁRIO
print("\n🔧 CONFIGURANDO BANCO DE DADOS...")

# Adicionar coluna 'ativo' se não existir
try:
    cursor.execute("ALTER TABLE clientes ADD COLUMN ativo BOOLEAN DEFAULT 1")
    print("✅ Coluna 'ativo' adicionada à tabela clientes")
except sqlite3.OperationalError:
    print("✅ Coluna 'ativo' já existe")

# Criar tabela de faturas se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS faturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        valor DECIMAL(10,2),
        data_vencimento DATE,
        status TEXT CHECK(status IN ('pendente', 'paga', 'atrasada')),
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    )
''')

# Inserir faturas de exemplo se a tabela estiver vazia
cursor.execute("SELECT COUNT(*) FROM faturas")
if cursor.fetchone()[0] == 0:
    cursor.executemany('''
        INSERT INTO faturas (cliente_id, valor, data_vencimento, status) 
        VALUES (?, ?, ?, ?)
    ''', [
        (1, 497.00, '2025-01-10', 'pendente'),
        (2, 297.00, '2025-01-10', 'pendente'),
        (3, 997.00, '2025-01-10', 'pendente')
    ])
    print("✅ Faturas de exemplo criadas")

conexao.commit()

# 2. MÉTRICAS PRINCIPAIS DO NEGÓCIO
print("\n💰 MÉTRICAS FINANCEIRAS")
print("-" * 40)

# Receita Mensal Recorrente (MRR)
cursor.execute('''
    SELECT 
        COUNT(*) as clientes_ativos,
        SUM(valor_mensal) as mrr_total,
        AVG(valor_mensal) as ticket_medio
    FROM clientes 
    WHERE ativo = 1 OR ativo IS NULL
''')
clientes, mrr, ticket_medio = cursor.fetchone()

print(f"• Clientes ativos: {clientes or 0}")
print(f"• MRR (Receita Mensal): R$ {mrr or 0:.2f}")
print(f"• Ticket médio: R$ {ticket_medio or 0:.2f}")

# 3. DISTRIBUIÇÃO POR PLANO
print("\n📋 ANÁLISE POR PLANO")
print("-" * 40)

cursor.execute('''
    SELECT 
        plano,
        COUNT(*) as quantidade,
        SUM(valor_mensal) as receita_plano,
        ROUND(100.0 * SUM(valor_mensal) / (SELECT SUM(valor_mensal) FROM clientes), 1) as percentual
    FROM clientes
    GROUP BY plano
    ORDER BY receita_plano DESC
''')

print("Plano        Qtd  Receita    % Total")
print("-" * 40)
for plano, qtd, receita, perc in cursor.fetchall():
    print(f"{plano:12} {qtd:2}  R$ {receita:7.2f}   {perc:5.1f}%")

# 4. SITUAÇÃO DE FATURAS
print("\n🧾 SITUAÇÃO DAS FATURAS")
print("-" * 40)

cursor.execute('''
    SELECT 
        status,
        COUNT(*) as quantidade,
        SUM(valor) as valor_total
    FROM faturas 
    GROUP BY status
    ORDER BY CASE status 
        WHEN 'atrasada' THEN 1 
        WHEN 'pendente' THEN 2 
        WHEN 'paga' THEN 3 
        ELSE 4 
    END
''')

for status, qtd, valor in cursor.fetchall():
    icone = "⚠️ " if status == 'atrasada' else "⏳" if status == 'pendente' else "✅"
    print(f"{icone} {status:10} {qtd:2} faturas  R$ {valor or 0:.2f}")

# 5. VISÃO GEOGRÁFICA DOS CLIENTES
print("\n📍 DISTRIBUIÇÃO GEOGRÁFICA")
print("-" * 40)

cursor.execute('''
    SELECT 
        e.estado,
        COUNT(DISTINCT c.id) as clientes_estado,
        GROUP_CONCAT(DISTINCT c.nome_empresa) as empresas
    FROM clientes c
    LEFT JOIN enderecos e ON c.id = e.cliente_id
    GROUP BY e.estado
    ORDER BY clientes_estado DESC
''')

for estado, qtd, empresas in cursor.fetchall():
    if estado:
        print(f"• {estado}: {qtd} cliente(s)")
        if empresas:
            print(f"  → {empresas[:50]}...")

# 6. PRÓXIMAS AÇÕES RECOMENDADAS
print("\n🎯 PRÓXIMAS AÇÕES RECOMENDADAS")
print("-" * 40)

cursor.execute("SELECT COUNT(*) FROM faturas WHERE status = 'atrasada'")
faturas_atrasadas = cursor.fetchone()[0]

if faturas_atrasadas > 0:
    print(f"1. ⚠️  Resgatar {faturas_atrasadas} fatura(s) atrasada(s)")
else:
    print("1. ✅ Nenhuma fatura atrasada")

cursor.execute("SELECT COUNT(*) FROM clientes WHERE plano = 'Básico'")
clientes_basico = cursor.fetchone()[0]
if clientes_basico > 0:
    print(f"2. 📈 Oferecer upgrade para {clientes_basico} cliente(s) Básico")

print("3. 🔄 Atualizar endereços de clientes faltantes")

conexao.close()

print("\n" + "=" * 60)
print(f"📅 Dashboard gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
print("💡 Dica: Execute semanalmente para acompanhar o crescimento!")

# Agende para rodar toda segunda-feira às 9h
# No Windows Task Scheduler ou com Python:


def executar_dashboard():
    os.system("python dashboard_perfeito.py > relatorio_semanal.txt")
    print("📊 Dashboard executado e salvo em relatorio_semanal.txt")


schedule.every().monday.at("09:00").do(executar_dashboard)

while True:
    schedule.run_pending()
    time.sleep(60)
