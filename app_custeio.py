import streamlit as st
import pandas as pd

# Configuração inicial (deve ser a primeira linha do Streamlit)
st.set_page_config(page_title="Laboratório de Finanças", layout="wide")

# --- MENU LATERAL ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135679.png", width=100)
st.sidebar.title("Menu da Disciplina")
modulo = st.sidebar.radio(
    "Escolha o Simulador da Aula:",
    [
        "1. Budget vs Forecast",
        "2. Tipos de Custeio",
        "3. Custo Padrão vs Real"
    ]
)

st.sidebar.divider()


# ==========================================
# MÓDULO 1: BUDGET VS FORECAST
# ==========================================
if modulo == "1. Budget vs Forecast":
    st.title("🌍 Simulador de Orçamento: Importadora Tech")
    st.markdown("""
    **Conceito:** O *Orçamento Estático (Budget)* é a nossa meta original fixada no início do ano. 
    O *Orçamento Revisado (Forecast)* é a nossa projeção ajustada para a realidade, considerando choques de mercado (como o câmbio).
    """)

    col_input, col_grafico = st.columns([1, 2])

    with col_input:
        st.subheader("Parâmetros do Ano")
        st.write("Cenário Original (Estático):")
        cambio_orcado = 5.00
        vol_orcado = 10000
        preco_venda_br = 5000
        custo_importacao_usd = 500

        st.info(f"Câmbio Orçado: R$ {cambio_orcado:.2f} | Volume Orçado: {vol_orcado} un.")

        st.write("---")
        st.write("Ajustes do Mercado (Forecast):")
        novo_cambio = st.slider("Novo Câmbio Projetado (R$/US$)", min_value=3.00, max_value=8.00, value=5.00, step=0.10)
        novo_vol = st.slider("Novo Volume de Vendas Projetado", min_value=5000, max_value=15000, value=10000, step=500)

    with col_grafico:
        receita_estatica = vol_orcado * preco_venda_br
        custo_estatico = vol_orcado * (custo_importacao_usd * cambio_orcado)
        lucro_estatico = receita_estatica - custo_estatico

        receita_forecast = novo_vol * preco_venda_br
        custo_forecast = novo_vol * (custo_importacao_usd * novo_cambio)
        lucro_forecast = receita_forecast - custo_forecast

        dados = {
            "Indicador": ["Receita Bruta (R$)", "Custo de Importação (R$)", "Lucro Projetado (R$)"],
            "Orçamento Estático (Fixado)": [receita_estatica, custo_estatico, lucro_estatico],
            "Forecast (Ajustado)": [receita_forecast, custo_forecast, lucro_forecast]
        }
        df_orcamento = pd.DataFrame(dados)

        st.subheader("Comparativo de Resultados")
        df_display = df_orcamento.copy()
        for col in ["Orçamento Estático (Fixado)", "Forecast (Ajustado)"]:
            df_display[col] = df_display[col].apply(lambda x: f"R$ {x:,.2f}")

        st.table(df_display.set_index("Indicador"))

        st.write("**Visualização do Lucro (Estático vs Forecast):**")
        df_grafico = pd.DataFrame({"Estático": [lucro_estatico], "Forecast": [lucro_forecast]}, index=["Lucro"])
        st.bar_chart(df_grafico.T)


