import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="GD EM MÃOS - UEFS", layout="wide")

st.title("🚀 GD EM MÃOS - UEFS")
st.markdown("### Geometria Descritiva 3D (Rotacionável) e Épura Interativa")
st.markdown("---")

menu = st.radio("Escolha o Assunto que deseja estudar:", ["PONTOS", "RETAS", "SÓLIDOS"], horizontal=True)
st.markdown("---")

# --- FUNÇÃO DE ÉPURA (MATPLOTLIB) ---
def gerar_epura(pontos, retas=[], solidos_base=[]):
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.axhline(0, color='black', linewidth=1.5, label="Linha de Terra (LT)")
    ax.set_xlabel("X (Abcissa)")
    ax.set_ylabel("Projeções (Cota / -Afastamento)")
    ax.set_xlim([-10, 15])
    ax.set_ylim([-10, 15])
    ax.grid(True, linestyle='--', alpha=0.5)

    # Plotar pontos na épura
    for nome, (x, y, z) in pontos.items():
        # Projeção Vertical P' (Cota acima da LT)
        ax.scatter(x, z, color='blue', s=40)
        ax.text(x, z + 0.3, f"{nome}'", fontsize=10, color='blue', fontweight='bold')
        
        # Projeção Horizontal P'' (Afastamento invertido abaixo da LT)
        ax.scatter(x, -y, color='green', s=40)
        ax.text(x, -y - 0.5, f"{nome}''", fontsize=10, color='green', fontweight='bold')
        
        # Linha de chamada unindo P' e P''
        ax.plot([x, x], [-y, z], color='gray', linestyle=':')

    # Plotar Retas na Épura
    for p1, p2 in retas:
        c1, c2 = pontos[p1], pontos[p2]
        # Projeção vertical
        ax.plot([c1[0], c2[0]], [c1[2], c2[2]], color='blue', linewidth=1.5)
        # Projeção horizontal
        ax.plot([c1[0], c2[0]], [-c1[1], -c2[1]], color='green', linewidth=1.5)

    ax.set_title("Épura (2D)")
    return fig

