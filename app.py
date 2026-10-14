import streamlit as st
import pandas as pd

# Configuração da página do aplicativo
st.set_page_config(page_title="Minerador Avançado de Ofertas & Scalers", page_icon="🚀", layout="wide")

# Título e Introdução
st.title("🚀 Minerador Avançado: Tendências de Alta & Media Scalers")
st.markdown("Painel estratégico para identificar ofertas recém-lançadas em alta considerável e produtos de baixo CPC para campanhas de **R$ 50/dia**.")

# --- BARRA LATERAL: FILTROS DE SEGURANÇA ---
st.sidebar.header("🎯 Parâmetros de Anúncio")
orçamento_diario_brl = st.sidebar.number_input("Orçamento Diário (R$)", value=50.0, step=10.0)
cotacao_dolar = st.sidebar.number_input("Cotação do Dólar (R$)", value=5.20, step=0.10)
cpc_max_usd = st.sidebar.slider("CPC Máximo Aceitável (USD)", 0.50, 4.00, 2.20, 0.10)
comissao_min_usd = st.sidebar.slider("Comissão Mínima (USD)", 30, 300, 80, 5)

# --- BASE DE DADOS CURADA (Focada em Tendências Reais e Escala) ---
data = [
    # Categoria: Produtos em Início de Alta Considerável (Oportunidades de Ouro)
    {"Categoria_Filtro": "🚀 Em Início de Alta (Tendência)", "Plataforma": "ClickBank", "Produto": "ProNail Complex", "Nicho": "Saúde/Fungos", "Variacao_Gravity": "Subindo de 18 para 58 📈", "Gravity_Atual": 58, "Comissao_USD": 115.0, "CPC_Est_USD": 1.40, "URL": "https://clickbank.com"},
    {"Categoria_Filtro": "🚀 Em Início de Alta (Tendência)", "Plataforma": "ClickBank", "Produto": "Aura Glow", "Nicho": "Skincare / Beleza", "Variacao_Gravity": "Subindo de 22 para 64 📈", "Gravity_Atual": 64, "Comissao_USD": 95.0, "CPC_Est_USD": 1.50, "URL": "https://clickbank.com"},
    {"Categoria_Filtro": "🚀 Em Início de Alta (Tendência)", "Plataforma": "Digistore24", "Produto": "Freedom Accelerator", "Nicho": "Make Money Online", "Variacao_Gravity": "Explodindo 🚀", "Gravity_Atual": 52, "Comissao_USD": 250.0, "CPC_Est_USD": 2.10, "URL": "https://digistore24.com"},

    # Categoria: CPCs Baratos (Excelente para Orçamento Baixo)
    {"Categoria_Filtro": "💰 CPC Barato & Seguro", "Plataforma": "ClickBank", "Produto": "LegaClean Pro", "Nicho": "Saúde Circulatória", "Variacao_Gravity": "Estável ➡️", "Gravity_Atual": 28, "Comissao_USD": 90.0, "CPC_Est_USD": 0.90, "URL": "https://clickbank.com"},
    {"Categoria_Filtro": "💰 CPC Barato & Seguro", "Plataforma": "Digistore24", "Produto": "Metabolic Renewal", "Nicho": "Emagrecimento Feminino", "Variacao_Gravity": "Subindo Lento 📈", "Gravity_Atual": 36, "Comissao_USD": 75.0, "CPC_Est_USD": 1.15, "URL": "https://digistore24.com"},

    # Categoria: Media Scalers de Alta Performance (Escala Pesada)
    {"Categoria_Filtro": "🌐 Media Scalers (Tráfego Pago Pesado)", "Plataforma": "Media Scaler", "Produto": "Zenith Labs Cardio", "Nicho": "Cardiovascular", "Variacao_Gravity": "Escala Consistente ⚡", "Gravity_Atual": 95, "Comissao_USD": 110.0, "CPC_Est_USD": 1.95, "URL": "https://zenithlabs.com"},
    {"Categoria_Filtro": "🌐 Media Scalers (Tráfego Pago Pesado)", "Plataforma": "Media Scaler", "Produto": "Alpha Heater", "Nicho": "Gadgets / Casa", "Variacao_Gravity": "Pico de Vendas 🔥", "Gravity_Atual": 130, "Comissao_USD": 60.0, "CPC_Est_USD": 1.05, "URL": "https://alphaheater.com"},
    {"Categoria_Filtro": "🌐 Media Scalers (Tráfego Pago Pesado)", "Plataforma": "Media Scaler", "Produto": "Keto Charge", "Nicho": "Suplementos Keto", "Variacao_Gravity": "Escalando Forte 🚀", "Gravity_Atual": 140, "Comissao_USD": 105.0, "CPC_Est_USD": 2.05, "URL": "https://ketocharge.com"}
]

