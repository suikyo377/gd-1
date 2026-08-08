import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="GD EM MÃOS - UEFS", layout="wide")

st.title("🚀 GD EM MÃOS - UEFS")
st.markdown("### Geometria Descritiva 3D e Épura com VG Rigorosa (Idêntica à Prancha)")
st.markdown("---")

menu = st.radio("Escolha o Assunto que deseja estudar:", ["PONTOS", "RETAS", "SÓLIDOS"], horizontal=True)
st.markdown("---")

# --- FUNÇÃO AUXILIAR: ORIENTAÇÃO TEÓRICA EXATA DA BASE ---
def obter_geometria_base(forma, ox, oy, oz, raio, lados):
    if forma in ["Cilindro", "Cone"]:
        angulos = np.linspace(0, 2 * np.pi, 100)
    else:
        if lados == 3: giro = -np.pi / 2  
        elif lados == 4: giro = np.pi / 4   
        elif lados == 5: giro = -np.pi / 2  # Pentágono apontando para cima
        elif lados == 6: giro = 0           # Hexágono com lados paralelos à LT
        elif lados == 8: giro = np.pi / 8   
        else: giro = -np.pi / 2 if lados % 2 != 0 else 0
        angulos = np.linspace(0, 2 * np.pi, lados + 1)[:-1] + giro
        
    bx = ox + raio * np.cos(angulos)
    by = oy + raio * np.sin(angulos)
    
    if forma in ["Prisma", "Pirâmide"]:
        bx = np.append(bx, bx[0])
        by = np.append(by, by[0])
        
    return bx, by

def desenhar_arco_rebatimento(ax, cx, cy, start_x, start_y, end_x):
    """Desenha o traço curvo do compasso simulando o rebatimento no papel"""
    r = np.hypot(start_x - cx, start_y - cy)
    theta1 = np.arctan2(start_y - cy, start_x - cx)
    # Se rebate para a direita, o arco vai até 0 graus. Para a esquerda, vai até 180 (pi).
    theta2 = 0.0 if end_x > cx else np.pi
    t = np.linspace(theta1, theta2, 30)
    ax.plot(cx + r * np.cos(t), cy + r * np.sin(t), color='gray', linestyle='-.', linewidth=1.2)

