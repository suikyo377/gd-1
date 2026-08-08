import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="GD EM MÃOS - UEFS", layout="wide")

st.title("🚀 GD EM MÃOS - UEFS")
st.markdown("### Geometria Descritiva 3D e Épura com VG Rigorosa (Método do Rebatimento)")
st.markdown("---")

menu = st.radio("Escolha o Assunto que deseja estudar:", ["PONTOS", "RETAS", "SÓLIDOS"], horizontal=True)
st.markdown("---")

def desenhar_arco_rebatimento(ax, cx, cy, start_x, start_y, end_x):
    """Função auxiliar para desenhar o traço do compasso no rebatimento"""
    r = np.hypot(start_x - cx, start_y - cy)
    theta1 = np.arctan2(start_y - cy, start_x - cx)
    theta2 = 0.0 if end_x > cx else np.pi
    
    t = np.linspace(theta1, theta2, 30)
    ax.plot(cx + r * np.cos(t), cy + r * np.sin(t), color='gray', linestyle='-.', linewidth=1.2)

# --- FUNÇÃO DE ÉPURA INTEGRADA COM REBATIMENTO DE VG ---
def gerar_epura_integrada(pontos_principais, retas=[], tipo_solido=None, dados_solido=None, dados_secao=None):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.axhline(0, color='black', linewidth=1.5, label="Linha de Terra (LT)")
    ax.set_xlabel("X (Abcissa)")
    ax.set_ylabel("Projeções e Rebatimento (VG)")
    ax.set_xlim([-5, 25])
    ax.set_ylim([-15, 15])
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # FUNDAMENTAL: Mantém a proporção real para que polígonos e circunferências não fiquem deformados
    ax.set_aspect('equal', adjustable='box')

    if tipo_solido and dados_solido and dados_secao:
        forma, ox, oy, oz, raio, altura, lados = dados_solido
        alpha_o, alpha_1 = dados_secao
        ang_rad = np.radians(alpha_1)

        # 1. Gerar os pontos da Base
        if forma in ["Cilindro", "Cone"]:
            angulos = np.linspace(0, 2*np.pi, 60)
        else:
            # Polígono regular (adicionado pi/2 para alinhar a base visualmente)
            angulos = np.linspace(0, 2*np.pi, lados + 1)[:-1] + (np.pi/2 if lados % 2 != 0 else np.pi/lados)
            
        px_base = ox + raio * np.cos(angulos)
        py_base = oy + raio * np.sin(angulos)
        
        if forma in ["Prisma", "Pirâmide"]:
            px_base = np.append(px_base, px_base[0])
            py_base = np.append(py_base, py_base[0])

        # 2. Plotar a Projeção Horizontal da Base (Verde)
        ax.plot(px_base, -py_base, color='green', linewidth=1.5, label="Base (Proj. Horizontal)")
        
        # 3. Calcular Interseção (Corte) com o Plano Secante
        sx_list, sy_list, sz_list = [], [], []
        for px, py in zip(px_base, py_base):
            if forma in ["Prisma", "Cilindro"]:
                t = (np.tan(ang_rad) * (px - alpha_o) - oz) / altura if altura != 0 else 0
                sx, sy = px, py
                sz = oz + t * altura # Z do corte na geratriz
            else: # Pirâmide, Cone (Geratrizes inclinadas para o vértice)
                den = altura - np.tan(ang_rad)*(ox - px)
                t = (np.tan(ang_rad)*(px - alpha_o) - oz) / den if abs(den) > 1e-5 else 0
                sx = px + t * (ox - px)
                sy = py + t * (oy - py)
                sz = oz + t * altura
                
            sx_list.append(sx)
            sy_list.append(sy)
            sz_list.append(sz)

        # 4. Desenhar Arestas/Geratrizes na Projeção Vertical (Azul)
        if forma in ["Prisma", "Pirâmide"]:
            for px, sz_corte in zip(px_base[:-1], sz_list[:-1]):
                if forma == "Prisma":
                    ax.plot([px, px], [oz, oz + altura], color='blue', linewidth=1.0, alpha=0.5)
                else:
                    ax.plot([px, ox], [oz, oz + altura], color='blue', linewidth=1.0, alpha=0.5)
        else: # Contornos do Cilindro/Cone
            ax.plot([ox-raio, ox-raio], [oz, oz+altura] if forma=="Cilindro" else [oz, oz], color='blue')
            ax.plot([ox+raio, ox+raio], [oz, oz+altura] if forma=="Cilindro" else [oz, oz], color='blue')
            if forma == "Cone":
                ax.plot([ox-raio, ox, ox+raio], [oz, oz+altura, oz], color='blue')

        # 5. Traço do Plano Secante
        x_linha = np.linspace(alpha_o - 2, alpha_o + 8, 10)
        z_linha = np.tan(ang_rad) * (x_linha - alpha_o)
        ax.plot(x_linha, z_linha, color='crimson', linewidth=2, label=f"Plano Secante α")

        # 6. REBATIMENTO RIGOROSO (VG)
        rx_list, ry_list = [], []
        
        # Selecionar pontos estratégicos para desenhar as linhas de construção (evitar poluição visual)
        pontos_construcao = range(len(sx_list)-1) if forma in ["Prisma", "Pirâmide"] else [0, 15, 30, 45]
        
        for i in range(len(sx_list)):
            sx, sy, sz = sx_list[i], sy_list[i], sz_list[i]
            
            # Distância do rebatimento: Hipotenusa do ponto até o traço alpha_o
            dist_rebatida = np.hypot(sx - alpha_o, sz)
            # Determina o lado do rebatimento
            direcao = np.sign(sx - alpha_o) if sx != alpha_o else 1
            rx = alpha_o + dist_rebatida * direcao
            ry = -sy # O afastamento se mantém
            
            rx_list.append(rx)
            ry_list.append(ry)
            
            # Desenhar o caminho do compasso e esquadro apenas para os vértices principais
            if i in pontos_construcao:
                # Arco do corte até a LT
                desenhar_arco_rebatimento(ax, alpha_o, 0, sx, sz, rx)
                # Linha vertical descendo da LT até o afastamento
                ax.plot([rx, rx], [0, ry], color='gray', linestyle=':', linewidth=1.2)
                # Linha horizontal puxando o afastamento da base
                ax.plot([sx, rx], [-sy, ry], color='gray', linestyle=':', linewidth=1.2)

        # 7. Plotar o Polígono/Elipse Final em Verdadeira Grandeza
        ax.plot(rx_list, ry_list, color='purple', linewidth=2.5, label="Verdadeira Grandeza (VG)")
        ax.fill(rx_list, ry_list, color='purple', alpha=0.2)
        
        # Marcar vértices da VG
        if forma in ["Prisma", "Pirâmide"]:
            ax.scatter(rx_list[:-1], ry_list[:-1], color='purple', s=30, zorder=5)

        ax.legend(loc='upper right')
        ax.set_title("Épura com Seção e Rebatimento Geométrico Exato (VG)")
        
    return fig

