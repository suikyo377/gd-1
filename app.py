import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="GD EM MÃOS - UEFS", layout="wide")

st.title("🚀 GD EM MÃOS - UEFS")
st.markdown("### Geometria Descritiva 3D e Épura (Orientação Clássica e VG Rigorosa)")
st.markdown("---")

menu = st.radio("Escolha o Assunto que deseja estudar:", ["PONTOS", "RETAS", "SÓLIDOS"], horizontal=True)
st.markdown("---")

# --- FUNÇÃO AUXILIAR: ORIENTAÇÃO TEÓRICA EXATA DA BASE ---
def obter_geometria_base(forma, ox, oy, oz, raio, lados):
    if forma in ["Cilindro", "Cone"]:
        angulos = np.linspace(0, 2*np.pi, 60)
    else:
        # Orientação geométrica clássica ditada pelo desenho técnico (Pranchas)
        if lados == 3:
            giro = -np.pi / 2  # Triângulo: Vértice apontando para cima (LT)
        elif lados == 4:
            giro = np.pi / 4   # Quadrado: Apoiado de forma plana
        elif lados == 5:
            giro = -np.pi / 2  # Pentágono: Vértice central para cima (LT)
        elif lados == 6:
            giro = 0           # Hexágono: Vértices nas laterais, lados planos em cima/baixo
        elif lados == 8:
            giro = np.pi / 8   # Octógono: Apoiado de forma plana
        else:
            giro = -np.pi / 2 if lados % 2 != 0 else 0
            
        angulos = np.linspace(0, 2*np.pi, lados + 1)[:-1] + giro
        
    bx = ox + raio * np.cos(angulos)
    by = oy + raio * np.sin(angulos)
    
    # Fechar o polígono para o desenho contínuo
    if forma in ["Prisma", "Pirâmide"]:
        bx = np.append(bx, bx[0])
        by = np.append(by, by[0])
        
    return bx, by

def desenhar_arco_rebatimento(ax, cx, cy, start_x, start_y, end_x):
    """Desenha o traço curvo do compasso simulando a mão do desenhista no papel"""
    r = np.hypot(start_x - cx, start_y - cy)
    theta1 = np.arctan2(start_y - cy, start_x - cx)
    theta2 = 0.0 if end_x > cx else np.pi
    
    t = np.linspace(theta1, theta2, 30)
    ax.plot(cx + r * np.cos(t), cy + r * np.sin(t), color='gray', linestyle='-.', linewidth=1.2)

