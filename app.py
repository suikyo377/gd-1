import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="GD EM MÃOS - UEFS", layout="wide")

def configurar_graficos():
    fig = plt.figure(figsize=(14, 6))
    
    # Gráfico 3D (Espacial com Planos)
    ax_3d = fig.add_subplot(121, projection='3d')
    ax_3d.set_title("Representação Espacial 3D")
    ax_3d.set_xlabel("X (Abcissa)")
    ax_3d.set_ylabel("Y (Afastamento)")
    ax_3d.set_zlabel("Z (Cota)")
    ax_3d.set_xlim([-10, 15])
    ax_3d.set_ylim([-10, 15])
    ax_3d.set_zlim([-10, 15])
    
    # Planos PV e PH transparentes
    xx = np.linspace(-10, 10, 10)
    zz = np.linspace(-10, 10, 10)
    XX, ZZ = np.meshgrid(xx, zz)
    YY = np.zeros_like(XX)
    ax_3d.plot_surface(XX, YY, ZZ, color='gray', alpha=0.15, edgecolor='none')
    
    XX_h, YY_h = np.meshgrid(np.linspace(-10, 10, 10), np.linspace(-10, 10, 10))
    ZZ_h = np.zeros_like(XX_h)
    ax_3d.plot_surface(XX_h, YY_h, ZZ_h, color='gray', alpha=0.15, edgecolor='none')
    ax_3d.plot([-10, 10], [0, 0], [0, 0], color='black', linewidth=2, label="Linha de Terra")

    # Gráfico 2D (Épura)
    ax_2d = fig.add_subplot(122)
    ax_2d.set_title("Épura (2D)")
    ax_2d.axhline(0, color='black', linewidth=1.5, label="Linha de Terra (LT)")
    ax_2d.set_xlabel("X (Abcissa)")
    ax_2d.set_ylabel("Projeções")
    ax_2d.set_xlim([-10, 15])
    ax_2d.set_ylim([-10, 15])
    ax_2d.grid(True, linestyle='--', alpha=0.5)
    
    return fig, ax_3d, ax_2d

def plotar_ponto(ax_3d, ax_2d, nome, x, y, z):
    ax_3d.scatter(x, y, z, color='black', s=40)
    ax_3d.text(x, y, z, f" ({nome})", fontsize=10, fontweight='bold')
    ax_3d.scatter(x, 0, z, color='blue', s=30)
    ax_3d.scatter(x, y, 0, color='green', s=30)
    ax_3d.plot([x, x], [y, y], [0, z], color='gray', linestyle='--', alpha=0.5)
    ax_3d.plot([x, x], [0, y], [z, z], color='gray', linestyle='--', alpha=0.5)

    ax_2d.scatter(x, z, color='blue', s=40)
    ax_2d.text(x, z + 0.3, f"{nome}'", fontsize=10, color='blue', fontweight='bold')
    ax_2d.scatter(x, -y, color='green', s=40)
    ax_2d.text(x, -y - 0.5, f"{nome}''", fontsize=10, color='green', fontweight='bold')
    ax_2d.plot([x, x], [-y, z], color='gray', linestyle=':')

# Título principal
st.title("🚀 GD EM MÃOS - UEFS")
st.markdown("### Geometria Descritiva 3D e Épura Interativa")

# Menu lateral para escolher o módulo
menu = st.sidebar.selectbox("Escolha o Assunto", ["PONTOS", "RETAS", "SÓLIDOS"])

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
            
        submitted = st.form_submit_button("Gerar Gráficos")
        
    if submitted:
        fig, ax_3d, ax_2d = configurar_graficos()
        for nome, (x, y, z) in pontos.items():
            plotar_ponto(ax_3d, ax_2d, nome, x, y, z)
        st.pyplot(fig)

elif menu == "RETAS":
    st.subheader("📏 Módulo: Estudo das Retas")
    st.markdown("Insira os dois pontos extremos da reta ($A$ e $B$):")
    
    with st.form("form_retas"):
        col1, col2, col3 = st.columns(3)
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
            
        submitted_reta = st.form_submit_button("Gerar Reta no 3D e Épura")
        
    if submitted_reta:
        fig, ax_3d, ax_2d = configurar_graficos()
        pontos = {'A': (ax, ay, az), 'B': (bx, by, bz)}
        
        for nome, (x, y, z) in pontos.items():
            plotar_ponto(ax_3d, ax_2d, nome, x, y, z)
            
        ax_3d.plot([ax, bx], [ay, by], [az, bz], color='purple', linewidth=2, label="Reta AB")
        ax_2d.plot([ax, bx], [az, bz], color='blue', linewidth=1.2, label="Projeção Vertical")
        ax_2d.plot([ax, bx], [-ay, -by], color='green', linewidth=1.2, label="Projeção Horizontal")
        
        ax_3d.legend()
        ax_2d.legend()
        st.pyplot(fig)

