import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="GD EM MÃOS - UEFS", layout="wide")

st.title("🚀 GD EM MÃOS - UEFS")
st.markdown("### Geometria Descritiva 3D (Interativo/Rotacionável) e Épura")

menu = st.sidebar.selectbox("Escolha o Assunto", ["PONTOS", "RETAS", "SÓLIDOS"])

# --- FUNÇÃO DE PLOTAGEM 3D INTERATIVA (PLOTLY) ---
def criar_grafico_3d_interativo(pontos, retas=[], solidos_faces=[]):
    fig = go.Figure()

    # Planos de Projeção (PV e PH transparentes)
    xx = np.linspace(-10, 10, 5)
    zz = np.linspace(-10, 10, 5)
    XX, ZZ = np.meshgrid(xx, zz)
    YY = np.zeros_like(XX)

    # Plano Vertical (PV - Y=0)
    fig.add_trace(go.Surface(x=XX, y=YY, z=ZZ, colorscale=[[0, 'gray'], [1, 'gray']], opacity=0.15, showscale=False))
    # Plano Horizontal (PH - Z=0)
    fig.add_trace(go.Surface(x=XX, y=ZZ, z=YY, colorscale=[[0, 'gray'], [1, 'gray']], opacity=0.15, showscale=False))

    # Linha de Terra (Eixo X)
    fig.add_trace(go.Scatter3d(x=[-10, 10], y=[0, 0], z=[0, 0], mode='lines', line=dict(color='black', width=6), name='Linha de Terra (LT)'))

    # Plotar Pontos
    for nome, (x, y, z) in pontos.items():
        # Ponto no espaço
        fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[z], mode='text+markers', marker=dict(size=5, color='black'), text=[f"({nome})"], textposition="top center"))
        # Projeção no PV (Cota)
        fig.add_trace(go.Scatter3d(x=[x], y=[0], z=[z], mode='markers', marker=dict(size=4, color='blue'), showlegend=False))
        # Projeção no PH (Afastamento)
        fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[0], mode='markers', marker=dict(size=4, color='green'), showlegend=False))
        # Linhas de chamada
        fig.add_trace(go.Scatter3d(x=[x, x], y=[y, y], z=[0, z], mode='lines', line=dict(color='gray', dash='dash', width=2), showlegend=False))
        fig.add_trace(go.Scatter3d(x=[x, x], y=[0, y], z=[z, z], mode='lines', line=dict(color='gray', dash='dash', width=2), showlegend=False))

    # Plotar Arestas / Retas / Sólidos
    for p1, p2 in retas:
        c1, c2 = pontos[p1], pontos[p2]
        fig.add_trace(go.Scatter3d(x=[c1[0], c2[0]], y=[c1[1], c2[1]], z=[c1[2], c2[2]], mode='lines', line=dict(color='purple', width=5), name=f'Reta {p1}{p2}'))

    fig.update_layout(
        title="Espacial 3D (Clique e arraste para girar livremente)",
        scene=dict(
            xaxis_title='X (Abcissa)',
            yaxis_title='Y (Afastamento)',
            zaxis_title='Z (Cota)',
            xaxis=dict(range=[-10, 15]),
            yaxis=dict(range=[-10, 15]),
            zaxis=dict(range=[-10, 15]),
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        height=600
    )
    return fig

# --- MÓDULO DE PONTOS NO STREAMLIT ---
if menu == "PONTOS":
    st.subheader("📌 Módulo: Estudo do Ponto")
    num_pontos = st.number_input("Quantos pontos deseja cadastrar?", min_value=1, max_value=10, value=2)
    
    pontos = {}
    with st.form("form_pontos"):
        for i in range(int(num_pontos)):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                nome = st.text_input(f"Nome {i+1}", value=chr(65+i), key=f"p_nome_{i}")
            with col2:
                x = st.number_input(f"X ({nome})", value=float(i*2), key=f"p_x_{i}")
            with col3:
                y = st.number_input(f"Y ({nome})", value=float(i), key=f"p_y_{i}")
            with col4:
                z = st.number_input(f"Z ({nome})", value=float(i), key=f"p_z_{i}")
            pontos[nome.strip().upper()] = (x, y, z)
            
        submitted = st.form_submit_button("Gerar Visualização 3D Interativa")
        
    if submitted:
        # Exibe o 3D interativo do Plotly onde o usuário pode girar com o mouse
        fig_3d = criar_grafico_3d_interativo(pontos)
        st.plotly_chart(fig_3d, use_container_width=True)
            
    else:
        st.info("Módulo de Cones e Cilindros prontos para configuração rápida via parâmetros na barra lateral ou formulários.")