# ==========================================
# MÓDULO 2: TIPOS DE CUSTEIO (O 1º APP)
# ==========================================
elif modulo == "2. Tipos de Custeio":
    st.title("🍺 Simulador de Custeio: Cervejaria Artesanal")
    st.markdown("""
    Neste simulador, vamos analisar como a escolha do método de custeio afeta o lucro líquido. 
    Experimente alterar os valores de **Produção** e **Vendas** para ver a mágica (ou o perigo) do custo fixo no estoque!
    """)

    col_params, col_vols = st.columns(2)

    with col_params:
        preco_venda = st.number_input("Preço de Venda por Litro (R$)", value=25.0, step=1.0)
        custo_var_unit = st.number_input("Custo Variável por Litro (R$)", value=10.0, step=1.0)
        custo_fixo_total = st.number_input("Custo Fixo Total de Produção (R$)", value=15000.0, step=1000.0)

    with col_vols:
        producao = st.slider("Quantidade Produzida (Litros)", min_value=1000, max_value=5000, value=2000, step=100)
        vendas = st.slider("Quantidade Vendida (Litros)", min_value=0, max_value=producao, value=1500, step=100)

    st.divider()

    receita_total = vendas * preco_venda
    estoque_final = producao - vendas

    # Absorção
    custo_fixo_unit = custo_fixo_total / producao if producao > 0 else 0
    custo_total_unit_absorcao = custo_var_unit + custo_fixo_unit
    cpv_absorcao = vendas * custo_total_unit_absorcao
    lucro_liquido_absorcao = receita_total - cpv_absorcao

    # Variável
    cpv_variavel = vendas * custo_var_unit
    margem_contribuicao = receita_total - cpv_variavel
    lucro_liquido_variavel = margem_contribuicao - custo_fixo_total

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📦 Custeio por Absorção")
        st.markdown("*(O custo fixo é rateado pela produção e vai para o produto)*")
        dre_absorcao = pd.DataFrame({
            "DRE - Absorção": ["Receita Bruta", "(-) CPV", "(=) Lucro Líquido"],
            "Valor (R$)": [f"R$ {receita_total:,.2f}", f"R$ -{cpv_absorcao:,.2f}", f"R$ {lucro_liquido_absorcao:,.2f}"]
        })
        st.table(dre_absorcao)
        st.info(f"Custo Fixo alocado em cada litro: **R$ {custo_fixo_unit:.2f}**")

    with col2:
        st.subheader("📉 Custeio Variável")
        st.markdown("*(O custo fixo é tratado como despesa do período)*")
        dre_variavel = pd.DataFrame({
            "DRE - Variável": ["Receita Bruta", "(-) Custos Variáveis", "(=) Margem de Contribuição",
                               "(-) Custos Fixos do Período", "(=) Lucro Líquido"],
            "Valor (R$)": [f"R$ {receita_total:,.2f}", f"R$ -{cpv_variavel:,.2f}", f"R$ {margem_contribuicao:,.2f}",
                           f"R$ -{custo_fixo_total:,.2f}", f"R$ {lucro_liquido_variavel:,.2f}"]
        })
        st.table(dre_variavel)
        st.warning(f"Custo Fixo abatido integralmente no mês: **R$ {custo_fixo_total:,.2f}**")

    st.divider()
    st.subheader("💡 O Pulo do Gato (Análise)")
    diferenca_lucro = lucro_liquido_absorcao - lucro_liquido_variavel
    custo_fixo_no_estoque = estoque_final * custo_fixo_unit

    if diferenca_lucro > 0:
        st.success(f"""
        **Atenção:** O Custeio por Absorção está mostrando um lucro **R$ {diferenca_lucro:,.2f}** maior que o Custeio Variável!  
        **Por que?** Porque a empresa produziu mais do que vendeu (Estoque final: {estoque_final} litros). 
        Parte do Custo Fixo (R$ {custo_fixo_no_estoque:,.2f}) ficou "presa" no estoque.
        """)
    else:
        st.info("A Produção foi igual às Vendas. Não sobrou estoque e ambos os métodos apresentam o mesmo lucro.")


# ==========================================
# MÓDULO 3: CUSTO PADRÃO VS REAL
# ==========================================
elif modulo == "3. Custo Padrão vs Real":
    st.title("🏭 Custo Padrão vs Custo Real (Custeio Direto)")
    st.markdown("""
    Vamos analisar as variações nos custos diretos de fabricação. 
    A culpa foi do setor de compras (pagou mais caro) ou da engenharia/produção (desperdiçou material)?
    """)

    col_padrao, col_real = st.columns(2)

    with col_padrao:
        st.success("🎯 CUSTO PADRÃO (A Meta)")
        preco_padrao = st.number_input("Preço Padrão do Material (R$/kg)", value=10.0)
        qtd_padrao = st.number_input("Quantidade Padrão Total (kg)", value=2000.0)
        custo_total_padrao = preco_padrao * qtd_padrao
        st.write(f"**Custo Total Padrão Estimado: R$ {custo_total_padrao:,.2f}**")

    with col_real:
        st.warning("📊 CUSTO REAL (O que Aconteceu)")
        preco_real = st.number_input("Preço Real Pago (R$/kg)", value=12.0)
        qtd_real = st.number_input("Quantidade Real Consumida (kg)", value=2100.0)
        custo_total_real = preco_real * qtd_real
        st.write(f"**Custo Total Real Incorrido: R$ {custo_total_real:,.2f}**")

    st.divider()
    st.subheader("🔍 Análise de Variações (Variances)")

    var_preco = (preco_real - preco_padrao) * qtd_real
    var_quantidade = (qtd_real - qtd_padrao) * preco_padrao
    var_total = custo_total_real - custo_total_padrao

    m1, m2, m3 = st.columns(3)


    def status_var(valor):
        return "Desfavorável 🔴" if valor > 0 else ("Favorável 🟢" if valor < 0 else "No Alvo ⚪")


    m1.metric("1. Variação de Preço (Compras)", f"R$ {abs(var_preco):,.2f}", status_var(var_preco),
              delta_color="inverse" if var_preco > 0 else "normal")
    m2.metric("2. Variação de Quantidade (Eficiência)", f"R$ {abs(var_quantidade):,.2f}", status_var(var_quantidade),
              delta_color="inverse" if var_quantidade > 0 else "normal")
    m3.metric("3. Variação Total", f"R$ {abs(var_total):,.2f}", status_var(var_total),
              delta_color="inverse" if var_total > 0 else "normal")

    st.info("""
    * A **Variação de Preço** isola o impacto financeiro de ter pago um preço diferente do planejado.
    * A **Variação de Quantidade** isola o impacto de ter consumido mais (desperdício) ou menos matéria-prima que o padrão exigia.
    """)