# --- FUNÇÃO DE ÉPURA INTEGRADA ---
def gerar_epura_integrada(pontos_principais, retas=[], tipo_solido=None, dados_solido=None, dados_secao=None):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.axhline(0, color='black', linewidth=1.5, label="Linha de Terra (LT)")
    ax.set_xlabel("X (Abcissa)")
    ax.set_ylabel("Projeções e Rebatimento (VG)")
    ax.set_xlim([-15, 25])
    ax.set_ylim([-15, 15])
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # Proporção geométrica real travada (evita círculos ovais e VG deformada)
    ax.set_aspect('equal', adjustable='box')

    if tipo_solido and dados_solido and dados_secao:
        forma, ox, oy, oz, raio, altura, lados = dados_solido
        alpha_o, alpha_1 = dados_secao
        ang_rad = np.radians(alpha_1)

        # 1. Obter a geometria perfeitamente orientada
        px_base, py_base = obter_geometria_base(forma, ox, oy, oz, raio, lados)

        # 2. Plotar a Projeção Horizontal da Base
        ax.plot(px_base, -py_base, color='green', linewidth=1.5, label="Base (Proj. Horizontal)")
        
        # 3. Calcular Interseção (Corte) com o Plano Secante
        sx_list, sy_list, sz_list = [], [], []
        for px, py in zip(px_base, py_base):
            if forma in ["Prisma", "Cilindro"]:
                t = (np.tan(ang_rad) * (px - alpha_o) - oz) / altura if altura != 0 else 0
                sx, sy = px, py
                sz = oz + t * altura
            else: # Pirâmide / Cone
                den = altura - np.tan(ang_rad)*(ox - px)
                t = (np.tan(ang_rad)*(px - alpha_o) - oz) / den if abs(den) > 1e-5 else 0
                sx = px + t * (ox - px)
                sy = py + t * (oy - py)
                sz = oz + t * altura
                
            sx_list.append(sx)
            sy_list.append(sy)
            sz_list.append(sz)

        # 4. Desenhar Arestas/Geratrizes na Projeção Vertical
        if forma in ["Prisma", "Pirâmide"]:
            for px, sz_corte in zip(px_base[:-1], sz_list[:-1]):
                if forma == "Prisma":
                    ax.plot([px, px], [oz, oz + altura], color='blue', linewidth=1.0, alpha=0.5)
                else:
                    ax.plot([px, ox], [oz, oz + altura], color='blue', linewidth=1.0, alpha=0.5)
        else: # Cilindro / Cone
            ax.plot([ox-raio, ox-raio], [oz, oz+altura] if forma=="Cilindro" else [oz, oz], color='blue')
            ax.plot([ox+raio, ox+raio], [oz, oz+altura] if forma=="Cilindro" else [oz, oz], color='blue')
            if forma == "Cone":
                ax.plot([ox-raio, ox, ox+raio], [oz, oz+altura, oz], color='blue')

        # 5. Traço do Plano Secante
        x_linha = np.linspace(alpha_o - 5, alpha_o + 10, 10)
        z_linha = np.tan(ang_rad) * (x_linha - alpha_o)
        ax.plot(x_linha, z_linha, color='crimson', linewidth=2, label=f"Plano Secante α")

        # 6. REBATIMENTO INTELIGENTE E EXATO
        direcao_rebate = -1 if ox >= alpha_o else 1 # Foge para o lado oposto do sólido
        
        rx_list, ry_list = [], []
        pontos_construcao = range(len(sx_list)-1) if forma in ["Prisma", "Pirâmide"] else [0, 15, 30, 45]
        
        for i in range(len(sx_list)):
            sx, sy, sz = sx_list[i], sy_list[i], sz_list[i]
            
            # Raio do compasso e rebatimento
            dist_rebatida = np.hypot(sx - alpha_o, sz)
            rx = alpha_o + dist_rebatida * direcao_rebate
            ry = -sy 
            
            rx_list.append(rx)
            ry_list.append(ry)
            
            # Linhas de Construção do compasso
            if i in pontos_construcao:
                desenhar_arco_rebatimento(ax, alpha_o, 0, sx, sz, rx) # Arco até a LT
                ax.plot([rx, rx], [0, ry], color='gray', linestyle=':', linewidth=1.2) # Chamada vertical
                ax.plot([sx, rx], [-sy, ry], color='gray', linestyle=':', linewidth=1.2) # Chamada horizontal

        # 7. Plotar a Verdadeira Grandeza (Polígono exato ou Elipse Final)
        ax.plot(rx_list, ry_list, color='purple', linewidth=2.5, label="Verdadeira Grandeza (VG)")
        ax.fill(rx_list, ry_list, color='purple', alpha=0.2)
        
        # Pontuar os vértices cortados
        if forma in ["Prisma", "Pirâmide"]:
            ax.scatter(rx_list[:-1], ry_list[:-1], color='purple', s=30, zorder=5)

        ax.legend(loc='upper right')
        ax.set_title("Épura com Seção e Rebatimento Geométrico Exato (VG)")
        
    return fig

# --- FUNÇÃO DE 3D INTERATIVO (PLOTLY) ---
def criar_grafico_3d(tipo_solido=None, dados_solido=None, dados_secao=None):
    fig = go.Figure()

    xx = np.linspace(-10, 15, 5)
    zz = np.linspace(-10, 15, 5)
    XX, ZZ = np.meshgrid(xx, zz)
    YY = np.zeros_like(XX)

    fig.add_trace(go.Surface(x=XX, y=YY, z=ZZ, colorscale=[[0, 'gray'], [1, 'gray']], opacity=0.15, showscale=False))
    fig.add_trace(go.Surface(x=XX, y=ZZ, z=YY, colorscale=[[0, 'gray'], [1, 'gray']], opacity=0.15, showscale=False))
    fig.add_trace(go.Scatter3d(x=[-10, 20], y=[0, 0], z=[0, 0], mode='lines', line=dict(color='black', width=6), name='Linha de Terra'))

    if tipo_solido and dados_solido:
        forma, ox, oy, oz, raio, altura, lados = dados_solido
        
        # Sincronização 3D com a orientação correta
        bx, by = obter_geometria_base(forma, ox, oy, oz, raio, lados)
        bz = np.full_like(bx, oz)
        topo_z = np.full_like(bx, oz + altura)
        
        # Base Inferior
        fig.add_trace(go.Scatter3d(x=bx, y=by, z=bz, mode='lines', line=dict(color='green', width=4), name='Base'))
        
        # Arestas / Geratrizes
        if forma == "Prisma":
            fig.add_trace(go.Scatter3d(x=bx, y=by, z=topo_z, mode='lines', line=dict(color='blue', width=4), name='Topo'))
            for i in range(len(bx)-1):
                fig.add_trace(go.Scatter3d(x=[bx[i], bx[i]], y=[by[i], by[i]], z=[oz, oz + altura], mode='lines', line=dict(color='blue', dash='dash')))
        elif forma == "Cilindro":
            fig.add_trace(go.Scatter3d(x=bx, y=by, z=topo_z, mode='lines', line=dict(color='blue', width=4), name='Topo'))
            for i in [0, 10, 20, 30]:
                fig.add_trace(go.Scatter3d(x=[bx[i], bx[i]], y=[by[i], by[i]], z=[oz, oz + altura], mode='lines', line=dict(color='blue', dash='dash')))
        else: # Pirâmide / Cone
            vx, vy, vz = ox, oy, oz + altura
            pontos_tracado = range(len(bx)-1) if forma == "Pirâmide" else [0, 10, 20, 30]
            for i in pontos_tracado:
                fig.add_trace(go.Scatter3d(x=[bx[i], vx], y=[by[i], vy], z=[bz[i], vz], mode='lines', line=dict(color='blue', dash='dash')))

    # Plano Secante e Polígono de Corte 3D
    if dados_secao:
        alpha_o, alpha_1 = dados_secao
        ang_rad = np.radians(alpha_1)
        
        # Desenhar o Plano Transparente
        yy_p = np.linspace(oy - raio - 2, oy + raio + 2, 5)
        xx_p = np.linspace(alpha_o - 5, alpha_o + 10, 5)
        XX_p, YY_p = np.meshgrid(xx_p, yy_p)
        ZZ_p = np.tan(ang_rad) * (XX_p - alpha_o)
        fig.add_trace(go.Surface(x=XX_p, y=YY_p, z=ZZ_p, colorscale=[[0, 'crimson'], [1, 'crimson']], opacity=0.3, showscale=False, name='Plano Secante'))

        # Desenhar a Seção real (Roxa) no espaço 3D
        sx_list, sy_list, sz_list = [], [], []
        for px, py in zip(bx, by):
            if forma in ["Prisma", "Cilindro"]:
                t = (np.tan(ang_rad) * (px - alpha_o) - oz) / altura if altura != 0 else 0
                sx, sy = px, py
                sz = oz + t * altura
            else:
                den = altura - np.tan(ang_rad)*(ox - px)
                t = (np.tan(ang_rad)*(px - alpha_o) - oz) / den if abs(den) > 1e-5 else 0
                sx = px + t * (ox - px)
                sy = py + t * (oy - py)
                sz = oz + t * altura
            sx_list.append(sx)
            sy_list.append(sy)
            sz_list.append(sz)
            
        fig.add_trace(go.Scatter3d(x=sx_list, y=sy_list, z=sz_list, mode='lines', line=dict(color='purple', width=6), name='Seção (Corte)'))

    fig.update_layout(
        title="Espacial 3D (Gire com o mouse)",
        scene=dict(xaxis_range=[-5, 15], yaxis_range=[-5, 15], zaxis_range=[-5, 15]),
        margin=dict(l=0, r=0, b=0, t=30),
        height=550
    )
    return fig

