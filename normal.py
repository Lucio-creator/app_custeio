import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

st.set_page_config(page_title="Distribuição Normal", layout="wide")

st.title("Análise Visual: Distribuição Normal vs. Reduzida (Z)")
st.write("Ajuste os parâmetros na barra lateral para visualizar o cálculo de probabilidades.")

# ==========================================
# 1. MENU LATERAL (INPUTS)
# ==========================================
st.sidebar.header("1. Parâmetros da Distribuição")
mu = st.sidebar.number_input("Média (μ)", value=100.0, step=1.0)
sigma = st.sidebar.number_input("Desvio Padrão (σ)", value=15.0, step=1.0, min_value=0.1)

st.sidebar.header("2. O que deseja calcular?")
tipo_calc = st.sidebar.radio(
    "Selecione a região de interesse:",
    ("Menor que X", "Maior que X", "Entre dois valores", "Do Centro (Média) até X")
)

st.sidebar.header("3. Valores de Interesse")

# Lógica para mostrar 1 ou 2 inputs dependendo da escolha
if tipo_calc == "Entre dois valores":
    x1 = st.sidebar.number_input("Valor de X1", value=85.0, step=1.0)
    x2 = st.sidebar.number_input("Valor de X2", value=115.0, step=1.0)
    # Garantir que o menor valor fique na esquerda
    x_min, x_max = min(x1, x2), max(x1, x2)
    z_min, z_max = (x_min - mu) / sigma, (x_max - mu) / sigma
    probabilidade = norm.cdf(z_max) - norm.cdf(z_min)

    texto_resultado = f"P({x_min} < X < {x_max}) = P({z_min:.2f} < Z < {z_max:.2f})"
else:
    x_val = st.sidebar.number_input("Valor de X", value=115.0, step=1.0)
    z_val = (x_val - mu) / sigma

    if tipo_calc == "Menor que X":
        probabilidade = norm.cdf(z_val)
        texto_resultado = f"P(X < {x_val}) = P(Z < {z_val:.2f})"
    elif tipo_calc == "Maior que X":
        probabilidade = 1 - norm.cdf(z_val)
        texto_resultado = f"P(X > {x_val}) = P(Z > {z_val:.2f})"
    elif tipo_calc == "Do Centro (Média) até X":
        probabilidade = abs(norm.cdf(z_val) - 0.5)
        # Se Z for negativo, a área é de Z até 0. Se for positivo, de 0 até Z.
        if z_val < 0:
            texto_resultado = f"P({x_val} < X < {mu}) = P({z_val:.2f} < Z < 0)"
        else:
            texto_resultado = f"P({mu} < X < {x_val}) = P(0 < Z < {z_val:.2f})"

# ==========================================
# 2. EXIBIÇÃO DOS RESULTADOS MATEMÁTICOS
# ==========================================
st.subheader("Resultados do Cálculo:")
st.markdown(f"**{texto_resultado}** = **{probabilidade:.4f}** (ou **{probabilidade * 100:.2f}%**)")

if tipo_calc != "Entre dois valores":
    st.markdown(f"*Valor do Z-score calculado:* **{z_val:.2f}**")

# ==========================================
# 3. CONSTRUÇÃO DOS GRÁFICOS
# ==========================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5))  # Reduzimos a altura de 8 para 5
fig.tight_layout(pad=2.0)  # Reduzimos o espaço em branco entre os gráficos
# Eixos X e Z globais (cobrindo 4 desvios padrões para cada lado)
x_axis = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 1000)
z_axis = np.linspace(-4, 4, 1000)

# Curvas principais
y_axis = norm.pdf(x_axis, mu, sigma)
y_axis_z = norm.pdf(z_axis, 0, 1)

ax1.plot(x_axis, y_axis, color='#1f77b4', linewidth=2)
ax2.plot(z_axis, y_axis_z, color='#2ca02c', linewidth=2)

ax1.set_title(f"Distribuição Original X  (Média = {mu}, Desvio = {sigma})", fontweight='bold')
ax2.set_title("Distribuição Normal Padrão Z  (Média = 0, Desvio = 1)", fontweight='bold')


# Função auxiliar para configurar e hachurar os gráficos
def aplicar_hachura(ax, eixo, curva, fill_min, fill_max, cor, media_val):
    # Definir região de hachura
    fill_x = np.linspace(fill_min, fill_max, 500)
    # Para o gráfico 1 usamos mu e sigma; para o gráfico 2 usamos 0 e 1
    if media_val == 0:
        fill_y = norm.pdf(fill_x, 0, 1)
    else:
        fill_y = norm.pdf(fill_x, mu, sigma)

    ax.fill_between(fill_x, fill_y, alpha=0.4, color=cor)
    ax.axvline(media_val, color='black', linestyle='--', alpha=0.6, label='Média')


# Definindo os limites de hachura baseado na seleção
if tipo_calc == "Entre dois valores":
    aplicar_hachura(ax1, x_axis, y_axis, x_min, x_max, '#1f77b4', mu)
    aplicar_hachura(ax2, z_axis, y_axis_z, z_min, z_max, '#2ca02c', 0)
    ax1.axvline(x_min, color='red', linestyle=':')
    ax1.axvline(x_max, color='red', linestyle=':')
    ax2.axvline(z_min, color='red', linestyle=':')
    ax2.axvline(z_max, color='red', linestyle=':')
else:
    # Definir limites para Menor, Maior ou Centro
    if tipo_calc == "Menor que X":
        limit_x_min, limit_x_max = mu - 4 * sigma, x_val
        limit_z_min, limit_z_max = -4, z_val
    elif tipo_calc == "Maior que X":
        limit_x_min, limit_x_max = x_val, mu + 4 * sigma
        limit_z_min, limit_z_max = z_val, 4
    elif tipo_calc == "Do Centro (Média) até X":
        limit_x_min, limit_x_max = min(mu, x_val), max(mu, x_val)
        limit_z_min, limit_z_max = min(0, z_val), max(0, z_val)

    aplicar_hachura(ax1, x_axis, y_axis, limit_x_min, limit_x_max, '#1f77b4', mu)
    aplicar_hachura(ax2, z_axis, y_axis_z, limit_z_min, limit_z_max, '#2ca02c', 0)
    ax1.axvline(x_val, color='red', linestyle='--', label=f'X = {x_val}')
    ax2.axvline(z_val, color='red', linestyle='--', label=f'Z = {z_val:.2f}')

ax1.legend()
ax2.legend()

# Exibir no Streamlit
st.pyplot(fig)