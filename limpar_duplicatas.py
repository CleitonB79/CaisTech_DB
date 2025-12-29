# limpar_duplicatas.py
import sqlite3

print("🧹 LIMPANDO DADOS DUPLICADOS - CAIS TECH")
print("=" * 50)

conexao = sqlite3.connect('caistech.db')
cursor = conexao.cursor()

# Contar antes
cursor.execute("SELECT COUNT(*) FROM enderecos")
total_antes = cursor.fetchone()[0]
print(f"Endereços antes: {total_antes}")

# Manter apenas o endereço mais recente de cada cliente+CEP
cursor.execute('''
    DELETE FROM enderecos 
    WHERE id NOT IN (
        SELECT MIN(id) 
        FROM enderecos 
        GROUP BY cliente_id, cep
    )
''')

linhas_removidas = cursor.rowcount
conexao.commit()

# Contar depois
cursor.execute("SELECT COUNT(*) FROM enderecos")
total_depois = cursor.fetchone()[0]

conexao.close()

print(f"Registros removidos: {linhas_removidas}")
print(f"Endereços depois: {total_depois}")
print(f"Economia de espaço: {linhas_removidas} registros")
print("=" * 50)
print("✅ Limpeza concluída!")
