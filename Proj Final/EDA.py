import pandas as pd
import numpy as np
import streamlit as st
#import altair as alt
#import plotly.graph_objects as go
#import io

st.set_option('deprecation.showfileUploaderEncoding', False)

# def criar_histogram(coluna, df):
#     chart = alt.Chart(df, width=600).mark_bar().encode(
#         alt.X(coluna, bin=True),
#         y="count()", tooltip=[coluna, "count()"]
#     ).interactive()
#     return st.altair_chart(chart, use_container_width=True)
#
#
# def criar_barras(coluna_num, coluna_cat, df):
#     bars = alt.Chart(df, width=600).mark_bar().encode(
#         x=alt.X(coluna_num, stack="zero"),
#         y=alt.WindowOnlyOp(coluna_cat),
#         tooltip=[coluna_cat, coluna_num]
#     ).interactive()
#     return st.altair_chart(bars, use_container_width=True)
#
#
# def criar_boxplot(coluna_num, coluna_cat,df):
#     boxplot = alt.Chart(df, width=600).mark_boxplot().encode(
#         x=coluna_num,
#         y=coluna_cat
#     )
#     return boxplot
#
#
# def criar_scatterplot(x, y, color, df):
#     scatter = alt.Chart(df, width=800, height=400).mark_circle().encode(
#         alt.X(x),
#         alt.Y(y),
#         color = color,
#         tooltip = [x,y]
#     ).interactive()
#     return scatter


@st.cache()
def inicializacao():
    return pd.read_csv("estaticos_market.csv",index_col=0)


@st.cache()
def merge_dataframes_similaridade(dataframe, arquivo):
    return dataframe.merge(arquivo, on = "id").sort_values("similarity",ascending=False,ignore_index=True)


@st.cache()
def lendo_arquivo(dataframe, arquivo):
    return merge_dataframes_similaridade(dataframe, pd.read_csv(arquivo))


@st.cache()
def ler_base(arquivo):
    return pd.read_csv(arquivo)


# https://gist.github.com/treuille/ff9194ed50af277fc56788d7aed7fcba
def display_dataframe_quickly(df, max_rows=2000, **st_dataframe_kwargs):
    """Display a subset of a DataFrame or Numpy Array to speed up app renders.

    Parameters
    ----------
    df : DataFrame | ndarray
        The DataFrame or NumpyArray to render.
    max_rows : int
        The number of rows to display.
    st_dataframe_kwargs : Dict[Any, Any]
        Keyword arguments to the st.dataframe method.
    """
    n_rows = len(df)
    if n_rows <= max_rows:
        # As a special case, display small dataframe directly.
        st.dataframe(df)

    else:
        # Slice the DataFrame to display less information.
        start_row = st.slider('Linha inicial', 0, n_rows - max_rows)
        end_row = start_row + max_rows
        df = df[start_row:end_row]

        # Reindex Numpy arrays to make them more understandable.
        if type(df) == np.ndarray:
            df = pd.DataFrame(df)
            df.index = range(start_row, end_row)

        # Display everything.
        st.dataframe(df, **st_dataframe_kwargs)
        st.text('Mostando linhas %i até %i de %i.' % (start_row, end_row - 1, n_rows))


st.sidebar.title("Filtros para Análise de Similaridade")
mercado = inicializacao()
similaridade = st.sidebar.slider("Nível de Similaridade Mínimo", 0.0, 100.0, step=0.01, format="%f%%")/100.0
st.sidebar.text("Recomenda-se valores acima de 94%")
de_saude_tributaria = st.sidebar.multiselect(label="Saúde Financeira",
                                             options=mercado["de_saude_tributaria"].unique())
de_saude_rescencia = st.sidebar.multiselect(label="Rescência da Saúde Financeira",
                                            options=mercado["de_saude_rescencia"].unique())
de_faixa_faturamento_estimado = st.sidebar.multiselect(label="Faturamento Estimado da Empresa",
                                                       options=mercado["de_faixa_faturamento_estimado"].unique())
de_faixa_faturamento_estimado_grupo = st.sidebar.multiselect(label="Faturamento Estimado do Grupo da Empresa",
                                                             options=mercado["de_faixa_faturamento_estimado_grupo"].unique())
sg_uf = st.sidebar.multiselect(label="Unidade Federativa",
                                        options=mercado["sg_uf"].unique())
nm_meso_regiao = st.sidebar.multiselect(label="Meso Região",
                                        options=mercado["nm_meso_regiao"].unique())
