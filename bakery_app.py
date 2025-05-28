import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="🥖 Artisan Bakery Analytics",
    page_icon="🥖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS with warm bakery theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global variables */
    :root {
        --primary-color: #D2691E;
        --primary-dark: #A0522D;
        --primary-light: #F4A460;
        --secondary-color: #8B4513;
        --accent-color: #FF6B35;
        --success-color: #2ECC71;
        --warning-color: #F39C12;
        --danger-color: #E74C3C;
        --background-primary: #FEFEFE;
        --background-secondary: #F8F6F3;
        --background-card: #FFFFFF;
        --text-primary: #2C3E50;
        --text-secondary: #7F8C8D;
        --text-light: #95A5A6;
        --border-color: #E8E8E8;
        --shadow-light: 0 2px 8px rgba(0,0,0,0.06);
        --shadow-medium: 0 4px 16px rgba(0,0,0,0.1);
        --shadow-heavy: 0 8px 32px rgba(0,0,0,0.15);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
    }
    
    /* Base styling */
    .stApp {
        background: linear-gradient(135deg, var(--background-primary) 0%, var(--background-secondary) 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
    }
    
    /* Remove default Streamlit padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: var(--radius-lg);
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-medium);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
        opacity: 0.3;
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 2;
    }
    
    .main-header p {
        font-size: 1.2rem;
        font-weight: 400;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        position: relative;
        z-index: 2;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: var(--background-card);
        border-right: 1px solid var(--border-color);
    }
    
    .sidebar .sidebar-content {
        background: var(--background-card);
    }
    
    /* Card containers */
    .metric-card {
        background: var(--background-card);
        padding: 1.5rem;
        border-radius: var(--radius-md);
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-light);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: var(--shadow-medium);
        transform: translateY(-2px);
    }
    
    /* Insight boxes */
    .insight-box {
        background: linear-gradient(135deg, var(--background-card) 0%, #FFF9F5 100%);
        padding: 2rem;
        border-radius: var(--radius-lg);
        border: 1px solid var(--border-color);
        border-left: 4px solid var(--primary-color);
        box-shadow: var(--shadow-light);
        margin: 1.5rem 0;
        color: var(--text-primary);
    }
    
    .insight-box h4 {
        color: var(--primary-dark);
        margin: 0 0 1rem 0;
        font-weight: 600;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .insight-box ul {
        color: var(--text-secondary);
        line-height: 1.7;
        margin: 0;
        padding-left: 1.2rem;
    }
    
    .insight-box li {
        margin-bottom: 0.6rem;
        position: relative;
    }
    
    .insight-box li::marker {
        color: var(--primary-color);
    }
    
    .insight-box strong {
        color: var(--text-primary);
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: white;
        border: none;
        border-radius: var(--radius-sm);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-light);
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--secondary-color) 100%);
        transform: translateY(-1px);
        box-shadow: var(--shadow-medium);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Radio button styling */
    .stRadio > div {
        background: var(--background-card);
        border-radius: var(--radius-sm);
        padding: 1rem;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-light);
    }
    
    .stRadio > div > label {
        color: var(--text-primary);
        font-weight: 500;
        padding: 0.5rem 0;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: var(--primary-color);
    }
    
    .stSlider > div > div > div[data-baseweb="slider"] > div > div:first-child {
        background: var(--primary-light);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: var(--background-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-sm);
    }
    
    /* Success/Info message styling */
    .stSuccess {
        background: linear-gradient(135deg, #D5EDDA 0%, #C3E6CB 100%);
        color: var(--success-color);
        border: 1px solid #C3E6CB;
        border-radius: var(--radius-sm);
        font-weight: 500;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #CCE5FF 0%, #B8DAFF 100%);
        color: #004085;
        border: 1px solid #B8DAFF;
        border-radius: var(--radius-sm);
        font-weight: 500;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--background-card);
        border-radius: var(--radius-sm);
        border: 1px solid var(--border-color);
        padding: 0.25rem;
        gap: 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--text-secondary);
        font-weight: 500;
        border-radius: var(--radius-sm);
        padding: 0.75rem 1rem;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-color);
        color: white;
        font-weight: 600;
    }
    
    /* Chart containers */
    .plot-container {
        background: var(--background-card);
        border-radius: var(--radius-md);
        padding: 1rem;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-light);
        margin: 1rem 0;
    }
    
    /* Section headers */
    .section-header {
        color: var(--primary-dark);
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--primary-light);
    }
    
    .subsection-header {
        color: var(--text-primary);
        font-size: 1.2rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Strategy indicators */
    .strategy-buy {
        background: linear-gradient(135deg, #FFE5E5 0%, #FFCCCC 100%);
        border-left: 4px solid var(--danger-color);
        color: var(--danger-color);
    }
    
    .strategy-consider {
        background: linear-gradient(135deg, #FFF3CD 0%, #FFEAA7 100%);
        border-left: 4px solid var(--warning-color);
        color: #B7791F;
    }
    
    .strategy-delay {
        background: linear-gradient(135deg, #D1ECF1 0%, #BEE5EB 100%);
        border-left: 4px solid var(--success-color);
        color: #0C5460;
    }
    
    .strategy-neutral {
        background: linear-gradient(135deg, #E2E3E5 0%, #D6D8DB 100%);
        border-left: 4px solid #6C757D;
        color: #495057;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--background-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-light);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-color);
    }
    
    /* Animation for loading states */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .insight-box {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🥖 Artisan Bakery Analytics</h1>
    <p>Advanced Monte Carlo Simulations for Strategic Decision Making</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'demand_data' not in st.session_state:
    st.session_state.demand_data = None
if 'cost_data' not in st.session_state:
    st.session_state.cost_data = None
if 'staff_data' not in st.session_state:
    st.session_state.staff_data = None

# Sidebar
st.sidebar.markdown("### 🎛️ Control Panel")
analysis_type = st.sidebar.radio(
    "**Select Analysis Module:**",
    ["📈 Demand Forecasting", "💰 Cost Analysis", "👥 Staff Planning", "📚 Help & Guide"],
    index=0
)

# Color scheme for charts
CHART_COLORS = {
    'primary': '#D2691E',
    'secondary': '#8B4513',
    'accent': '#FF6B35',
    'success': '#2ECC71',
    'warning': '#F39C12',
    'info': '#3498DB',
    'danger': '#E74C3C'
}

# Demand Forecasting
if analysis_type == "📈 Demand Forecasting":
    st.markdown('<h2 class="section-header">📈 Demand Forecasting</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.markdown('<h3 class="subsection-header">🎯 Configuration</h3>', unsafe_allow_html=True)
        
        with st.container():
            product_type = st.selectbox(
                "**Product Category:**",
                ["🥐 Croissants", "🍞 Sourdough Bread", "🧁 Cupcakes", "🍪 Cookies", "🥯 Bagels"],
                index=0
            )
            
            avg_demand = st.slider("**Average Daily Demand (units):**", 50, 300, 150, step=10)
            demand_var = st.slider("**Demand Variability (%):**", 10, 80, 30, step=5) / 100
            sim_days = st.slider("**Simulation Period (days):**", 7, 90, 30, step=1)
            
            st.markdown("---")
            
            if st.button("🚀 **Run Demand Simulation**", type="primary"):
                # Run simulation with progress
                with st.spinner("Running Monte Carlo simulation..."):
                    np.random.seed(42)
                    base_demand = np.random.normal(avg_demand, avg_demand * demand_var, sim_days)
                    day_effects = 1 + 0.3 * np.sin(np.arange(sim_days) * 2 * np.pi / 7)
                    seasonal_trend = 1 + 0.1 * np.sin(np.arange(sim_days) * 2 * np.pi / 30)
                    demand = np.maximum(0, base_demand * day_effects * seasonal_trend)
                    
                    st.session_state.demand_data = {
                        'days': np.arange(1, sim_days + 1),
                        'demand': demand,
                        'avg_demand': avg_demand,
                        'product_type': product_type,
                        'demand_var': demand_var
                    }
                st.success("✅ **Simulation completed successfully!**")
    
    with col2:
        if st.session_state.demand_data is not None:
            data = st.session_state.demand_data
            
            # Create enhanced interactive plot
            fig = go.Figure()
            
            # Main demand line
            fig.add_trace(go.Scatter(
                x=data['days'],
                y=data['demand'],
                mode='lines+markers',
                name=f'{data["product_type"]} Demand',
                line=dict(color=CHART_COLORS['primary'], width=3),
                marker=dict(size=6, color=CHART_COLORS['primary'])
            ))
            
            # Confidence bands
            upper_bound = data['demand'] + data['avg_demand'] * data['demand_var']
            lower_bound = np.maximum(0, data['demand'] - data['avg_demand'] * data['demand_var'])
            
            fig.add_trace(go.Scatter(
                x=np.concatenate([data['days'], data['days'][::-1]]),
                y=np.concatenate([upper_bound, lower_bound[::-1]]),
                fill='toself',
                fillcolor=f"rgba(210, 105, 30, 0.15)",
                line=dict(color='rgba(255,255,255,0)'),
                name='Confidence Band',
                hoverinfo="skip"
            ))
            
            # Reference lines
            fig.add_hline(y=data['avg_demand'], line_dash="dash", line_color=CHART_COLORS['info'],
                         annotation_text=f"Target: {data['avg_demand']} units")
            
            p90 = np.percentile(data['demand'], 90)
            fig.add_hline(y=p90, line_dash="dot", line_color=CHART_COLORS['warning'],
                         annotation_text=f"90th Percentile: {p90:.0f} units")
            
            fig.update_layout(
                title=dict(
                    text=f'{data["product_type"]} Demand Forecast - {len(data["days"])} Days',
                    font=dict(size=16, color=CHART_COLORS['primary'])
                ),
                xaxis_title='Day',
                yaxis_title='Units Demanded',
                hovermode='x unified',
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#2C3E50'),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            fig.update_xaxes(gridcolor='rgba(0,0,0,0.1)')
            fig.update_yaxes(gridcolor='rgba(0,0,0,0.1)')
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Enhanced insights
            cv = np.std(data['demand']) / np.mean(data['demand'])
            trend = np.polyfit(data['days'], data['demand'], 1)[0]
            waste_risk = np.mean(data['demand'] < data['avg_demand'] * 0.7) * 100
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>💡 Key Performance Metrics</h4>
                <ul>
                    <li><strong>Average Daily Demand:</strong> {np.mean(data['demand']):.0f} units</li>
                    <li><strong>Peak Demand (90th %):</strong> {p90:.0f} units</li>
                    <li><strong>Demand Variability (CV):</strong> {cv:.2f}</li>
                    <li><strong>Daily Trend:</strong> {trend:+.1f} units/day</li>
                    <li><strong>Waste Risk Probability:</strong> {waste_risk:.1f}%</li>
                </ul>
                
                <h4>🎯 Strategic Recommendations</h4>
                <ul>
                    <li><strong>Optimal Daily Production:</strong> {p90:.0f} units</li>
                    <li><strong>Safety Buffer Required:</strong> {(p90 - data['avg_demand']):.0f} units</li>
                    <li><strong>Inventory Strategy:</strong> {'🔴 High variability - implement flexible production' if cv > 0.3 else '✅ Stable demand - maintain consistent production'}</li>
                    <li><strong>Market Trend:</strong> {'📈 Growing demand detected - consider capacity expansion' if trend > 0.5 else '📉 Declining demand - optimize costs' if trend < -0.5 else '➡️ Stable market conditions'}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# Cost Analysis
elif analysis_type == "💰 Cost Analysis":
    st.markdown('<h2 class="section-header">💰 Cost Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.markdown('<h3 class="subsection-header">💸 Parameters</h3>', unsafe_allow_html=True)
        
        ingredient = st.selectbox(
            "**Ingredient Category:**",
            ["🌾 Premium Flour", "🍯 Organic Sugar", "🧈 European Butter", "🥚 Farm Eggs", "🍄 Active Yeast", "🍫 Belgian Chocolate"],
            index=0
        )
        
        current_price = st.slider("**Current Price (₹/kg):**", 50, 500, 150, step=10)
        price_volatility = st.slider("**Price Volatility (%):**", 5, 50, 15, step=5) / 100
        forecast_months = st.slider("**Forecast Horizon (months):**", 1, 24, 6, step=1)
        
        st.markdown("---")
        
        if st.button("🔮 **Generate Cost Forecast**", type="primary"):
            with st.spinner("Modeling price dynamics..."):
                # Enhanced simulation
                np.random.seed(42)
                dt = 1/12
                drift = 0.03
                n_scenarios = 1000
                price_paths = []
                
                for _ in range(n_scenarios):
                    prices = [current_price]
                    for _ in range(forecast_months):
                        shock = np.random.normal(0, price_volatility)
                        new_price = prices[-1] * np.exp((drift - 0.5 * price_volatility**2) * dt + 
                                                       price_volatility * np.sqrt(dt) * shock)
                        prices.append(max(new_price, current_price * 0.5))
                    price_paths.append(prices)
                
                price_paths = np.array(price_paths)
                mean_path = np.mean(price_paths, axis=0)
                p10_path = np.percentile(price_paths, 10, axis=0)
                p90_path = np.percentile(price_paths, 90, axis=0)
                
                st.session_state.cost_data = {
                    'months': np.arange(len(mean_path)),
                    'mean_path': mean_path,
                    'p10_path': p10_path,
                    'p90_path': p90_path,
                    'current_price': current_price,
                    'ingredient': ingredient
                }
            st.success("✅ **Forecast generated successfully!**")
    
    with col2:
        if st.session_state.cost_data is not None:
            data = st.session_state.cost_data
            
            # Enhanced price forecast chart
            fig = go.Figure()
            
            # Mean price line
            fig.add_trace(go.Scatter(
                x=data['months'],
                y=data['mean_path'],
                mode='lines+markers',
                name='Expected Price',
                line=dict(color=CHART_COLORS['danger'], width=3),
                marker=dict(size=6)
            ))
            
            # Confidence bands
            fig.add_trace(go.Scatter(
                x=np.concatenate([data['months'], data['months'][::-1]]),
                y=np.concatenate([data['p90_path'], data['p10_path'][::-1]]),
                fill='toself',
                fillcolor=f"rgba(231, 76, 60, 0.15)",
                line=dict(color='rgba(255,255,255,0)'),
                name='80% Confidence Band',
                hoverinfo="skip"
            ))
            
            fig.add_hline(y=data['current_price'], line_dash="dash", line_color=CHART_COLORS['info'],
                         annotation_text=f"Current: ₹{data['current_price']:.0f}/kg")
            
            fig.update_layout(
                title=dict(
                    text=f'{data["ingredient"]} Price Forecast - {len(data["months"])-1} Months',
                    font=dict(size=16, color=CHART_COLORS['primary'])
                ),
                xaxis_title='Month',
                yaxis_title='Price (₹/kg)',
                hovermode='x unified',
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#2C3E50')
            )
            
            fig.update_xaxes(gridcolor='rgba(0,0,0,0.1)')
            fig.update_yaxes(gridcolor='rgba(0,0,0,0.1)')
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Enhanced insights with strategy
            final_price = data['mean_path'][-1]
            change_pct = (final_price - data['current_price']) / data['current_price'] * 100
            max_price = np.max(data['p90_path'])
            
            if change_pct > 10:
                strategy = "🔴 URGENT BUY - Major price increase expected"
                strategy_class = "strategy-buy"
            elif change_pct > 5:
                strategy = "🟡 CONSIDER BUYING - Moderate increase likely"
                strategy_class = "strategy-consider"
            elif change_pct < -5:
                strategy = "🟢 DELAY PURCHASE - Price decrease expected"
                strategy_class = "strategy-delay"
            else:
                strategy = "🔵 NEUTRAL STANCE - Stable pricing"
                strategy_class = "strategy-neutral"
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>💰 Financial Analysis</h4>
                <ul>
                    <li><strong>Current Price:</strong> ₹{data['current_price']:.2f}/kg</li>
                    <li><strong>Expected Final Price:</strong> ₹{final_price:.2f}/kg</li>
                    <li><strong>Projected Change:</strong> {change_pct:+.1f}%</li>
                    <li><strong>Maximum Risk Price:</strong> ₹{max_price:.2f}/kg</li>
                    <li><strong>Price Volatility:</strong> {np.std(data['mean_path'])/np.mean(data['mean_path'])*100:.1f}%</li>
                </ul>
            </div>
            
            <div class="insight-box {strategy_class}">
                <h4>🎯 Procurement Strategy</h4>
                <p><strong>{strategy}</strong></p>
            </div>
            
            <div class="insight-box">
                <h4>💡 Action Items</h4>
                <ul>
                    <li><strong>Budget Buffer:</strong> {np.std(data['mean_path'])/np.mean(data['mean_path'])*100:.1f}% additional allocation</li>
                    <li><strong>Price Alert Threshold:</strong> ₹{data['current_price']*1.1:.2f}/kg</li>
                    <li><strong>Bulk Purchase Trigger:</strong> ₹{data['current_price']*0.95:.2f}/kg</li>
                    <li><strong>Contract Negotiation:</strong> Lock rates if price > ₹{data['current_price']*1.05:.2f}/kg</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# Staff Planning
elif analysis_type == "👥 Staff Planning":
    st.markdown('<h2 class="section-header">👥 Staff Planning</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.markdown('<h3 class="subsection-header">👥 Workforce Parameters</h3>', unsafe_allow_html=True)
        
        avg_customers = st.slider("**Daily Customer Count:**", 50, 300, 120, step=10)
        customer_var = st.slider("**Customer Flow Variability (%):**", 10, 50, 25, step=5) / 100
        service_rate = st.slider("**Service Rate (customers/hour/staff):**", 5, 15, 8, step=1)
        
        st.markdown("---")
        
        if st.button("⚡ **Optimize Staffing**", type="primary"):
            with st.spinner("Analyzing customer patterns..."):
                # Enhanced simulation
                hours = np.arange(8, 20)
                base_pattern = np.array([0.4, 0.6, 0.8, 1.0, 1.4, 1.8, 1.6, 1.2, 0.9, 0.7, 0.8, 1.1])
                hourly_customers = avg_customers * base_pattern / np.sum(base_pattern)
                
                np.random.seed(42)
                n_days = 30
                daily_patterns = []
                
                for day in range(n_days):
                    day_multiplier = 1.3 if day % 7 in [5, 6] else 1.0
                    adjusted_customers = hourly_customers * day_multiplier
                    actual_customers = np.maximum(0, np.random.normal(adjusted_customers, 
                                                                     adjusted_customers * customer_var))
                    daily_patterns.append(actual_customers)
                
                daily_patterns = np.array(daily_patterns)
                staff_needed = np.ceil(daily_patterns / service_rate)
                avg_staff = np.mean(staff_needed, axis=0)
                p90_staff = np.percentile(staff_needed, 90, axis=0)
                
                st.session_state.staff_data = {
                    'hours': hours,
                    'avg_staff': avg_staff,
                    'p90_staff': p90_staff,
                    'hourly_customers': np.mean(daily_patterns, axis=0),
                    'service_rate': service_rate
                }
            st.success("✅ **Staffing analysis completed!**")
    
    with col2:
        if st.session_state.staff_data is not None:
            data = st.session_state.staff_data
            
            # Enhanced dual-axis staffing chart
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Staff bars
            fig.add_trace(
                go.Bar(x=[f"{h}:00" for h in data['hours']], 
                      y=data['avg_staff'],
                      name='Average Staff Required',
                      marker_color=CHART_COLORS['secondary'],
                      opacity=0.8),
                secondary_y=False,
            )
            
            # 90th percentile line
            fig.add_trace(
                go.Scatter(x=[f"{h}:00" for h in data['hours']], 
                          y=data['p90_staff'],
                          mode='lines+markers',
                          name='Peak Staffing (90th %)',
                          line=dict(color=CHART_COLORS['danger'], width=3),
                          marker=dict(size=8)),
                secondary_y=False,
            )
            
            # Customer flow
            fig.add_trace(
                go.Scatter(x=[f"{h}:00" for h in data['hours']], 
                          y=data['hourly_customers'],
                          mode='lines+markers',
                          name='Customer Flow',
                          line=dict(color=CHART_COLORS['info'], width=2, dash='dot'),
                          marker=dict(size=6),
                          opacity=0.8),
                secondary_y=True,
            )
            
            fig.update_xaxes(title_text="Operating Hours")
            fig.update_yaxes(title_text="Staff Members Required", secondary_y=False)
            fig.update_yaxes(title_text="Customers per Hour", secondary_y=True)
            
            fig.update_layout(
                title=dict(
                    text='Optimal Staffing Schedule Analysis',
                    font=dict(size=16, color=CHART_COLORS['primary'])
                ),
                hovermode='x unified',
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#2C3E50')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Enhanced staffing insights
            peak_hour = data['hours'][np.argmax(data['avg_staff'])]
            peak_staff = int(np.max(data['avg_staff']))
            min_staff = int(np.min(data['avg_staff']))
            total_hours = np.sum(data['avg_staff'])
            daily_cost = total_hours * 200
            
            st.markdown(f"""
            <div class="insight-box">
                <h4>👥 Workforce Analytics</h4>
                <ul>
                    <li><strong>Peak Operating Hour:</strong> {peak_hour}:00 ({peak_staff} staff members)</li>
                    <li><strong>Minimum Staffing:</strong> {min_staff} members required</li>
                    <li><strong>Total Daily Staff Hours:</strong> {total_hours:.1f} hours</li>
                    <li><strong>Daily Labor Investment:</strong> ₹{daily_cost:.0f}</li>
                    <li><strong>Service Efficiency:</strong> {data['service_rate']} customers/hour/staff</li>
                </ul>
                
                <h4>💡 Staffing Strategy</h4>
                <ul>
                    <li><strong>Core Team:</strong> {min_staff} full-time members (8:00-20:00)</li>
                    <li><strong>Peak Support:</strong> +{peak_staff - min_staff} part-time members ({peak_hour-1}:00-{peak_hour+2}:00)</li>
                    <li><strong>Weekend Boost:</strong> +{int(peak_staff*0.3)} additional members</li>
                    <li><strong>Monthly Budget:</strong> ₹{daily_cost*30:.0f} (30 days)</li>
                </ul>
                
                <h4>🎯 Optimization Opportunities</h4>
                <ul>
                    <li><strong>Flexible Scheduling:</strong> Implement split shifts during peaks</li>
                    <li><strong>Cross-Training:</strong> Multi-skill staff for operational flexibility</li>
                    <li><strong>Performance Monitoring:</strong> Track actual vs predicted patterns weekly</li>
                    <li><strong>Technology Integration:</strong> Consider queue management systems</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# Help & Guide
else:
    st.markdown('<h2 class="section-header">📚 User Guide & Documentation</h2>', unsafe_allow_html=True)
    
    # Create tabs for better organization
    tab1, tab2, tab3, tab4 = st.tabs(["🔬 **Overview**", "📊 **Features**", "🎯 **Best Practices**", "🚀 **Advanced Tips**"])
    
    with tab1:
        st.markdown("""
        <div class="insight-box">
            <h4>🔬 Monte Carlo Simulation for Bakery Operations</h4>
            <p>This advanced analytics suite leverages statistical modeling and Monte Carlo simulations to provide data-driven insights for bakery management decisions.</p>
            
            <h4>🎯 Core Methodology</h4>
            <ul>
                <li><strong>Probabilistic Modeling:</strong> Accounts for real-world variability and uncertainty</li>
                <li><strong>Historical Pattern Recognition:</strong> Incorporates seasonal and cyclical trends</li>
                <li><strong>Risk Assessment:</strong> Quantifies operational and financial risks</li>
                <li><strong>Scenario Planning:</strong> Enables what-if analysis for strategic planning</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="insight-box">
            <h4>📈 Demand Forecasting Module</h4>
            <ul>
                <li><strong>Purpose:</strong> Predicts daily sales with realistic variability modeling</li>
                <li><strong>Benefits:</strong> Optimizes production planning and inventory management</li>
                <li><strong>Output:</strong> Conservative estimates with confidence intervals</li>
                <li><strong>Key Metrics:</strong> Peak demand, waste risk, trend analysis</li>
            </ul>
        </div>
        
        <div class="insight-box">
            <h4>💰 Cost Analysis Module</h4>
            <ul>
                <li><strong>Purpose:</strong> Forecasts ingredient prices using stochastic modeling</li>
                <li><strong>Benefits:</strong> Optimizes procurement timing and budget allocation</li>
                <li><strong>Output:</strong> Price trajectories with confidence bands</li>
                <li><strong>Key Metrics:</strong> Expected price, volatility, procurement strategy</li>
            </ul>
        </div>
        
        <div class="insight-box">
            <h4>👥 Staff Planning Module</h4>
            <ul>
                <li><strong>Purpose:</strong> Models customer arrival patterns by operational hour</li>
                <li><strong>Benefits:</strong> Balances service quality with labor cost optimization</li>
                <li><strong>Output:</strong> Optimal staffing schedules with peak analysis</li>
                <li><strong>Key Metrics:</strong> Service efficiency, labor cost, peak requirements</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div class="insight-box">
            <h4>🎯 Implementation Guidelines</h4>
            <ol>
                <li><strong>Weekly Simulation Runs:</strong> Update forecasts regularly for accuracy</li>
                <li><strong>Parameter Calibration:</strong> Adjust based on actual vs predicted performance</li>
                <li><strong>Scenario Comparison:</strong> Test multiple parameter combinations</li>
                <li><strong>90th Percentile Planning:</strong> Use conservative estimates for safety margins</li>
                <li><strong>Trend Monitoring:</strong> Track long-term patterns for strategic planning</li>
            </ol>
        </div>
        
        <div class="insight-box">
            <h4>💡 Decision Framework</h4>
            <ul>
                <li><strong>Green Zone:</strong> Actual performance within confidence bands</li>
                <li><strong>Yellow Zone:</strong> Performance outside bands but within 10%</li>
                <li><strong>Red Zone:</strong> Significant deviation requiring parameter adjustment</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("""
        <div class="insight-box">
            <h4>🚀 Advanced Optimization Techniques</h4>
            <ul>
                <li><strong>Multi-Product Portfolio:</strong> Run simulations for product mix optimization</li>
                <li><strong>Seasonal Adjustments:</strong> Incorporate holiday and event impacts</li>
                <li><strong>Competitive Analysis:</strong> Model market share fluctuations</li>
                <li><strong>Supply Chain Integration:</strong> Link cost and demand forecasts</li>
            </ul>
        </div>
        
        <div class="insight-box">
            <h4>📊 Performance Metrics</h4>
            <ul>
                <li><strong>Forecast Accuracy:</strong> MAPE < 15% for demand predictions</li>
                <li><strong>Cost Variance:</strong> Budget variance < 10% for procurement</li>
                <li><strong>Service Level:</strong> >95% customer satisfaction during peak hours</li>
                <li><strong>Waste Reduction:</strong> <5% product waste through optimized production</li>
            </ul>
        </div>
        
        <div class="insight-box">
            <h4>🔮 Future Enhancements</h4>
            <ul>
                <li><strong>Machine Learning Integration:</strong> Adaptive parameter learning</li>
                <li><strong>Real-time Data Feeds:</strong> Live market price integration</li>
                <li><strong>Multi-location Analysis:</strong> Franchise network optimization</li>
                <li><strong>Customer Segmentation:</strong> Demographic-based demand modeling</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Info banner
st.info("💡 **Pro Tip:** Start with Demand Forecasting to establish baseline requirements, then optimize with Cost Analysis for procurement strategies, and finally balance with Staff Planning for operational efficiency.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7F8C8D; font-size: 0.9rem; padding: 1rem;">
    <strong>🥖 Artisan Bakery Analytics Suite</strong><br>
    Developed by J. Inigo Papu Vinodhan, St. Joseph's College, Trichy<br>
    Powered by Advanced Monte Carlo Simulations & Modern UI Design
</div>
""", unsafe_allow_html=True)
