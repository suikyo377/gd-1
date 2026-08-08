import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="GD EM MÃOS - UEFS", layout="wide")

st.title("🚀 GD EM MÃOS - UEFS")
st.markdown("### Geometria Descritiva 3D e Épura com Seção e Rebatimento de VG")
st.markdown("---")

menu = st.radio("Escolha o Assunto que deseja estudar:", ["PONTOS", "RETAS", "SÓLIDOS"], horizontal=True)
st.markdown("---")

# --- FUNÇÃO DE ÉPURA INTEGRADA COM REBATIMENTO DE VG ---
def gerar_epura_integrada(pontos_principais, retas=[], tipo_solido=None, dados_solido=None, dados_secao=None):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.axhline(0, color='black', linewidth=1.5, label="Linha de Terra (LT)")
    ax.set_xlabel("X (Abcissa)")
    ax.set_ylabel("Projeções e Rebatimento (VG)")
    ax.set_xlim([-10, 25])
    ax.set_ylim([-15, 15])
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_aspect('equal', adjustable='box')

    # Plotar pontos principais na Épura
    for nome, (x, y, z) in pontos_principais.items():
        if nome.startswith('B') and len(nome) > 1: continue
        ax.scatter(x, z, color='blue', s=40)
        ax.text(x, z + 0.3, f"{nome}'", fontsize=10, color='blue', fontweight='bold')
        
        ax.scatter(x, -y, color='green', s=40)
        ax.text(x, -y - 0.5, f"{nome}''", fontsize=10, color='green', fontweight='bold')
        
        ax.plot([x, x], [-y, z], color='gray', linestyle=':')

    # Plotar Retas
    for p1, p2 in retas:
        if p1 in pontos_principais and p2 in pontos_principais:
            c1, c2 = pontos_principais[p1], pontos_principais[p2]
            ax.plot([c1[0], c2[0]], [c1[2], c2[2]], color='blue', linewidth=1.5)
            ax.plot([c1[0], c2[0]], [-c1[1], -c2[1]], color='green', linewidth=1.5)

    # Renderização na Épura para Seção Oblíqua
    if tipo_solido and dados_solido:
        forma, ox, oy, oz, raio, altura, lados = dados_solido
        z_base = oz
        z_topo = oz + altura
        
        if forma in ["Cilindro", "Prisma"]:
            x_esq = ox - raio
            x_dir = ox + raio
            ax.plot([x_esq, x_esq], [z_base, z_topo], color='blue', linewidth=1.5)
            ax.plot([x_dir, x_dir], [z_base, z_topo], color='blue', linewidth=1.5)
            ax.plot([x_esq, x_dir], [z_base, z_base], color='blue', linestyle='--', linewidth=1)
            ax.plot([x_esq, x_dir], [z_topo, z_topo], color='blue', linestyle='--', linewidth=1)
        else: # Cone / Pirâmide
            x_esq = ox - raio
            x_dir = ox + raio
            ax.plot([x_esq, ox, x_dir], [z_base, z_topo, z_base], color='blue', linewidth=1.5)
            ax.plot([x_esq, x_dir], [z_base, z_base], color='blue', linestyle='--', linewidth=1)

        # Projeção Horizontal
        if forma in ["Cilindro", "Cone"]:
            theta = np.linspace(0, 2*np.pi, 100)
            cx = ox + raio * np.cos(theta)
            cy_afastamento = -oy + raio * np.sin(theta)
            ax.plot(cx, cy_afastamento, color='green', linewidth=1.5, label="Base (Projeção Horizontal)")
        else:
            # Polígono regular na base horizontal
            angulos = np.linspace(0, 2*np.pi, lados + 1)[:-1]
            px = ox + raio * np.cos(angulos)
            py = -oy + raio * np.sin(angulos)
            px = np.append(px, px[0])
            py = np.append(py, py[0])
            ax.plot(px, py, color='green', linewidth=1.5, label="Base Poligonal H")

    # Plano Secante e Verdadeira Grandeza (Rebatimento)
    if dados_secao:
        alpha_o, alpha_1 = dados_secao
        ang_rad = np.radians(alpha_1)
        
        x_linha = np.linspace(alpha_o - 4, alpha_o + 4, 10)
        z_linha = np.tan(ang_rad) * (x_linha - alpha_o)
        ax.plot(x_linha, z_linha, color='crimson', linewidth=2, label=f"Plano Secante α")

        # Rebatimento da Seção (VG)
        centro_vg_x = alpha_o + 2.0
        centro_vg_z = -6.0
        t_vg = np.linspace(0, 2*np.pi, 100)
        semi_eixo_menor = raio
        fator_elipse = 1.0 / max(0.2, abs(np.sin(ang_rad)))
        semi_eixo_maior = raio * fator_elipse
        
        vg_x = centro_vg_x + (semi_eixo_menor * np.cos(t_vg))
        vg_z = centro_vg_z + (semi_eixo_maior * np.sin(t_vg))
        
        ax.plot(vg_x, vg_z, color='purple', linewidth=2.5, label="Verdadeira Grandeza (VG)")
        ax.fill(vg_x, vg_z, color='purple', alpha=0.15)
        
        ax.legend(loc='upper right')

    ax.set_title("Épura com Seção e Verdadeira Grandeza Integrada")
    return fig

