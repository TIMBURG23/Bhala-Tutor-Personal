import streamlit as st

st.set_page_config(
    page_title="Tutor Ed",
    page_icon="🎓",
    layout="wide"
)

# --- HERO SECTION ---
st.markdown("""
<style>
    .hero {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .hero h1 {
        font-family: 'Arial Rounded MT Bold', sans-serif;
        font-size: 4em;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px #000;
        letter-spacing: 2px;
    }
    .hero p {
        font-size: 1.3em;
        opacity: 0.9;
        font-weight: 300;
    }
    .card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
        transition: transform 0.3s, box-shadow 0.3s;
        border: 1px solid #f0f0f0;
        height: 100%;
    }
    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border-color: #2c5364;
    }
    .card h3 { color: #2c5364; margin-top: 10px;}
    .status-online { color: #27ae60; font-weight: bold; font-size: 0.8em; letter-spacing: 1px;}
    .status-soon { color: #e67e22; font-weight: bold; font-size: 0.8em; letter-spacing: 1px;}
    .status-locked { color: #c0392b; font-weight: bold; font-size: 0.8em; letter-spacing: 1px;}
    .icon { font-size: 3em; margin-bottom: 10px; }
</style>

<div class="hero">
    <h1>🎓 Tutor Ed</h1>
    <p>Your Offline AI Learning Companion</p>
</div>
""", unsafe_allow_html=True)

# --- APP SELECTOR ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <div class="icon">📝</div>
        <h3>Bhala-Smart</h3>
        <p>English FAL Essay Assistant</p>
        <p class="status-online">● READY</p>
    </div>
    """, unsafe_allow_html=True)
    st.success("👈 Click **Bhala_Smart** in the sidebar to start.")

with col2:
    st.markdown("""
    <div class="card">
        <div class="icon">🔬</div>
        <h3>Ukufunda-Sci</h3>
        <p>Science Concept Translator</p>
        <p class="status-soon">● COMING SOON</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Build Science App Next"):
        st.toast("Let's build Ukufunda-Sci!")

with col3:
    st.markdown("""
    <div class="card">
        <div class="icon">📐</div>
        <h3>GeoVision</h3>
        <p>Geometry Visual Solver</p>
        <p class="status-locked">● LOCKED</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2026 Tutor Ed • Offline Mode • SA CAPS Aligned")