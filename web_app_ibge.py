from operator import index
import re
from altair import Order
import requests
from pprint import pprint
import streamlit as st
import pandas as pd


def pegar_nome_por_decadas(nome):

    url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}"


    dados_decadas= get_url(url)

    if not dados_decadas:
        return {}

    disc_decadas = {}
    for dados in dados_decadas[0]["res"]:
        decadas = dados["periodo"]
        quantidade = dados["frequencia"]
        disc_decadas[decadas] = quantidade
        
    return disc_decadas
    

def get_url(url, params=None):
    response= requests.get(url, params=params)

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print(f"Ocorreu um erro: {e}")
        resultado = None
    else:
        resultado = response.json()
    return resultado

def main():
    st.title("Web App Nomes")
    st.write("Dados do IBG (font: https://servicodados.ibge.gov.br/api/docs/nomes?versao=2)")

    nome = st.text_input("Consulte um nome:")
    if not nome:
        st.stop()
    disc_decadas = pegar_nome_por_decadas(nome)

    if not disc_decadas:
        st.warning(f"Nenhum dado encontrado para o nome: {nome}")
        st.stop()

    df = pd.DataFrame.from_dict(disc_decadas, orient="index")

    cols1,cols2 = st.columns([0.3,0.7])

    with cols1:
        st.write("Frequência por década")
        st.dataframe(df)
    with cols2:
        st.write("Evolução no tempo")
        st.line_chart(df)

   

if __name__ == "__main__":
    main()
