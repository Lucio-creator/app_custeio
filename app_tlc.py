import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Simulador TLC", layout="wide")

st.title("Simulador do Teorema do Limite Central (TLC)")
st.write("Veja a mágica acontecer: conforme o tamanho da amostra aumenta, a distribuição das médias se transforma em uma Curva Normal!")

# ==========================================
# 1. MENU LATERAL (INPUTS)
# ==========================================
st.sidebar.header("1. População Original")
dist_type = st.sidebar.selectbox(
    "Escolha o formato dos dados originais:", 
    ["Exponencial (Muito Assimétrica)", "Uniforme (Plana, ex: dado)", "Normal (Sino perfeito)"]
)

st.sidebar.header("2. Parâmetros da Amostra")
n_samples = st.sidebar.slider("Tamanho da Amostra (n)", min_value=1, max_value=100, value=5, step=1)
num_simulations = st.sidebar.slider("Quantas amostras vamos sortear?", min_value=100, max_value=5000, value=1000, step=100)

# ==========================================
# 2. GERANDO OS DADOS DA POPULAÇÃO
# ==========================================
pop_size = 50000
if dist_type == "Exponencial (Muito Assimétrica)":
    population = np.random.exponential(scale=2.0, size=pop_size)
    cor_pop = 'orange'
elif dist_type == "Uniforme (Plana, ex: dado)":
    population = np.random.uniform(0, 10, size=pop_size)
    cor_pop = 'purple'
else:
    population = np.random.normal(loc=5.0, scale=2.0, size=pop_size)
    cor_pop = 'green'

# ==========================================
# 3. SORTEANDO AS AMOSTRAS (A MÁGICA)
# ==========================================
sample_means = []
for _ in range(num_simulations):
    # Sorteia "n" elementos da população
    sample = np.random.choice(population, size=n_samples, replace=True)
    sample_means.append(np.mean(sample)) # Guarda a média dessa amostra

# ==========================================
# 4. CONSTRUÇÃO DOS GRÁFICOS
# ==========================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
fig.tight_layout(pad=4.0)

# Gráfico 1: A População Original (O que estamos medindo)
sns.histplot(population, bins=50, ax=ax1, color=cor_pop, kde=False, stat="density")
ax1.set_title(f"Distribuição Original da População: {dist_type}", fontweight='bold')
ax1.set_xlabel("Valores Individuais (X)")
ax1.set_ylabel("Frequência")
ax1.set_xlim(np.min(population), np.max(population))

# Gráfico 2: As Médias Amostrais (O resultado do TLC)
sns.histplot(sample_means, bins=30, ax=ax2, color="#1f77b4", kde=True, stat="density")
ax2.set_title(f"Distribuição das Médias Amostrais (Amostras de tamanho n = {n_samples})", fontweight='bold')
ax2.set_xlabel("Médias Amostrais (X̄)")
ax2.set_ylabel("Densidade")

# Adiciona um aviso visual da regra de ouro (n >= 30)
if n_samples >= 30:
    ax2.text(0.95, 0.95, 'n ≥ 30: O TLC garante a Normalidade!', horizontalalignment='right', 
             verticalalignment='top', transform=ax2.transAxes, color='green', fontsize=12, fontweight='bold')
elif n_samples == 1:
    ax2.text(0.95, 0.95, 'n = 1: A distribuição é idêntica à população', horizontalalignment='right', 
             verticalalignment='top', transform=ax2.transAxes, color='red', fontsize=12, fontweight='bold')
else:
    ax2.text(0.95, 0.95, 'n < 30: A curva começa a se formar...', horizontalalignment='right', 
             verticalalignment='top', transform=ax2.transAxes, color='orange', fontsize=12, fontweight='bold')

# Exibir no Streamlit
st.pyplot(fig)