# --- FUNÇÃO DE 3D INTERATIVO (PLOTLY) ---
def criar_grafico_3d(pontos, retas=[]):
    fig = go.Figure()

    xx = np.linspace(-10, 10, 5)
    zz = np.linspace(-10, 10, 5)
    XX, ZZ = np.meshgrid(xx, zz)
    YY = np.zeros_like(XX)

    fig.add_trace(go.Surface(x=XX, y=YY, z=ZZ, colorscale=[[0, 'gray'], [1, 'gray']], opacity=0.15, showscale=False))
    fig.add_trace(go.Surface(x=XX, y=ZZ, z=YY, colorscale=[[0, 'gray'], [1, 'gray']], opacity=0.15, showscale=False))
    fig.add_trace(go.Scatter3d(x=[-10, 10], y=[0, 0], z=[0, 0], mode='lines', line=dict(color='black', width=6), name='Linha de Terra'))

    for nome, (x, y, z) in pontos.items():
        fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[z], mode='text+markers', marker=dict(size=5, color='black'), text=[f"({nome})"], textposition="top center"))
        fig.add_trace(go.Scatter3d(x=[x], y=[0], z=[z], mode='markers', marker=dict(size=4, color='blue'), showlegend=False))
        fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[0], mode='markers', marker=dict(size=4, color='green'), showlegend=False))
        fig.add_trace(go.Scatter3d(x=[x, x], y=[y, y], z=[0, z], mode='lines', line=dict(color='gray', dash='dash', width=2), showlegend=False))
        fig.add_trace(go.Scatter3d(x=[x, x], y=[0, y], z=[z, z], mode='lines', line=dict(color='gray', dash='dash', width=2), showlegend=False))

    for p1, p2 in retas:
        c1, c2 = pontos[p1], pontos[p2]
        fig.add_trace(go.Scatter3d(x=[c1[0], c2[0]], y=[c1[1], c2[1]], z=[c1[2], c2[2]], mode='lines', line=dict(color='purple', width=5)))

    fig.update_layout(
        title="Espacial 3D (Gire com o mouse)",
        scene=dict(xaxis_range=[-10, 15], yaxis_range=[-10, 15], zaxis_range=[-10, 15]),
        margin=dict(l=0, r=0, b=0, t=30),
        height=550
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
            with col1: nome = st.text_input(f"Nome {i+1}", value=chr(65+i), key=f"p_nome_{i}")
            with col2: x = st.number_input(f"X ({nome})", value=float(i*2), key=f"p_x_{i}")
            with col3: y = st.number_input(f"Y ({nome})", value=float(i), key=f"p_y_{i}")
            with col4: z = st.number_input(f"Z ({nome})", value=float(i), key=f"p_z_{i}")
            pontos[nome.strip().upper()] = (x, y, z)
        submitted = st.form_submit_button("Gerar Visualização")
        
    if submitted:
        col_3d, col_2d = st.columns(2)
        with col_3d:
            st.plotly_chart(criar_grafico_3d(pontos), use_container_width=True)
        with col_2d:
            st.pyplot(gerar_epura(pontos))

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
        submitted_reta = st.form_submit_button("Gerar Reta")
        
    if submitted_reta:
        pontos = {'A': (ax, ay, az), 'B': (bx, by, bz)}
        col_3d, col_2d = st.columns(2)
        with col_3d:
            st.plotly_chart(criar_grafico_3d(pontos, retas=[('A', 'B')]), use_container_width=True)
        with col_2d:
            st.pyplot(gerar_epura(pontos, retas=[('A', 'B')]))

# --- MÓDULO DE SÓLIDOS ---
elif menu == "SÓLIDOS":
    st.subheader("📐 Módulo: Sólidos Geométricos")
    tipo_solido = st.selectbox("Escolha o tipo de sólido:", ["Prisma / Pirâmide (Base Regular por A e B)", "Cone / Cilindro (Base Circular por Centro e Raio)"])
    
    if tipo_solido == "Prisma / Pirâmide (Base Regular por A e B)":
        with st.form("form_sol_reg"):
            col1, col2 = st.columns(2)
            with col1:
                ax = st.number_input("X de A", value=1.0, key="sax")
                ay = st.number_input("Y de A", value=1.0, key="say")
                az = st.number_input("Z de A", value=0.0, key="saz")
            with col2:
                bx = st.number_input("X de B", value=3.0, key="sbx")
                by = st.number_input("Y de B", value=1.0, key="sby")
                bz = st.number_input("Z de B", value=0.0, key="sbz")
            lados = st.slider("Lados da base:", 3, 8, 6)
            altura = st.number_input("Altura:", 5.0)
            tipo_topo = st.radio("Topo:", ["Prisma", "Pirâmide"])
            submitted_sol = st.form_submit_button("Gerar Sólido Poligonal")
            
        if submitted_sol:
            pontos = {'A': (ax, ay, az), 'B': (bx, by, bz)}
            v_x, v_y = bx - ax, by - ay
            lado_tam = np.hypot(v_x, v_y)
            angulo_ext = np.pi - ((lados - 2) * np.pi / lados)
            nomes_vert = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            curr_x, curr_y = bx, by
            angulo_atual = np.arctan2(v_y, v_x)
            
            retas_extras = [('A', 'B')]
            for i in range(2, lados):
                angulo_atual += angulo_ext
                curr_x += lado_tam * np.cos(angulo_atual)
                curr_y += lado_tam * np.sin(angulo_atual)
                p_nome = nomes_vert[i]
                pontos[p_nome] = (curr_x, curr_y, az)
                retas_extras.append((nomes_vert[i-1], p_nome))
            retas_extras.append((nomes_vert[lados-1], 'A'))
            
            base_nomes = list(pontos.keys())
            if tipo_topo == "Prisma":
                for original in base_nomes:
                    px, py, pz = pontos[original]
                    t_nome = f"{original}'"
                    pontos[t_nome] = (px, py, pz + altura)
            else:
                vx, vy, vz = (ax + bx)/2, (ay + by)/2, az + altura
                pontos['V'] = (vx, vy, vz)

            col_3d, col_2d = st.columns(2)
            with col_3d:
                st.plotly_chart(criar_grafico_3d(pontos, retas=retas_extras), use_container_width=True)
            with col_2d:
                st.pyplot(gerar_epura(pontos, retas=retas_extras))

    else:
        with st.form("form_redondo"):
            col1, col2, col3 = st.columns(3)
            with col1: ox = st.number_input("X do Centro (O)", value=3.0)
            with col2: oy = st.number_input("Y do Centro (O)", value=3.0)
            with col3: oz = st.number_input("Z do Centro (O)", value=0.0)
            raio = st.number_input("Raio da Base", value=2.5)
            altura = st.number_input("Altura", value=6.0)
            tipo_red = st.selectbox("Forma:", ["Cilindro", "Cone"])
            submitted_red = st.form_submit_button("Gerar Corpo Redondo")

        if submitted_red:
            pontos = {'O': (ox, oy, oz)}
            theta = np.linspace(0, 2*np.pi, 20)
            base_x = ox + raio * np.cos(theta)
            base_y = oy + raio * np.sin(theta)
            
            # Adicionar pontos amostrais da base no dicionário para a épura
            for i, (bx, by) in enumerate(zip(base_x, base_y)):
                pontos[f'B{i}'] = (bx, by, oz)

            col_3d, col_2d = st.columns(2)
            with col_3d:
                fig_3d = criar_grafico_3d(pontos)
                # Adicionar superfícies circulares no Plotly para cone/cilindro
                topo_z = np.full_like(theta, oz + altura)
                fig_3d.add_trace(go.Scatter3d(x=base_x, y=base_y, z=np.full_like(theta, oz), mode='lines', line=dict(color='purple', width=4), name='Base'))
                if tipo_red == "Cilindro":
                    fig_3d.add_trace(go.Scatter3d(x=base_x, y=base_y, z=topo_z, mode='lines', line=dict(color='purple', width=4), name='Topo'))
                else:
                    fig_3d.add_trace(go.Scatter3d(x=[ox], y=[oy], z=[oz+altura], mode='text+markers', text=['(V)']))
                st.plotly_chart(fig_3d, use_container_width=True)
            with col_2d:
                st.pyplot(gerar_epura(pontos))
