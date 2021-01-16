import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from time import sleep


@st.cache
def load_data(path):
    """Load data and keep them in cache"""
    data = pd.read_csv(path)
    sleep(5)
    return data


def grafico_comparativo(data: dict, causa='TODAS DOENÇAS', uf='BRASIL'):
    """
        Recebe um dicionário contendo os anos dos dados como chave e os 
        dataframe como valores, e retorna um dataframe contendo os dados de 
        óbitos contidos no dataframe por doença e por estado.

        inputs
        :data: Dicionário contendo os dados no formato { 'ano': dataframe }
        :causa: Causa(doença) do óbito a ser analisado
        :uf: Estado dos óbitos de interesse

        outputs
        :fig: Gráfico comparando os óbitos entre os anos trazidos no dicionário
    """
    anos = []
    lista = []

    if causa == 'TODAS DOENÇAS':
        if uf == 'BRASIL':
            for ano, dataframe in data.items():
                # Soma o total de óbitos no ano
                obitos = dataframe.sum()
                lista.append(int(obitos['total']))  # Armazeno o valor
                anos.append(ano)  # Armazena o ano

        else:
            for ano, dataframe in data.items():
                # Soma o total de óbitos na UF especificada no ano
                obitos = dataframe.groupby('uf').sum()
                lista.append(int(obitos.loc[uf]))  # Armazena o valor
                anos.append(ano)  # Armazena o ano

    else:
        if uf == 'BRASIL':
            for ano, dataframe in data.items():
                # Soma o total de óbitos pela doença especificada no ano
                obitos = dataframe.groupby('tipo_doenca').sum()
                lista.append(int(obitos.loc[causa]))  # Armazena o valor
                anos.append(ano)  # Armazena o ano

        else:
            for ano, dataframe in data.items():
                # Soma o total de óbitos por UF, por doença no ano
                obitos = dataframe.groupby(['uf', 'tipo_doenca']).sum()
                lista.append(int(obitos.loc[uf, causa]))  # Armazena o valor
                anos.append(ano)  # Armazena o ano

    data = pd.DataFrame({'Total': lista, 'Ano': anos})

    fig, ax = plt.subplots(figsize=(12, 6))
    ax = sns.barplot(x='Ano', y='Total', data=data)
    ax.set_title(f'Total de óbitos por {causa}')

    return fig


def main():

    st.set_page_config(page_title='Análise de óbitos 2019-2021',
                       page_icon=':bar_chart:')

    datas = {
        '2019': load_data('dados/obitos-2019.csv'),
        '2020': load_data('dados/obitos-2020.csv'),
        '2021': load_data('dados/obitos-2021.csv'),
    }
    causes = datas['2019']['tipo_doenca'].unique().tolist()
    causes.append('TODAS DOENÇAS')
    states = datas['2019']['uf'].unique().tolist()
    states.append('BRASIL')

    st.title('Análise de Óbitos 2019-2021')
    st.markdown('Este trabalho analisa dados dos **óbitos entre 2019 e 2021**')
    cause = st.sidebar.selectbox('Selecione a doença', causes)
    state = st.sidebar.selectbox('Selecione o estado', states)
    figure = grafico_comparativo(datas, causa=cause, uf=state)

    st.pyplot(figure)


if __name__ == '__main__':
    main()
