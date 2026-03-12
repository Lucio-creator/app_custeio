import streamlit as st
import pandas as pd

st.set_page_config(page_title="Construtor de Custo Padrão", layout="wide")

# ==========================================
# 1. INICIALIZAÇÃO DA MEMÓRIA (SESSION STATE)
# ==========================================
# Isso garante que a Ficha Padrão (Página 5) funcione mesmo se o aluno for direto para ela,
# pois carregamos os valores do exemplo do PDF como padrão.
valores_iniciais = {
    # Materiais
    'mat_base': 1.10, 'mat_perda': 0.04, 'mat_refugo': 0.01,
    'preco_compra': 20.70, 'custo_fin': 2.70, 'frete': 2.00,
    # MOD
    'mod_base': 50.00, 'mod_paradas': 7.00, 'mod_retrabalho': 3.00,
    'salario_base': 2.20, 'encargos': 1.32, 'beneficios': 0.29,
    # CIV
    'civ_total': 275000.00, 'civ_horas_prev': 453600.00, 'civ_horas_unid': 60.00,
    # CIF
    'cif_total': 484680.00, 'cif_vol': 11540.00
}

for key, value in valores_iniciais.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================================
# 2. MENU DE NAVEGAÇÃO
# ==========================================
st.sidebar.title("Etapas do Custeio")
pagina = st.sidebar.radio(
    "Navegue pelos passos:",
    [
        "1. Materiais Diretos",
        "2. Mão-de-Obra Direta",
        "3. Custos Indiretos Variáveis",
        "4. Custos Indiretos Fixos",
        "5. Ficha-Padrão (Consolidado)"
    ]
)
st.sidebar.divider()
st.sidebar.info("Preencha cada etapa para construir a Ficha-Padrão final do produto.")

