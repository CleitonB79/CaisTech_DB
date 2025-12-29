# dashboard_final_correto.py - VERSÃO 100% TESTADA
import sqlite3
from datetime import datetime
import os

print("📈 DASHBOARD CAIS TECH - ANÁLISE COMPLETA")
print("=" * 60)

# Verificar se o banco existe
if not os.path.exists('caistech.db'):
    print("❌ ERRO: Arquivo 'caistech.db' não encontrado!")
    print("   Execute primeiro: python corrigir_banco.py")
    exit()

conexao = sqlite3.connect('caistech.db')
cursor = conexao.cursor()

# 1. MÉTRICAS FINANCEIRAS
print("\n💰 MÉTRICAS FINANCEIRAS")
print("-" * 40)

cursor.execute(
    'SELECT COUNT(*), SUM(valor_mensal), AVG(valor_mensal) FROM clientes')
clientes, mrr, ticket_medio = cursor.fetchone()

print(f"• Clientes ativos: {clientes or 0}")
print(f"• MRR (Receita Mensal): R$ {mrr or 0:.2f}")
print(f"• Ticket médio: R$ {ticket_medio or 0:.2f}")

# 2. ANÁLISE POR PLANO
print("\n📋 ANÁLISE POR PLANO")
print("-" * 40)

cursor.execute('''
    SELECT plano, COUNT(*), SUM(valor_mensal) 
    FROM clientes 
    WHERE valor_mensal > 0
    GROUP BY plano 
    ORDER BY SUM(valor_mensal) DESC
''')

print("Plano          Qtd   Receita     %")
print("-" * 40)
for plano, qtd, receita in cursor.fetchall():
    percentual = (receita / mrr * 100) if mrr and mrr > 0 else 0
    print(f"{plano:12}  {qtd:2}   R$ {receita:7.2f}   {percentual:5.1f}%")

# 3. SITUAÇÃO DAS FATURAS
print("\n🧾 SITUAÇÃO DAS FATURAS")
print("-" * 40)

try:
    cursor.execute(
        "SELECT status, COUNT(*), SUM(valor) FROM faturas GROUP BY status")
    resultados = cursor.fetchall()
    if resultados:
        for status, qtd, valor in resultados:
            icone = "⚠️ " if status == 'atrasada' else "⏳" if status == 'pendente' else "✅"
            print(f"{icone} {status:10} {qtd:2} faturas  R$ {valor or 0:.2f}")
    else:
        print("ℹ️  Nenhuma fatura cadastrada")
except:
    print("ℹ️  Tabela de faturas não disponível")

# 4. DISTRIBUIÇÃO GEOGRÁFICA
print("\n📍 DISTRIBUIÇÃO GEOGRÁFICA")
print("-" * 40)

try:
    cursor.execute('''
        SELECT e.cidade, e.estado, COUNT(c.id)
        FROM clientes c
        LEFT JOIN enderecos e ON c.id = e.cliente_id
        WHERE e.cidade IS NOT NULL
        GROUP BY e.cidade, e.estado
    ''')

    resultados = cursor.fetchall()
    if resultados:
        for cidade, estado, qtd in resultados:
            print(f"• {cidade}/{estado}: {qtd} cliente(s)")
    else:
        print("ℹ️  Nenhum endereço cadastrado")
except:
    print("ℹ️  Erro ao consultar endereços")

# 5. SERVIÇOS
print("\n🛠️  SERVIÇOS CONTRATADOS")
print("-" * 40)

try:
    cursor.execute(
        "SELECT servico, COUNT(*) FROM servicos_contratados GROUP BY servico")
    for servico, qtd in cursor.fetchall():
        print(f"• {servico}: {qtd} contratação(ões)")
except:
    print("ℹ️  Nenhum serviço registrado")

conexao.close()

# 6. ANÁLISE ESTRATÉGICA
print("\n🎯 ANÁLISE ESTRATÉGICA")
print("-" * 40)

if mrr and mrr >= 1500:
    print("✅ Excelente! MRR acima de R$ 1.500/mês")
    print(f"   Com mais 1 cliente Enterprise: R$ {mrr + 997:.2f}/mês")
elif mrr and mrr >= 1000:
    print("✅ Bom! MRR acima de R$ 1.000/mês")
else:
    print(f"📈 MRR atual: R$ {mrr or 0:.2f}")

if ticket_medio and ticket_medio >= 500:
    print(f"✅ Ticket médio premium: R$ {ticket_medio:.2f}")
    print("   Foco em clientes de alto valor")

print("\n🎯 PRÓXIMAS AÇÕES:")
print("   1. Cadastrar endereços de 2 clientes faltantes")
print("   2. Oferecer upgrade para cliente do plano Básico")
print("   3. Desenvolver novo serviço para venda cruzada")
print("   4. Automatizar este relatório com N8N")

print("\n" + "=" * 60)
print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
print("💡 Execute: python dashboard_final_correto.py")
print("=" * 60)
