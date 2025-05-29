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
    page_title="SJC Bakery Analytics Suite",
    page_icon="🍞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with bakery-themed color scheme and improved visibility
st.markdown("""
<style>
    .title-banner {
        background: linear-gradient(90deg, #FF8C42 0%, #FFB347 50%, #FFD700 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        border: 3px solid #5D4037;
    }
    .title-text {
        font-size: 2.8rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0.5rem;
    }
    .subtitle-text {
        font-size: 1.3rem;
        font-weight: 500;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    .metric-container {
        background: linear-gradient(90deg, #FFFFFF 0%, #FFF9E6 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF8C42;
        margin: 1rem 0;
        color: #3E2723;
    }
    .insight-box {
        background: #FFFFFF;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #FF8C42;
        margin: 1rem 0;
        color: #3E2723;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    /* Improved dropdown visibility */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #FFF9E6 !important;
        color: #3E2723 !important;
    }
    .stSelectbox div[data-baseweb="select"]:hover > div {
        background-color: #FFE4B5 !important;
    }
    /* Selected item in dropdown */
    .stSelectbox div[data-baseweb="select"] > div > div > div {
        color: #5D4037 !important;
        font-weight: 500;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #5D4037;
        color: #FFFFFF;
        text-align: center;
        padding: 10px 0;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Header with vibrant banner
st.markdown("""
<div class="title-banner">
    <div class="title-text">🍞 SJC Bakery Analytics Suite</div>
    <div class="subtitle-text">Monte Carlo Simulations for Strategic Decisions</div>
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
st.sidebar.title("🎛️ Control Panel")
analysis_type = st.sidebar.radio(
    "Select Analysis Type:",
    ["📈 Demand Forecasting", "💰 Cost Analysis", "👥 Staff Planning", "📚 Help & Guide"]
)

# Demand Forecasting
if analysis_type == "📈 Demand Forecasting":
    st.header("📈 Demand Forecasting")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎯 Parameters")
        
        product_type = st.selectbox(
            "Product Type:",
            ["Croissants", "Sourdough Bread", "Cupcakes", "Cookies", "Bagels"]
        )
        
        avg_demand = st.slider("Average Daily Demand (units):", 50, 300, 150)
        demand_var = st.slider("Demand Variability (%):", 10, 80, 30) / 100
        sim_days = st.slider("Simulation Days:", 7, 90, 30)
        
        if st.button("🚀 Run Demand Simulation", type="primary"):
            # Run simulation
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
            st.success("✅ Simulation completed!")
    
    with col2:
        if st.session_state.demand_data is not None:
            data = st.session_state.demand_data
            
            # Create interactive plot
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=data['days'],
                y=data['demand'],
                mode='lines+markers',
                name=f'{data["product_type"]} Demand',
                line=dict(color='#D2691E', width=3),
                marker=dict(size=6)
            ))
            
            # Add confidence bands
            upper_bound = data['demand'] + data['avg_demand'] * data['demand_var']
            lower_bound = np.maximum(0, data['demand'] - data['avg_demand'] * data['demand_var'])
            
            fig.add_trace(go.Scatter(
                x=np.concatenate([data['days'], data['days'][::-1]]),
                y=np.concatenate([upper_bound, lower_bound[::-1]]),
                fill='toself',
                fillcolor='rgba(210, 105, 30, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Confidence Band',
                hoverinfo="skip"
            ))
            
            # Add reference lines
            fig.add_hline(y=data['avg_demand'], line_dash="dash", line_color="#8B4513",
                         annotation_text=f"Target: {data['avg_demand']}")
            
            p90 = np.percentile(data['demand'], 90)
            fig.add_hline(y=p90, line_dash="dot", line_color="#CD853F",
                         annotation_text=f"90th %: {p90:.0f}")
            
            fig.update_layout(
                title=f'{data["product_type"]} Demand Forecast - {len(data["days"])} Days',
                xaxis_title='Day',
                yaxis_title='Units',
                hovermode='x unified',
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Insights
            cv = np.std(data['demand']) / np.mean(data['demand'])
            trend = np.polyfit(data['days'], data['demand'], 1)[0]
            waste_risk = np.mean(data['demand'] < data['avg_demand'] * 0.7) * 100
            
            st.markdown(f"""
            <div class="insight-box">
            <h4>💡 Key Insights</h4>
            <ul>
            <li><strong>Average Daily Demand:</strong> {np.mean(data['demand']):.0f} units</li>
            <li><strong>Peak Demand (90th %):</strong> {p90:.0f} units</li>
            <li><strong>Demand Variability:</strong> {cv:.2f}</li>
            <li><strong>Daily Trend:</strong> {trend:+.1f} units/day</li>
            <li><strong>Waste Risk:</strong> {waste_risk:.1f}%</li>
            </ul>
            
            <h4>🎯 Recommendations</h4>
            <ul>
            <li><strong>Optimal Production:</strong> {p90:.0f} units/day</li>
            <li><strong>Safety Buffer:</strong> {(p90 - data['avg_demand']):.0f} units</li>
            <li>{'⚠️ High variability - consider demand smoothing' if cv > 0.3 else '✅ Stable demand pattern'}</li>
            <li>{'📈 Increasing trend detected' if trend > 0.5 else '📉 Decreasing trend detected' if trend < -0.5 else '➡️ Stable trend'}</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

# Cost Analysis
elif analysis_type == "💰 Cost Analysis":
    st.header("💰 Cost Analysis")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("💸 Parameters")
        
        ingredient = st.selectbox(
            "Ingredient:",
            ["Flour", "Sugar", "Butter", "Eggs", "Yeast", "Chocolate"]
        )
        
        current_price = st.slider("Current Price (₹/kg):", 50, 500, 150)
        price_volatility = st.slider("Price Volatility (%):", 5, 50, 15) / 100
        forecast_months = st.slider("Forecast Period (months):", 1, 24, 6)
        
        if st.button("🔮 Run Cost Forecast", type="primary"):
            # Run simulation
            np.random.seed(42)
            dt = 1/12
            drift = 0.03
            n_scenarios = 500
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
            st.success("✅ Forecast completed!")
    
    with col2:
        if st.session_state.cost_data is not None:
            data = st.session_state.cost_data
            
            # Create interactive plot
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=data['months'],
                y=data['mean_path'],
                mode='lines+markers',
                name='Expected Price',
                line=dict(color='#B8860B', width=3),
                marker=dict(size=6)
            ))
            
            # Add confidence bands
            fig.add_trace(go.Scatter(
                x=np.concatenate([data['months'], data['months'][::-1]]),
                y=np.concatenate([data['p90_path'], data['p10_path'][::-1]]),
                fill='toself',
                fillcolor='rgba(184, 134, 11, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='90% Confidence Band',
                hoverinfo="skip"
            ))
            
            fig.add_hline(y=data['current_price'], line_dash="dash", line_color="#8B4513",
                         annotation_text=f"Current: ₹{data['current_price']:.0f}/kg")
            
            fig.update_layout(
                title=f'{data["ingredient"]} Price Forecast - {len(data["months"])-1} Months',
                xaxis_title='Month',
                yaxis_title='Price (₹/kg)',
                hovermode='x unified',
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Insights
            final_price = data['mean_path'][-1]
            change_pct = (final_price - data['current_price']) / data['current_price'] * 100
            max_price = np.max(data['p90_path'])
            
            if change_pct > 10:
                strategy = "🔴 BUY NOW - Major increase expected"
                strategy_color = "#A0522D"
            elif change_pct > 5:
                strategy = "🟡 CONSIDER BUYING - Moderate increase likely"
                strategy_color = "#DAA520"
            elif change_pct < -5:
                strategy = "🟢 DELAY PURCHASE - Price decrease expected"
                strategy_color = "#228B22"
            else:
                strategy = "🔵 NEUTRAL - Stable prices"
                strategy_color = "#4682B4"
            
            st.markdown(f"""
            <div class="insight-box">
            <h4>💰 Cost Insights</h4>
            <ul>
            <li><strong>Current Price:</strong> ₹{data['current_price']:.2f}/kg</li>
            <li><strong>Expected Final Price:</strong> ₹{final_price:.2f}/kg</li>
            <li><strong>Projected Change:</strong> {change_pct:+.1f}%</li>
            <li><strong>Maximum Risk:</strong> ₹{max_price:.2f}/kg</li>
            </ul>
            
            <h4 style="color: {strategy_color}">🎯 Strategy: {strategy}</h4>
            
            <h4>💡 Recommendations</h4>
            <ul>
            <li><strong>Budget Buffer:</strong> {np.std(data['mean_path'])/np.mean(data['mean_path'])*100:.1f}%</li>
            <li><strong>Purchase Alert:</strong> ₹{data['current_price']*1.1:.2f}/kg</li>
            <li><strong>Bulk Buy Threshold:</strong> ₹{data['current_price']*0.95:.2f}/kg</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

# Staff Planning
elif analysis_type == "👥 Staff Planning":
    st.header("👥 Staff Planning")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("👥 Parameters")
        
        avg_customers = st.slider("Daily Customers:", 50, 300, 120)
        customer_var = st.slider("Customer Variability (%):", 10, 50, 25) / 100
        service_rate = st.slider("Service Rate (customers/hour/staff):", 5, 15, 8)
        
        if st.button("⚡ Analyze Staffing", type="primary"):
            # Run simulation
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
            st.success("✅ Analysis completed!")
    
    with col2:
        if st.session_state.staff_data is not None:
            data = st.session_state.staff_data
            
            # Create dual-axis plot
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Staff bars
            fig.add_trace(
                go.Bar(x=[f"{h}:00" for h in data['hours']], 
                      y=data['avg_staff'],
                      name='Average Staff',
                      marker_color='#DEB887',
                      opacity=0.7),
                secondary_y=False,
            )
            
            # 90th percentile line
            fig.add_trace(
                go.Scatter(x=[f"{h}:00" for h in data['hours']], 
                          y=data['p90_staff'],
                          mode='lines+markers',
                          name='90th Percentile',
                          line=dict(color='#A0522D', width=3),
                          marker=dict(size=8)),
                secondary_y=False,
            )
            
            # Customer flow
            fig.add_trace(
                go.Scatter(x=[f"{h}:00" for h in data['hours']], 
                          y=data['hourly_customers'],
                          mode='lines',
                          name='Customer Flow',
                          line=dict(color='#D2691E', width=2, dash='dot'),
                          opacity=0.7),
                secondary_y=True,
            )
            
            fig.update_xaxes(title_text="Hour")
            fig.update_yaxes(title_text="Staff Required", secondary_y=False)
            fig.update_yaxes(title_text="Customers per Hour", secondary_y=True)
            
            fig.update_layout(
                title='Optimal Staffing Schedule',
                hovermode='x unified',
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Insights
            peak_hour = data['hours'][np.argmax(data['avg_staff'])]
            peak_staff = int(np.max(data['avg_staff']))
            min_staff = int(np.min(data['avg_staff']))
            total_hours = np.sum(data['avg_staff'])
            daily_cost = total_hours * 200
            
            st.markdown(f"""
            <div class="insight-box">
            <h4>👥 Staffing Insights</h4>
            <ul>
            <li><strong>Peak Hour:</strong> {peak_hour}:00 ({peak_staff} staff)</li>
            <li><strong>Minimum Staff:</strong> {min_staff} members</li>
            <li><strong>Total Daily Hours:</strong> {total_hours:.1f}</li>
            <li><strong>Daily Labor Cost:</strong> ₹{daily_cost:.0f}</li>
            </ul>
            
            <h4>💡 Recommendations</h4>
            <ul>
            <li><strong>Core Staff:</strong> {min_staff} members (all day)</li>
            <li><strong>Peak Boost:</strong> +{peak_staff - min_staff} members ({peak_hour-1}-{peak_hour+1}:00)</li>
            <li><strong>Weekend Staff:</strong> +{int(peak_staff*0.3)} members</li>
            <li><strong>Monthly Budget:</strong> ₹{daily_cost*30:.0f}</li>
            </ul>
            
            <h4>🎯 Optimization Tips</h4>
            <ul>
            <li>Consider part-time staff for peaks</li>
            <li>Cross-train for flexibility</li>
            <li>Monitor actual patterns weekly</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

# Help & Guide
else:
    st.header("📚 User Guide")
    
    st.markdown("""
    ## 🔬 Monte Carlo Simulation for Bakeries
    
    This analytics suite uses statistical modeling for data-driven bakery decisions.
    
    ### 📈 Demand Forecasting
    - **Purpose**: Predicts daily sales with realistic variability
    - **Benefits**: Models customer behavior and seasonal patterns
    - **Output**: Provides conservative estimates for production planning
    
    ### 💰 Cost Analysis
    - **Purpose**: Forecasts ingredient prices using advanced modeling
    - **Benefits**: Optimizes purchasing timing and strategies
    - **Output**: Provides inflation-adjusted projections
    
    ### 👥 Staff Planning
    - **Purpose**: Models customer arrival patterns by hour
    - **Benefits**: Calculates optimal staffing levels
    - **Output**: Balances service quality with labor costs
    
    ## 🎯 How to Use
    1. **Select Analysis Type** from the sidebar
    2. **Adjust Parameters** using the sliders and dropdowns
    3. **Click the Simulation Button** to generate forecasts
    4. **Review Charts and Insights** for decision making
    5. **Use 90th Percentile Values** for conservative planning
    
    ## 💡 Key Tips
    - Run simulations weekly for best results
    - Compare scenarios by adjusting parameters
    - Monitor actual vs predicted performance
    - Consider external factors not in the model
    
    ## 🚀 Advanced Features
    - Interactive charts with hover details
    - Downloadable results (coming soon)
    - Historical data integration (coming soon)
    - Multi-location analysis (coming soon)
    """)
    
    st.info("💡 **Pro Tip**: Start with the Demand Forecasting to understand your base requirements, then use Cost Analysis for purchasing decisions, and finally optimize with Staff Planning.")

# Footer
st.markdown("""
<div class="footer">
    Web Application |  Developed with 🧡 by J. Inigo Papu Vinodhan, Asst. Prof., BBA Dept., St. Joseph's College, Trichy
</div>
""", unsafe_allow_html=True)
