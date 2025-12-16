"""
🌍 FOREX COMMAND CENTER
Sistema Inteligente de Gerenciamento de Operações Forex
Desenvolvido para Wander - Trader Profissional
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import re

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO DA PÁGINA
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Forex Command Center",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# CSS CUSTOMIZADO - TEMA DARK PROFISSIONAL FOREX
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --bg-primary: #0a0a0f;
        --bg-secondary: #12121a;
        --bg-card: #1a1a24;
        --accent-green: #00ff88;
        --accent-red: #ff4757;
        --accent-blue: #00d4ff;
        --accent-gold: #ffd700;
        --accent-purple: #a855f7;
        --accent-orange: #ff9f43;
        --text-primary: #ffffff;
        --text-secondary: #8b8b9a;
        --border-color: #2a2a3a;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a12 0%, #0f1419 50%, #0a0a12 100%);
    }
    
    .main-header {
        font-family: 'Orbitron', monospace;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ffd700 0%, #ff9f43 50%, #00d4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: 3px;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
    }
    
    .sub-header {
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-secondary);
        text-align: center;
        font-size: 0.9rem;
        margin-bottom: 2rem;
        letter-spacing: 2px;
    }
    
    .metric-card {
        background: linear-gradient(145deg, var(--bg-card) 0%, #1f1f2e 100%);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(255, 215, 0, 0.15);
        border-color: var(--accent-gold);
    }
    
    .metric-label {
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-secondary);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    
    .metric-positive { color: var(--accent-green); text-shadow: 0 0 20px rgba(0, 255, 136, 0.4); }
    .metric-negative { color: var(--accent-red); text-shadow: 0 0 20px rgba(255, 71, 87, 0.4); }
    .metric-neutral { color: var(--accent-blue); text-shadow: 0 0 20px rgba(0, 212, 255, 0.4); }
    .metric-gold { color: var(--accent-gold); text-shadow: 0 0 20px rgba(255, 215, 0, 0.4); }
    .metric-orange { color: var(--accent-orange); text-shadow: 0 0 20px rgba(255, 159, 67, 0.4); }
    
    .metric-change {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
    }
    
    .section-title {
        font-family: 'Orbitron', monospace;
        font-size: 1.3rem;
        color: var(--accent-gold);
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border-color);
        letter-spacing: 2px;
    }
    
    .insight-card {
        background: linear-gradient(145deg, #1a2a1a 0%, #1f2f1f 100%);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
    }
    
    .warning-card {
        background: linear-gradient(145deg, #2a1a1a 0%, #2f1f1f 100%);
        border: 1px solid rgba(255, 71, 87, 0.3);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
    }
    
    .info-card {
        background: linear-gradient(145deg, #1a1a2a 0%, #1f1f2f 100%);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
    }
    
    .gold-card {
        background: linear-gradient(145deg, #2a2a1a 0%, #2f2f1f 100%);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
    }
    
    .asset-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .badge-gold { background: linear-gradient(90deg, #ffd700, #ff9f43); color: #000; }
    .badge-forex { background: linear-gradient(90deg, #00d4ff, #00ff88); color: #000; }
    .badge-crypto { background: linear-gradient(90deg, #a855f7, #ec4899); color: #fff; }
    
    .stSidebar {
        background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
    }
    
    .mood-emoji {
        font-size: 2.5rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .progress-bar-container {
        background: var(--bg-card);
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .stDataFrame {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    div[data-testid="stMetricValue"] {
        font-family: 'Orbitron', monospace !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--bg-card);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'JetBrains Mono', monospace;
        background: transparent;
        border-radius: 8px;
        color: var(--text-secondary);
        padding: 0.5rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, var(--accent-gold), var(--accent-orange));
        color: var(--bg-primary) !important;
    }
    
    .session-card {
        background: linear-gradient(145deg, #1a1a24 0%, #1f1f2e 100%);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    
    .session-active {
        border-color: var(--accent-green);
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES AUXILIARES
# ═══════════════════════════════════════════════════════════════════════════════

def parse_forex_xlsx(uploaded_file):
    """Parse do arquivo Excel de histórico do MT5"""
    df_raw = pd.read_excel(uploaded_file, header=None)
    
    # Extrair informações do cabeçalho
    account_info = {}
    for i in range(min(10, len(df_raw))):
        row = df_raw.iloc[i]
        row_str = str(row[0]) if pd.notna(row[0]) else ""
        
        if 'Nome:' in row_str:
            account_info['nome'] = str(row[3]) if pd.notna(row[3]) else ''
        elif 'Conta:' in row_str:
            account_info['conta'] = str(row[3]) if pd.notna(row[3]) else ''
        elif 'Empresa:' in row_str:
            account_info['empresa'] = str(row[3]) if pd.notna(row[3]) else ''
        elif 'Data:' in row_str:
            account_info['data_relatorio'] = str(row[3]) if pd.notna(row[3]) else ''
    
    # Encontrar linha do header das posições
    header_row = None
    for i in range(len(df_raw)):
        if str(df_raw.iloc[i, 0]).strip() == 'Horário' and str(df_raw.iloc[i, 1]).strip() == 'Position':
            header_row = i
            break
    
    if header_row is None:
        st.error("Não foi possível encontrar o cabeçalho das operações")
        return pd.DataFrame(), account_info
    
    # Extrair dados das operações
    columns = ['Abertura', 'Position', 'Ativo', 'Tipo', 'Volume', 'Preco_Entrada', 
               'SL', 'TP', 'Fechamento', 'Preco_Saida', 'Comissao', 'Swap', 'Lucro']
    
    data_rows = []
    for i in range(header_row + 1, len(df_raw)):
        row = df_raw.iloc[i]
        
        # Parar se encontrar seção de resultados ou linhas vazias consecutivas
        if pd.isna(row[0]) or str(row[0]).strip() == '' or 'Resultados' in str(row[0]):
            break
        
        # Verificar se é uma linha de dados válida
        try:
            if pd.notna(row[1]) and pd.notna(row[2]):  # Position e Ativo devem existir
                data_rows.append(row[:13].tolist())
        except:
            continue
    
    if len(data_rows) == 0:
        return pd.DataFrame(), account_info
    
    df = pd.DataFrame(data_rows, columns=columns)
    
    # Limpar e converter dados
    df['Abertura'] = pd.to_datetime(df['Abertura'], errors='coerce')
    df['Fechamento'] = pd.to_datetime(df['Fechamento'], errors='coerce')
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
    df['Preco_Entrada'] = pd.to_numeric(df['Preco_Entrada'], errors='coerce')
    df['Preco_Saida'] = pd.to_numeric(df['Preco_Saida'], errors='coerce')
    df['Comissao'] = pd.to_numeric(df['Comissao'], errors='coerce').fillna(0)
    df['Swap'] = pd.to_numeric(df['Swap'], errors='coerce').fillna(0)
    df['Lucro'] = pd.to_numeric(df['Lucro'], errors='coerce')
    
    # Remover linhas sem dados válidos
    df = df.dropna(subset=['Abertura', 'Lucro'])
    
    # Extrair informações adicionais
    df['Data'] = df['Abertura'].dt.date
    df['Hora_Abertura'] = df['Abertura'].dt.hour
    df['Minuto_Abertura'] = df['Abertura'].dt.minute
    df['Dia_Semana'] = df['Abertura'].dt.day_name()
    df['Dia_Semana_Num'] = df['Abertura'].dt.dayofweek
    
    # Calcular duração
    df['Duracao'] = df['Fechamento'] - df['Abertura']
    df['Duracao_Min'] = df['Duracao'].dt.total_seconds() / 60
    
    # Resultado líquido (lucro - comissão + swap)
    df['Resultado'] = df['Lucro'] + df['Swap'] - df['Comissao'].abs()
    
    # Classificar operação
    df['Status'] = df['Resultado'].apply(lambda x: 'Gain' if x > 0 else ('Loss' if x < 0 else 'Empate'))
    
    # Classificar tipo de ativo
    def classify_asset(ativo):
        ativo = str(ativo).upper()
        if 'XAU' in ativo or 'GOLD' in ativo:
            return 'Ouro'
        elif 'XAG' in ativo or 'SILVER' in ativo:
            return 'Prata'
        elif 'BTC' in ativo or 'ETH' in ativo or 'CRYPTO' in ativo:
            return 'Crypto'
        elif 'OIL' in ativo or 'WTI' in ativo or 'BRENT' in ativo:
            return 'Petróleo'
        else:
            return 'Forex'
    
    df['Categoria'] = df['Ativo'].apply(classify_asset)
    
    # Identificar sessão de trading
    def get_session(hour):
        if 0 <= hour < 8:
            return 'Ásia'
        elif 8 <= hour < 13:
            return 'Londres'
        elif 13 <= hour < 21:
            return 'Nova York'
        else:
            return 'Ásia'
    
    df['Sessao'] = df['Hora_Abertura'].apply(get_session)
    
    # Extrair métricas do relatório
    summary_info = {}
    for i in range(len(df_raw)):
        row = df_raw.iloc[i]
        row_str = str(row[0]) if pd.notna(row[0]) else ""
        
        if 'Lucro Líquido Total:' in row_str:
            summary_info['lucro_liquido'] = row[3]
            summary_info['lucro_bruto'] = row[7]
        elif 'Fator de Lucro:' in row_str:
            summary_info['fator_lucro'] = row[3]
            summary_info['payoff'] = row[7]
        elif 'Fator de Recuperação:' in row_str:
            summary_info['fator_recuperacao'] = row[3]
            summary_info['sharpe'] = row[7]
        elif 'Rebaixamento Absoluto' in row_str:
            summary_info['dd_absoluto'] = row[3]
            # Parse max drawdown
            dd_max_str = str(row[7]) if pd.notna(row[7]) else "0"
            try:
                dd_match = re.search(r'([\d\s,\.]+)', dd_max_str)
                if dd_match:
                    summary_info['dd_maximo'] = float(dd_match.group(1).replace(' ', '').replace(',', '.'))
            except:
                summary_info['dd_maximo'] = 0
        elif 'Total de Negociações:' in row_str:
            summary_info['total_negocios'] = row[3]
    
    account_info['summary'] = summary_info
    
    return df, account_info

def calculate_forex_metrics(df, capital_inicial, meta_diaria_pct):
    """Calcula todas as métricas do dashboard Forex"""
    metrics = {}
    
    if len(df) == 0:
        return metrics
    
    # Capital e lucro
    lucro_total = df['Resultado'].sum()
    capital_atual = capital_inicial + lucro_total
    
    metrics['capital_inicial'] = capital_inicial
    metrics['lucro_total'] = lucro_total
    metrics['capital_atual'] = capital_atual
    metrics['retorno_total_pct'] = (lucro_total / capital_inicial) * 100 if capital_inicial > 0 else 0
    
    # Meta diária
    meta_diaria_valor = capital_atual * (meta_diaria_pct / 100)
    metrics['meta_diaria_pct'] = meta_diaria_pct
    metrics['meta_diaria_valor'] = meta_diaria_valor
    
    # Operações
    total_ops = len(df)
    gains = len(df[df['Status'] == 'Gain'])
    losses = len(df[df['Status'] == 'Loss'])
    empates = len(df[df['Status'] == 'Empate'])
    
    metrics['total_operacoes'] = total_ops
    metrics['gains'] = gains
    metrics['losses'] = losses
    metrics['empates'] = empates
    metrics['win_rate'] = (gains / total_ops) * 100 if total_ops > 0 else 0
    
    # Análise de ganhos/perdas
    df_gains = df[df['Resultado'] > 0]['Resultado']
    df_losses = df[df['Resultado'] < 0]['Resultado']
    
    metrics['media_gain'] = df_gains.mean() if len(df_gains) > 0 else 0
    metrics['media_loss'] = abs(df_losses.mean()) if len(df_losses) > 0 else 0
    metrics['maior_gain'] = df_gains.max() if len(df_gains) > 0 else 0
    metrics['maior_loss'] = abs(df_losses.min()) if len(df_losses) > 0 else 0
    
    # Payoff
    metrics['payoff'] = metrics['media_gain'] / metrics['media_loss'] if metrics['media_loss'] > 0 else 0
    
    # Fator de lucro
    soma_gains = df_gains.sum() if len(df_gains) > 0 else 0
    soma_losses = abs(df_losses.sum()) if len(df_losses) > 0 else 0
    metrics['fator_lucro'] = soma_gains / soma_losses if soma_losses > 0 else float('inf')
    
    # Drawdown
    df_sorted = df.sort_values('Abertura')
    df_sorted['Resultado_Acum'] = df_sorted['Resultado'].cumsum()
    df_sorted['Pico'] = df_sorted['Resultado_Acum'].cummax()
    df_sorted['Drawdown'] = df_sorted['Pico'] - df_sorted['Resultado_Acum']
    
    metrics['max_drawdown'] = df_sorted['Drawdown'].max()
    metrics['max_drawdown_pct'] = (metrics['max_drawdown'] / capital_inicial) * 100 if capital_inicial > 0 else 0
    
    # Volume total
    metrics['volume_total'] = df['Volume'].sum()
    metrics['volume_medio'] = df['Volume'].mean()
    
    # Swap e Comissão
    metrics['total_swap'] = df['Swap'].sum()
    metrics['total_comissao'] = df['Comissao'].abs().sum()
    
    # Análise por dia
    df_by_day = df.groupby('Data').agg({
        'Resultado': ['sum', 'count'],
        'Status': lambda x: (x == 'Gain').sum()
    }).reset_index()
    df_by_day.columns = ['Data', 'Resultado_Dia', 'Ops_Dia', 'Gains_Dia']
    
    metrics['dias_operados'] = len(df_by_day)
    metrics['dias_positivos'] = len(df_by_day[df_by_day['Resultado_Dia'] > 0])
    metrics['dias_negativos'] = len(df_by_day[df_by_day['Resultado_Dia'] < 0])
    metrics['media_resultado_dia'] = df_by_day['Resultado_Dia'].mean()
    
    # Análise por hora
    df_by_hour = df.groupby('Hora_Abertura').agg({
        'Resultado': ['sum', 'mean', 'count'],
        'Status': lambda x: (x == 'Gain').sum()
    }).reset_index()
    df_by_hour.columns = ['Hora', 'Resultado_Total', 'Resultado_Medio', 'Total_Ops', 'Gains']
    df_by_hour['Win_Rate'] = (df_by_hour['Gains'] / df_by_hour['Total_Ops']) * 100
    
    metrics['analise_hora'] = df_by_hour
    if len(df_by_hour) > 0:
        metrics['melhor_hora'] = df_by_hour.loc[df_by_hour['Resultado_Total'].idxmax()]
        metrics['pior_hora'] = df_by_hour.loc[df_by_hour['Resultado_Total'].idxmin()]
    
    # Análise por dia da semana
    dias_pt = {
        'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta',
        'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
    }
    df['Dia_Semana_PT'] = df['Dia_Semana'].map(dias_pt)
    
    df_by_weekday = df.groupby(['Dia_Semana_Num', 'Dia_Semana_PT']).agg({
        'Resultado': ['sum', 'mean', 'count'],
        'Status': lambda x: (x == 'Gain').sum()
    }).reset_index()
    df_by_weekday.columns = ['Dia_Num', 'Dia_Semana', 'Resultado_Total', 'Resultado_Medio', 'Total_Ops', 'Gains']
    df_by_weekday['Win_Rate'] = (df_by_weekday['Gains'] / df_by_weekday['Total_Ops']) * 100
    df_by_weekday = df_by_weekday.sort_values('Dia_Num')
    
    metrics['analise_dia_semana'] = df_by_weekday
    if len(df_by_weekday) > 0:
        metrics['melhor_dia_semana'] = df_by_weekday.loc[df_by_weekday['Resultado_Total'].idxmax()]
        metrics['pior_dia_semana'] = df_by_weekday.loc[df_by_weekday['Resultado_Total'].idxmin()]
    
    # Análise por Ativo
    df_by_asset = df.groupby('Ativo').agg({
        'Resultado': ['sum', 'mean', 'count'],
        'Status': lambda x: (x == 'Gain').sum(),
        'Volume': 'sum'
    }).reset_index()
    df_by_asset.columns = ['Ativo', 'Resultado_Total', 'Resultado_Medio', 'Total_Ops', 'Gains', 'Volume_Total']
    df_by_asset['Win_Rate'] = (df_by_asset['Gains'] / df_by_asset['Total_Ops']) * 100
    df_by_asset = df_by_asset.sort_values('Resultado_Total', ascending=False)
    
    metrics['analise_ativo'] = df_by_asset
    if len(df_by_asset) > 0:
        metrics['melhor_ativo'] = df_by_asset.iloc[0]
        metrics['pior_ativo'] = df_by_asset.iloc[-1]
    
    # Análise por Sessão
    df_by_session = df.groupby('Sessao').agg({
        'Resultado': ['sum', 'mean', 'count'],
        'Status': lambda x: (x == 'Gain').sum()
    }).reset_index()
    df_by_session.columns = ['Sessao', 'Resultado_Total', 'Resultado_Medio', 'Total_Ops', 'Gains']
    df_by_session['Win_Rate'] = (df_by_session['Gains'] / df_by_session['Total_Ops']) * 100
    
    metrics['analise_sessao'] = df_by_session
    
    # Análise por Tipo (Buy/Sell)
    df_by_type = df.groupby('Tipo').agg({
        'Resultado': ['sum', 'mean', 'count'],
        'Status': lambda x: (x == 'Gain').sum()
    }).reset_index()
    df_by_type.columns = ['Tipo', 'Resultado_Total', 'Resultado_Medio', 'Total_Ops', 'Gains']
    df_by_type['Win_Rate'] = (df_by_type['Gains'] / df_by_type['Total_Ops']) * 100
    
    metrics['analise_tipo'] = df_by_type
    
    # Resultado de hoje
    hoje = datetime.now().date()
    df_hoje = df[df['Data'] == hoje]
    metrics['resultado_hoje'] = df_hoje['Resultado'].sum() if len(df_hoje) > 0 else 0
    metrics['ops_hoje'] = len(df_hoje)
    
    # Progresso da meta
    metrics['progresso_meta'] = (metrics['resultado_hoje'] / meta_diaria_valor) * 100 if meta_diaria_valor > 0 else 0
    
    # Sequências
    df_sorted = df.sort_values('Abertura')
    current_streak = 0
    max_win_streak = 0
    max_loss_streak = 0
    current_type = None
    
    for status in df_sorted['Status']:
        if status == 'Gain':
            if current_type == 'Gain':
                current_streak += 1
            else:
                current_streak = 1
                current_type = 'Gain'
            max_win_streak = max(max_win_streak, current_streak)
        elif status == 'Loss':
            if current_type == 'Loss':
                current_streak += 1
            else:
                current_streak = 1
                current_type = 'Loss'
            max_loss_streak = max(max_loss_streak, current_streak)
    
    metrics['max_win_streak'] = max_win_streak
    metrics['max_loss_streak'] = max_loss_streak
    
    # Expectativa matemática
    prob_gain = gains / total_ops if total_ops > 0 else 0
    prob_loss = losses / total_ops if total_ops > 0 else 0
    metrics['expectativa'] = (prob_gain * metrics['media_gain']) - (prob_loss * metrics['media_loss'])
    
    # Duração média
    metrics['duracao_media'] = df['Duracao_Min'].mean()
    
    # Projeção mensal
    metrics['projecao_mensal'] = metrics['media_resultado_dia'] * 20 if metrics['dias_operados'] > 0 else 0
    
    return metrics

def get_mood_analysis(metrics):
    """Analisa o humor/qualidade das operações do dia"""
    resultado_hoje = metrics.get('resultado_hoje', 0)
    ops_hoje = metrics.get('ops_hoje', 0)
    progresso_meta = metrics.get('progresso_meta', 0)
    
    if ops_hoje == 0:
        return "😴", "Aguardando operações", "#8b8b9a"
    
    if progresso_meta >= 100:
        return "🏆", "META BATIDA! Excelente dia!", "#ffd700"
    elif resultado_hoje > 0 and progresso_meta >= 50:
        return "🚀", "Ótimo progresso!", "#00ff88"
    elif resultado_hoje > 0:
        return "😊", "Dia positivo, continue assim!", "#00d4ff"
    elif resultado_hoje == 0:
        return "😐", "Dia no zero", "#8b8b9a"
    elif resultado_hoje > -metrics.get('meta_diaria_valor', 0) * 0.5:
        return "😟", "Dia negativo, mas controlado", "#ffa500"
    else:
        return "🛑", "STOP! Reavalie antes de continuar", "#ff4757"

def get_forex_insights(df, metrics):
    """Gera insights inteligentes para Forex"""
    insights = []
    warnings = []
    
    # Melhor horário
    if 'melhor_hora' in metrics:
        hora = int(metrics['melhor_hora']['Hora'])
        insights.append(f"📈 Seu melhor horário é às **{hora}h** (UTC) - foque suas operações aqui")
    
    # Pior horário
    if 'pior_hora' in metrics and metrics['pior_hora']['Resultado_Total'] < 0:
        hora = int(metrics['pior_hora']['Hora'])
        warnings.append(f"⚠️ Evite operar às **{hora}h** - histórico negativo")
    
    # Melhor ativo
    if 'melhor_ativo' in metrics:
        ativo = metrics['melhor_ativo']['Ativo']
        resultado = metrics['melhor_ativo']['Resultado_Total']
        win_rate = metrics['melhor_ativo']['Win_Rate']
        insights.append(f"💰 **{ativo}** é seu melhor ativo: ${resultado:.2f} | WR: {win_rate:.0f}%")
    
    # Pior ativo
    if 'pior_ativo' in metrics and metrics['pior_ativo']['Resultado_Total'] < 0:
        ativo = metrics['pior_ativo']['Ativo']
        warnings.append(f"🚫 Considere parar de operar **{ativo}** - resultados negativos")
    
    # Melhor sessão
    if 'analise_sessao' in metrics and len(metrics['analise_sessao']) > 0:
        df_sessao = metrics['analise_sessao']
        melhor_sessao = df_sessao.loc[df_sessao['Resultado_Total'].idxmax()]
        insights.append(f"🌍 Sessão de **{melhor_sessao['Sessao']}** é a mais lucrativa para você")
    
    # Win rate
    win_rate = metrics.get('win_rate', 0)
    if win_rate >= 70:
        insights.append(f"✅ Win rate excepcional de **{win_rate:.1f}%**!")
    elif win_rate >= 50:
        insights.append(f"✅ Win rate de **{win_rate:.1f}%** - acima da média")
    elif win_rate < 40:
        warnings.append(f"⚠️ Win rate de **{win_rate:.1f}%** - revise sua estratégia")
    
    # Payoff
    payoff = metrics.get('payoff', 0)
    if payoff >= 2:
        insights.append(f"💎 Payoff de **{payoff:.2f}** - excelente gestão de risco!")
    elif payoff < 1:
        warnings.append(f"⚠️ Payoff de **{payoff:.2f}** - seus ganhos não compensam as perdas")
    
    # Drawdown
    dd_pct = metrics.get('max_drawdown_pct', 0)
    if dd_pct > 20:
        warnings.append(f"🔴 Drawdown máximo de **{dd_pct:.1f}%** - risco muito elevado!")
    elif dd_pct > 10:
        warnings.append(f"⚠️ Drawdown de **{dd_pct:.1f}%** - monitore o risco")
    
    # Tipo de operação (Buy vs Sell)
    if 'analise_tipo' in metrics and len(metrics['analise_tipo']) > 0:
        df_tipo = metrics['analise_tipo']
        for _, row in df_tipo.iterrows():
            tipo = row['Tipo'].upper()
            resultado = row['Resultado_Total']
            if resultado < -100:
                warnings.append(f"⚠️ Operações de **{tipo}** estão negativas (${resultado:.2f})")
    
    # Swap
    total_swap = metrics.get('total_swap', 0)
    if total_swap < -50:
        warnings.append(f"💸 Swap acumulado de **${total_swap:.2f}** - evite carregar posições overnight")
    
    # Consistência
    dias_pos = metrics.get('dias_positivos', 0)
    dias_total = metrics.get('dias_operados', 1)
    taxa_dias_pos = (dias_pos / dias_total) * 100 if dias_total > 0 else 0
    if taxa_dias_pos >= 70:
        insights.append(f"📊 **{taxa_dias_pos:.0f}%** dos dias positivos - trader consistente!")
    
    return insights, warnings

# ═══════════════════════════════════════════════════════════════════════════════
# ESTADO DA SESSÃO
# ═══════════════════════════════════════════════════════════════════════════════

if 'df_forex' not in st.session_state:
    st.session_state.df_forex = None
if 'account_info_forex' not in st.session_state:
    st.session_state.account_info_forex = {}
if 'capital_inicial_forex' not in st.session_state:
    st.session_state.capital_inicial_forex = 1000.0
if 'meta_diaria_forex' not in st.session_state:
    st.session_state.meta_diaria_forex = 2.0
if 'humor_dia_forex' not in st.session_state:
    st.session_state.humor_dia_forex = "Neutro"

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <span style='font-family: Orbitron; font-size: 1.5rem; color: #ffd700;'>⚙️ CONFIGURAÇÕES</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Upload de arquivo
    st.markdown("### 📁 Importar Relatório MT5")
    uploaded_file = st.file_uploader("Arraste seu arquivo aqui", type=['xlsx', 'xls'], 
                                     help="Arquivo Excel exportado do MetaTrader 5")
    
    if uploaded_file is not None:
        try:
            df, account_info = parse_forex_xlsx(uploaded_file)
            st.session_state.df_forex = df
            st.session_state.account_info_forex = account_info
            st.success(f"✅ {len(df)} operações carregadas!")
        except Exception as e:
            st.error(f"Erro ao processar arquivo: {e}")
    
    st.markdown("---")
    
    # Configurações de capital
    st.markdown("### 💰 Capital")
    
    capital_inicial = st.number_input(
        "Capital Inicial (USD)",
        min_value=0.0,
        value=st.session_state.capital_inicial_forex,
        step=100.0,
        help="Valor inicial da conta em dólares"
    )
    st.session_state.capital_inicial_forex = capital_inicial
    
    st.markdown("---")
    
    # Meta diária
    st.markdown("### 🎯 Meta Diária")
    
    meta_diaria_pct = st.slider(
        "Meta (%)",
        min_value=0.5,
        max_value=10.0,
        value=st.session_state.meta_diaria_forex,
        step=0.5,
        help="Porcentagem de ganho diário desejada"
    )
    st.session_state.meta_diaria_forex = meta_diaria_pct
    
    meta_valor = capital_inicial * (meta_diaria_pct / 100)
    st.info(f"Meta: **$ {meta_valor:.2f}**/dia")
    
    st.markdown("---")
    
    # Humor do dia
    st.markdown("### 🧠 Registro do Dia")
    
    humor_options = ["😤 Ansioso", "😊 Confiante", "😐 Neutro", "😴 Cansado", "🎯 Focado", "😰 Nervoso"]
    humor_dia = st.selectbox("Como você está hoje?", humor_options, index=2)
    st.session_state.humor_dia_forex = humor_dia
    
    st.markdown("---")
    
    # Sessões de Trading
    st.markdown("### 🌍 Sessões de Mercado")
    
    hora_atual = datetime.now().hour
    
    sessoes = [
        ("Ásia", "00:00 - 08:00", 0, 8),
        ("Londres", "08:00 - 13:00", 8, 13),
        ("Nova York", "13:00 - 21:00", 13, 21)
    ]
    
    for nome, horario, inicio, fim in sessoes:
        is_active = inicio <= hora_atual < fim
        status = "🟢 ATIVA" if is_active else "⚫"
        st.markdown(f"**{nome}** {status}\n{horario} UTC")
    
    st.markdown("---")
    
    # Info da conta
    if st.session_state.account_info_forex:
        st.markdown("### 📋 Info da Conta")
        info = st.session_state.account_info_forex
        st.write(f"**Nome:** {info.get('nome', 'N/A')}")
        st.write(f"**Conta:** {info.get('conta', 'N/A')}")
        st.write(f"**Corretora:** {info.get('empresa', 'N/A')}")

# ═══════════════════════════════════════════════════════════════════════════════
# CONTEÚDO PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

# Header
st.markdown('<h1 class="main-header">🌍 FOREX COMMAND CENTER</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">SISTEMA INTELIGENTE DE GERENCIAMENTO • FOREX & COMMODITIES</p>', unsafe_allow_html=True)

if st.session_state.df_forex is not None and len(st.session_state.df_forex) > 0:
    df = st.session_state.df_forex
    metrics = calculate_forex_metrics(
        df, 
        st.session_state.capital_inicial_forex, 
        st.session_state.meta_diaria_forex
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MÉTRICAS PRINCIPAIS
    # ═══════════════════════════════════════════════════════════════════════════
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        valor = metrics['capital_atual']
        delta = metrics['lucro_total']
        delta_pct = metrics['retorno_total_pct']
        color_class = "metric-positive" if delta >= 0 else "metric-negative"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💼 CAPITAL ATUAL</div>
            <div class="metric-value {color_class}">$ {valor:,.2f}</div>
            <div class="metric-change {color_class}">{"+" if delta >= 0 else ""}${delta:,.2f} ({delta_pct:+.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        valor = metrics['resultado_hoje']
        progresso = metrics['progresso_meta']
        color_class = "metric-positive" if valor > 0 else ("metric-negative" if valor < 0 else "metric-neutral")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📊 HOJE</div>
            <div class="metric-value {color_class}">$ {valor:,.2f}</div>
            <div class="metric-change">Meta: {progresso:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        win_rate = metrics['win_rate']
        color_class = "metric-positive" if win_rate >= 50 else "metric-negative"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🎯 WIN RATE</div>
            <div class="metric-value {color_class}">{win_rate:.1f}%</div>
            <div class="metric-change">{metrics['gains']}W / {metrics['losses']}L</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        payoff = metrics['payoff']
        color_class = "metric-positive" if payoff >= 1 else "metric-negative"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⚖️ PAYOFF</div>
            <div class="metric-value {color_class}">{payoff:.2f}</div>
            <div class="metric-change">+${metrics['media_gain']:.0f} / -${metrics['media_loss']:.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        fl = metrics['fator_lucro']
        color_class = "metric-positive" if fl >= 1.5 else ("metric-gold" if fl >= 1 else "metric-negative")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📈 FATOR LUCRO</div>
            <div class="metric-value {color_class}">{fl:.2f}</div>
            <div class="metric-change">{metrics['total_operacoes']} trades</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        dd = metrics['max_drawdown']
        dd_pct = metrics['max_drawdown_pct']
        color_class = "metric-negative" if dd_pct > 10 else ("metric-gold" if dd_pct > 5 else "metric-positive")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📉 MAX DD</div>
            <div class="metric-value {color_class}">$ {dd:,.2f}</div>
            <div class="metric-change">{dd_pct:.1f}% do capital</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # HUMOR E PROGRESSO
    # ═══════════════════════════════════════════════════════════════════════════
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        emoji, mensagem, cor = get_mood_analysis(metrics)
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <div class="mood-emoji">{emoji}</div>
            <div style="color: {cor}; font-family: 'JetBrains Mono'; font-size: 0.9rem;">{mensagem}</div>
            <div style="color: #8b8b9a; font-size: 0.8rem; margin-top: 0.5rem;">{st.session_state.humor_dia_forex}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Barra de progresso da meta
        progresso = min(metrics['progresso_meta'], 100)
        cor_barra = "#ffd700" if progresso >= 100 else ("#00ff88" if progresso > 0 else "#ff4757")
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📈 PROGRESSO DA META DIÁRIA</div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: #fff; font-family: 'Orbitron'; font-size: 1.2rem;">
                    $ {metrics['resultado_hoje']:,.2f}
                </span>
                <span style="color: #8b8b9a;">
                    Meta: $ {metrics['meta_diaria_valor']:,.2f}
                </span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar" style="width: {max(progresso, 0)}%; background: linear-gradient(90deg, {cor_barra}, {cor_barra}88);"></div>
            </div>
            <div style="text-align: center; color: {cor_barra}; font-family: 'Orbitron'; font-size: 1.5rem; margin-top: 0.5rem;">
                {progresso:.0f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Ativos operados
        ativos = df['Ativo'].unique()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🎲 ATIVOS OPERADOS</div>
            <div style="margin-top: 0.5rem;">
        """, unsafe_allow_html=True)
        
        for ativo in ativos[:6]:  # Mostrar até 6 ativos
            categoria = df[df['Ativo'] == ativo]['Categoria'].iloc[0]
            badge_class = 'badge-gold' if categoria == 'Ouro' else ('badge-crypto' if categoria == 'Crypto' else 'badge-forex')
            st.markdown(f'<span class="asset-badge {badge_class}">{ativo}</span>', unsafe_allow_html=True)
        
        if len(ativos) > 6:
            st.markdown(f'<span style="color: #8b8b9a; font-size: 0.8rem;">+{len(ativos)-6} mais</span>', unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TABS PRINCIPAIS
    # ═══════════════════════════════════════════════════════════════════════════
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["📊 Análises", "💹 Ativos", "⏰ Horários", "📅 Dias", "📈 Evolução", "📋 Operações", "📆 Mensal", "🧮 Calculadora", "💰 Juros Compostos"])
    
    # TAB 1: ANÁLISES E INSIGHTS
    with tab1:
        insights, warnings = get_forex_insights(df, metrics)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-title">✅ INSIGHTS POSITIVOS</div>', unsafe_allow_html=True)
            if insights:
                for insight in insights:
                    st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)
            else:
                st.info("Continue operando para gerar insights")
        
        with col2:
            st.markdown('<div class="section-title">⚠️ PONTOS DE ATENÇÃO</div>', unsafe_allow_html=True)
            if warnings:
                for warning in warnings:
                    st.markdown(f'<div class="warning-card">{warning}</div>', unsafe_allow_html=True)
            else:
                st.success("Nenhum alerta no momento!")
        
        # Estatísticas detalhadas
        st.markdown('<div class="section-title">📊 ESTATÍSTICAS DETALHADAS</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="info-card">
                <div style="color: #ffd700; font-weight: bold;">📈 OPERAÇÕES</div>
                <div style="color: #fff; margin-top: 0.5rem;">
                    Total: <strong>{metrics['total_operacoes']}</strong><br>
                    Wins: <strong style="color: #00ff88;">{metrics['gains']}</strong><br>
                    Losses: <strong style="color: #ff4757;">{metrics['losses']}</strong><br>
                    Volume: <strong>{metrics['volume_total']:.2f}</strong> lotes
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="info-card">
                <div style="color: #ffd700; font-weight: bold;">💰 RESULTADOS</div>
                <div style="color: #fff; margin-top: 0.5rem;">
                    Maior Gain: <strong style="color: #00ff88;">$ {metrics['maior_gain']:,.2f}</strong><br>
                    Maior Loss: <strong style="color: #ff4757;">$ {metrics['maior_loss']:,.2f}</strong><br>
                    Média/Dia: <strong>$ {metrics['media_resultado_dia']:,.2f}</strong><br>
                    Expectativa: <strong>$ {metrics['expectativa']:,.2f}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="info-card">
                <div style="color: #ffd700; font-weight: bold;">📅 DIAS</div>
                <div style="color: #fff; margin-top: 0.5rem;">
                    Operados: <strong>{metrics['dias_operados']}</strong><br>
                    Positivos: <strong style="color: #00ff88;">{metrics['dias_positivos']}</strong><br>
                    Negativos: <strong style="color: #ff4757;">{metrics['dias_negativos']}</strong><br>
                    Taxa: <strong>{(metrics['dias_positivos']/max(metrics['dias_operados'],1))*100:.0f}%</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="info-card">
                <div style="color: #ffd700; font-weight: bold;">💸 CUSTOS</div>
                <div style="color: #fff; margin-top: 0.5rem;">
                    Swap: <strong style="color: {'#ff4757' if metrics['total_swap'] < 0 else '#00ff88'};">$ {metrics['total_swap']:,.2f}</strong><br>
                    Comissão: <strong style="color: #ff4757;">$ {metrics['total_comissao']:,.2f}</strong><br>
                    Duração Média: <strong>{metrics['duracao_media']:.0f} min</strong><br>
                    Projeção/Mês: <strong>$ {metrics['projecao_mensal']:,.2f}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Análise por Sessão
        st.markdown('<div class="section-title">🌍 PERFORMANCE POR SESSÃO</div>', unsafe_allow_html=True)
        
        if 'analise_sessao' in metrics and len(metrics['analise_sessao']) > 0:
            df_sessao = metrics['analise_sessao']
            
            cols = st.columns(len(df_sessao))
            for idx, (_, row) in enumerate(df_sessao.iterrows()):
                with cols[idx]:
                    resultado = row['Resultado_Total']
                    cor = '#00ff88' if resultado > 0 else ('#ff4757' if resultado < 0 else '#8b8b9a')
                    emoji_sessao = '🌏' if row['Sessao'] == 'Ásia' else ('🇬🇧' if row['Sessao'] == 'Londres' else '🗽')
                    
                    st.markdown(f"""
                    <div class="metric-card" style="text-align: center;">
                        <div style="font-size: 2rem;">{emoji_sessao}</div>
                        <div style="color: #ffd700; font-weight: bold;">{row['Sessao']}</div>
                        <div style="color: {cor}; font-family: 'Orbitron'; font-size: 1.3rem;">$ {resultado:,.2f}</div>
                        <div style="color: #8b8b9a; font-size: 0.8rem;">{int(row['Total_Ops'])} ops | WR: {row['Win_Rate']:.0f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # TAB 2: ANÁLISE POR ATIVO
    with tab2:
        st.markdown('<div class="section-title">💹 PERFORMANCE POR ATIVO</div>', unsafe_allow_html=True)
        
        if 'analise_ativo' in metrics and len(metrics['analise_ativo']) > 0:
            df_ativo = metrics['analise_ativo'].copy()
            
            # Gráfico de barras por ativo
            fig = go.Figure()
            
            colors = ['#ffd700' if 'XAU' in str(x) else ('#00ff88' if r > 0 else '#ff4757') 
                     for x, r in zip(df_ativo['Ativo'], df_ativo['Resultado_Total'])]
            
            fig.add_trace(go.Bar(
                x=df_ativo['Ativo'],
                y=df_ativo['Resultado_Total'],
                marker_color=colors,
                text=[f'${x:,.0f}' for x in df_ativo['Resultado_Total']],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Resultado: $%{y:,.2f}<extra></extra>'
            ))
            
            fig.update_layout(
                title=dict(text='Resultado por Ativo', font=dict(color='#ffd700', family='Orbitron')),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fff', family='JetBrains Mono'),
                xaxis=dict(gridcolor='#2a2a3a'),
                yaxis=dict(gridcolor='#2a2a3a', title='Resultado ($)'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Cards dos melhores e piores
            col1, col2 = st.columns(2)
            
            with col1:
                if 'melhor_ativo' in metrics:
                    ativo = metrics['melhor_ativo']
                    st.markdown(f"""
                    <div class="insight-card">
                        <div style="font-size: 1.5rem;">🏆 MELHOR ATIVO</div>
                        <div style="font-family: 'Orbitron'; font-size: 1.8rem; color: #ffd700;">{ativo['Ativo']}</div>
                        <div>Resultado: <strong style="color: #00ff88;">$ {ativo['Resultado_Total']:,.2f}</strong></div>
                        <div>Operações: {int(ativo['Total_Ops'])} | Win Rate: {ativo['Win_Rate']:.0f}%</div>
                        <div>Volume: {ativo['Volume_Total']:.2f} lotes</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                if 'pior_ativo' in metrics:
                    ativo = metrics['pior_ativo']
                    cor = '#ff4757' if ativo['Resultado_Total'] < 0 else '#ffa500'
                    st.markdown(f"""
                    <div class="warning-card">
                        <div style="font-size: 1.5rem;">⚠️ ATIVO A EVITAR</div>
                        <div style="font-family: 'Orbitron'; font-size: 1.8rem; color: {cor};">{ativo['Ativo']}</div>
                        <div>Resultado: <strong style="color: {cor};">$ {ativo['Resultado_Total']:,.2f}</strong></div>
                        <div>Operações: {int(ativo['Total_Ops'])} | Win Rate: {ativo['Win_Rate']:.0f}%</div>
                        <div>Volume: {ativo['Volume_Total']:.2f} lotes</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Tabela detalhada
            st.markdown("#### Detalhamento por Ativo")
            df_display = df_ativo.copy()
            df_display['Resultado_Total'] = df_display['Resultado_Total'].apply(lambda x: f'$ {x:,.2f}')
            df_display['Resultado_Medio'] = df_display['Resultado_Medio'].apply(lambda x: f'$ {x:,.2f}')
            df_display['Win_Rate'] = df_display['Win_Rate'].apply(lambda x: f'{x:.0f}%')
            df_display['Volume_Total'] = df_display['Volume_Total'].apply(lambda x: f'{x:.2f}')
            df_display.columns = ['Ativo', 'Total ($)', 'Média ($)', 'Operações', 'Gains', 'Volume', 'Win Rate']
            st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # TAB 3: ANÁLISE POR HORÁRIO
    with tab3:
        st.markdown('<div class="section-title">⏰ PERFORMANCE POR HORÁRIO (UTC)</div>', unsafe_allow_html=True)
        
        if 'analise_hora' in metrics and len(metrics['analise_hora']) > 0:
            df_hora = metrics['analise_hora'].copy()
            
            # Heatmap style chart
            fig = go.Figure()
            
            colors = ['#00ff88' if x > 0 else '#ff4757' for x in df_hora['Resultado_Total']]
            
            fig.add_trace(go.Bar(
                x=df_hora['Hora'].astype(str) + 'h',
                y=df_hora['Resultado_Total'],
                marker_color=colors,
                text=[f'${x:,.0f}' for x in df_hora['Resultado_Total']],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Resultado: $%{y:,.2f}<extra></extra>'
            ))
            
            fig.update_layout(
                title=dict(text='Resultado por Horário', font=dict(color='#ffd700', family='Orbitron')),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fff', family='JetBrains Mono'),
                xaxis=dict(gridcolor='#2a2a3a', title='Horário (UTC)'),
                yaxis=dict(gridcolor='#2a2a3a', title='Resultado ($)'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if 'melhor_hora' in metrics:
                    hora = int(metrics['melhor_hora']['Hora'])
                    resultado = metrics['melhor_hora']['Resultado_Total']
                    win_rate = metrics['melhor_hora']['Win_Rate']
                    st.markdown(f"""
                    <div class="insight-card">
                        <div style="font-size: 1.5rem;">🏆 MELHOR HORÁRIO</div>
                        <div style="font-family: 'Orbitron'; font-size: 2rem; color: #00ff88;">{hora}h UTC</div>
                        <div>Resultado: $ {resultado:,.2f}</div>
                        <div>Win Rate: {win_rate:.0f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                if 'pior_hora' in metrics:
                    hora = int(metrics['pior_hora']['Hora'])
                    resultado = metrics['pior_hora']['Resultado_Total']
                    win_rate = metrics['pior_hora']['Win_Rate']
                    st.markdown(f"""
                    <div class="warning-card">
                        <div style="font-size: 1.5rem;">⚠️ EVITAR HORÁRIO</div>
                        <div style="font-family: 'Orbitron'; font-size: 2rem; color: #ff4757;">{hora}h UTC</div>
                        <div>Resultado: $ {resultado:,.2f}</div>
                        <div>Win Rate: {win_rate:.0f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # TAB 4: ANÁLISE POR DIA DA SEMANA
    with tab4:
        st.markdown('<div class="section-title">📅 PERFORMANCE POR DIA DA SEMANA</div>', unsafe_allow_html=True)
        
        if 'analise_dia_semana' in metrics and len(metrics['analise_dia_semana']) > 0:
            df_dia = metrics['analise_dia_semana'].copy()
            
            fig = go.Figure()
            
            colors = ['#00ff88' if x > 0 else '#ff4757' for x in df_dia['Resultado_Total']]
            
            fig.add_trace(go.Bar(
                x=df_dia['Dia_Semana'],
                y=df_dia['Resultado_Total'],
                marker_color=colors,
                text=[f'${x:,.0f}' for x in df_dia['Resultado_Total']],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Resultado: $%{y:,.2f}<extra></extra>'
            ))
            
            fig.update_layout(
                title=dict(text='Resultado por Dia da Semana', font=dict(color='#ffd700', family='Orbitron')),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#fff', family='JetBrains Mono'),
                xaxis=dict(gridcolor='#2a2a3a'),
                yaxis=dict(gridcolor='#2a2a3a', title='Resultado ($)'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if 'melhor_dia_semana' in metrics:
                    dia = metrics['melhor_dia_semana']['Dia_Semana']
                    resultado = metrics['melhor_dia_semana']['Resultado_Total']
                    win_rate = metrics['melhor_dia_semana']['Win_Rate']
                    st.markdown(f"""
                    <div class="insight-card">
                        <div style="font-size: 1.5rem;">🏆 MELHOR DIA</div>
                        <div style="font-family: 'Orbitron'; font-size: 2rem; color: #00ff88;">{dia}</div>
                        <div>Resultado: $ {resultado:,.2f}</div>
                        <div>Win Rate: {win_rate:.0f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                if 'pior_dia_semana' in metrics:
                    dia = metrics['pior_dia_semana']['Dia_Semana']
                    resultado = metrics['pior_dia_semana']['Resultado_Total']
                    win_rate = metrics['pior_dia_semana']['Win_Rate']
                    cor = '#ff4757' if resultado < 0 else '#ffa500'
                    st.markdown(f"""
                    <div class="warning-card">
                        <div style="font-size: 1.5rem;">⚠️ PIOR DIA</div>
                        <div style="font-family: 'Orbitron'; font-size: 2rem; color: {cor};">{dia}</div>
                        <div>Resultado: $ {resultado:,.2f}</div>
                        <div>Win Rate: {win_rate:.0f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # TAB 5: EVOLUÇÃO DO CAPITAL
    with tab5:
        st.markdown('<div class="section-title">📈 EVOLUÇÃO DO CAPITAL</div>', unsafe_allow_html=True)
        
        # Preparar dados de evolução
        df_sorted = df.sort_values('Abertura').copy()
        df_sorted['Resultado_Acum'] = df_sorted['Resultado'].cumsum()
        df_sorted['Capital'] = st.session_state.capital_inicial_forex + df_sorted['Resultado_Acum']
        
        # Gráfico de área
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_sorted['Abertura'],
            y=df_sorted['Capital'],
            mode='lines',
            name='Capital',
            line=dict(color='#ffd700', width=2),
            fill='tozeroy',
            fillcolor='rgba(255, 215, 0, 0.1)',
            hovertemplate='<b>%{x}</b><br>Capital: $%{y:,.2f}<extra></extra>'
        ))
        
        # Linha do capital inicial
        fig.add_hline(
            y=st.session_state.capital_inicial_forex,
            line_dash="dash",
            line_color="#00d4ff",
            annotation_text="Capital Inicial"
        )
        
        fig.update_layout(
            title=dict(text='Evolução do Capital', font=dict(color='#ffd700', family='Orbitron')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#fff', family='JetBrains Mono'),
            xaxis=dict(gridcolor='#2a2a3a', title='Data/Hora'),
            yaxis=dict(gridcolor='#2a2a3a', title='Capital ($)'),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico de resultado por operação
        fig2 = go.Figure()
        
        colors = ['#ffd700' if 'XAU' in str(a) else ('#00ff88' if r > 0 else '#ff4757') 
                 for a, r in zip(df_sorted['Ativo'], df_sorted['Resultado'])]
        
        fig2.add_trace(go.Bar(
            x=list(range(1, len(df_sorted) + 1)),
            y=df_sorted['Resultado'],
            marker_color=colors,
            hovertemplate='<b>Op #%{x}</b><br>Resultado: $%{y:,.2f}<extra></extra>'
        ))
        
        fig2.update_layout(
            title=dict(text='Resultado por Operação', font=dict(color='#ffd700', family='Orbitron')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#fff', family='JetBrains Mono'),
            xaxis=dict(gridcolor='#2a2a3a', title='Número da Operação'),
            yaxis=dict(gridcolor='#2a2a3a', title='Resultado ($)'),
            height=300
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # TAB 6: HISTÓRICO DE OPERAÇÕES
    with tab6:
        st.markdown('<div class="section-title">📋 HISTÓRICO DE OPERAÇÕES</div>', unsafe_allow_html=True)
        
        # Filtros
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            filtro_status = st.multiselect("Status", ['Gain', 'Loss', 'Empate'], default=['Gain', 'Loss', 'Empate'])
        
        with col2:
            ativos_lista = ['Todos'] + list(df['Ativo'].unique())
            filtro_ativo = st.selectbox("Ativo", ativos_lista)
        
        with col3:
            filtro_tipo = st.multiselect("Tipo", ['buy', 'sell'], default=['buy', 'sell'])
        
        with col4:
            ordem = st.selectbox("Ordenar por", ["Mais recentes", "Mais antigas", "Maior ganho", "Maior perda"])
        
        # Aplicar filtros
        df_filtrado = df[df['Status'].isin(filtro_status)].copy()
        df_filtrado = df_filtrado[df_filtrado['Tipo'].isin(filtro_tipo)]
        
        if filtro_ativo != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Ativo'] == filtro_ativo]
        
        # Ordenar
        if ordem == "Mais recentes":
            df_filtrado = df_filtrado.sort_values('Abertura', ascending=False)
        elif ordem == "Mais antigas":
            df_filtrado = df_filtrado.sort_values('Abertura', ascending=True)
        elif ordem == "Maior ganho":
            df_filtrado = df_filtrado.sort_values('Resultado', ascending=False)
        else:
            df_filtrado = df_filtrado.sort_values('Resultado', ascending=True)
        
        # Exibir tabela
        df_display = df_filtrado[['Abertura', 'Ativo', 'Tipo', 'Volume', 'Preco_Entrada', 'Preco_Saida', 'Resultado', 'Swap', 'Status']].copy()
        df_display.columns = ['Abertura', 'Ativo', 'Tipo', 'Volume', 'Entrada', 'Saída', 'Resultado ($)', 'Swap', 'Status']
        
        # Formatar
        df_display['Abertura'] = df_display['Abertura'].dt.strftime('%d/%m %H:%M')
        df_display['Resultado ($)'] = df_display['Resultado ($)'].apply(lambda x: f'$ {x:,.2f}')
        df_display['Swap'] = df_display['Swap'].apply(lambda x: f'$ {x:,.2f}')
        
        st.dataframe(df_display, use_container_width=True, hide_index=True, height=400)
        
        # Resumo
        total_filtrado = df_filtrado['Resultado'].sum()
        cor_total = '#00ff88' if total_filtrado > 0 else '#ff4757'
        st.markdown(f"""
        <div class="info-card" style="margin-top: 1rem;">
            <strong>Resumo:</strong> {len(df_filtrado)} operações filtradas | 
            Gains: {len(df_filtrado[df_filtrado['Status'] == 'Gain'])} | 
            Losses: {len(df_filtrado[df_filtrado['Status'] == 'Loss'])} | 
            Total: <span style="color: {cor_total};">$ {total_filtrado:,.2f}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # TAB 7: ANÁLISE MENSAL
    with tab7:
        st.markdown('<div class="section-title">📆 PERFORMANCE MENSAL</div>', unsafe_allow_html=True)
        
        # Criar coluna de mês/ano
        df['Mes_Ano'] = df['Abertura'].dt.to_period('M')
        df['Mes_Ano_Str'] = df['Abertura'].dt.strftime('%Y-%m')
        df['Mes_Nome'] = df['Abertura'].dt.strftime('%b/%Y')
        
        # Agrupar por mês
        df_mensal = df.groupby(['Mes_Ano_Str', 'Mes_Nome']).agg({
            'Resultado': ['sum', 'count'],
            'Status': lambda x: (x == 'Gain').sum(),
            'Volume': 'sum'
        }).reset_index()
        df_mensal.columns = ['Mes_Ano', 'Mes_Nome', 'Resultado_Total', 'Total_Ops', 'Gains', 'Volume_Total']
        df_mensal['Win_Rate'] = (df_mensal['Gains'] / df_mensal['Total_Ops']) * 100
        df_mensal = df_mensal.sort_values('Mes_Ano')
        
        # Calcular capital acumulado e % de ganho por mês
        capital_base = st.session_state.capital_inicial_forex
        df_mensal['Capital_Inicio_Mes'] = capital_base
        df_mensal['Capital_Fim_Mes'] = capital_base
        df_mensal['Ganho_Pct'] = 0.0
        
        capital_atual_calc = capital_base
        for idx in df_mensal.index:
            df_mensal.loc[idx, 'Capital_Inicio_Mes'] = capital_atual_calc
            resultado_mes = df_mensal.loc[idx, 'Resultado_Total']
            capital_fim = capital_atual_calc + resultado_mes
            df_mensal.loc[idx, 'Capital_Fim_Mes'] = capital_fim
            df_mensal.loc[idx, 'Ganho_Pct'] = (resultado_mes / capital_atual_calc) * 100 if capital_atual_calc > 0 else 0
            capital_atual_calc = capital_fim
        
        # Gráfico de barras do resultado mensal
        fig = go.Figure()
        
        colors = ['#00ff88' if x > 0 else '#ff4757' for x in df_mensal['Resultado_Total']]
        
        fig.add_trace(go.Bar(
            x=df_mensal['Mes_Nome'],
            y=df_mensal['Resultado_Total'],
            marker_color=colors,
            text=[f'${x:,.0f}' for x in df_mensal['Resultado_Total']],
            textposition='outside',
            name='Resultado ($)',
            hovertemplate='<b>%{x}</b><br>Resultado: $%{y:,.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text='Resultado Mensal ($)', font=dict(color='#ffd700', family='Orbitron')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#fff', family='JetBrains Mono'),
            xaxis=dict(gridcolor='#2a2a3a', title='Mês'),
            yaxis=dict(gridcolor='#2a2a3a', title='Resultado ($)'),
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico de % de ganho por mês
        fig2 = go.Figure()
        
        colors_pct = ['#00ff88' if x > 0 else '#ff4757' for x in df_mensal['Ganho_Pct']]
        
        fig2.add_trace(go.Bar(
            x=df_mensal['Mes_Nome'],
            y=df_mensal['Ganho_Pct'],
            marker_color=colors_pct,
            text=[f'{x:+.1f}%' for x in df_mensal['Ganho_Pct']],
            textposition='outside',
            name='Ganho (%)',
            hovertemplate='<b>%{x}</b><br>Ganho: %{y:.2f}%<extra></extra>'
        ))
        
        fig2.update_layout(
            title=dict(text='Ganho Mensal (%)', font=dict(color='#ffd700', family='Orbitron')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#fff', family='JetBrains Mono'),
            xaxis=dict(gridcolor='#2a2a3a', title='Mês'),
            yaxis=dict(gridcolor='#2a2a3a', title='Ganho (%)'),
            height=350
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Cards de resumo mensal
        st.markdown("#### 📊 Detalhamento Mensal")
        
        cols = st.columns(min(len(df_mensal), 4))
        for idx, (_, row) in enumerate(df_mensal.iterrows()):
            col_idx = idx % 4
            with cols[col_idx]:
                resultado = row['Resultado_Total']
                ganho_pct = row['Ganho_Pct']
                cor = '#00ff88' if resultado > 0 else '#ff4757'
                
                st.markdown(f"""
                <div class="metric-card" style="text-align: center; margin-bottom: 1rem;">
                    <div style="color: #ffd700; font-weight: bold; font-size: 1rem;">{row['Mes_Nome']}</div>
                    <div style="color: {cor}; font-family: 'Orbitron'; font-size: 1.5rem;">$ {resultado:,.2f}</div>
                    <div style="color: {cor}; font-size: 1.2rem; font-weight: bold;">{ganho_pct:+.1f}%</div>
                    <div style="color: #8b8b9a; font-size: 0.75rem; margin-top: 0.5rem;">
                        {int(row['Total_Ops'])} ops | WR: {row['Win_Rate']:.0f}%
                    </div>
                    <div style="color: #8b8b9a; font-size: 0.7rem;">
                        Capital: ${row['Capital_Inicio_Mes']:,.0f} → ${row['Capital_Fim_Mes']:,.0f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Tabela completa
        st.markdown("#### 📋 Tabela Completa")
        df_display_mensal = df_mensal.copy()
        df_display_mensal['Resultado_Total'] = df_display_mensal['Resultado_Total'].apply(lambda x: f'$ {x:,.2f}')
        df_display_mensal['Ganho_Pct'] = df_display_mensal['Ganho_Pct'].apply(lambda x: f'{x:+.2f}%')
        df_display_mensal['Win_Rate'] = df_display_mensal['Win_Rate'].apply(lambda x: f'{x:.1f}%')
        df_display_mensal['Capital_Inicio_Mes'] = df_display_mensal['Capital_Inicio_Mes'].apply(lambda x: f'$ {x:,.2f}')
        df_display_mensal['Capital_Fim_Mes'] = df_display_mensal['Capital_Fim_Mes'].apply(lambda x: f'$ {x:,.2f}')
        df_display_mensal['Volume_Total'] = df_display_mensal['Volume_Total'].apply(lambda x: f'{x:.2f}')
        
        df_display_mensal = df_display_mensal[['Mes_Nome', 'Resultado_Total', 'Ganho_Pct', 'Total_Ops', 'Gains', 'Win_Rate', 'Capital_Inicio_Mes', 'Capital_Fim_Mes']]
        df_display_mensal.columns = ['Mês', 'Resultado ($)', 'Ganho (%)', 'Operações', 'Gains', 'Win Rate', 'Capital Início', 'Capital Fim']
        
        st.dataframe(df_display_mensal, use_container_width=True, hide_index=True)
        
        # Resumo geral
        total_meses = len(df_mensal)
        meses_positivos = len(df_mensal[df_mensal['Resultado_Total'] > 0])
        media_mensal = df_mensal['Resultado_Total'].mean()
        media_pct = df_mensal['Ganho_Pct'].mean()
        melhor_mes = df_mensal.loc[df_mensal['Resultado_Total'].idxmax()]
        pior_mes = df_mensal.loc[df_mensal['Resultado_Total'].idxmin()]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="info-card">
                <div style="color: #ffd700; font-weight: bold;">📊 RESUMO</div>
                <div style="color: #fff; margin-top: 0.5rem;">
                    Total Meses: <strong>{total_meses}</strong><br>
                    Meses +: <strong style="color: #00ff88;">{meses_positivos}</strong><br>
                    Meses -: <strong style="color: #ff4757;">{total_meses - meses_positivos}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            cor_media = '#00ff88' if media_mensal > 0 else '#ff4757'
            st.markdown(f"""
            <div class="info-card">
                <div style="color: #ffd700; font-weight: bold;">📈 MÉDIA MENSAL</div>
                <div style="color: {cor_media}; font-family: 'Orbitron'; font-size: 1.3rem; margin-top: 0.5rem;">
                    $ {media_mensal:,.2f}
                </div>
                <div style="color: {cor_media};">
                    {media_pct:+.2f}% ao mês
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="insight-card">
                <div style="color: #00ff88; font-weight: bold;">🏆 MELHOR MÊS</div>
                <div style="color: #fff; margin-top: 0.5rem;">
                    <strong>{melhor_mes['Mes_Nome']}</strong><br>
                    $ {melhor_mes['Resultado_Total']:,.2f}<br>
                    {melhor_mes['Ganho_Pct']:+.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="warning-card">
                <div style="color: #ff4757; font-weight: bold;">📉 PIOR MÊS</div>
                <div style="color: #fff; margin-top: 0.5rem;">
                    <strong>{pior_mes['Mes_Nome']}</strong><br>
                    $ {pior_mes['Resultado_Total']:,.2f}<br>
                    {pior_mes['Ganho_Pct']:+.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # TAB 8: CALCULADORA DE PONTOS
    with tab8:
        st.markdown('<div class="section-title">🧮 CALCULADORA DE PONTOS / PIPS</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <p>Calcule o valor financeiro dos pontos/pips para diferentes ativos e tamanhos de lote.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ⚙️ Configuração")
            
            # Seleção do ativo
            ativo_calc = st.selectbox(
                "Selecione o Ativo",
                ["XAUUSD (Ouro)", "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", 
                 "XAGUSD (Prata)", "US30 (Dow Jones)", "NAS100 (Nasdaq)", "WIN (Mini Índice BR)", "Personalizado"],
                index=0
            )
            
            # Configurações do ativo
            ativo_configs = {
                "XAUUSD (Ouro)": {"pip_value": 0.01, "contract_size": 100, "pip_name": "ponto", "decimals": 2},
                "EURUSD": {"pip_value": 0.0001, "contract_size": 100000, "pip_name": "pip", "decimals": 4},
                "GBPUSD": {"pip_value": 0.0001, "contract_size": 100000, "pip_name": "pip", "decimals": 4},
                "USDJPY": {"pip_value": 0.01, "contract_size": 100000, "pip_name": "pip", "decimals": 2},
                "AUDUSD": {"pip_value": 0.0001, "contract_size": 100000, "pip_name": "pip", "decimals": 4},
                "USDCAD": {"pip_value": 0.0001, "contract_size": 100000, "pip_name": "pip", "decimals": 4},
                "XAGUSD (Prata)": {"pip_value": 0.01, "contract_size": 5000, "pip_name": "ponto", "decimals": 2},
                "US30 (Dow Jones)": {"pip_value": 1, "contract_size": 1, "pip_name": "ponto", "decimals": 0},
                "NAS100 (Nasdaq)": {"pip_value": 1, "contract_size": 1, "pip_name": "ponto", "decimals": 0},
                "WIN (Mini Índice BR)": {"pip_value": 5, "contract_size": 1, "pip_name": "ponto", "decimals": 0},
            }
            
            if ativo_calc == "Personalizado":
                pip_value = st.number_input("Valor do Pip/Ponto", value=0.0001, format="%.5f")
                contract_size = st.number_input("Tamanho do Contrato", value=100000, step=1000)
                pip_name = st.text_input("Nome (pip/ponto)", value="pip")
            else:
                config = ativo_configs[ativo_calc]
                pip_value = config["pip_value"]
                contract_size = config["contract_size"]
                pip_name = config["pip_name"]
                
                st.info(f"**{ativo_calc}**\n\nValor do {pip_name}: {pip_value}\n\nTamanho do contrato: {contract_size:,}")
            
            st.markdown("---")
            
            # Inputs
            lote = st.number_input("Tamanho do Lote", value=0.01, min_value=0.01, step=0.01, format="%.2f")
            pontos = st.number_input(f"Quantidade de {pip_name}s", value=10.0, step=1.0)
            
            # Cálculo
            valor_por_pip = lote * contract_size * pip_value
            resultado_calc = pontos * valor_por_pip
        
        with col2:
            st.markdown("### 📊 Resultado")
            
            st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <div class="metric-label">VALOR POR {pip_name.upper()}</div>
                <div class="metric-value metric-gold">$ {valor_por_pip:.2f}</div>
                <div class="metric-change">Com lote de {lote}</div>
            </div>
            """, unsafe_allow_html=True)
            
            cor_resultado = "metric-positive" if resultado_calc >= 0 else "metric-negative"
            st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <div class="metric-label">RESULTADO ({pontos:.0f} {pip_name}s)</div>
                <div class="metric-value {cor_resultado}">$ {resultado_calc:,.2f}</div>
                <div class="metric-change">{"Lucro" if resultado_calc >= 0 else "Prejuízo"} estimado</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Tabela de referência rápida
            st.markdown("#### 📋 Tabela de Referência")
            
            lotes_ref = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]
            pontos_ref = [5, 10, 20, 50, 100]
            
            tabela_data = []
            for l in lotes_ref:
                row = {"Lote": l}
                for p in pontos_ref:
                    valor = l * contract_size * pip_value * p
                    row[f"{p} {pip_name}s"] = f"${valor:.2f}"
                tabela_data.append(row)
            
            df_tabela = pd.DataFrame(tabela_data)
            st.dataframe(df_tabela, use_container_width=True, hide_index=True)
        
        # Calculadora de risco
        st.markdown("---")
        st.markdown("### 🎯 Calculadora de Risco")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            capital_risco = st.number_input("Capital da Conta ($)", value=float(st.session_state.capital_inicial_forex), step=100.0)
            risco_pct = st.slider("Risco por Operação (%)", 0.5, 5.0, 1.0, 0.5)
        
        with col2:
            stop_loss_pontos = st.number_input(f"Stop Loss ({pip_name}s)", value=20.0, step=1.0)
        
        with col3:
            # Cálculo do lote ideal
            valor_risco = capital_risco * (risco_pct / 100)
            if stop_loss_pontos > 0 and contract_size > 0 and pip_value > 0:
                lote_ideal = valor_risco / (stop_loss_pontos * contract_size * pip_value)
            else:
                lote_ideal = 0
            
            st.markdown(f"""
            <div class="gold-card" style="text-align: center;">
                <div style="color: #ffd700; font-weight: bold; font-size: 1rem;">💰 LOTE IDEAL</div>
                <div style="font-family: 'Orbitron'; font-size: 2rem; color: #fff;">{lote_ideal:.2f}</div>
                <div style="color: #8b8b9a; font-size: 0.8rem;">
                    Risco: ${valor_risco:.2f} ({risco_pct}%)<br>
                    Stop: {stop_loss_pontos:.0f} {pip_name}s
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # TAB 9: CALCULADORA DE JUROS COMPOSTOS
    with tab9:
        st.markdown('<div class="section-title">💰 CALCULADORA DE JUROS COMPOSTOS</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <p>Simule o crescimento do seu capital com juros compostos ao longo do tempo.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ⚙️ Configuração")
            
            capital_jc = st.number_input("Capital Inicial ($)", value=1000.0, min_value=1.0, step=100.0, key="capital_jc")
            
            modo_juros = st.radio("Modo de Cálculo", ["Taxa Diária (%)", "Taxa Mensal (%)", "Meta Diária ($)"])
            
            if modo_juros == "Taxa Diária (%)":
                taxa_dia = st.slider("Taxa Diária (%)", 0.1, 10.0, 2.0, 0.1, key="taxa_dia")
                taxa_mensal_calc = ((1 + taxa_dia/100) ** 20 - 1) * 100  # 20 dias úteis
            elif modo_juros == "Taxa Mensal (%)":
                taxa_mes = st.slider("Taxa Mensal (%)", 1.0, 100.0, 10.0, 1.0, key="taxa_mes")
                taxa_dia = ((1 + taxa_mes/100) ** (1/20) - 1) * 100
                taxa_mensal_calc = taxa_mes
            else:
                meta_dia_valor = st.number_input("Meta Diária ($)", value=50.0, min_value=1.0, step=10.0)
                taxa_dia = (meta_dia_valor / capital_jc) * 100
                taxa_mensal_calc = ((1 + taxa_dia/100) ** 20 - 1) * 100
            
            aporte_mensal = st.number_input("Aporte Mensal ($)", value=0.0, min_value=0.0, step=50.0)
            periodo_meses = st.slider("Período (meses)", 1, 60, 12)
            dias_uteis_mes = st.number_input("Dias úteis por mês", value=20, min_value=15, max_value=23)
            
            st.info(f"Taxa diária equivalente: **{taxa_dia:.2f}%**\n\nTaxa mensal equivalente: **{taxa_mensal_calc:.2f}%**")
        
        with col2:
            st.markdown("### 📊 Projeção")
            
            # Calcular projeção
            dados_projecao = []
            capital_acum = capital_jc
            total_aportes = 0
            
            for mes in range(1, periodo_meses + 1):
                capital_inicio = capital_acum
                
                # Aplicar juros diários
                for dia in range(dias_uteis_mes):
                    capital_acum = capital_acum * (1 + taxa_dia/100)
                
                # Adicionar aporte mensal
                capital_acum += aporte_mensal
                total_aportes += aporte_mensal
                
                lucro_mes = capital_acum - capital_inicio - aporte_mensal
                lucro_pct_mes = (lucro_mes / capital_inicio) * 100
                
                dados_projecao.append({
                    'Mes': mes,
                    'Capital_Inicio': capital_inicio,
                    'Lucro': lucro_mes,
                    'Lucro_Pct': lucro_pct_mes,
                    'Aporte': aporte_mensal,
                    'Capital_Final': capital_acum
                })
            
            df_projecao = pd.DataFrame(dados_projecao)
            
            # Métricas finais
            lucro_total_jc = capital_acum - capital_jc - total_aportes
            retorno_total = (lucro_total_jc / capital_jc) * 100
            
            st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <div class="metric-label">💎 CAPITAL FINAL</div>
                <div class="metric-value metric-gold">$ {capital_acum:,.2f}</div>
                <div class="metric-change">Em {periodo_meses} meses</div>
            </div>
            """, unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"""
                <div class="insight-card" style="text-align: center;">
                    <div style="color: #00ff88; font-weight: bold;">💰 LUCRO TOTAL</div>
                    <div style="font-family: 'Orbitron'; font-size: 1.5rem; color: #00ff88;">$ {lucro_total_jc:,.2f}</div>
                    <div style="color: #8b8b9a;">{retorno_total:,.1f}% de retorno</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown(f"""
                <div class="info-card" style="text-align: center;">
                    <div style="color: #00d4ff; font-weight: bold;">📥 TOTAL APORTES</div>
                    <div style="font-family: 'Orbitron'; font-size: 1.5rem; color: #00d4ff;">$ {total_aportes:,.2f}</div>
                    <div style="color: #8b8b9a;">{periodo_meses} meses</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Gráfico de evolução
        st.markdown("---")
        st.markdown("### 📈 Gráfico de Evolução")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_projecao['Mes'],
            y=df_projecao['Capital_Final'],
            mode='lines+markers',
            name='Capital',
            line=dict(color='#ffd700', width=3),
            fill='tozeroy',
            fillcolor='rgba(255, 215, 0, 0.1)',
            hovertemplate='<b>Mês %{x}</b><br>Capital: $%{y:,.2f}<extra></extra>'
        ))
        
        # Linha do capital inicial
        fig.add_hline(
            y=capital_jc,
            line_dash="dash",
            line_color="#00d4ff",
            annotation_text="Capital Inicial"
        )
        
        fig.update_layout(
            title=dict(text='Evolução do Capital com Juros Compostos', font=dict(color='#ffd700', family='Orbitron')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#fff', family='JetBrains Mono'),
            xaxis=dict(gridcolor='#2a2a3a', title='Mês', dtick=1),
            yaxis=dict(gridcolor='#2a2a3a', title='Capital ($)'),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela de projeção
        st.markdown("### 📋 Tabela de Projeção Mensal")
        
        df_display_jc = df_projecao.copy()
        df_display_jc['Capital_Inicio'] = df_display_jc['Capital_Inicio'].apply(lambda x: f'$ {x:,.2f}')
        df_display_jc['Lucro'] = df_display_jc['Lucro'].apply(lambda x: f'$ {x:,.2f}')
        df_display_jc['Lucro_Pct'] = df_display_jc['Lucro_Pct'].apply(lambda x: f'{x:+.2f}%')
        df_display_jc['Aporte'] = df_display_jc['Aporte'].apply(lambda x: f'$ {x:,.2f}')
        df_display_jc['Capital_Final'] = df_display_jc['Capital_Final'].apply(lambda x: f'$ {x:,.2f}')
        df_display_jc.columns = ['Mês', 'Capital Início', 'Lucro ($)', 'Lucro (%)', 'Aporte', 'Capital Final']
        
        st.dataframe(df_display_jc, use_container_width=True, hide_index=True, height=400)
        
        # Marcos importantes
        st.markdown("### 🏆 Marcos Importantes")
        
        marcos = [
            ("Dobrar Capital", capital_jc * 2),
            ("5x Capital", capital_jc * 5),
            ("10x Capital", capital_jc * 10),
            ("$10.000", 10000),
            ("$50.000", 50000),
            ("$100.000", 100000),
        ]
        
        cols_marcos = st.columns(3)
        for idx, (nome, valor_alvo) in enumerate(marcos):
            # Calcular meses para atingir
            capital_temp = capital_jc
            meses_para_atingir = 0
            max_meses = 120  # 10 anos máximo
            
            while capital_temp < valor_alvo and meses_para_atingir < max_meses:
                for dia in range(dias_uteis_mes):
                    capital_temp = capital_temp * (1 + taxa_dia/100)
                capital_temp += aporte_mensal
                meses_para_atingir += 1
            
            with cols_marcos[idx % 3]:
                if capital_temp >= valor_alvo and meses_para_atingir < max_meses:
                    anos = meses_para_atingir // 12
                    meses_resto = meses_para_atingir % 12
                    tempo_str = f"{anos}a {meses_resto}m" if anos > 0 else f"{meses_resto} meses"
                    
                    st.markdown(f"""
                    <div class="gold-card" style="text-align: center; margin-bottom: 1rem;">
                        <div style="color: #ffd700; font-weight: bold;">{nome}</div>
                        <div style="font-family: 'Orbitron'; font-size: 1.2rem; color: #fff;">$ {valor_alvo:,.0f}</div>
                        <div style="color: #00ff88;">{tempo_str}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="info-card" style="text-align: center; margin-bottom: 1rem;">
                        <div style="color: #8b8b9a; font-weight: bold;">{nome}</div>
                        <div style="font-family: 'Orbitron'; font-size: 1.2rem; color: #8b8b9a;">$ {valor_alvo:,.0f}</div>
                        <div style="color: #8b8b9a;">+10 anos</div>
                    </div>
                    """, unsafe_allow_html=True)

else:
    # Estado inicial - sem dados
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem;">
        <div style="font-size: 5rem; margin-bottom: 1rem;">🌍</div>
        <h2 style="color: #ffd700; font-family: 'Orbitron';">Bem-vindo ao Forex Command Center</h2>
        <p style="color: #8b8b9a; font-size: 1.1rem; max-width: 600px; margin: 1rem auto;">
            Importe seu relatório do MetaTrader 5 (arquivo .xlsx) usando o menu lateral para começar a análise inteligente do seu trading.
        </p>
        <div style="background: linear-gradient(145deg, #1a1a24, #1f1f2e); border: 1px solid #2a2a3a; 
                    border-radius: 16px; padding: 2rem; max-width: 500px; margin: 2rem auto; text-align: left;">
            <h4 style="color: #ffd700;">📁 Como começar:</h4>
            <ol style="color: #fff; line-height: 2;">
                <li>No MetaTrader 5, vá em <strong>Histórico</strong></li>
                <li>Clique com botão direito → <strong>Relatório</strong></li>
                <li>Salve como <strong>Excel (*.xlsx)</strong></li>
                <li>Importe o arquivo na barra lateral</li>
            </ol>
        </div>
        <div style="margin-top: 2rem;">
            <span style="color: #ffd700;">💡</span>
            <span style="color: #8b8b9a;">Dica: Descubra seu melhor horário, ativo e sessão de trading!</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #8b8b9a; font-family: 'JetBrains Mono'; font-size: 0.8rem;">
    🌍 Forex Command Center v1.0 | Desenvolvido para Traders Profissionais<br>
    <span style="color: #ffd700;">Disciplina • Consistência • Evolução</span>
</div>
""", unsafe_allow_html=True)
