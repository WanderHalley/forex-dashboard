"""
🌍 FOREX COMMAND CENTER v2.0
COM PERSISTÊNCIA DE DADOS
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import io
import json

# Configuração da página
st.set_page_config(page_title="Forex Command Center", page_icon="🌍", layout="wide")

# ═══════════════════════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@400;500&display=swap');
    .main-header { font-family: 'Orbitron'; font-size: 2.5rem; font-weight: 700; background: linear-gradient(90deg, #ffd700, #ff9f43, #00d4ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 2rem; }
    .metric-card { background: linear-gradient(145deg, #1a1a24, #1f1f2e); border: 1px solid #2a2a3a; border-radius: 16px; padding: 1.5rem; margin: 0.5rem 0; }
    .metric-label { font-family: 'JetBrains Mono'; color: #8b8b9a; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; }
    .metric-value { font-family: 'Orbitron'; font-size: 1.8rem; font-weight: 700; }
    .metric-positive { color: #00ff88; }
    .metric-negative { color: #ff4757; }
    .metric-gold { color: #ffd700; }
    .insight-card { background: linear-gradient(145deg, #1a2a1a, #1f2f1f); border: 1px solid rgba(0, 255, 136, 0.3); border-radius: 12px; padding: 1rem; margin: 0.5rem 0; }
    .warning-card { background: linear-gradient(145deg, #2a1a1a, #2f1f1f); border: 1px solid rgba(255, 71, 87, 0.3); border-radius: 12px; padding: 1rem; margin: 0.5rem 0; }
    .gold-card { background: linear-gradient(145deg, #2a2a1a, #2f2f1f); border: 1px solid rgba(255, 215, 0, 0.3); border-radius: 12px; padding: 1rem; margin: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DE PERSISTÊNCIA
# ═══════════════════════════════════════════════════════════════════════════════

def df_to_json(df):
    if df is None: return None
    return df.to_json(orient='split', date_format='iso')

def json_to_df(json_str):
    if json_str is None: return None
    try: return pd.read_json(io.StringIO(json_str), orient='split')
    except: return None

def export_backup():
    """Exporta todos os dados como JSON para download"""
    data = {
        'df_forex': df_to_json(st.session_state.get('df_forex')),
        'capital_inicial': st.session_state.get('capital_inicial_forex', 1000),
        'meta_diaria': st.session_state.get('meta_diaria_forex', 2.0),
        'humor_dia': st.session_state.get('humor_dia_forex', 'Neutro'),
        'notas': st.session_state.get('notas_dia', ''),
        'ultimo_upload': st.session_state.get('ultimo_upload', ''),
        'account_info': st.session_state.get('account_info_forex', {}),
        'exported_at': datetime.now().isoformat()
    }
    return json.dumps(data, ensure_ascii=False, indent=2)

def import_backup(json_str):
    """Importa dados de um backup JSON"""
    try:
        data = json.loads(json_str)
        st.session_state.df_forex = json_to_df(data.get('df_forex'))
        st.session_state.capital_inicial_forex = data.get('capital_inicial', 1000)
        st.session_state.meta_diaria_forex = data.get('meta_diaria', 2.0)
        st.session_state.humor_dia_forex = data.get('humor_dia', 'Neutro')
        st.session_state.notas_dia = data.get('notas', '')
        st.session_state.ultimo_upload = data.get('ultimo_upload', '')
        st.session_state.account_info_forex = data.get('account_info', {})
        return True
    except Exception as e:
        st.error(f"Erro ao importar: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# PARSE DO ARQUIVO MT5
# ═══════════════════════════════════════════════════════════════════════════════

def parse_forex_xlsx(uploaded_file):
    df_raw = pd.read_excel(uploaded_file, header=None)
    
    account_info = {}
    for i in range(min(10, len(df_raw))):
        row = df_raw.iloc[i]
        row_str = str(row[0]) if pd.notna(row[0]) else ""
        if 'Nome:' in row_str: account_info['nome'] = str(row[3]) if pd.notna(row[3]) else ''
        elif 'Conta:' in row_str: account_info['conta'] = str(row[3]) if pd.notna(row[3]) else ''
        elif 'Empresa:' in row_str: account_info['empresa'] = str(row[3]) if pd.notna(row[3]) else ''
    
    header_row = None
    for i in range(len(df_raw)):
        if str(df_raw.iloc[i, 0]).strip() == 'Horário' and str(df_raw.iloc[i, 1]).strip() == 'Position':
            header_row = i
            break
    
    if header_row is None: return pd.DataFrame(), account_info
    
    columns = ['Abertura', 'Position', 'Ativo', 'Tipo', 'Volume', 'Preco_Entrada', 'SL', 'TP', 'Fechamento', 'Preco_Saida', 'Comissao', 'Swap', 'Lucro']
    
    data_rows = []
    for i in range(header_row + 1, len(df_raw)):
        row = df_raw.iloc[i]
        if pd.isna(row[0]) or str(row[0]).strip() == '' or 'Resultados' in str(row[0]): break
        try:
            if pd.notna(row[1]) and pd.notna(row[2]): data_rows.append(row[:13].tolist())
        except: continue
    
    if len(data_rows) == 0: return pd.DataFrame(), account_info
    
    df = pd.DataFrame(data_rows, columns=columns)
    df['Abertura'] = pd.to_datetime(df['Abertura'], errors='coerce')
    df['Fechamento'] = pd.to_datetime(df['Fechamento'], errors='coerce')
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
    df['Comissao'] = pd.to_numeric(df['Comissao'], errors='coerce').fillna(0)
    df['Swap'] = pd.to_numeric(df['Swap'], errors='coerce').fillna(0)
    df['Lucro'] = pd.to_numeric(df['Lucro'], errors='coerce')
    df = df.dropna(subset=['Abertura', 'Lucro'])
    
    df['Data'] = df['Abertura'].dt.date
    df['Hora_Abertura'] = df['Abertura'].dt.hour
    df['Dia_Semana'] = df['Abertura'].dt.day_name()
    df['Dia_Semana_Num'] = df['Abertura'].dt.dayofweek
    df['Resultado'] = df['Lucro'] + df['Swap'] - df['Comissao'].abs()
    df['Status'] = df['Resultado'].apply(lambda x: 'Gain' if x > 0 else ('Loss' if x < 0 else 'Empate'))
    
    def get_session(hour):
        if 0 <= hour < 8: return 'Ásia'
        elif 8 <= hour < 13: return 'Londres'
        elif 13 <= hour < 21: return 'Nova York'
        else: return 'Ásia'
    df['Sessao'] = df['Hora_Abertura'].apply(get_session)
    
    return df, account_info

# ═══════════════════════════════════════════════════════════════════════════════
# CÁLCULO DE MÉTRICAS
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_metrics(df, capital_inicial, meta_pct):
    if df is None or len(df) == 0: return {}
    
    m = {}
    m['lucro_total'] = df['Resultado'].sum()
    m['capital_atual'] = capital_inicial + m['lucro_total']
    m['retorno_pct'] = (m['lucro_total'] / capital_inicial) * 100 if capital_inicial > 0 else 0
    m['meta_valor'] = m['capital_atual'] * (meta_pct / 100)
    
    m['total_ops'] = len(df)
    m['gains'] = len(df[df['Status'] == 'Gain'])
    m['losses'] = len(df[df['Status'] == 'Loss'])
    m['win_rate'] = (m['gains'] / m['total_ops']) * 100 if m['total_ops'] > 0 else 0
    
    df_g = df[df['Resultado'] > 0]['Resultado']
    df_l = df[df['Resultado'] < 0]['Resultado']
    m['media_gain'] = df_g.mean() if len(df_g) > 0 else 0
    m['media_loss'] = abs(df_l.mean()) if len(df_l) > 0 else 0
    m['maior_gain'] = df_g.max() if len(df_g) > 0 else 0
    m['maior_loss'] = abs(df_l.min()) if len(df_l) > 0 else 0
    m['payoff'] = m['media_gain'] / m['media_loss'] if m['media_loss'] > 0 else 0
    
    soma_g = df_g.sum() if len(df_g) > 0 else 0
    soma_l = abs(df_l.sum()) if len(df_l) > 0 else 0
    m['fator_lucro'] = soma_g / soma_l if soma_l > 0 else 0
    
    df_s = df.sort_values('Abertura')
    df_s['Acum'] = df_s['Resultado'].cumsum()
    df_s['Pico'] = df_s['Acum'].cummax()
    df_s['DD'] = df_s['Pico'] - df_s['Acum']
    m['max_dd'] = df_s['DD'].max()
    m['max_dd_pct'] = (m['max_dd'] / capital_inicial) * 100 if capital_inicial > 0 else 0
    
    m['swap_total'] = df['Swap'].sum()
    m['comissao_total'] = df['Comissao'].abs().sum()
    
    # Hoje
    hoje = datetime.now().date()
    df_h = df[df['Data'] == hoje]
    m['resultado_hoje'] = df_h['Resultado'].sum() if len(df_h) > 0 else 0
    m['ops_hoje'] = len(df_h)
    m['progresso_meta'] = (m['resultado_hoje'] / m['meta_valor']) * 100 if m['meta_valor'] > 0 else 0
    
    # Por mês
    df['Mes'] = df['Abertura'].dt.to_period('M').astype(str)
    m['por_mes'] = df.groupby('Mes').agg({'Resultado': 'sum', 'Status': 'count'}).reset_index()
    m['por_mes'].columns = ['Mes', 'Resultado', 'Ops']
    
    # Por hora
    m['por_hora'] = df.groupby('Hora_Abertura')['Resultado'].sum().reset_index()
    m['por_hora'].columns = ['Hora', 'Resultado']
    
    # Por dia semana
    dias_pt = {'Monday': 'Seg', 'Tuesday': 'Ter', 'Wednesday': 'Qua', 'Thursday': 'Qui', 'Friday': 'Sex'}
    df['Dia_PT'] = df['Dia_Semana'].map(dias_pt)
    m['por_dia'] = df.groupby(['Dia_Semana_Num', 'Dia_PT'])['Resultado'].sum().reset_index().sort_values('Dia_Semana_Num')
    
    # Por ativo
    m['por_ativo'] = df.groupby('Ativo').agg({'Resultado': 'sum', 'Status': 'count'}).reset_index()
    m['por_ativo'].columns = ['Ativo', 'Resultado', 'Ops']
    m['por_ativo'] = m['por_ativo'].sort_values('Resultado', ascending=False)
    
    # Por sessão
    m['por_sessao'] = df.groupby('Sessao')['Resultado'].sum().reset_index()
    
    return m

# ═══════════════════════════════════════════════════════════════════════════════
# INICIALIZAÇÃO
# ═══════════════════════════════════════════════════════════════════════════════

if 'df_forex' not in st.session_state: st.session_state.df_forex = None
if 'account_info_forex' not in st.session_state: st.session_state.account_info_forex = {}
if 'capital_inicial_forex' not in st.session_state: st.session_state.capital_inicial_forex = 1000.0
if 'meta_diaria_forex' not in st.session_state: st.session_state.meta_diaria_forex = 2.0
if 'humor_dia_forex' not in st.session_state: st.session_state.humor_dia_forex = "Neutro"
if 'notas_dia' not in st.session_state: st.session_state.notas_dia = ""
if 'ultimo_upload' not in st.session_state: st.session_state.ultimo_upload = ""

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## ⚙️ Configurações")
    
    # Status
    if st.session_state.df_forex is not None:
        st.success(f"✅ Dados carregados\n📅 {st.session_state.ultimo_upload}")
    
    st.markdown("---")
    
    # Upload CSV/XLSX
    st.markdown("### 📁 Importar Relatório MT5")
    uploaded = st.file_uploader("Arquivo Excel (.xlsx)", type=['xlsx', 'xls'])
    
    if uploaded:
        try:
            df, info = parse_forex_xlsx(uploaded)
            if len(df) > 0:
                st.session_state.df_forex = df
                st.session_state.account_info_forex = info
                st.session_state.ultimo_upload = datetime.now().strftime("%d/%m/%Y %H:%M")
                st.success(f"✅ {len(df)} operações!")
                st.rerun()
        except Exception as e:
            st.error(f"Erro: {e}")
    
    st.markdown("---")
    
    # Backup/Restore
    st.markdown("### 💾 Backup dos Dados")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.df_forex is not None:
            backup_data = export_backup()
            st.download_button("📥 Baixar", backup_data, "forex_backup.json", "application/json", use_container_width=True)
    
    with col2:
        backup_file = st.file_uploader("📤 Restaurar", type=['json'], label_visibility="collapsed")
        if backup_file:
            if import_backup(backup_file.read().decode('utf-8')):
                st.success("Restaurado!")
                st.rerun()
    
    st.markdown("---")
    
    # Configurações
    st.markdown("### 💰 Capital & Meta")
    
    capital = st.number_input("Capital Inicial ($)", value=st.session_state.capital_inicial_forex, step=100.0)
    st.session_state.capital_inicial_forex = capital
    
    meta = st.slider("Meta Diária (%)", 0.5, 10.0, st.session_state.meta_diaria_forex, 0.5)
    st.session_state.meta_diaria_forex = meta
    
    st.info(f"Meta: **${capital * meta / 100:.2f}**/dia")
    
    st.markdown("---")
    
    # Humor
    st.markdown("### 🧠 Registro")
    humor = st.selectbox("Humor", ["😤 Ansioso", "😊 Confiante", "😐 Neutro", "😴 Cansado", "🎯 Focado"])
    st.session_state.humor_dia_forex = humor
    
    notas = st.text_area("Notas", value=st.session_state.notas_dia)
    st.session_state.notas_dia = notas
    
    # Info conta
    if st.session_state.account_info_forex:
        st.markdown("---")
        st.markdown("### 📋 Conta")
        info = st.session_state.account_info_forex
        st.write(f"**{info.get('nome', '')}**")
        st.write(f"Conta: {info.get('conta', '')}")
        st.write(f"{info.get('empresa', '')}")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<h1 class="main-header">🌍 FOREX COMMAND CENTER</h1>', unsafe_allow_html=True)

if st.session_state.df_forex is not None and len(st.session_state.df_forex) > 0:
    df = st.session_state.df_forex
    m = calculate_metrics(df, st.session_state.capital_inicial_forex, st.session_state.meta_diaria_forex)
    
    # Métricas principais
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    
    with c1:
        cor = "metric-positive" if m['lucro_total'] >= 0 else "metric-negative"
        st.markdown(f"""<div class="metric-card"><div class="metric-label">💼 CAPITAL</div>
        <div class="metric-value {cor}">${m['capital_atual']:,.2f}</div>
        <div style="color:#8b8b9a">{m['retorno_pct']:+.1f}%</div></div>""", unsafe_allow_html=True)
    
    with c2:
        cor = "metric-positive" if m['resultado_hoje'] > 0 else ("metric-negative" if m['resultado_hoje'] < 0 else "")
        st.markdown(f"""<div class="metric-card"><div class="metric-label">📊 HOJE</div>
        <div class="metric-value {cor}">${m['resultado_hoje']:,.2f}</div>
        <div style="color:#8b8b9a">Meta: {m['progresso_meta']:.0f}%</div></div>""", unsafe_allow_html=True)
    
    with c3:
        cor = "metric-positive" if m['win_rate'] >= 50 else "metric-negative"
        st.markdown(f"""<div class="metric-card"><div class="metric-label">🎯 WIN RATE</div>
        <div class="metric-value {cor}">{m['win_rate']:.1f}%</div>
        <div style="color:#8b8b9a">{m['gains']}W / {m['losses']}L</div></div>""", unsafe_allow_html=True)
    
    with c4:
        cor = "metric-positive" if m['payoff'] >= 1 else "metric-negative"
        st.markdown(f"""<div class="metric-card"><div class="metric-label">⚖️ PAYOFF</div>
        <div class="metric-value {cor}">{m['payoff']:.2f}</div>
        <div style="color:#8b8b9a">+${m['media_gain']:.0f} / -${m['media_loss']:.0f}</div></div>""", unsafe_allow_html=True)
    
    with c5:
        cor = "metric-positive" if m['fator_lucro'] >= 1.5 else "metric-gold"
        st.markdown(f"""<div class="metric-card"><div class="metric-label">📈 FATOR LUCRO</div>
        <div class="metric-value {cor}">{m['fator_lucro']:.2f}</div>
        <div style="color:#8b8b9a">{m['total_ops']} trades</div></div>""", unsafe_allow_html=True)
    
    with c6:
        cor = "metric-negative" if m['max_dd_pct'] > 10 else "metric-gold"
        st.markdown(f"""<div class="metric-card"><div class="metric-label">📉 MAX DD</div>
        <div class="metric-value {cor}">${m['max_dd']:,.2f}</div>
        <div style="color:#8b8b9a">{m['max_dd_pct']:.1f}%</div></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📆 Mensal", "💹 Ativos", "⏰ Horários", "📅 Dias", "📈 Evolução", "🧮 Calculadoras"])
    
    # TAB MENSAL
    with tab1:
        st.subheader("📆 Performance Mensal")
        
        if len(m['por_mes']) > 0:
            df_mes = m['por_mes'].copy()
            
            # Calcular % de ganho por mês
            capital_calc = st.session_state.capital_inicial_forex
            pcts = []
            for _, row in df_mes.iterrows():
                pct = (row['Resultado'] / capital_calc) * 100 if capital_calc > 0 else 0
                pcts.append(pct)
                capital_calc += row['Resultado']
            df_mes['Ganho_Pct'] = pcts
            
            # Gráfico
            colors = ['#00ff88' if x > 0 else '#ff4757' for x in df_mes['Ganho_Pct']]
            fig = go.Figure(go.Bar(x=df_mes['Mes'], y=df_mes['Ganho_Pct'], marker_color=colors,
                                   text=[f'{x:+.1f}%' for x in df_mes['Ganho_Pct']], textposition='outside'))
            fig.update_layout(title='Ganho Mensal (%)', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#fff'), xaxis=dict(gridcolor='#2a2a3a'), yaxis=dict(gridcolor='#2a2a3a'), height=350)
            st.plotly_chart(fig, use_container_width=True)
            
            # Cards
            cols = st.columns(min(len(df_mes), 6))
            for i, (_, row) in enumerate(df_mes.iterrows()):
                with cols[i % 6]:
                    cor = '#00ff88' if row['Resultado'] > 0 else '#ff4757'
                    st.markdown(f"""<div class="metric-card" style="text-align:center">
                    <div style="color:#ffd700;font-weight:bold">{row['Mes']}</div>
                    <div style="color:{cor};font-family:Orbitron;font-size:1.3rem">${row['Resultado']:,.2f}</div>
                    <div style="color:{cor};font-size:1.1rem">{row['Ganho_Pct']:+.1f}%</div>
                    <div style="color:#8b8b9a;font-size:0.8rem">{int(row['Ops'])} ops</div></div>""", unsafe_allow_html=True)
    
    # TAB ATIVOS
    with tab2:
        st.subheader("💹 Performance por Ativo")
        
        if len(m['por_ativo']) > 0:
            df_at = m['por_ativo']
            colors = ['#ffd700' if 'XAU' in str(x) else ('#00ff88' if r > 0 else '#ff4757') for x, r in zip(df_at['Ativo'], df_at['Resultado'])]
            fig = go.Figure(go.Bar(x=df_at['Ativo'], y=df_at['Resultado'], marker_color=colors,
                                  text=[f'${x:,.0f}' for x in df_at['Resultado']], textposition='outside'))
            fig.update_layout(title='Resultado por Ativo', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#fff'), xaxis=dict(gridcolor='#2a2a3a'), yaxis=dict(gridcolor='#2a2a3a'), height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB HORÁRIOS
    with tab3:
        st.subheader("⏰ Performance por Horário")
        
        if len(m['por_hora']) > 0:
            df_h = m['por_hora']
            colors = ['#00ff88' if x > 0 else '#ff4757' for x in df_h['Resultado']]
            fig = go.Figure(go.Bar(x=[f"{h}h" for h in df_h['Hora']], y=df_h['Resultado'], marker_color=colors,
                                  text=[f'${x:,.0f}' for x in df_h['Resultado']], textposition='outside'))
            fig.update_layout(title='Resultado por Hora (UTC)', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#fff'), xaxis=dict(gridcolor='#2a2a3a'), yaxis=dict(gridcolor='#2a2a3a'), height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Melhor/pior hora
            melhor = df_h.loc[df_h['Resultado'].idxmax()]
            pior = df_h.loc[df_h['Resultado'].idxmin()]
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""<div class="insight-card"><b>🏆 Melhor Horário:</b> {int(melhor['Hora'])}h UTC<br>Resultado: ${melhor['Resultado']:,.2f}</div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class="warning-card"><b>⚠️ Evitar:</b> {int(pior['Hora'])}h UTC<br>Resultado: ${pior['Resultado']:,.2f}</div>""", unsafe_allow_html=True)
    
    # TAB DIAS
    with tab4:
        st.subheader("📅 Performance por Dia da Semana")
        
        if len(m['por_dia']) > 0:
            df_d = m['por_dia']
            colors = ['#00ff88' if x > 0 else '#ff4757' for x in df_d['Resultado']]
            fig = go.Figure(go.Bar(x=df_d['Dia_PT'], y=df_d['Resultado'], marker_color=colors,
                                  text=[f'${x:,.0f}' for x in df_d['Resultado']], textposition='outside'))
            fig.update_layout(title='Resultado por Dia', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#fff'), xaxis=dict(gridcolor='#2a2a3a'), yaxis=dict(gridcolor='#2a2a3a'), height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB EVOLUÇÃO
    with tab5:
        st.subheader("📈 Evolução do Capital")
        
        df_s = df.sort_values('Abertura').copy()
        df_s['Capital'] = st.session_state.capital_inicial_forex + df_s['Resultado'].cumsum()
        
        fig = go.Figure(go.Scatter(x=df_s['Abertura'], y=df_s['Capital'], mode='lines', fill='tozeroy',
                                   line=dict(color='#ffd700', width=2), fillcolor='rgba(255,215,0,0.1)'))
        fig.add_hline(y=st.session_state.capital_inicial_forex, line_dash="dash", line_color="#00d4ff", annotation_text="Capital Inicial")
        fig.update_layout(title='Evolução do Capital', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         font=dict(color='#fff'), xaxis=dict(gridcolor='#2a2a3a'), yaxis=dict(gridcolor='#2a2a3a'), height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # TAB CALCULADORAS
    with tab6:
        calc_tab1, calc_tab2 = st.tabs(["🧮 Calculadora de Pontos", "💰 Juros Compostos"])
        
        with calc_tab1:
            st.subheader("🧮 Calculadora de Pontos/Pips")
            
            c1, c2 = st.columns(2)
            with c1:
                ativo = st.selectbox("Ativo", ["XAUUSD (Ouro)", "EURUSD", "GBPUSD", "USDJPY", "WIN (Mini Índice)"])
                configs = {
                    "XAUUSD (Ouro)": (0.01, 100, "ponto"),
                    "EURUSD": (0.0001, 100000, "pip"),
                    "GBPUSD": (0.0001, 100000, "pip"),
                    "USDJPY": (0.01, 100000, "pip"),
                    "WIN (Mini Índice)": (5, 1, "ponto")
                }
                pip_val, contract, pip_name = configs[ativo]
                
                lote = st.number_input("Lote", value=0.01, step=0.01, format="%.2f")
                pontos = st.number_input(f"{pip_name}s", value=10.0, step=1.0)
            
            with c2:
                valor_pip = lote * contract * pip_val
                resultado = pontos * valor_pip
                
                st.markdown(f"""<div class="gold-card" style="text-align:center">
                <div style="color:#ffd700;font-weight:bold">VALOR POR {pip_name.upper()}</div>
                <div style="font-family:Orbitron;font-size:2rem;color:#fff">${valor_pip:.2f}</div></div>""", unsafe_allow_html=True)
                
                cor = "metric-positive" if resultado >= 0 else "metric-negative"
                st.markdown(f"""<div class="metric-card" style="text-align:center">
                <div class="metric-label">RESULTADO ({pontos:.0f} {pip_name}s)</div>
                <div class="metric-value {cor}">${resultado:,.2f}</div></div>""", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 🎯 Calculadora de Risco")
            c1, c2, c3 = st.columns(3)
            with c1:
                cap_risco = st.number_input("Capital ($)", value=st.session_state.capital_inicial_forex, step=100.0)
                risco_pct = st.slider("Risco (%)", 0.5, 5.0, 1.0, 0.5)
            with c2:
                stop = st.number_input(f"Stop ({pip_name}s)", value=20.0, step=1.0)
            with c3:
                val_risco = cap_risco * risco_pct / 100
                lote_ideal = val_risco / (stop * contract * pip_val) if stop > 0 else 0
                st.markdown(f"""<div class="gold-card" style="text-align:center">
                <div style="color:#ffd700;font-weight:bold">💰 LOTE IDEAL</div>
                <div style="font-family:Orbitron;font-size:2rem;color:#fff">{lote_ideal:.2f}</div>
                <div style="color:#8b8b9a">Risco: ${val_risco:.2f}</div></div>""", unsafe_allow_html=True)
        
        with calc_tab2:
            st.subheader("💰 Calculadora de Juros Compostos")
            
            c1, c2 = st.columns(2)
            with c1:
                cap_jc = st.number_input("Capital Inicial ($)", value=1000.0, step=100.0, key="jc_cap")
                taxa_dia = st.slider("Taxa Diária (%)", 0.1, 10.0, 2.0, 0.1)
                aporte = st.number_input("Aporte Mensal ($)", value=0.0, step=50.0)
                meses = st.slider("Período (meses)", 1, 60, 12)
            
            with c2:
                # Calcular
                capital_jc = cap_jc
                for mes in range(meses):
                    for _ in range(20):  # 20 dias úteis
                        capital_jc *= (1 + taxa_dia/100)
                    capital_jc += aporte
                
                lucro_jc = capital_jc - cap_jc - (aporte * meses)
                retorno_jc = (lucro_jc / cap_jc) * 100
                
                st.markdown(f"""<div class="metric-card" style="text-align:center">
                <div class="metric-label">💎 CAPITAL FINAL</div>
                <div class="metric-value metric-gold">${capital_jc:,.2f}</div>
                <div style="color:#8b8b9a">Em {meses} meses</div></div>""", unsafe_allow_html=True)
                
                st.markdown(f"""<div class="insight-card" style="text-align:center">
                <div style="color:#00ff88;font-weight:bold">💰 LUCRO</div>
                <div style="font-family:Orbitron;font-size:1.5rem;color:#00ff88">${lucro_jc:,.2f}</div>
                <div style="color:#8b8b9a">{retorno_jc:,.0f}% de retorno</div></div>""", unsafe_allow_html=True)
            
            # Marcos
            st.markdown("### 🏆 Marcos")
            marcos = [("2x", cap_jc*2), ("5x", cap_jc*5), ("10x", cap_jc*10), ("$10k", 10000), ("$100k", 100000)]
            cols = st.columns(5)
            for i, (nome, alvo) in enumerate(marcos):
                cap_t = cap_jc
                meses_t = 0
                while cap_t < alvo and meses_t < 120:
                    for _ in range(20): cap_t *= (1 + taxa_dia/100)
                    cap_t += aporte
                    meses_t += 1
                with cols[i]:
                    if meses_t < 120:
                        st.markdown(f"""<div class="gold-card" style="text-align:center">
                        <div style="color:#ffd700">{nome}</div>
                        <div style="color:#00ff88">{meses_t//12}a {meses_t%12}m</div></div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""<div class="metric-card" style="text-align:center">
                        <div style="color:#8b8b9a">{nome}</div>
                        <div style="color:#8b8b9a">+10a</div></div>""", unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align: center; padding: 4rem;">
        <div style="font-size: 5rem;">🌍</div>
        <h2 style="color: #ffd700;">Bem-vindo ao Forex Command Center</h2>
        <p style="color: #8b8b9a;">Importe seu relatório do MetaTrader 5 (.xlsx) ou restaure um backup para começar.</p>
        <div style="background: #1a1a24; border-radius: 16px; padding: 2rem; max-width: 400px; margin: 2rem auto; text-align: left;">
            <h4 style="color: #ffd700;">📁 Como começar:</h4>
            <ol style="color: #fff;">
                <li>No MT5, vá em Histórico</li>
                <li>Botão direito → Relatório</li>
                <li>Salve como Excel (.xlsx)</li>
                <li>Importe na barra lateral</li>
            </ol>
        </div>
        <p style="color: #ffd700;">💾 Dica: Faça backup dos dados para não perder!</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<p style="text-align:center;color:#8b8b9a;font-size:0.8rem;">🌍 Forex Command Center v2.0 | 💾 Lembre-se de fazer backup dos seus dados!</p>', unsafe_allow_html=True)
