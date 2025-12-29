# exportar_dados.py
import sqlite3
import csv

print('💾 EXPORTANDO DADOS DA CAIS TECH...')

conexao = sqlite3.connect('caistech.db')
cursor = conexao.cursor()

# 1. Exportar CLIENTES
cursor.execute('SELECT * FROM clientes')
with open('clientes_exportados.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow([i[0] for i in cursor.description])
    writer.writerows(cursor.fetchall())
print('✅ clientes_exportados.csv criado')

# 2. Exportar FATURAS
cursor.execute('SELECT * FROM faturas')
with open('faturas_exportadas.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow([i[0] for i in cursor.description])
    writer.writerows(cursor.fetchall())
print('✅ faturas_exportadas.csv criado')

# 3. Exportar ENDEREÇOS
cursor.execute('SELECT * FROM enderecos')
with open('enderecos_exportados.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow([i[0] for i in cursor.description])
    writer.writerows(cursor.fetchall())
print('✅ enderecos_exportados.csv criado')

# 4. Criar RESUMO EXECUTIVO
with open('resumo_executivo.txt', 'w', encoding='utf-8') as f:
    f.write('RESUMO EXECUTIVO - CAIS TECH\n')
    f.write('='*50 + '\n')
    cursor.execute('SELECT COUNT(*), SUM(valor_mensal) FROM clientes')
    total_clientes, mrr = cursor.fetchone()
    f.write(f'Clientes ativos: {total_clientes}\n')
    f.write(f'MRR (Receita Mensal): R$ {mrr:.2f}\n\n')

    f.write('Distribuição por plano:\n')
    cursor.execute(
        'SELECT plano, COUNT(*), SUM(valor_mensal) FROM clientes GROUP BY plano')
    for plano, qtd, valor in cursor.fetchall():
        f.write(f'  • {plano}: {qtd} clientes (R$ {valor:.2f})\n')

    f.write('\nPróximas metas:\n')
    f.write(f'  • +1 cliente Enterprise: R$ {mrr + 997:.2f}/mês\n')
    f.write(f'  • +2 clientes Profissional: R$ {mrr + 994:.2f}/mês\n')

conexao.close()
print('✅ resumo_executivo.txt criado')
print('🎉 Exportação concluída!')
