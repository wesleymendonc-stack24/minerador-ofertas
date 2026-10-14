import streamlit as st
import pandas as pd

# Configuração da página do aplicativo
st.set_page_config(page_title="Minerador de Ofertas Gringas", page_icon="🚀", layout="wide")

# Título e Introdução
st.title("🚀 Minerador Inteligente de Ofertas (ClickBank & Digistore24)")
st.markdown("Análise quantitativa de produtos para anúncios no **Google Ads (Fundo de Funil)** com baixo orçamento.")

# --- BARRA LATERAL: CONFIGURAÇÕES E FILTROS ---
st.sidebar.header("🎯 Filtros de Segurança (R$ 50/dia)")

orçamento_diario_brl = st.sidebar.number_input("Orçamento Diário (R$)", value=50.0, step=10.0)
cotacao_dolar = st.sidebar.number_input("Cotação do Dólar (R$)", value=5.20, step=0.10)

st.sidebar.markdown("---")
cpc_max_usd = st.sidebar.slider("CPC Máximo Aceitável (USD)", 0.50, 5.00, 2.50, 0.10)
comissao_min_usd = st.sidebar.slider("Comissão Mínima (USD)", 30, 300, 80, 5)
gravity_min, gravity_max = st.sidebar.slider("Faixa de Gravity (ClickBank)", 10, 300, (30, 90))

st.sidebar.markdown("---")
st.sidebar.subheader("🔌 Configuração de APIs (Opcional)")
st.sidebar.text_input("ClickBank API Key", type="password")
st.sidebar.text_input("Digistore24 API Key", type="password")

# --- BASE DE DADOS (Estruturada para produtos) ---
data = [
    {"Plataforma": "ClickBank", "Produto": "ProDentim", "Categoria": "Saúde/Dental", "Gravity": 65, "Comissao_USD": 120.0, "CPC_Est_USD": 1.80, "URL": "https://prodentim.com"},
    {"Plataforma": "ClickBank", "Produto": "Alpilean", "Categoria": "Emagrecimento", "Gravity": 180, "Comissao_USD": 140.0, "CPC_Est_USD": 4.20, "URL": "https://alpilean.com"},
    {"Plataforma": "Digistore24", "Produto": "Tube Mastery", "Categoria": "Negócios", "Gravity": 45, "Comissao_USD": 225.0, "CPC_Est_USD": 2.10, "URL": "https://digistore24.com"},
    {"Plataforma": "ClickBank", "Produto": "Puravive", "Categoria": "Emagrecimento", "Gravity": 75, "Comissao_USD": 135.0, "CPC_Est_USD": 2.20, "URL": "https://puravive.com"},
    {"Plataforma": "Digistore24", "Produto": "Metabolic Renewal", "Categoria": "Saúde", "Gravity": 35, "Comissao_USD": 70.0, "CPC_Est_USD": 1.20, "URL": "https://digistore24.com"},
    {"Plataforma": "ClickBank", "Produto": "LegaClean Pro", "Categoria": "Saúde", "Gravity": 15, "Comissao_USD": 90.0, "CPC_Est_USD": 0.90, "URL": "https://legaclean.com"},
]

df = pd.DataFrame(data)

# --- CÁLCULOS AUTOMÁTICOS DO SOFTWARE ---
df["Cliques_Dia_R$50"] = (orçamento_diario_brl / cotacao_dolar) / df["CPC_Est_USD"]
df["Cliques_Dia_R$50"] = df["Cliques_Dia_R$50"].round(1)

df["Score_Lucratividade"] = df["Comissao_USD"] / df["CPC_Est_USD"]
df["Score_Lucratividade"] = df["Score_Lucratividade"].round(1)

def classificar_oferta(row):
    if row["CPC_Est_USD"] <= cpc_max_usd and row["Comissao_USD"] >= comissao_min_usd and gravity_min <= row["Gravity"] <= gravity_max:
        return "🟢 OURO (Ideal para R$50/dia)"
    elif row["CPC_Est_USD"] > cpc_max_usd:
        return "🔴 RISCO (CPC Muito Alto)"
    elif row["Gravity"] > gravity_max:
        return "🟡 ATENÇÃO (Alta Concorrência)"
    else:
        return "⚪ FORA DOS FILTROS"

df["Status_Decisao"] = df.apply(classificar_oferta, axis=1)

# --- FILTRAGEM DINÂMICA ---
df_filtrado = df[
    (df["Comissao_USD"] >= comissao_min_usd) &
    (df["Gravity"] >= gravity_min) &
    (df["Gravity"] <= gravity_max)
].sort_values(by="Score_Lucratividade", ascending=False)

# --- EXIBIÇÃO NO DASHBOARD ---
st.subheader("📊 Métrica Geral do Mercado Minerado")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Produtos Analisados", len(df))
col2.metric("Oportunidades Ouro", len(df[df["Status_Decisao"].str.contains("OURO")]))
col3.metric("CPC Médio Estimado", f"US$ {df['CPC_Est_USD'].mean():.2f}")
col4.metric("Comissão Média", f"US$ {df['Comissao_USD'].mean():.2f}")

st.markdown("---")
st.subheader("🏆 Melhores Produtos Ordenados por Score")

st.dataframe(
    df_filtrado[[
        "Status_Decisao", "Produto", "Plataforma", "Score_Lucratividade", 
        "Comissao_USD", "CPC_Est_USD", "Cliques_Dia_R$50", "Gravity", "Categoria"
    ]],
    use_container_width=True
)

st.info("💡 **Dica do Software:** Foque em produtos marcados com **🟢 OURO** que ofereçam pelo menos 3 a 5 cliques por dia com seu orçamento de R$ 50.")