# --- FUNÇÃO DE ÉPURA INTEGRADA ---
def gerar_epura_integrada(pontos_principais=None, retas=None, tipo_solido=None, dados_circulo=None, dados_solido=None, dados_secao=None):
    if pontos_principais is None: pontos_principais = {}
    if retas is None: retas = []
    
    fig, ax = plt.subplots(figsize=(11, 10))
    ax.axhline(0, color='black', linewidth=1.5, label="Linha de Terra (LT)")
    ax.set_xlabel("X (Abcissa)")
    ax.set_ylabel("Projeções e Rebatimento (VG)")
    ax.set_xlim([-15, 25])
    ax.set_ylim([-15, 15])
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # Fundamental: Proporção real para a elipse e a base não ficarem "amassadas"
    ax.set_aspect('equal', adjustable='box')

    # 1. PONTOS E RETAS BÁSICAS
    for nome, (x, y, z) in pontos_principais.items():
        if nome.startswith('B') and len(nome) > 1: continue
        ax.scatter(x, z, color='blue', s=40)
        ax.text(x, z + 0.3, f"{nome}'", fontsize=10, color='blue', fontweight='bold')
        ax.scatter(x, -y, color='green', s=40)
        ax.text(x, -y - 0.5, f"{nome}''", fontsize=10, color='green', fontweight='bold')
        ax.plot([x, x], [-y, z], color='gray', linestyle=':')

    for p1, p2 in retas:
        if p1 in pontos_principais and p2 in pontos_principais:
            c1, c2 = pontos_principais[p1], pontos_principais[p2]
            ax.plot([c1[0], c2[0]], [c1[2], c2[2]], color='blue', linewidth=1.5)
            ax.plot([c1[0], c2[0]], [-c1[1], -c2[1]], color='green', linewidth=1.5)

    # 2. SÓLIDOS REDONDOS SIMPLES
    if tipo_solido == "Redondo" and dados_circulo:
        ox, oy, oz, raio, altura, forma = dados_circulo
        z_base, z_topo = oz, oz + altura
        x_esq, x_dir = ox - raio, ox + raio
        if forma == "Cilindro":
            ax.plot([x_esq, x_esq], [z_base, z_topo], color='blue', linewidth=1.5)
            ax.plot([x_dir, x_dir], [z_base, z_topo], color='blue', linewidth=1.5)
            ax.plot([x_esq, x_dir], [z_base, z_base], color='blue', linestyle='--', linewidth=1)
            ax.plot([x_esq, x_dir], [z_topo, z_topo], color='blue', linestyle='--', linewidth=1)
        else:
            ax.plot([x_esq, ox, x_dir], [z_base, z_topo, z_base], color='blue', linewidth=1.5)
            ax.plot([x_esq, x_dir], [z_base, z_base], color='blue', linestyle='--', linewidth=1)
        theta = np.linspace(0, 2 * np.pi, 100)
        ax.plot(ox + raio * np.cos(theta), -oy + raio * np.sin(theta), color='green', linewidth=1.5)

    # 3. SÓLIDOS COM SEÇÃO E REBATIMENTO (A MÁGICA DA PRANCHA)
    if dados_solido and dados_secao:
        forma, ox, oy, oz, raio, altura, lados = dados_solido
        alpha_o, alpha_1 = dados_secao
        ang_rad = np.radians(alpha_1)

        px_base, py_base = obter_geometria_base(forma, ox, oy, oz, raio, lados)
        
        # Projeção Horizontal (Base verde)
        ax.plot(px_base, -py_base, color='green', linewidth=1.5, label="Base (Proj. Horizontal)")
        
        # Cruz de Eixos na base do Cilindro/Cone (idêntico à sua foto)
        if forma in ["Cilindro", "Cone"]:
            ax.plot([ox-raio-0.5, ox+raio+0.5], [-oy, -oy], color='gray', linestyle='-.', linewidth=1)
            ax.plot([ox, ox], [-oy-raio-0.5, -oy+raio+0.5], color='gray', linestyle='-.', linewidth=1)
        
        # Cálculo das interseções de corte
        sx_list, sy_list, sz_list = [], [], []
        for px, py in zip(px_base, py_base):
            if forma in ["Prisma", "Cilindro"]:
                sz = np.tan(ang_rad) * (px - alpha_o)
                sx, sy = px, py
            else:
                den = altura - np.tan(ang_rad)*(ox - px)
                t = (np.tan(ang_rad)*(px - alpha_o) - oz) / den if abs(den) > 1e-5 else 0
                sx = px + t * (ox - px)
                sy = py + t * (oy - py)
                sz = oz + t * altura
            sx_list.append(sx); sy_list.append(sy); sz_list.append(sz)

        # Projeção Vertical (Retângulo exato do Cilindro)
        if forma in ["Prisma", "Pirâmide"]:
            for px, sz_corte in zip(px_base[:-1], sz_list[:-1]):
                if forma == "Prisma":
                    ax.plot([px, px], [oz, oz + altura], color='blue', linewidth=1.0, alpha=0.5)
                else:
                    ax.plot([px, ox], [oz, oz + altura], color='blue', linewidth=1.0, alpha=0.5)
            # Bases horizontais do prisma
            ax.plot([min(px_base), max(px_base)], [oz, oz], color='blue', linestyle='--', alpha=0.6)
            if forma == "Prisma": ax.plot([min(px_base), max(px_base)], [oz + altura, oz + altura], color='blue', linestyle='--', alpha=0.6)
        else: 
            if forma == "Cilindro":
                # Retângulo Perfeito
                ax.plot([ox-raio, ox-raio], [oz, oz+altura], color='blue', linewidth=1.5)
                ax.plot([ox+raio, ox+raio], [oz, oz+altura], color='blue', linewidth=1.5)
                ax.plot([ox-raio, ox+raio], [oz, oz], color='blue', linewidth=1.5)
                ax.plot([ox-raio, ox+raio], [oz+altura, oz+altura], color='blue', linewidth=1.5)
                # Eixo central vertical
                ax.plot([ox, ox], [oz-0.5, oz+altura+0.5], color='gray', linestyle='-.', linewidth=1)
            elif forma == "Cone": 
                ax.plot([ox-raio, ox, ox+raio], [oz, oz+altura, oz], color='blue', linewidth=1.5)
                ax.plot([ox-raio, ox+raio], [oz, oz], color='blue', linewidth=1.5)
                ax.plot([ox, ox], [oz-0.5, oz+altura+0.5], color='gray', linestyle='-.', linewidth=1)

        # Traço do Plano Secante
        x_linha = np.linspace(alpha_o - 5, alpha_o + 10, 10)
        ax.plot(x_linha, np.tan(ang_rad) * (x_linha - alpha_o), color='crimson', linewidth=2, label=f"Plano Secante α")

        # --- A REGRA DE OURO DO REBATIMENTO: FUGIR DO CORTE ---
        rx_list, ry_list = [], []
        
        # Pontos âncora para traçar as linhas de compasso no desenho (8 divisões do cilindro)
        if forma in ["Prisma", "Pirâmide"]:
            pontos_construcao = range(len(sx_list)-1)
        else:
            pontos_construcao = [0, 12, 25, 37, 50, 62, 75, 87]
        
        for i in range(len(sx_list)):
            sx, sy, sz = sx_list[i], sy_list[i], sz_list[i]
            
            # Distância matemática exata ao longo do plano secante
            # Sinal define se está na frente ou atrás da charneira (alpha_o)
            sinal = 1 if sx >= alpha_o else -1
            dist_plano = sinal * np.hypot(sx - alpha_o, sz)
            
            # Mágica linear geométrica: Rebate tudo perfeitamente sem deformar ou dobrar!
            rx = alpha_o + dist_plano
            ry = -sy 
            
            rx_list.append(rx); ry_list.append(ry)
            
            # Desenha as linhas do compasso
            if i in pontos_construcao:
                desenhar_arco_rebatimento(ax, alpha_o, 0, sx, sz, rx) 
                ax.plot([rx, rx], [0, ry], color='gray', linestyle=':', linewidth=1.2) 
                ax.plot([sx, rx], [-sy, ry], color='gray', linestyle=':', linewidth=1.2) 

        # Plotar a VG Final (Elipse ou Polígono Perfeito)
        ax.plot(rx_list, ry_list, color='purple', linewidth=2.5, label="Verdadeira Grandeza (VG)")
        ax.fill(rx_list, ry_list, color='purple', alpha=0.2)
        
        if forma in ["Prisma", "Pirâmide"]: 
            ax.scatter(rx_list[:-1], ry_list[:-1], color='purple', s=30, zorder=5)
            
        # Cruz de Eixos na VG do Cilindro (idêntico à sua foto)
        if forma == "Cilindro":
            sz_center = np.tan(ang_rad) * (ox - alpha_o)
            sinal_c = 1 if ox >= alpha_o else -1
            rx_c = alpha_o + (sinal_c * np.hypot(ox - alpha_o, sz_center))
            ry_c = -oy
            sec_val = np.sqrt(1 + np.tan(ang_rad)**2)
            semi_major = raio * sec_val
            
            ax.plot([rx_c - semi_major - 0.5, rx_c + semi_major + 0.5], [ry_c, ry_c], color='gray', linestyle='-.', linewidth=1)
            ax.plot([rx_c, rx_c], [ry_c - raio - 0.5, ry_c + raio + 0.5], color='gray', linestyle='-.', linewidth=1)
            
        ax.legend(loc='upper right')

    if tipo_solido or dados_solido:
        ax.set_title("Épura com Seção e VG (Rebatimento Oposto Rigoroso)")
    else:
        ax.set_title("Épura (Pontos e Retas)")
        
    return fig

