import streamlit as st
import pandas as pd

# Configuração inicial da página
st.set_page_config(page_title="Simulador de Custeio", layout="wide")

st.title("🍺 Simulador de Custeio: Cervejaria Artesanal")
st.markdown("""
Neste simulador, vamos analisar como a escolha do método de custeio afeta o lucro líquido da nossa cervejaria. 
Experimente alterar os valores de **Produção** e **Vendas** para ver a mágica (ou o perigo) do custo fixo no estoque!
""")

st.divider()

# --- BARRA LATERAL PARA INPUTS ---
st.sidebar.header("Parâmetros do Mês")

preco_venda = st.sidebar.number_input("Preço de Venda por Litro (R$)", value=25.0, step=1.0)
custo_var_unit = st.sidebar.number_input("Custo Variável por Litro (R$)", value=10.0, step=1.0)
custo_fixo_total = st.sidebar.number_input("Custo Fixo Total de Produção (R$)", value=15000.0, step=1000.0)

st.sidebar.markdown("---")
st.sidebar.subheader("Volume (Litros)")

# É importante que a produção seja maior ou igual à venda para o exemplo funcionar de forma simples
producao = st.sidebar.slider("Quantidade Produzida", min_value=1000, max_value=5000, value=2000, step=100)
vendas = st.sidebar.slider("Quantidade Vendida", min_value=0, max_value=producao, value=1500, step=100)

# --- CÁLCULOS ---
receita_total = vendas * preco_venda
estoque_final = producao - vendas

# 1. Custeio por Absorção
custo_fixo_unit = custo_fixo_total / producao if producao > 0 else 0
custo_total_unit_absorcao = custo_var_unit + custo_fixo_unit
cpv_absorcao = vendas * custo_total_unit_absorcao
lucro_bruto_absorcao = receita_total - cpv_absorcao
lucro_liquido_absorcao = lucro_bruto_absorcao  # Assumindo zero despesas adm para simplificar a aula

# 2. Custeio Variável
cpv_variavel = vendas * custo_var_unit
margem_contribuicao = receita_total - cpv_variavel
lucro_liquido_variavel = margem_contribuicao - custo_fixo_total

# --- EXIBIÇÃO DOS RESULTADOS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Custeio por Absorção")
    st.markdown("*(O custo fixo é rateado pela produção e vai para o produto)*")

    dre_absorcao = pd.DataFrame({
        "DRE - Absorção": [
            f"Receita Bruta",
            f"(-) CPV",
            f"(=) Lucro Bruto / Líquido"
        ],
        "Valor (R$)": [
            f"R$ {receita_total:,.2f}",
            f"R$ -{cpv_absorcao:,.2f}",
            f"R$ {lucro_liquido_absorcao:,.2f}"
        ]
    })
    st.table(dre_absorcao)
    st.info(f"Custo Fixo alocado em cada litro: **R$ {custo_fixo_unit:.2f}**")

with col2:
    st.subheader("📉 Custeio Variável")
    st.markdown("*(O custo fixo é tratado como despesa do período)*")

    dre_variavel = pd.DataFrame({
        "DRE - Variável": [
            f"Receita Bruta",
            f"(-) Custos Variáveis",
            f"(=) Margem de Contribuição",
            f"(-) Custos Fixos do Período",
            f"(=) Lucro Líquido"
        ],
        "Valor (R$)": [
            f"R$ {receita_total:,.2f}",
            f"R$ -{cpv_variavel:,.2f}",
            f"R$ {margem_contribuicao:,.2f}",
            f"R$ -{custo_fixo_total:,.2f}",
            f"R$ {lucro_liquido_variavel:,.2f}"
        ]
    })
    st.table(dre_variavel)
    st.warning(f"Custo Fixo abatido integralmente no mês: **R$ {custo_fixo_total:,.2f}**")

# --- O GRANDE "AHA! MOMENT" DA AULA ---
st.divider()
st.subheader("💡 O Pulo do Gato (Análise para os Alunos)")

diferenca_lucro = lucro_liquido_absorcao - lucro_liquido_variavel
custo_fixo_no_estoque = estoque_final * custo_fixo_unit

if diferenca_lucro > 0:
    st.success(f"""
    **Atenção:** O Custeio por Absorção está mostrando um lucro **R$ {diferenca_lucro:,.2f}** maior que o Custeio Variável!  
    **Por que isso acontece?** Porque a empresa produziu mais do que vendeu (Estoque final: {estoque_final} litros). 
    Uma parte do Custo Fixo (exatamente R$ {custo_fixo_no_estoque:,.2f}) ficou "presa" no estoque e não transitou pela DRE como despesa.
    Isso pode iludir o gestor achando que o desempenho foi melhor do que a realidade do caixa!
    """)
elif diferenca_lucro == 0:
    st.info(
        "A Produção foi igual às Vendas. Portanto, não sobrou estoque e ambos os métodos apresentam o **mesmo lucro líquido**.")