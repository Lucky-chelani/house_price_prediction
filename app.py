import streamlit as st
import joblib
import numpy as np
import plotly.express as px
import pandas as pd

# Page configuration - Mobile optimized
st.set_page_config(
    page_title="🏠 House Price AI",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Mobile-first responsive CSS
st.markdown("""
<style>
    /* Reset and base styles */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    /* Header styles */
    .mobile-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 1rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .mobile-header h1 {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .mobile-header p {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    /* Input container */
    .input-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border: 1px solid #e0e0e0;
    }
    
    .input-section {
        margin-bottom: 1.5rem;
    }
    
    .input-section h3 {
        color: #333;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
    
    /* Summary cards - mobile stack */
    .summary-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.8rem;
        margin-bottom: 1.5rem;
    }
    
    .summary-card {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .summary-card h4 {
        font-size: 0.8rem;
        margin-bottom: 0.3rem;
        opacity: 0.9;
    }
    
    .summary-card h2 {
        font-size: 1.4rem;
        margin: 0;
        font-weight: 700;
    }
    
    /* Button styles - mobile optimized */
    .stButton > button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 700;
        width: 100%;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.6);
    }
    
    /* Prediction result */
    .prediction-result {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        animation: slideUp 0.5s ease-out;
    }
    
    .prediction-result h2 {
        font-size: 1.3rem;
        margin-bottom: 0.5rem;
    }
    
    .prediction-result .price {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0.5rem 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .prediction-result p {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Analysis cards - mobile grid */
    .analysis-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .analysis-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        text-align: center;
    }
    
    .analysis-card h4 {
        color: #667eea;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .analysis-card .value {
        font-size: 1.3rem;
        font-weight: 700;
        color: #333;
    }
    
    .analysis-card .delta {
        font-size: 0.9rem;
        color: #666;
    }
    
    /* Ready state */
    .ready-state {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem 1.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(240, 147, 251, 0.3);
    }
    
    .ready-state h3 {
        font-size: 1.2rem;
        margin-bottom: 0.8rem;
    }
    
    .ready-state p {
        font-size: 0.9rem;
        opacity: 0.9;
        line-height: 1.4;
    }
    
    /* Footer */
    .mobile-footer {
        text-align: center;
        padding: 1.5rem 1rem;
        color: #666;
        font-size: 0.8rem;
        border-top: 1px solid #e0e0e0;
        margin-top: 2rem;
    }
    
    /* Animations */
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mobile specific adjustments */
    @media (max-width: 768px) {
        .mobile-header h1 {
            font-size: 1.5rem;
        }
        
        .summary-container {
            grid-template-columns: 1fr;
            gap: 0.5rem;
        }
        
        .prediction-result .price {
            font-size: 1.8rem;
        }
        
        .stButton > button {
            padding: 0.8rem 1.5rem;
            font-size: 1rem;
        }
    }
    
    /* Input styling */
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 0.5rem;
        font-size: 1rem;
    }
    
    .stSelectbox > div > div > div {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
    }
    
    /* Chart container */
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load model with caching for better performance
@st.cache_resource
def load_model():
    try:
        return joblib.load("model.pkl")
    except:
        return None

model = load_model()
model_loaded = model is not None

# Mobile Header
st.markdown("""
<div class="mobile-header">
    <h1>🏠 Smart House Price AI</h1>
    <p>Get instant property valuations on any device</p>
</div>
""", unsafe_allow_html=True)

if not model_loaded:
    st.error("🚨 Model not found! Please ensure 'model.pkl' exists.")
    st.stop()

# Input Section
st.markdown('<div class="input-container">', unsafe_allow_html=True)

st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown('<h3>🏗️ Property Details</h3>', unsafe_allow_html=True)

# First row of inputs
col1, col2 = st.columns(2)
with col1:
    bedrooms = st.number_input("�️ Bedrooms", min_value=0, max_value=10, value=3, key="bed")
    livingarea = st.number_input("📐 Area (sq ft)", min_value=500, max_value=10000, value=2000, step=100, key="area")
    numberofschools = st.number_input("🏫 Schools", min_value=0, max_value=20, value=2, key="schools")

with col2:
    bathrooms = st.number_input("🚿 Bathrooms", min_value=0, max_value=10, value=2, key="bath")
    condition = st.selectbox("⭐ Condition", 
                            options=[1, 2, 3, 4, 5], 
                            index=2,
                            format_func=lambda x: f"{'⭐' * x} {['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'][x-1]}",
                            key="cond")
    distancefromairport = st.number_input("✈️ Airport (miles)", min_value=1, max_value=100, value=15, key="airport")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Summary Cards
st.markdown(f"""
<div class="summary-container">
    <div class="summary-card">
        <h4>🏠 Total Rooms</h4>
        <h2>{bedrooms + bathrooms}</h2>
    </div>
    <div class="summary-card">
        <h4>� Size</h4>
        <h2>{livingarea:,} ft²</h2>
    </div>
    <div class="summary-card">
        <h4>⭐ Condition</h4>
        <h2>{'⭐' * condition}</h2>
    </div>
    <div class="summary-card">
        <h4>🎯 Location</h4>
        <h2>{numberofschools} 🏫</h2>
    </div>
</div>
""", unsafe_allow_html=True)

# Prediction Button
predict_button = st.button("🔮 GET PRICE PREDICTION", key="predict_btn")

if predict_button:
    # Create feature array
    X = [[bedrooms, bathrooms, livingarea, condition, numberofschools, distancefromairport]]
    X_array = np.array(X)
    
    try:
        prediction = model.predict(X_array)
        predicted_price = prediction[0]
        
        # Add visual effect
        st.balloons()
        
        # Prediction Result
        st.markdown(f"""
        <div class="prediction-result">
            <h2>🎯 Estimated Value</h2>
            <div class="price">${predicted_price:,.0f}</div>
            <p>Based on current market analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Analysis Cards
        price_per_sqft = predicted_price / livingarea
        avg_market = 300000
        difference = predicted_price - avg_market
        variance = predicted_price * 0.1
        
        st.markdown(f"""
        <div class="analysis-grid">
            <div class="analysis-card">
                <h4>💰 Price per Sq Ft</h4>
                <div class="value">${price_per_sqft:.0f}</div>
            </div>
            <div class="analysis-card">
                <h4>📊 vs Market Average</h4>
                <div class="value">${avg_market:,.0f}</div>
                <div class="delta">{"+" if difference > 0 else ""}{difference:,.0f}</div>
            </div>
            <div class="analysis-card">
                <h4>📍 Price Range</h4>
                <div class="value">±${variance:,.0f}</div>
                <div class="delta">10% variance</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Simple Mobile Chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Create mobile-friendly chart
        chart_data = {
            'Features': ['Beds', 'Baths', 'Area/1000', 'Condition', 'Schools', 'Airport/10'],
            'Values': [bedrooms, bathrooms, livingarea/1000, condition, numberofschools, distancefromairport/10]
        }
        
        fig = px.bar(
            x=chart_data['Features'], 
            y=chart_data['Values'],
            title="Property Features Overview",
            color=chart_data['Values'],
            color_continuous_scale="viridis"
        )
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=10),
            showlegend=False
        )
        
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Prediction failed: {str(e)}")

else:
    # Ready State
    st.markdown("""
    <div class="ready-state">
        <h3>🚀 Ready to Get Started?</h3>
        <p>Enter your property details above and tap the prediction button to get an instant AI-powered valuation!</p>
    </div>
    """, unsafe_allow_html=True)

# Mobile Footer with social links
st.markdown("""
<div class="mobile-footer">
    <p>🤖 <strong>AI-Powered House Price Predictions</strong></p>
    <p>Built with ❤️ by <strong>Lucky Chelani</strong> using Python & Machine Learning</p>
    <p><small>🔗 Connect with me on <a href="https://linkedin.com/in/your-profile" target="_blank" style="color: #667eea;">LinkedIn</a> | 
    ⭐ Star this project on <a href="https://github.com/your-username/house-price-prediction" target="_blank" style="color: #667eea;">GitHub</a></small></p>
    <p><small>📊 Predictions are ML estimates based on historical data - use as guidance only</small></p>
</div>
""", unsafe_allow_html=True)



























#order of X Index(['number of bedrooms', 'number of bathrooms', 'living area',
      # 'condition of the house', 'Number of schools nearby',
      # 'Distance from the airport'],
    #  dtype='object')