# --- FUNÇÃO DE 3D INTERATIVO (PLOTLY) ---
def criar_grafico_3d(pontos_principais, retas=[], tipo_solido=None, dados_solido=None, dados_secao=None):
    fig = go.Figure()

    xx = np.linspace(-10, 15, 5)
    zz = np.linspace(-10, 15, 5)
    XX, ZZ = np.meshgrid(xx, zz)
    YY = np.zeros_like(XX)

    fig.add_trace(go.Surface(x=XX, y=YY, z=ZZ, colorscale=[[0, 'gray'], [1, 'gray']], opacity=0.15, showscale=False))
    fig.add_trace(go.Surface(x=XX, y=ZZ, z=YY, colorscale=[[0, 'gray'], [1, 'gray']], opacity=0.15, showscale=False))
    fig.add_trace(go.Scatter3d(x=[-10, 15], y=[0, 0], z=[0, 0], mode='lines', line=dict(color='black', width=6), name='Linha de Terra'))

    for nome, (x, y, z) in pontos_principais.items():
        if nome.startswith('B') and len(nome) > 1: continue
        fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[z], mode='text+markers', marker=dict(size=5, color='black'), text=[f"({nome})"], textposition="top center"))
        fig.add_trace(go.Scatter3d(x=[x], y=[0], z=[z], mode='markers', marker=dict(size=4, color='blue'), showlegend=False))
        fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[0], mode='markers', marker=dict(size=4, color='green'), showlegend=False))
        fig.add_trace(go.Scatter3d(x=[x, x], y=[y, y], z=[0, z], mode='lines', line=dict(color='gray', dash='dash', width=2), showlegend=False))
        fig.add_trace(go.Scatter3d(x=[x, x], y=[0, y], z=[z, z], mode='lines', line=dict(color='gray', dash='dash', width=2), showlegend=False))

    for p1, p2 in retas:
        if p1 in pontos_principais and p2 in pontos_principais:
            c1, c2 = pontos_principais[p1], pontos_principais[p2]
            fig.add_trace(go.Scatter3d(x=[c1[0], c2[0]], y=[c1[1], c2[1]], z=[c1[2], c2[2]], mode='lines', line=dict(color='purple', width=5)))

    if tipo_solido and dados_solido:
        forma, ox, oy, oz, raio, altura, lados = dados_solido
        theta = np.linspace(0, 2*np.pi, 40)
        bz = np.full_like(theta, oz)
        topo_z = np.full_like(theta, oz + altura)
        
        if forma in ["Cilindro", "Cone"]:
            bx = ox + raio * np.cos(theta)
            by = oy + raio * np.sin(theta)
            fig.add_trace(go.Scatter3d(x=bx, y=by, z=bz, mode='lines', line=dict(color='purple', width=4), name='Base'))
            if forma == "Cilindro":
                fig.add_trace(go.Scatter3d(x=bx, y=by, z=topo_z, mode='lines', line=dict(color='purple', width=4), name='Topo'))
                for i in [0, 10, 20, 30]:
                    fig.add_trace(go.Scatter3d(x=[bx[i], bx[i]], y=[by[i], by[i]], z=[bz[i], topo_z[i]], mode='lines', line=dict(color='purple', dash='dash')))
            else:
                vx, vy, vz = ox, oy, oz + altura
                for i in [0, 10, 20, 30]:
                    fig.add_trace(go.Scatter3d(x=[bx[i], vx], y=[by[i], vy], z=[bz[i], vz], mode='lines', line=dict(color='purple', dash='dash')))
        else: # Prisma ou Pirâmide poligonal
            angulos = np.linspace(0, 2*np.pi, lados + 1)
            bx = ox + raio * np.cos(angulos)
            by = oy + raio * np.sin(angulos)
            fig.add_trace(go.Scatter3d(x=bx, y=by, z=np.full_like(bx, oz), mode='lines', line=dict(color='purple', width=4), name='Base'))
            if forma == "Prisma":
                topo_x = bx
                topo_y = by
                topo_z_arr = np.full_like(bx, oz + altura)
                fig.add_trace(go.Scatter3d(x=topo_x, y=topo_y, z=topo_z_arr, mode='lines', line=dict(color='purple', width=4), name='Topo'))
                for i in range(len(bx)):
                    fig.add_trace(go.Scatter3d(x=[bx[i], topo_x[i]], y=[by[i], topo_y[i]], z=[oz, oz + altura], mode='lines', line=dict(color='purple', dash='dash')))
            else: # Pirâmide
                vx, vy, vz = ox, oy, oz + altura
                for i in range(len(bx)):
                    fig.add_trace(go.Scatter3d(x=[bx[i], vx], y=[by[i], vy], z=[oz, vz], mode='lines', line=dict(color='purple', dash='dash')))

    if dados_secao:
        alpha_o, alpha_1 = dados_secao
        ang_rad = np.radians(alpha_1)
        yy_p = np.linspace(-10, 10, 5)
        xx_p = np.linspace(alpha_o - 5, alpha_o + 5, 5)
        XX_p, YY_p = np.meshgrid(xx_p, yy_p)
        ZZ_p = np.tan(ang_rad) * (XX_p - alpha_o)
        fig.add_trace(go.Surface(x=XX_p, y=YY_p, z=ZZ_p, colorscale=[[0, 'crimson'], [1, 'crimson']], opacity=0.4, showscale=False, name='Plano Secante'))

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
        with col_3d: st.plotly_chart(criar_grafico_3d(pontos), use_container_width=True)
        with col_2d: st.pyplot(gerar_epura_integrada(pontos))

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
        with col_3d: st.plotly_chart(criar_grafico_3d(pontos, retas=[('A', 'B')]), use_container_width=True)
        with col_2d: st.pyplot(gerar_epura_integrada(pontos, retas=[('A', 'B')]))