# ==========================================
# PÁGINA 1: MATERIAIS DIRETOS
# ==========================================
if pagina == "1. Materiais Diretos":
    st.title("📦 Etapa 1: Materiais Diretos")
    st.write(
        "Determine a quantidade e o preço padrão dos materiais, considerando perdas normais e expurgos financeiros.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("A. Padrão de Quantidade (Ton)")
        st.session_state.mat_base = st.number_input("Material A por unidade", value=st.session_state.mat_base,
                                                    step=0.01)
        st.session_state.mat_perda = st.number_input("Perda normal no processo", value=st.session_state.mat_perda,
                                                     step=0.01)
        st.session_state.mat_refugo = st.number_input("Estimativa de refugos", value=st.session_state.mat_refugo,
                                                      step=0.01)

        qtd_padrao = st.session_state.mat_base + st.session_state.mat_perda + st.session_state.mat_refugo
        st.info(f"**Quantidade-padrão por unidade:** {qtd_padrao:.2f} Toneladas")

    with col2:
        st.subheader("B. Padrão de Preço (R$)")
        st.session_state.preco_compra = st.number_input("Preço de compra s/ impostos",
                                                        value=st.session_state.preco_compra, step=0.50)
        st.session_state.custo_fin = st.number_input("(-) Custo financeiro (prazo)", value=st.session_state.custo_fin,
                                                     step=0.10)
        st.session_state.frete = st.number_input("(+) Frete e despesas", value=st.session_state.frete, step=0.10)

        preco_padrao = st.session_state.preco_compra - st.session_state.custo_fin + st.session_state.frete
        st.info(f"**Preço-padrão do Material:** R$ {preco_padrao:.2f}")

    st.divider()
    custo_total_mat = qtd_padrao * preco_padrao
    st.metric("Custo Padrão Total de Materiais (por unidade)", f"R$ {custo_total_mat:.2f}")

# ==========================================
# PÁGINA 2: MÃO-DE-OBRA DIRETA (MOD)
# ==========================================
elif pagina == "2. Mão-de-Obra Direta":
    st.title("👷 Etapa 2: Mão-de-Obra Direta")
    st.write("Determine o tempo necessário de produção e o custo horário médio com encargos.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("A. Padrão de Quantidade (Horas)")
        st.session_state.mod_base = st.number_input("Horas de montagem/unidade", value=st.session_state.mod_base,
                                                    step=1.0)
        st.session_state.mod_paradas = st.number_input("Paradas e necessidades", value=st.session_state.mod_paradas,
                                                       step=1.0)
        st.session_state.mod_retrabalho = st.number_input("Horas de retrabalho", value=st.session_state.mod_retrabalho,
                                                          step=1.0)

        horas_padrao = st.session_state.mod_base + st.session_state.mod_paradas + st.session_state.mod_retrabalho
        st.info(f"**Horas-padrão por unidade:** {horas_padrao:.2f} Horas")

    with col2:
        st.subheader("B. Padrão de Valor (R$/Hora)")
        st.session_state.salario_base = st.number_input("Salário horário médio", value=st.session_state.salario_base,
                                                        step=0.10)
        st.session_state.encargos = st.number_input("Encargos sociais legais", value=st.session_state.encargos,
                                                    step=0.10)
        st.session_state.beneficios = st.number_input("Benefícios espontâneos", value=st.session_state.beneficios,
                                                      step=0.10)

        custo_hora = st.session_state.salario_base + st.session_state.encargos + st.session_state.beneficios
        st.info(f"**Custo horário da MOD:** R$ {custo_hora:.2f}")

    st.divider()
    custo_total_mod = horas_padrao * custo_hora
    st.metric("Custo Padrão Total de MOD (por unidade)", f"R$ {custo_total_mod:.2f}")

# ==========================================
# PÁGINA 3: CUSTOS INDIRETOS VARIÁVEIS (CIV)
# ==========================================
elif pagina == "3. Custos Indiretos Variáveis":
    st.title("⚡ Etapa 3: Custos Indiretos Variáveis")
    st.write("São padronizados através de taxas predeterminadas baseadas na atividade (ex: horas diretas trabalhadas).")

    st.session_state.civ_total = st.number_input("Custos indiretos variáveis estimados p/ período (R$)",
                                                 value=st.session_state.civ_total, step=1000.0)
    st.session_state.civ_horas_prev = st.number_input("Total de horas diretas previstas no período",
                                                      value=st.session_state.civ_horas_prev, step=1000.0)

    taxa_civ = st.session_state.civ_total / st.session_state.civ_horas_prev if st.session_state.civ_horas_prev > 0 else 0
    st.write(f"**Custo variável por hora direta calculada:** R$ {taxa_civ:.2f}")

    st.divider()
    st.session_state.civ_horas_unid = st.number_input("Horas necessárias para 1 unidade (do padrão de MOD)",
                                                      value=st.session_state.civ_horas_unid, step=1.0)

    custo_total_civ = taxa_civ * st.session_state.civ_horas_unid
    st.metric("Custos Indiretos Variáveis (por unidade)", f"R$ {custo_total_civ:.2f}")

# ==========================================
# PÁGINA 4: CUSTOS INDIRETOS FIXOS (CIF)
# ==========================================
elif pagina == "4. Custos Indiretos Fixos":
    st.title("🏭 Etapa 4: Custos Indiretos Fixos")
    st.write("Para o custeio por absorção, os custos fixos são rateados com base no volume de produção estimado.")

    st.session_state.cif_total = st.number_input("Custos indiretos fixos estimados p/ período (R$)",
                                                 value=st.session_state.cif_total, step=1000.0)
    st.session_state.cif_vol = st.number_input("Volume de produção previsto (unidades)", value=st.session_state.cif_vol,
                                               step=100.0)

    st.divider()
    custo_total_cif = st.session_state.cif_total / st.session_state.cif_vol if st.session_state.cif_vol > 0 else 0
    st.metric("Custos Fixos Indiretos (por unidade)", f"R$ {custo_total_cif:.2f}")

# ==========================================
# PÁGINA 5: FICHA-PADRÃO (CONSOLIDADO)
# ==========================================
elif pagina == "5. Ficha-Padrão (Consolidado)":
    st.title("📋 Etapa 5: Ficha-Padrão do Produto")
    st.write(
        "Este é o documento gerencial final. Ele consolida todas as decisões técnicas e financeiras tomadas nas etapas anteriores.")

    # Recalculando os totais com base no Session State
    qtd_mat = st.session_state.mat_base + st.session_state.mat_perda + st.session_state.mat_refugo
    preco_mat = st.session_state.preco_compra - st.session_state.custo_fin + st.session_state.frete
    total_mat = qtd_mat * preco_mat

    qtd_mod = st.session_state.mod_base + st.session_state.mod_paradas + st.session_state.mod_retrabalho
    preco_mod = st.session_state.salario_base + st.session_state.encargos + st.session_state.beneficios
    total_mod = qtd_mod * preco_mod

    taxa_civ = st.session_state.civ_total / st.session_state.civ_horas_prev if st.session_state.civ_horas_prev > 0 else 0
    qtd_civ = st.session_state.civ_horas_unid
    total_civ = taxa_civ * qtd_civ

    total_cif = st.session_state.cif_total / st.session_state.cif_vol if st.session_state.cif_vol > 0 else 0

    custo_padrao_total = total_mat + total_mod + total_civ + total_cif

    # Criando o DataFrame (Tabela)
    dados = {
        "Elementos de Custo": ["Materiais Diretos", "Mão-de-Obra Direta", "Custos Indiretos Variáveis",
                               "Custos Indiretos Fixos"],
        "Quantidade": [f"{qtd_mat:.2f}", f"{qtd_mod:.2f}", f"{qtd_civ:.2f}", "-"],
        "Unidade de Medida": ["Toneladas", "Horas", "Horas", "-"],
        "Custo Unitário (R$)": [f"{preco_mat:.2f}", f"{preco_mod:.2f}", f"{taxa_civ:.2f}", f"{total_cif:.2f}"],
        "Custo Total (R$)": [f"{total_mat:.2f}", f"{total_mod:.2f}", f"{total_civ:.2f}", f"{total_cif:.2f}"]
    }

    df_ficha = pd.DataFrame(dados)

    # Exibindo a tabela formatada
    st.table(df_ficha.set_index("Elementos de Custo"))

    # Destaque para o valor final
    st.success(f"### 🎯 Custo-Padrão Total por Unidade: R$ {custo_padrao_total:.2f}")

    st.info(
        "💡 **Dica para Aula:** Mude os valores nas páginas anteriores e veja como a Ficha-Padrão é atualizada automaticamente em tempo real!")