"""
Uncomment with care"
"""
# for i in range(9999):
#     st.balloons()
st.image("og-iesb.png", use_column_width=True)
st.title("Recomendação clientes B2B")
st.header("Esta página teve como objetivo explorar os resultados da análise de similaridade de empresas B2B")
st.subheader("Autor: Lucas Perin Manchine")
st.subheader("Professor: Marcello Sandi Pinheiro")
st.text("")
st.text("Github: https://github.com/perinm/PI-2020.1/tree/master/Proj%20Final")
st.text("Linkedin: https://www.linkedin.com/in/lucasmanchine/")

for i in range(3):
    st.text("")

base = st.file_uploader("Escolha base de clientes que deseja analisar (.csv)", type="csv")

if base is not None:
    df_base = ler_base(base)
    df_base = df_base[["id", "de_natureza_juridica", "natureza_juridica_macro", "de_ramo", "setor", "nm_divisao",
                       "nm_segmento", "nm_meso_regiao", "de_saude_tributaria", "de_saude_rescencia",
                       "de_faixa_faturamento_estimado", "de_faixa_faturamento_estimado_grupo"]]
    display_dataframe_quickly(df_base, width=1600)

for i in range(3):
    st.text("")

file = st.file_uploader("Escolha modelo de base de clientes para similaridade (.csv)", type="csv")

for i in range(3):
    st.text("")

st.write("Após selecionar a tabela de clientes, fique à vontade para selecionar filtros e explorar seus potenciais clientes")

if file is not None:
    st.subheader("Explorando dataframe de mercado de possíveis clientes")
    df = lendo_arquivo(mercado, file)
    for filtro in ["de_saude_tributaria", "de_saude_rescencia", "de_faixa_faturamento_estimado", "nm_meso_regiao",
                   "de_faixa_faturamento_estimado_grupo", "sg_uf"]:
        if len(eval(filtro)) != 0:
            df = df[df[filtro].isin(eval(filtro))]
    if similaridade != 0:
        df = df[df["similarity"]>similaridade]

    df = df[["id","similarity","de_natureza_juridica","natureza_juridica_macro","de_ramo","setor","nm_divisao","nm_segmento",
             "nm_meso_regiao","de_saude_tributaria","de_saude_rescencia","de_faixa_faturamento_estimado",
             "de_faixa_faturamento_estimado_grupo"]]
    display_dataframe_quickly(df, width=1600)
    # aux = pd.DataFrame({"colunas":df.columns, "tipos":df.dtypes})
    # colunas_numericas = list(aux[aux["tipos"] != "object"]["colunas"])
    # colunas_object = list(aux[aux["tipos"] == "object"]["colunas"])

    # st.write(colunas_object)
    # filter_faturamento_estimado = st.selectbox("Selecione o faturamento estimado, que deseja filtrar" +
    #                                            " (por padrão, verde):",
    #                                             df["de_faixa_faturamento_estimado"].unique())
    # col_sort = st.selectbox("Selecione a saúde rescencia, que deseja filtrar (por padrão, verde):",
    #                         df["de_saude_rescencia"].unique())
    #
    # col = st.selectbox("Selecione a coluna :", colunas_numericas,index=0)
    #
    #
    # if col is not None:
    #     st.markdown("Selecione o que deseja analisar :")
    #     mean = st.checkbox("Média")
    #     if mean:
    #         st.markdown(df[col].mean())
    #     median = st.checkbox("mediana")
    #     if median:
    #         st.markdown(df[col].median())
    #     std = st.checkbox("Desvio padrão")
    #     if std:
    #         st.markdown(df[col].std())
    # st.subheader("Visualização dos dados")
    # st.markdown("Selecione a visualização")
    # histograma = st.checkbox("Histograma")
    # if histograma:
    #     col_num = st.selectbox("Selecione a Coluna Numerica: ", colunas_numericas,key="unique")
    #     st.markdown("Histograma da coluna : "+col_num)
    #     st.write(criar_histogram(col_num,df))
    # barras = st.checkbox("Gráfico de barras")
    # if barras:
    #     col_num_barras = st.selectbox("Selecione a coluna numerica : ",
    #                                   colunas_numericas,key="unique")
    #     col_cat_barras = st.selectbox("Selecione uma coluna categorica : ",
    #                                   colunas_object, key= "unique")
    #     st.markdown("Gráfico de barras da coluna "+ col_cat_barras +
    #                 " pela coluna "+ col_num_barras)
    #     st.write(criar_barras(col_num_barras,col_cat_barras,df))
    # boxplot = st.checkbox("Boxplot")
    # if boxplot:
    #     col_num_box = st.selectbox("Selecione a coluna numerica :", colunas_numericas, key="unique")
    #     col_cat_box = st.selectbox("Selecione uma coluna categorica :", colunas_object, key="unique")
    #     st.markdown("Boxplot "+col_cat_box+ " pela coluna " + col_num_box)
    #     st.write(criar_boxplot(col_num_box, col_cat_box, df))