# --- MÓDULO DE SÓLIDOS & SEÇÕES ---
elif menu == "SÓLIDOS":
    st.subheader("📐 Módulo: Sólidos e Seções com Eixo Oblíquo")
    tipo_solido = st.selectbox("Escolha o tipo de sólido:", [
        "Prisma / Pirâmide (Base Regular por A e B)", 
        "Cone / Cilindro (Base Circular por Centro e Raio)", 
        "Sólido com Eixo Oblíquo e Plano Secante (Seção + VG)"
    ])
    
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
            topos_nomes = []
            
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
                    topos_nomes.append(t_nome)
                    retas_extras.append((original, t_nome))
                for i in range(len(topos_nomes)):
                    p1 = topos_nomes[i]
                    p2 = topos_nomes[(i + 1) % len(topos_nomes)]
                    retas_extras.append((p1, p2))
            else:
                coords_base = list(pontos.values())
                vx = sum(c[0] for c in coords_base) / len(coords_base)
                vy = sum(c[1] for c in coords_base) / len(coords_base)
                vz = (sum(c[2] for c in coords_base) / len(coords_base)) + altura
                pontos['V'] = (vx, vy, vz)
                for original in base_nomes:
                    retas_extras.append((original, 'V'))

            col_3d, col_2d = st.columns(2)
            with col_3d: st.plotly_chart(criar_grafico_3d(pontos, retas=retas_extras), use_container_width=True)
            with col_2d: st.pyplot(gerar_epura_integrada(pontos, retas=retas_extras))

    elif tipo_solido == "Cone / Cilindro (Base Circular por Centro e Raio)":
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
            dados_sol = (tipo_red, ox, oy, oz, raio, altura, 0)
            col_3d, col_2d = st.columns(2)
            with col_3d:
                st.plotly_chart(criar_grafico_3d(pontos, tipo_solido="Redondo", dados_solido=dados_sol), use_container_width=True)
            with col_2d:
                st.pyplot(gerar_epura_integrada(pontos, tipo_solido="Redondo", dados_solido=dados_sol))

    else:
        st.markdown("### Parâmetros de Seção com Plano Secante ($\alpha$) e Eixo Oblíquo")
        with st.form("form_secao_oblíqua"):
            col1, col2, col3 = st.columns(3)
            with col1: ox = st.number_input("X do Centro da Base (O)", value=2.0)
            with col2: oy = st.number_input("Y do Centro da Base (O)", value=4.0)
            with col3: oz = st.number_input("Z do Centro da Base (O)", value=0.0)
            
            col4, col5 = st.columns(2)
            with col4: raio = st.number_input("Raio / Dimensão da Base", value=3.0)
            with col5: altura = st.number_input("Altura do Sólido", value=6.5)
            
            # ADICIONADO: Seleção de todos os 4 sólidos e ajuste de lados de 3 a 8
            st.markdown("#### Configuração do Sólido e Geometria da Base")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                tipo_sol_obl = st.selectbox("Tipo de Sólido Secionado:", ["Cilindro", "Cone", "Prisma", "Pirâmide"])
            with col_s2:
                lados_base = st.slider("Número de lados da base (para Prisma/Pirâmide):", 3, 8, 6)
            
            st.markdown("#### Configuração do Plano Secante ($\alpha$) / Corte")
            col6, col7 = st.columns(2)
            with col6: alpha_o = st.number_input("Traço $\\alpha_0$ (Abcissa de interseção na LT)", value=9.0)
            with col7: alpha_1 = st.number_input("Ângulo $\\alpha_1$ (Graus com a LT)", value=150.0)
            
            submitted_sec = st.form_submit_button("Gerar Sólido, Seção e Rebatimento de VG")

        if submitted_sec:
            pontos = {'O': (ox, oy, oz)}
            dados_sol = (tipo_sol_obl, ox, oy, oz, raio, altura, lados_base)
            dados_secao = (alpha_o, alpha_1)
            
            col_3d, col_2d = st.columns(2)
            with col_3d:
                st.plotly_chart(criar_grafico_3d(pontos, tipo_solido="Geral", dados_solido=dados_sol, dados_secao=dados_secao), use_container_width=True)
            with col_2d:
                st.pyplot(gerar_epura_integrada(pontos, tipo_solido="Geral", dados_solido=dados_sol, dados_secao=dados_secao))