elif menu == "SÓLIDOS":
    st.subheader("📐 Módulo: Sólidos Geométricos")
    tipo_solido = st.selectbox("Selecione o tipo de sólido:", ["Prisma / Pirâmide (Base Regular por A e B)", "Cone / Cilindro (Base Circular)"])
    
    if tipo_solido == "Prisma / Pirâmide (Base Regular por A e B)":
        with st.form("form_solido_reg"):
            st.markdown("### Definição da Aresta Inicial (AB) da Base")
            col1, col2 = st.columns(2)
            with col1:
                ax = st.number_input("X de A", value=1.0, key="sax")
                ay = st.number_input("Y de A", value=1.0, key="say")
                az = st.number_input("Z de A", value=0.0, key="saz")
            with col2:
                bx = st.number_input("X de B", value=3.0, key="sbx")
                by = st.number_input("Y de B", value=1.0, key="sby")
                bz = st.number_input("Z de B", value=0.0, key="sbz")
                
            lados = st.slider("Número de lados da base regular:", min_value=3, max_value=8, value=6)
            altura = st.number_input("Altura do sólido:", value=5.0)
            tipo_topo = st.radio("Topo do Sólido:", ["Prisma (Base Superior igual)", "Pirâmide (Vértice no Topo)"])
            
            submitted_sol = st.form_submit_button("Gerar Sólido")
            
        if submitted_sol:
            fig, ax_3d, ax_2d = configurar_graficos()
            pontos = {'A': (ax, ay, az), 'B': (bx, by, bz)}
            
            v_x = bx - ax
            v_y = by - ay
            lado_tam = np.hypot(v_x, v_y)
            angulo_interno = (lados - 2) * np.pi / lados
            angulo_rot_externo = np.pi - angulo_interno
            
            nomes_vert = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
            curr_x, curr_y = bx, by
            angulo_atual = np.arctan2(v_y, v_x)
            
            for i in range(2, lados):
                angulo_atual += angulo_rot_externo
                curr_x += lado_tam * np.cos(angulo_atual)
                curr_y += lado_tam * np.sin(angulo_atual)
                pontos[nomes_vert[i]] = (curr_x, curr_y, az)
                
            base_nomes = list(pontos.keys())
            topo_nomes = []
            
            if "Prisma" in tipo_topo:
                for original in base_nomes:
                    px, py, pz = pontos[original]
                    t_nome = f"{original}'"
                    pontos[t_nome] = (px, py, pz + altura)
                    topo_nomes.append(t_nome)
            
            for nome, (x, y, z) in pontos.items():
                plotar_ponto(ax_3d, ax_2d, nome, x, y, z)
                
            # Desenhar base inferior
            for i in range(len(base_nomes)):
                p1, p2 = pontos[base_nomes[i]], pontos[base_nomes[(i+1)%len(base_nomes)]]
                ax_3d.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='purple', linewidth=2)
                ax_2d.plot([p1[0], p2[0]], [p1[2], p2[2]], color='blue', linewidth=1.2)
                ax_2d.plot([p1[0], p2[0]], [-p1[1], -p2[1]], color='green', linewidth=1.2)
                
            if topo_nomes:
                for i in range(len(topo_nomes)):
                    p1, p2 = pontos[topo_nomes[i]], pontos[topo_nomes[(i+1)%len(topo_nomes)]]
                    ax_3d.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='purple', linewidth=2)
                    ax_2d.plot([p1[0], p2[0]], [p1[2], p2[2]], color='blue', linewidth=1.2)
                    ax_2d.plot([p1[0], p2[0]], [-p1[1], -p2[1]], color='green', linewidth=1.2)
                    
                for i in range(len(base_nomes)):
                    p1, p2 = pontos[base_nomes[i]], pontos[topo_nomes[i]]
                    ax_3d.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='purple', linestyle='--')
                    ax_2d.plot([p1[0], p2[0]], [p1[2], p2[2]], color='blue', linestyle='--')
                    ax_2d.plot([p1[0], p2[0]], [-p1[1], -p2[1]], color='green', linestyle='--')
            else:
                # Pirâmide
                vx, vy, vz = (ax + bx)/2, (ay + by)/2, az + altura
                plotar_ponto(ax_3d, ax_2d, 'V', vx, vy, vz)
                for b_nome in base_nomes:
                    b_coord = pontos[b_nome]
                    ax_3d.plot([b_coord[0], vx], [b_coord[1], vy], [b_coord[2], vz], color='purple', linestyle='--')
                    ax_2d.plot([b_coord[0], vx], [b_coord[2], vz], color='blue', linestyle='--')
                    ax_2d.plot([b_coord[0], vx], [-b_coord[1], -vy], color='green', linestyle='--')
                    
            st.pyplot(fig)
            
    else:
        st.info("Módulo de Cones e Cilindros prontos para configuração rápida via parâmetros na barra lateral ou formulários.")