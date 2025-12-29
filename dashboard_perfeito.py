# dashboard_perfeito.py - VERSÃO 100% FUNCIONAL
import pandas as pd
import sqlite3
from datetime import datetime

print("📈 DASHBOARD CAIS TECH - ANÁLISE COMPLETA")
print("=" * 60)

conexao = sqlite3.connect('caistech.db')
cursor = conexao.cursor()

# 1. MÉTRICAS FINANCEIRAS
print("\n💰 MÉTRICAS FINANCEIRAS")
print("-" * 40)

cursor.execute('''
    SELECT 
        COUNT(*) as clientes_ativos,
        SUM(valor_mensal) as mrr_total,
        AVG(valor_mensal) as ticket_medio
    FROM clientes 
    WHERE ativo = 1 OR ativo IS NULL
''')
clientes, mrr, ticket_medio = cursor.fetchone()

print(f"• Clientes ativos: {clientes}")
print(f"• MRR (Receita Mensal): R$ {mrr:.2f}")
print(f"• Ticket médio: R$ {ticket_medio:.2f}")

# 2. ANÁLISE POR PLANO
print("\n📋 ANÁLISE POR PLANO")
print("-" * 40)

cursor.execute('''
    SELECT 
        plano,
        COUNT(*) as quantidade,
        SUM(valor_mensal) as receita_plano
    FROM clientes
    GROUP BY plano
    ORDER BY receita_plano DESC
''')

print("Plano          Qtd   Receita     %")
print("-" * 40)
for plano, qtd, receita in cursor.fetchall():
    percentual = (receita / mrr * 100) if mrr > 0 else 0
    print(f"{plano:12}  {qtd:2}   R$ {receita:7.2f}   {percentual:5.1f}%")

# 3. SITUAÇÃO DAS FATURAS
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
    print(f"{icone} {status:10} {qtd:2} faturas  R$ {valor:.2f}")

# 4. DISTRIBUIÇÃO GEOGRÁFICA (CORRIGIDO)
print("\n📍 DISTRIBUIÇÃO GEOGRÁFICA")
print("-" * 40)

cursor.execute('''
    SELECT 
        e.estado,
        e.cidade,
        COUNT(c.id) as clientes_localidade
    FROM clientes c
    LEFT JOIN enderecos e ON c.id = e.cliente_id
    WHERE e.estado IS NOT NULL
    GROUP BY e.estado, e.cidade
    ORDER BY clientes_localidade DESC
''')

resultados = cursor.fetchall()
if resultados:
    for estado, cidade, qtd in resultados:
        print(f"• {cidade}/{estado}: {qtd} cliente(s)")
else:
    print("ℹ️  Nenhum endereço cadastrado")

# 5. SERVIÇOS CONTRATADOS
print("\n🛠️  SERVIÇOS MAIS POPULARES")
print("-" * 40)

try:
    cursor.execute('SELECT COUNT(*) FROM servicos_contratados')
    if cursor.fetchone()[0] > 0:
        cursor.execute('''
            SELECT 
                servico,
                COUNT(*) as total
            FROM servicos_contratados 
            GROUP BY servico
            ORDER BY total DESC
        ''')

        for servico, qtd in cursor.fetchall():
            print(f"• {servico}: {qtd} contratação(ões)")
    else:
        print("ℹ️  Nenhum serviço registrado")
except:
    print("ℹ️  Tabela de serviços não disponível")

# 6. ENDEREÇOS POR CLIENTE
print("\n🏢 CLIENTES COM ENDEREÇO CADASTRADO")
print("-" * 40)

cursor.execute('''
    SELECT 
        c.nome_empresa,
        e.cep,
        e.cidade,
        e.estado
    FROM clientes c
    INNER JOIN enderecos e ON c.id = e.cliente_id
    ORDER BY c.nome_empresa
''')

resultados = cursor.fetchall()
if resultados:
    for nome, cep, cidade, estado in resultados:
        print(f"• {nome}: {cep} - {cidade}/{estado}")
else:
    print("ℹ️  Nenhum cliente com endereço cadastrado")

conexao.close()

# 7. ANÁLISE ESTRATÉGICA
print("\n🎯 ANÁLISE ESTRATÉGICA")
print("-" * 40)

if mrr >= 1500:
    print("✅ Excelente! MRR acima de R$ 1.500/mês")
    print("   Considere contratar um assistente ou estagiário")
elif mrr >= 1000:
    print("✅ Bom! MRR acima de R$ 1.000/mês")
    print("   Meta alcançada - hora de escalar")
else:
    print(f"📈 MRR atual: R$ {mrr:.2f}")
    print(f"   Faltam R$ {1000 - mrr:.2f} para atingir R$ 1.000/mês")

if ticket_medio >= 500:
    print("✅ Ticket médio premium: R$ {:.2f}".format(ticket_medio))
    print("   Foco em clientes de alto valor agregado")
else:
    print(f"📊 Ticket médio: R$ {ticket_medio:.2f}")
    print("   Considere ajustar precificação")

print("\n🎯 PRÓXIMAS AÇÕES RECOMENDADAS:")
print("   1. Cadastrar endereços dos clientes faltantes")
print("   2. Oferecer upgrade para clientes do plano Básico")
print("   3. Desenvolver 1 novo serviço para venda cruzada")
print("   4. Automatizar envio deste relatório (N8N)")

print("\n" + "=" * 60)
print(f"📅 Dashboard gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
print("💡 Execute semanalmente para acompanhar crescimento")
print("=" * 60)

# Adicione ao final do dashboard_perfeito.py

conexao = sqlite3.connect('caistech.db')
df_clientes = pd.read_sql_query("SELECT * FROM clientes", conexao)
df_faturas = pd.read_sql_query("SELECT * FROM faturas", conexao)

with pd.ExcelWriter('relatorio_caistech.xlsx') as writer:
    df_clientes.to_excel(writer, sheet_name='Clientes', index=False)
    df_faturas.to_excel(writer, sheet_name='Faturas', index=False)

print("📄 Relatório exportado para Excel: relatorio_caistech.xlsx")
