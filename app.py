from flask import Flask, render_template
import pandas as pd
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def obter_dados_jogadas():
    url = "https://www.placard.co.mz"  # Substitua pelo URL real
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraia os dados do HTML conforme a estrutura da página
        # Este é um exemplo fictício; você precisa ajustar conforme a estrutura real
        dados_jogadas = []
        for row in soup.select("table tr"):
            cells = row.find_all("td")
            if len(cells) > 1:
                horario = cells[0].get_text()
                multiplicador = float(cells[1].get_text())
                dados_jogadas.append({'horario': horario, 'multiplicador': multiplicador})
        
        df = pd.DataFrame(dados_jogadas)
        df['horario'] = pd.to_datetime(df['horario'])
        return df
    else:
        print(f"Erro ao acessar a página: {response.status_code}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

def prever_proximo_multiplicador(df):
    return df['multiplicador'].mean()

def classificar_multiplicador(multiplicador):
    if 1.00 <= multiplicador <= 1.99:
        return 'Azul'
    elif 2.00 <= multiplicador <= 9.99:
        return 'Roxo'
    elif 10.00 <= multiplicador <= 99.99:
        return 'Rosa'
    elif 100.00 <= multiplicador <= 10000.00:
        return 'Rosa grande'
    else:
        return 'Fora do intervalo'

@app.route('/')
def index():
    dados_jogadas = obter_dados_jogadas()
    multiplicador_previsto = prever_proximo_multiplicador(dados_jogadas)
    categoria = classificar_multiplicador(multiplicador_previsto)
    return render_template('index.html', multiplicador=multiplicador_previsto, categoria=categoria)

if __name__ == '__main__':
    app.run(debug=True)