# --- FUNÇÃO DE 3D INTERATIVO (PLOTLY) ---
def criar_grafico_3d(pontos_principais=None, retas=None, tipo_solido=None, dados_circulo=None, dados_solido=None, dados_secao=None):
    if pontos_principais is None: pontos_principais = {}
    if retas is None: retas = []
    
    fig = go.Figure()

    xx = np.linspace(-10, 15, 5)
    zz = np.linspace(-10, 15, 5)
    XX, ZZ = np.meshgrid(xx, zz)
    YY = np.zeros_like(XX)

    fig.add_trace(go.Surface(x=XX, y=YY, z=ZZ, colorscale=[[0, 'gray'], [1, 'gray']], opacity=0.15, showscale=False))
    fig.add_trace(go.Surface(x=XX, y=ZZ, z=YY, colorscale=[[0, 'gray'], [1, 'gray']], opacity=0.15, showscale=False))
    fig.add_trace(go.Scatter3d(x=[-10, 20], y=[0, 0], z=[0, 0], mode='lines', line=dict(color='black', width=6), name='Linha de Terra'))

    # 1. PONTOS E RETAS BÁSICAS
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

    # 2. SÓLIDOS REDONDOS SIMPLES
    if tipo_solido == "Redondo" and dados_circulo:
        ox, oy, oz, raio, altura, forma = dados_circulo
        theta = np.linspace(0, 2*np.pi, 40)
        bx, by = ox + raio * np.cos(theta), oy + raio * np.sin(theta)
        bz, topo_z = np.full_like(theta, oz), np.full_like(theta, oz + altura)
        
        fig.add_trace(go.Scatter3d(x=bx, y=by, z=bz, mode='lines', line=dict(color='purple', width=4), name='Base'))
        if forma == "Cilindro":
            fig.add_trace(go.Scatter3d(x=bx, y=by, z=topo_z, mode='lines', line=dict(color='purple', width=4), name='Topo'))
            for i in [0, 10, 20, 30]: fig.add_trace(go.Scatter3d(x=[bx[i], bx[i]], y=[by[i], by[i]], z=[bz[i], topo_z[i]], mode='lines', line=dict(color='purple', dash='dash')))
        else:
            vx, vy, vz = ox, oy, oz + altura
            for i in [0, 10, 20, 30]: fig.add_trace(go.Scatter3d(x=[bx[i], vx], y=[by[i], vy], z=[bz[i], vz], mode='lines', line=dict(color='purple', dash='dash')))

    # 3. SÓLIDOS COM SEÇÃO
    if dados_solido:
        forma, ox, oy, oz, raio, altura, lados = dados_solido
        bx, by = obter_geometria_base(forma, ox, oy, oz, raio, lados)
        bz = np.full_like(bx, oz)
        topo_z = np.full_like(bx, oz + altura)
        
        fig.add_trace(go.Scatter3d(x=bx, y=by, z=bz, mode='lines', line=dict(color='green', width=4), name='Base'))
        
        if forma == "Prisma":
            fig.add_trace(go.Scatter3d(x=bx, y=by, z=topo_z, mode='lines', line=dict(color='blue', width=4), name='Topo'))
            for i in range(len(bx)-1): fig.add_trace(go.Scatter3d(x=[bx[i], bx[i]], y=[by[i], by[i]], z=[oz, oz + altura], mode='lines', line=dict(color='blue', dash='dash')))
        elif forma == "Cilindro":
            fig.add_trace(go.Scatter3d(x=bx, y=by, z=topo_z, mode='lines', line=dict(color='blue', width=4), name='Topo'))
            for i in [0, 10, 20, 30]: fig.add_trace(go.Scatter3d(x=[bx[i], bx[i]], y=[by[i], by[i]], z=[oz, oz + altura], mode='lines', line=dict(color='blue', dash='dash')))
        else: 
            vx, vy, vz = ox, oy, oz + altura
            pontos_tracado = range(len(bx)-1) if forma == "Pirâmide" else [0, 10, 20, 30]
            for i in pontos_tracado: fig.add_trace(go.Scatter3d(x=[bx[i], vx], y=[by[i], vy], z=[bz[i], vz], mode='lines', line=dict(color='blue', dash='dash')))

        if dados_secao:
            alpha_o, alpha_1 = dados_secao
            ang_rad = np.radians(alpha_1)
            yy_p = np.linspace(oy - raio - 2, oy + raio + 2, 5)
            xx_p = np.linspace(alpha_o - 5, alpha_o + 10, 5)
            XX_p, YY_p = np.meshgrid(xx_p, yy_p)
            
            fig.add_trace(go.Surface(x=XX_p, y=YY_p, z=np.tan(ang_rad) * (XX_p - alpha_o), colorscale=[[0, 'crimson'], [1, 'crimson']], opacity=0.3, showscale=False, name='Plano Secante'))

            sx_list, sy_list, sz_list = [], [], []
            for px, py in zip(bx, by):
                if forma in ["Prisma", "Cilindro"]:
                    sz = np.tan(ang_rad) * (px - alpha_o)
                    sx, sy = px, py
                else:
                    den = altura - np.tan(ang_rad)*(ox - px)
                    t = (np.tan(ang_rad)*(px - alpha_o) - oz) / den if abs(den) > 1e-5 else 0
                    sx, sy, sz = px + t * (ox - px), py + t * (oy - py), oz + t * altura
                sx_list.append(sx); sy_list.append(sy); sz_list.append(sz)
                
            fig.add_trace(go.Scatter3d(x=sx_list, y=sy_list, z=sz_list, mode='lines', line=dict(color='purple', width=6), name='Seção (Corte)'))

    fig.update_layout(title="Espacial 3D (Gire com o mouse)", scene=dict(xaxis_range=[-10, 15], yaxis_range=[-10, 15], zaxis_range=[-10, 15]), margin=dict(l=0, r=0, b=0, t=30), height=550)
    return fig

