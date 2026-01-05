import streamlit as st
import base64

# =====================
# Page Config
# =====================
st.set_page_config(
    page_title="Douggle",
    page_icon="🟠",
    layout="wide"
)

# =====================
# Helper: load image as base64 (STABIL)
# =====================
def load_base64_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = load_base64_image("assets/logo.png")

# =====================
# Global CSS
# =====================
st.markdown("""
<style>
/* Reduce top padding */
.block-container { padding-top: 2rem; }

/* ===== HEADER ===== */
.header-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    margin-top: 36px;
    margin-bottom: 6px;
}
.header-logo {
    width: 48px;
    height: auto;
}
.header-title {
    font-size: 56px;
    font-weight: 800;
    background: linear-gradient(90deg, #ff8c00, #ffb347);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}
.subtitle {
    text-align: center;
    color: #6b6b6b;
    font-size: 16px;
    margin-bottom: 36px;
}

/* ===== SEARCH ===== */
.search-wrapper {
    max-width: 880px;
    margin: 0 auto 28px auto;
}

/* ===== FILTER ===== */
.filter-box {
    background: #fafafa;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}

/* ===== RESULT CARD ===== */
.result-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}
.result-title {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 6px;
}
.result-meta {
    font-size: 13px;
    color: #888;
    margin-bottom: 8px;
}
.result-snippet {
    font-size: 14px;
    color: #333;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

# =====================
# Header (INLINE + BASE64)
# =====================
st.markdown(f"""
<div class="header-container">
    <img src="data:image/png;base64,{logo_base64}" class="header-logo" />
    <div class="header-title">Douggle</div>
</div>
<div class="subtitle">
    Search and explore academic knowledge
</div>
""", unsafe_allow_html=True)

# =====================
# Search Bar
# =====================
st.markdown('<div class="search-wrapper">', unsafe_allow_html=True)
query = st.text_input(
    "",
    placeholder="Search research papers, methods, or topics..."
)
st.markdown('</div>', unsafe_allow_html=True)

# =====================
# Layout: Filter + Results
# =====================
col_filter, col_results = st.columns([1, 3], gap="large")

# -------- Filter --------
with col_filter:
    st.markdown('<div class="filter-box">', unsafe_allow_html=True)
    st.markdown("### Filter Results")
    max_docs = st.slider("Number of documents", 1, 20, 5)
    st.markdown('</div>', unsafe_allow_html=True)

# -------- Results --------
with col_results:
    if not query.strip():
        st.info("Start by typing a query above.")
    else:
        # Dummy data (UI ONLY)
        dummy_results = [
            {
                "title": "Information Retrieval Using TF-IDF",
                "score": 0.82,
                "snippet": "This paper discusses TF-IDF and cosine similarity for document ranking in IR systems."
            },
            {
                "title": "Text Preprocessing Techniques in NLP",
                "score": 0.76,
                "snippet": "Overview of tokenization, stopword removal, and stemming for text data."
            },
            {
                "title": "Evaluation Metrics for Search Engines",
                "score": 0.71,
                "snippet": "Precision, recall, and F1-score as standard IR evaluation metrics."
            }
        ]

        for r in dummy_results[:max_docs]:
            st.markdown(f"""
            <div class="result-card">
                <div class="result-title">{r['title']}</div>
                <div class="result-meta">Similarity score: {r['score']:.2f}</div>
                <div class="result-snippet">{r['snippet']}</div>
            </div>
            """, unsafe_allow_html=True)
