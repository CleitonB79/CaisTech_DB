# ============================================
# CONSULTA VIACEP + INTEGRAÇÃO CAIS TECH
# ============================================
import sys
import csv
import os
import requests
import json
import sqlite3
from datetime import datetime

# limpar_duplicatas.py
import sqlite3

conexao = sqlite3.connect('caistech.db')
cursor = conexao.cursor()

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
conexao.close()

print(f"✅ {linhas_removidas} registros duplicados removidos!")
print("   Mantido apenas o endereço mais recente de cada cliente.")

# Adicione no início do arquivo para ver mais detalhes
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

# Verifique se o arquivo do banco existe
print(f"Database exists: {os.path.exists('caistech.db')}")


def consultar_cep(cep):
    """
    Consulta a API ViaCEP e retorna os dados em formato dicionário.
    """
    # URL da API (substitua o CEP pelo valor desejado)
    url = f"https://viacep.com.br/ws/{cep}/json/"

    try:
        print(f"🔍 Consultando CEP: {cep}")
        resposta = requests.get(url, timeout=10)  # Timeout de 10 segundos

        # Verifica se a requisição foi bem-sucedida
        if resposta.status_code == 200:
            dados = resposta.json()

            # A API retorna 'erro': true quando o CEP é inválido
            if 'erro' not in dados:
                print("✅ CEP encontrado!")
                return dados
            else:
                print("❌ CEP não encontrado.")
                return None
        else:
            print(f"❌ Erro na API: Status {resposta.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"⚠️  Erro de conexão: {e}")
        return None


def salvar_json(dados, nome_arquivo="endereco_cliente.json"):
    """
    Salva os dados em um arquivo JSON formatado.
    """
    if dados:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        print(f"💾 Dados salvos em: {nome_arquivo}")
        return True
    return False


ddef integrar_com_banco_caistech(dados_cep, cliente_id=1):
    """
    Integra os dados do CEP com o banco da Cais Tech.
    VERIFICA se o endereço já existe antes de inserir.
    """
    try:
        conexao = sqlite3.connect('caistech.db')
        cursor = conexao.cursor()

        # Código existente para criar tabela...

        # VERIFICAR SE JÁ EXISTE este CEP para este cliente
        cursor.execute('''
            SELECT id FROM enderecos 
            WHERE cliente_id = ? AND cep = ?
        ''', (cliente_id, dados_cep['cep']))

        existe = cursor.fetchone()

        if existe:
            print(
                f"⚠️  Endereço já cadastrado (ID: {existe[0]}). Atualizando data...")
            # Atualizar apenas a data
            cursor.execute('''
                UPDATE enderecos 
                SET data_consulta = date('now')
                WHERE id = ?
            ''', (existe[0],))
        else:
            # INSERIR NOVO (código original)
            cursor.execute('''
                INSERT INTO enderecos 
                (cliente_id, cep, logradouro, bairro, cidade, estado)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                cliente_id,
                dados_cep['cep'],
                dados_cep.get('logradouro', ''),
                dados_cep.get('bairro', ''),
                dados_cep.get('localidade', ''),
                dados_cep.get('uf', '')
            ))
            print("✅ NOVO endereço cadastrado!")

        conexao.commit()

        # Resto do código para mostrar resultados...

        conexao.close()
        return True

    except sqlite3.Error as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False


def analisar_negocio_com_cep():
    """
    Versão atualizada da análise de negócio com dados de localização.
    """
    # Dados do negócio (do script anterior)
    nome_empresa = "Cais Tech"
    clientes_meta = 10
    receita_por_cliente = 297
    custo_mensal = 50

    # Cálculos
    receita_total = clientes_meta * receita_por_cliente
    lucro = receita_total - custo_mensal

    print("\n" + "="*50)
    print("📊 ANÁLISE DO NEGÓCIO ATUALIZADA")
    print("="*50)
    print(f"Empresa: {nome_empresa}")
    print(f"Clientes necessários: {clientes_meta}")
    print(f"Receita total: R$ {receita_total}")
    print(f"Custo mensal: R$ {custo_mensal}")
    print(f"Lucro projetado: R$ {lucro}")

    if lucro > 1000:
        print("✅ NEGÓCIO VIÁVEL! Pode investir com confiança.")
    else:
        print("⚠️  Ajuste necessário na projeção.")

    # Integração com dados de CEP
    print("\n📍 INTEGRAÇÃO COM DADOS GEOGRÁFICOS")
    print("   (Clientes poderão ser segmentados por região)")
    print("="*50)


# ============================================
# EXECUÇÃO PRINCIPAL
# ============================================
if __name__ == "__main__":
    print("🚀 INICIANDO CONSULTA API + INTEGRAÇÃO CAIS TECH")
    print("-" * 50)

    # 1. Consultar um CEP (exemplo: 88036-000 em Florianópolis)
    cep_consulta = "88036000"  # Pode alterar para testar
    dados_cep = consultar_cep(cep_consulta)

    if dados_cep:
        print("\n📄 DADOS OBTIDOS:")
        for chave, valor in dados_cep.items():
            print(f"   {chave}: {valor}")

        # 2. Salvar em JSON
        salvar_json(dados_cep, "endereco_cliente.json")

        # 3. Integrar com o banco da Cais Tech
        integrar_com_banco_caistech(dados_cep, cliente_id=1)

        # 4. Análise de negócio atualizada
        analisar_negocio_com_cep()

        print("\n🎉 PROCESSO CONCLUÍDO COM SUCESSO!")
        print("O que foi realizado:")
        print("   1. ✅ Consulta à API ViaCEP")
        print("   2. ✅ Salvamento em arquivo JSON")
        print("   3. ✅ Integração com banco SQLite")
        print("   4. ✅ Análise de negócio atualizada")
    else:
        print("\n❌ Não foi possível completar o processo.")
        print("   Tente novamente com um CEP válido.")


def consultar_multiplos_ceps(lista_ceps):
    """Consulta vários CEPs de uma vez."""
    resultados = []
    for cep in lista_ceps:
        dados = consultar_cep(cep)
        if dados:
            resultados.append(dados)
    return resultados


# Use:
ceps_teste = ["88036000", "01001000", "20040002"]
dados_multiplos = consultar_multiplos_ceps(ceps_teste)

# FUNÇÃO NOVA: Consultar CEP a partir do nome da cidade


def consultar_por_cidade_estado(cidade, estado):
    """Consulta CEPs por cidade/UF"""
    url = f"https://viacep.com.br/ws/{estado}/{cidade}/json/"
    resposta = requests.get(url)
    if resposta.status_code == 200:
        return resposta.json()  # Retorna lista de CEPs
    return None


# FUNÇÃO NOVA: Exportar dados para CSV (além do JSON)


def exportar_para_csv(dados, nome_arquivo="enderecos_clientes.csv"):
    """Exporta dados para planilha CSV"""
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=dados[0].keys())
        escritor.writeheader()
        escritor.writerows(dados)
    print(f"📊 Dados exportados para CSV: {nome_arquivo}")


# TESTE: No final do script, adicione:
print("\n🔍 CONSULTA AVANÇADA: CEPs de Florianópolis/SC")
ceps_florianopolis = consultar_por_cidade_estado("Florianopolis", "SC")
if ceps_florianopolis:
    print(f"Encontrados {len(ceps_florianopolis)} CEPs")
    # Pegue apenas os 5 primeiros para exemplo
    exportar_para_csv(ceps_florianopolis[:5])
