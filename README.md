# 🌍 Forex Command Center

Sistema inteligente de gerenciamento de operações para traders de Forex e Commodities.

## ✨ Funcionalidades

### 📊 Dashboard Principal
- **Capital Atual**: Acompanhamento em tempo real do saldo em USD
- **Resultado do Dia**: Progresso em relação à meta diária
- **Win Rate**: Taxa de acerto das operações
- **Payoff**: Relação média entre ganhos e perdas
- **Fator de Lucro**: Relação entre lucro bruto e perda bruta
- **Drawdown**: Máxima perda acumulada

### 💹 Análise por Ativo
- Performance individual de cada par (XAUUSD, USDJPY, etc.)
- Identificação do melhor e pior ativo
- Volume operado por instrumento
- Win rate específico de cada ativo

### 🌍 Análise por Sessão
- Performance na sessão Asiática (00:00-08:00 UTC)
- Performance na sessão de Londres (08:00-13:00 UTC)
- Performance na sessão de Nova York (13:00-21:00 UTC)
- Identificação da sua melhor sessão

### ⏰ Análise por Horário
- Gráfico de resultados por hora do dia
- Identificação dos melhores e piores horários
- Win rate por período

### 📅 Análise por Dia da Semana
- Performance em cada dia da semana
- Identificação de dias a evitar

### 📈 Evolução do Capital
- Gráfico de crescimento ao longo do tempo
- Visualização de cada operação
- Identificação de padrões

### 🧠 Insights Inteligentes
- Recomendações automáticas baseadas nos dados
- Alertas sobre swap, drawdown e custos
- Sugestões para melhorar a consistência

## 🚀 Como Usar

### Instalação

```bash
# Clone ou baixe os arquivos
cd forex_dashboard

# Instale as dependências
pip install -r requirements.txt

# Execute o dashboard
streamlit run app.py
```

### Exportando do MetaTrader 5

1. Abra o MetaTrader 5
2. Vá até a aba **Histórico** (History)
3. Selecione o período desejado
4. Clique com botão direito → **Relatório** (Report)
5. Escolha **Excel (*.xlsx)**
6. Salve o arquivo
7. Importe no dashboard

### Primeiro Uso

1. **Importe seu arquivo Excel**: Use o botão na barra lateral
2. **Configure o Capital**: Informe o capital inicial da conta
3. **Defina a Meta**: Ajuste sua meta diária (padrão 2%)
4. **Explore**: Navegue pelas abas para ver todas as análises

## 📊 Métricas Calculadas

| Métrica | Descrição |
|---------|-----------|
| Win Rate | (Gains / Total) × 100 |
| Payoff | Média Ganhos / Média Perdas |
| Fator de Lucro | Soma Ganhos / Soma Perdas |
| Drawdown | Máxima queda do pico |
| Expectativa | (P(gain) × Média) - (P(loss) × Média) |

## 🌐 Sessões de Trading

| Sessão | Horário (UTC) | Características |
|--------|---------------|-----------------|
| Ásia | 00:00 - 08:00 | Menor volatilidade, bom para ranges |
| Londres | 08:00 - 13:00 | Alta volatilidade, breakouts |
| Nova York | 13:00 - 21:00 | Overlap com Londres, alta liquidez |

## 🎨 Interface

O dashboard utiliza um tema dark profissional com:
- Dourado para XAUUSD (Ouro)
- Verde para gains
- Vermelho para losses
- Azul para informações neutras

## 💡 Dicas de Uso

1. **Atualize semanalmente**: Exporte o histórico regularmente
2. **Observe os padrões**: Use as análises de sessão e horário
3. **Gerencie o risco**: Monitore o drawdown constantemente
4. **Evite custos**: Observe o impacto do swap nas operações overnight

## 📋 Ativos Suportados

- **Forex**: EURUSD, GBPUSD, USDJPY, etc.
- **Metais**: XAUUSD (Ouro), XAGUSD (Prata)
- **Commodities**: WTI, Brent
- **Índices**: US30, NAS100, etc.
- **Crypto**: BTCUSD, ETHUSD (se disponível)

---

**Desenvolvido para traders que buscam consistência e evolução.**

*Disciplina • Consistência • Evolução*