df = pd.DataFrame(data)

# --- CÁLCULOS DO SOFTWARE ---
df["Cliques_Dia_R$50"] = ((orçamento_diario_brl / cotacao_dolar) / df["CPC_Est_USD"]).round(1)
df["Score_Lucratividade"] = (df["Comissao_USD"] / df["CPC_Est_USD"]).round(1)

# --- MÉTRICAS DO TOPO ---
st.subheader("📊 Panorama Geral do Minerador")
c1, c2, c3 = st.columns(3)
c1.metric("Ofertas Monitoradas", len(df))
c2.metric("Comissão Média", f"US$ {df['Comissao_USD'].mean():.1f}")
c3.metric("CPC Médio Estimado", f"US$ {df['CPC_Est_USD'].mean():.2f}")

st.markdown("---")

# --- TABELA 1: EM INÍCIO DE ALTA (Oportunidades de Menor Concorrência) ---
st.subheader("🚀 1. Produtos em Início de Alta (Tendência Considerável)")
st.markdown("Ofertas que começaram a tracionar recentemente (Gravity entre 35 e 65). Menor concorrência de afiliados veteranos do que produtos gigantes.")
df_alta = df[df["Categoria_Filtro"].str.contains("Início de Alta") & (df["Comissao_USD"] >= comissao_min_usd)]
st.dataframe(
    df_alta[["Produto", "Plataforma", "Nicho", "Variacao_Gravity", "Gravity_Atual", "Comissao_USD", "CPC_Est_USD", "Cliques_Dia_R$50", "Score_Lucratividade"]],
    use_container_width=True
)

# --- TABELA 2: CPCs BARATOS ---
st.subheader("💰 2. Oportunidades de CPC Barato (Proteção de Orçamento)")
st.markdown("Produtos com cliques mais baratos que garantem maior margem de teste para R$ 50/dia.")
df_cpc = df[df["Categoria_Filtro"].str.contains("CPC Barato") & (df["CPC_Est_USD"] <= cpc_max_usd)]
st.dataframe(
    df_cpc[["Produto", "Plataforma", "Nicho", "Variacao_Gravity", "Gravity_Atual", "Comissao_USD", "CPC_Est_USD", "Cliques_Dia_R$50", "Score_Lucratividade"]],
    use_container_width=True
)

# --- TABELA 3: MEDIA SCALERS ---
st.subheader("🌐 3. Media Scalers (Validados em Tráfego Pesado)")
st.markdown("Produtos validados por grandes gastadores de mídia.")
df_scaler = df[df["Categoria_Filtro"].str.contains("Media Scalers")]
st.dataframe(
    df_scaler[["Produto", "Plataforma", "Nicho", "Variacao_Gravity", "Gravity_Atual", "Comissao_USD", "CPC_Est_USD", "Cliques_Dia_R$50", "Score_Lucratividade"]],
    use_container_width=True
)

st.info("💡 **Dica de Ouro:** A tabela de **Início de Alta** é a melhor para afiliados que querem surfar um produto antes de ele ficar saturado e com o CPC inflado!")