# --- MÓDULO PRINCIPAL ---
if menu == "PONTOS":
    st.info("Para testar as novidades rigorosas, acesse a aba 'SÓLIDOS' -> 'Seção e Rebatimento'.")
elif menu == "RETAS":
    st.info("Para testar as novidades rigorosas, acesse a aba 'SÓLIDOS' -> 'Seção e Rebatimento'.")

elif menu == "SÓLIDOS":
    st.subheader("📐 Módulo: Sólidos e Seções com Eixo Oblíquo")
    
    st.markdown("### Parâmetros do Sólido e do Plano Secante ($\alpha$)")
    with st.form("form_secao_obliqua"):
        col1, col2, col3 = st.columns(3)
        with col1: ox = st.number_input("X do Centro da Base (O)", value=4.0)
        with col2: oy = st.number_input("Y do Centro da Base (O)", value=4.0)
        with col3: oz = st.number_input("Z do Centro da Base (O)", value=0.0)
        
        col4, col5 = st.columns(2)
        with col4: raio = st.number_input("Raio / Dimensão da Base", value=2.5)
        with col5: altura = st.number_input("Altura do Sólido", value=7.0)
        
        st.markdown("#### Configuração do Sólido e Geometria da Base")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            tipo_sol_obl = st.selectbox("Tipo de Sólido Secionado:", ["Prisma", "Pirâmide", "Cilindro", "Cone"])
        with col_s2:
            lados_base = st.slider("Número de lados da base (para Prisma/Pirâmide):", 3, 8, 5)
        
        st.markdown("#### Configuração do Plano Secante ($\alpha$) / Corte")
        col6, col7 = st.columns(2)
        with col6: alpha_o = st.number_input("Traço $\\alpha_0$ (Abcissa de interseção na LT)", value=2.0)
        with col7: alpha_1 = st.number_input("Ângulo $\\alpha_1$ (Graus com a LT)", value=30.0)
        
        submitted_sec = st.form_submit_button("Gerar Geometria Clássica e Rebatimento")

    if submitted_sec:
        dados_sol = (tipo_sol_obl, ox, oy, oz, raio, altura, lados_base)
        dados_secao = (alpha_o, alpha_1)
        
        col_3d, col_2d = st.columns(2)
        with col_3d:
            st.plotly_chart(criar_grafico_3d(tipo_solido="Geral", dados_solido=dados_sol, dados_secao=dados_secao), use_container_width=True)
        with col_2d:
            st.pyplot(gerar_epura_integrada({}, retas=[], tipo_solido="Geral", dados_solido=dados_sol, dados_secao=dados_secao))
