from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Função para processar o arquivo
def processar_vendas():
    # Define o caminho do arquivo
    caminho_arquivo = r'C:\Projeto\Dados\vendas_2023.txt'
    
    # Leitura do arquivo com o delimitador correto
    df = pd.read_csv(caminho_arquivo, sep=',', encoding='utf-8')
    
    # Imprime as colunas para diagnóstico
    print("Colunas disponíveis:", df.columns.tolist())
    
    # Verifica se a coluna 'cpf' está presente
    if 'cpf' not in df.columns:
        raise ValueError("A coluna 'cpf' não foi encontrada no arquivo.")
    
    # Transformações
    df['cpf'] = df['cpf'].str.replace('.', '').str.replace('-', '')
    df['hora_data_venda'] = pd.to_datetime(df['hora_data_venda']).dt.strftime('%d/%m/%Y %H:%M:%S')
    df['valor_total'] = df['valor_total'].apply(lambda x: f'R$ {x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    # Tratamento da coluna 'local' para garantir caracteres especiais
    df['local'] = df['local'].apply(lambda x: x.encode('utf-8').decode('utf-8'))

    # Retorna os dados processados
    return df.to_dict(orient='records')

@app.route('/api/vendas', methods=['GET'])
def get_vendas():
    dados_processados = processar_vendas()
    return jsonify(dados_processados)

if __name__ == '__main__':
    app.run(debug=True)