# --- MÓDULOS DA INTERFACE (STREAMLIT) ---

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
        with col_3d: st.plotly_chart(criar_grafico_3d(pontos_principais=pontos), use_container_width=True)
        with col_2d: st.pyplot(gerar_epura_integrada(pontos_principais=pontos))

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
        with col_3d: st.plotly_chart(criar_grafico_3d(pontos_principais=pontos, retas=[('A', 'B')]), use_container_width=True)
        with col_2d: st.pyplot(gerar_epura_integrada(pontos_principais=pontos, retas=[('A', 'B')]))

elif menu == "SÓLIDOS":
    st.subheader("📐 Módulo: Sólidos e Seções Geométricas")
    tipo_modulo = st.selectbox("Escolha o método do Sólido:", [
        "Sólido com Plano Secante e Rebatimento (VG Rigorosa)",
        "Prisma / Pirâmide (Polígono manual por Pontos A e B)", 
        "Cone / Cilindro Simples (Base Circular por Centro)"
    ])
    
    if tipo_modulo == "Prisma / Pirâmide (Polígono manual por Pontos A e B)":
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
            submitted_sol = st.form_submit_button("Gerar Sólido Poligonal Básico")
            
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
                    retas_extras.append((topos_nomes[i], topos_nomes[(i + 1) % len(topos_nomes)]))
            else:
                coords_base = list(pontos.values())
                vx, vy, vz = sum(c[0] for c in coords_base)/len(coords_base), sum(c[1] for c in coords_base)/len(coords_base), az + altura
                pontos['V'] = (vx, vy, vz)
                for original in base_nomes: 
                    retas_extras.append((original, 'V'))

            col_3d, col_2d = st.columns(2)
            with col_3d: st.plotly_chart(criar_grafico_3d(pontos_principais=pontos, retas=retas_extras), use_container_width=True)
            with col_2d: st.pyplot(gerar_epura_integrada(pontos_principais=pontos, retas=retas_extras))

    elif tipo_modulo == "Cone / Cilindro Simples (Base Circular por Centro)":
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
            dados_circ = (ox, oy, oz, raio, altura, tipo_red)
            col_3d, col_2d = st.columns(2)
            with col_3d: st.plotly_chart(criar_grafico_3d(pontos_principais=pontos, tipo_solido="Redondo", dados_circulo=dados_circ), use_container_width=True)
            with col_2d: st.pyplot(gerar_epura_integrada(pontos_principais=pontos, tipo_solido="Redondo", dados_circulo=dados_circ))

    else:
        with st.form("form_secao_obliqua"):
            col1, col2, col3 = st.columns(3)
            with col1: ox = st.number_input("X do Centro da Base (O)", value=4.0)
            with col2: oy = st.number_input("Y do Centro da Base (O)", value=4.0)
            with col3: oz = st.number_input("Z do Centro da Base (O)", value=0.0)
            
            col4, col5 = st.columns(2)
            with col4: raio = st.number_input("Raio / Dimensão da Base", value=2.5)
            with col5: altura = st.number_input("Altura do Sólido", value=7.0)
            
            col_s1, col_s2 = st.columns(2)
            with col_s1: tipo_sol_obl = st.selectbox("Tipo de Sólido Secionado:", ["Prisma", "Pirâmide", "Cilindro", "Cone"])
            with col_s2: lados_base = st.slider("Lados da base (Prisma/Pirâmide):", 3, 8, 5)
            
            col6, col7 = st.columns(2)
            with col6: alpha_o = st.number_input("Traço $\\alpha_0$ (Abcissa na LT)", value=2.0)
            with col7: alpha_1 = st.number_input("Ângulo $\\alpha_1$ (Graus com a LT)", value=30.0)
            
            submitted_sec = st.form_submit_button("Gerar Geometria Clássica e Rebatimento")

        if submitted_sec:
            dados_sol = (tipo_sol_obl, ox, oy, oz, raio, altura, lados_base)
            dados_secao = (alpha_o, alpha_1)
            col_3d, col_2d = st.columns(2)
            with col_3d: st.plotly_chart(criar_grafico_3d(dados_solido=dados_sol, dados_secao=dados_secao), use_container_width=True)
            with col_2d: st.pyplot(gerar_epura_integrada(dados_solido=dados_sol, dados_secao=dados_secao))
