import streamlit as st
from query import ask

st.set_page_config(
    page_title="ESG Intelligence",
    page_icon="🌿",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1f1a 40%, #0a1628 100%);
    min-height: 100vh;
}

/* Hide streamlit default elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.hero-section {
    text-align: center;
    padding: 4rem 2rem 2rem;
}

.badge {
    display: inline-block;
    background: rgba(74, 222, 128, 0.1);
    border: 1px solid rgba(74, 222, 128, 0.3);
    color: #4ade80;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.4rem 1.2rem;
    border-radius: 100px;
    margin-bottom: 1.5rem;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 4.8rem;
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #ffffff 0%, #a8d5b5 50%, #4ade80 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    color: #8b9ab0;
    font-size: 1.25rem;
    font-weight: 300;
    line-height: 1.6;
    max-width: 520px;
    margin: 0 auto 3rem;
}

.search-container {
    max-width: 680px;
    margin: 0 auto 1rem;
    position: relative;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 16px !important;
    color: #1a1a2e !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1.15rem !important;
    padding: 1.1rem 1.5rem !important;
    transition: all 0.3s ease !important;
    backdrop-filter: blur(10px) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #4a5568 !important;
}

.stTextInput > div > div > input:focus {
    border-color: rgba(74, 222, 128, 0.5) !important;
    background: rgba(255,255,255,0.07) !important;
    box-shadow: 0 0 0 3px rgba(74, 222, 128, 0.08), 0 8px 32px rgba(0,0,0,0.3) !important;
}

.hint-text {
    text-align: center;
    color: #3d4f63;
    font-size: 0.82rem;
    margin-top: 0.75rem;
    letter-spacing: 0.02em;
}

.divider-line {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(74,222,128,0.2), transparent);
    margin: 2.5rem auto;
    max-width: 680px;
}

.answer-container {
    max-width: 680px;
    margin: 0 auto;
}

.answer-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.answer-dot {
    width: 8px;
    height: 8px;
    background: #4ade80;
    border-radius: 50%;
    box-shadow: 0 0 8px #4ade80;
}

.answer-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #4ade80;
}

.answer-box {
    background: linear-gradient(135deg, rgba(26,35,50,0.9) 0%, rgba(20,40,30,0.9) 100%);
    border: 1px solid rgba(74, 222, 128, 0.15);
    border-radius: 16px;
    padding: 2rem;
    color: #d4e4d8;
    font-size: 1.15rem;
    line-height: 1.85;
    font-weight: 300;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
}

.sources-section {
    margin-top: 1.5rem;
}

.sources-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #3d5a6b;
    margin-bottom: 0.75rem;
}

.source-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(74, 222, 128, 0.06);
    border: 1px solid rgba(74, 222, 128, 0.2);
    color: #6bba8a;
    font-size: 0.8rem;
    font-weight: 500;
    padding: 0.4rem 1rem;
    border-radius: 100px;
    margin: 0.25rem 0.3rem 0.25rem 0;
    letter-spacing: 0.01em;
}

.stats-row {
    display: flex;
    justify-content: center;
    gap: 3rem;
    margin: 3rem auto 0;
    max-width: 500px;
    padding-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.05);
}

.stat-item {
    text-align: center;
}

.stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #4ade80;
    line-height: 1;
}

.stat-label {
    font-size: 0.72rem;
    color: #3d4f63;
    margin-top: 0.3rem;
    letter-spacing: 0.05em;
}

.stSpinner > div {
    border-top-color: #4ade80 !important;
}
</style>
""", unsafe_allow_html=True)

# Hero section
st.markdown("""
<div class="hero-section">
    <div class="badge">🌿 ESG Intelligence Platform</div>
    <h1 class="hero-title">Ask Anything About<br>Sustainability Reports</h1>
    <p class="hero-subtitle">
        Instantly query ESG disclosures from BHP, Woodside, CommBank and more.
        Powered by RAG — grounded in real documents, not hallucinations.
    </p>
</div>
""", unsafe_allow_html=True)

# Search
question = st.text_input("", placeholder="e.g. What are BHP's Scope 1 emissions targets for 2030?", key="query")
st.markdown('<p class="hint-text">Press Enter to search across all ESG documents</p>', unsafe_allow_html=True)

if question:
    st.markdown('<hr class="divider-line">', unsafe_allow_html=True)
    
    with st.spinner("Searching documents..."):
        answer, sources = ask(question)

    st.markdown(f"""
    <div class="answer-container">
        <div class="answer-header">
            <div class="answer-dot"></div>
            <span class="answer-label">Analysis</span>
        </div>
        <div class="answer-box">{answer}</div>
        <div class="sources-section">
            <div class="sources-label">Referenced Documents</div>
            {"".join([f'<span class="source-chip">📄 {s.replace(".md","").replace("-"," ").replace("_"," ")}</span>' for s in set(sources)])}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Stats footer
st.markdown("""
<div class="stats-row">
    <div class="stat-item">
        <div class="stat-number">4</div>
        <div class="stat-label">ESG Reports</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">2,082</div>
        <div class="stat-label">Document Chunks</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">3</div>
        <div class="stat-label">Companies</div>
    </div>
</div>
""", unsafe_allow_html=True)