# --- FUNÇÃO DE 3D INTERATIVO (PLOTLY) ---
def criar_grafico_3d(tipo_solido=None, dados_solido=None, dados_secao=None):
    fig = go.Figure()

    xx = np.linspace(-5, 15, 5)
    zz = np.linspace(-5, 15, 5)
    XX, ZZ = np.meshgrid(xx, zz)
    YY = np.zeros_like(XX)

    fig.add_trace(go.Surface(x=XX, y=YY, z=ZZ, colorscale=[[0, 'gray'], [1, 'gray']], opacity=0.15, showscale=False))
    fig.add_trace(go.Surface(x=XX, y=ZZ, z=YY, colorscale=[[0, 'gray'], [1, 'gray']], opacity=0.15, showscale=False))
    fig.add_trace(go.Scatter3d(x=[-5, 20], y=[0, 0], z=[0, 0], mode='lines', line=dict(color='black', width=6), name='Linha de Terra'))

    if tipo_solido and dados_solido:
        forma, ox, oy, oz, raio, altura, lados = dados_solido
        
        if forma in ["Cilindro", "Cone"]:
            angulos = np.linspace(0, 2*np.pi, 40)
        else:
            angulos = np.linspace(0, 2*np.pi, lados + 1)[:-1] + (np.pi/2 if lados % 2 != 0 else np.pi/lados)
            
        bx = ox + raio * np.cos(angulos)
        by = oy + raio * np.sin(angulos)
        
        if forma in ["Prisma", "Pirâmide"]:
            bx = np.append(bx, bx[0])
            by = np.append(by, by[0])
            
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
        xx_p = np.linspace(alpha_o - 2, alpha_o + 8, 5)
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
    with st.form("form_secao_oblíqua"):
        col1, col2, col3 = st.columns(3)
        with col1: ox = st.number_input("X do Centro da Base (O)", value=4.0)
        with col2: oy = st.number_input("Y do Centro da Base (O)", value=4.0)
        with col3: oz = st.number_input("Z do Centro da Base (O)", value=0.0)
        
        col4, col5 = st.columns(2)
        with col4: raio = st.number_input("Raio / Dimensão da Base", value=2.5)
        with col5: altura = st.number_input("Altura do Sólido", value=7.0)
        
        st.markdown("#### Configuração do Sólido")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            tipo_sol_obl = st.selectbox("Tipo de Sólido Secionado:", ["Prisma", "Pirâmide", "Cilindro", "Cone"])
        with col_s2:
            lados_base = st.slider("Número de lados da base (para Prisma/Pirâmide):", 3, 8, 5)
        
        st.markdown("#### Configuração do Plano Secante ($\alpha$) / Corte")
        col6, col7 = st.columns(2)
        with col6: alpha_o = st.number_input("Traço $\\alpha_0$ (Abcissa de interseção na LT)", value=2.0)
        with col7: alpha_1 = st.number_input("Ângulo $\\alpha_1$ (Graus com a LT)", value=30.0)
        
        submitted_sec = st.form_submit_button("Gerar Geometria e Rebatimento")

    if submitted_sec:
        dados_sol = (tipo_sol_obl, ox, oy, oz, raio, altura, lados_base)
        dados_secao = (alpha_o, alpha_1)
        
        col_3d, col_2d = st.columns(2)
        with col_3d:
            st.plotly_chart(criar_grafico_3d(tipo_solido="Geral", dados_solido=dados_sol, dados_secao=dados_secao), use_container_width=True)
        with col_2d:
            st.pyplot(gerar_epura_integrada({}, retas=[], tipo_solido="Geral", dados_solido=dados_sol, dados_secao=dados_secao))
