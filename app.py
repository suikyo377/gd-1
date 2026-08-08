import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="GD EM MÃOS - UEFS", layout="wide")

st.title("🚀 GD EM MÃOS - UEFS")
st.markdown("### Geometria Descritiva 3D (Rotacionável) e Épura")
st.markdown("---")

# Menu principal na tela (evita sumir na barra lateral)
menu = st.radio("Escolha o Assunto que deseja estudar:", ["PONTOS", "RETAS", "SÓLIDOS"], horizontal=True)
st.markdown("---")

# --- FUNÇÃO DE PLOTAGEM 3D INTERATIVA (PLOTLY) ---
def criar_grafico_3d_interativo(pontos, retas=[]):
    fig = go.Figure()

    # Planos de Projeção (PV e PH transparentes)
    xx = np.linspace(-10, 10, 5)
    zz = np.linspace(-10, 10, 5)
    XX, ZZ = np.meshgrid(xx, zz)
    YY = np.zeros_like(XX)

    # Plano Vertical (PV - Y=0)
    fig.add_trace(go.Surface(x=XX, y=YY, z=ZZ, colorscale=[[0, 'gray'], [1, 'gray']], opacity=0.15, showscale=False, name='PV'))
    # Plano Horizontal (PH - Z=0)
    fig.add_trace(go.Surface(x=XX, y=ZZ, z=YY, colorscale=[[0, 'gray'], [1, 'gray']], opacity=0.15, showscale=False, name='PH'))

    # Linha de Terra (Eixo X)
    fig.add_trace(go.Scatter3d(x=[-10, 10], y=[0, 0], z=[0, 0], mode='lines', line=dict(color='black', width=6), name='Linha de Terra (LT)'))

    # Plotar Pontos
    for nome, (x, y, z) in pontos.items():
        fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[z], mode='text+markers', marker=dict(size=6, color='black'), text=[f"({nome})"], textposition="top center"))
        fig.add_trace(go.Scatter3d(x=[x], y=[0], z=[z], mode='markers', marker=dict(size=4, color='blue'), showlegend=False))
        fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[0], mode='markers', marker=dict(size=4, color='green'), showlegend=False))
        fig.add_trace(go.Scatter3d(x=[x, x], y=[y, y], z=[0, z], mode='lines', line=dict(color='gray', dash='dash', width=2), showlegend=False))
        fig.add_trace(go.Scatter3d(x=[x, x], y=[0, y], z=[z, z], mode='lines', line=dict(color='gray', dash='dash', width=2), showlegend=False))

    # Plotar Retas
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

# --- MÓDULO DE PONTOS ---
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
            
        submitted = st.form_submit_button("Gerar Visualização 3D")
        
    if submitted:
        fig_3d = criar_grafico_3d_interativo(pontos)
        st.plotly_chart(fig_3d, use_container_width=True)

# --- MÓDULO DE RETAS ---
elif menu == "RETAS":
    st.subheader("📏 Módulo: Estudo das Retas")
    with st.form("form_retas"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Ponto A**")
            ax = st.number_input("X de A", value=1.0, key="ax")
            ay = st.number_input("Y de A", value=1.5, key="ay")
            az = st.number_input("Z de A", value=2.0, key="az")
        with col2:
            st.markdown("**Ponto B**")
            bx = st.number_input("X de B", value=5.0, key="bx")
            by = st.number_input("Y de B", value=-2.0, key="by")
            bz = st.number_input("Z de B", value=3.0, key="bz")
            
        submitted_reta = st.form_submit_button("Gerar Reta 3D")
        
    if submitted_reta:
        pontos = {'A': (ax, ay, az), 'B': (bx, by, bz)}
        fig_3d = criar_grafico_3d_interativo(pontos, retas=[('A', 'B')])
        st.plotly_chart(fig_3d, use_container_width=True)

# --- MÓDULO DE SÓLIDOS ---
elif menu == "SÓLIDOS":
    st.subheader("📐 Módulo: Sólidos Geométricos")
    st.markdown("Insira os dados da base regular (Aresta AB) e altura:")
    
    with st.form("form_solidos"):
        col1, col2 = st.columns(2)
        with col1:
            ax = st.number_input("X de A", value=1.0, key="sax")
            ay = st.number_input("Y de A", value=1.0, key="say")
            az = st.number_input("Z de A", value=0.0, key="saz")
        with col2:
            bx = st.number_input("X de B", value=3.0, key="sbx")
            by = st.number_input("Y de B", value=1.0, key="sby")
            bz = st.number_input("Z de B", value=0.0, key="sbz")
            
        lados = st.slider("Número de lados da base:", min_value=3, max_value=8, value=6)
        altura = st.number_input("Altura:", value=5.0)
        
        submitted_sol = st.form_submit_button("Gerar Sólido 3D")
        
    if submitted_sol:
        pontos = {'A': (ax, ay, az), 'B': (bx, by, bz)}
        v_x = bx - ax
        v_y = by - ay
        lado_tam = np.hypot(v_x, v_y)
        angulo_externo = np.pi - ((lados - 2) * np.pi / lados)
        
        nomes_vert = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        curr_x, curr_y = bx, by
        angulo_atual = np.arctan2(v_y, v_x)
        
        for i in range(2, lados):
            angulo_atual += angulo_externo
            curr_x += lado_tam * np.cos(angulo_atual)
            curr_y += lado_tam * np.sin(angulo_atual)
            pontos[nomes_vert[i]] = (curr_x, curr_y, az)
            
        fig_3d = criar_grafico_3d_interativo(pontos)
        st.plotly_chart(fig_3d, use_container_width=True)
