import streamlit as st
import base64
import sys
import os
import pickle
from datetime import datetime
from pathlib import Path

# Tambahkan path absolute
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from dataset import load_documents
from preprocessing import preprocess_kumpulan_dokumen, preprocess_query_pengguna
from retrieval import build_index, search
from evaluation import evaluate_system, auto_save_evaluation

# =====================
# Page Config
# =====================
st.set_page_config(
    page_title="Douggle",
    page_icon="🟠",
    layout="wide"
)

# =====================
# Helper Functions
# =====================
def load_base64_image(path: str) -> str:
    """Load image as base64"""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def save_to_cache(data, filename):
    """Save data to cache folder"""
    cache_dir = os.path.join(current_dir, "cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, filename)
    with open(cache_path, 'wb') as f:
        pickle.dump(data, f)
    return cache_path

def load_from_cache(filename):
    """Load data from cache folder"""
    cache_path = os.path.join(current_dir, "cache", filename)
    if os.path.exists(cache_path):
        with open(cache_path, 'rb') as f:
            return pickle.load(f)
    return None

def check_cache_valid(raw_docs):
    """Check if cache is valid by comparing document count"""
    cache_count = load_from_cache("doc_count.pkl")
    current_count = len(raw_docs) if raw_docs else 0
    return cache_count == current_count

# =====================
# Auto-Load System dengan Cache
# =====================
def auto_load_system(folder_path="data"):
    """Auto-load system dengan cache mechanism"""
    
    # Gunakan absolute path
    data_folder = os.path.join(current_dir, folder_path)
    
    # Cek folder data
    if not os.path.exists(data_folder):
        os.makedirs(data_folder, exist_ok=True)
        return False, f"📁 Folder 'data' dibuat di: {data_folder}\nSilakan tambahkan file .txt"
    
    # Load raw documents
    raw_docs = load_documents(data_folder)
    
    if isinstance(raw_docs, str):
        return False, f"❌ Error: {raw_docs}"
    
    if not raw_docs:
        return False, f"🔭 Folder 'data' kosong: {data_folder}\nTambahkan file .txt"
    
    # Simpan jumlah dokumen untuk cache validation
    doc_count = len(raw_docs)
    save_to_cache(doc_count, "doc_count.pkl")
    
    # Cek cache
    processed_docs = load_from_cache("processed_docs.pkl")
    vectorizer = load_from_cache("vectorizer.pkl")
    doc_vectors = load_from_cache("doc_vectors.pkl")
    
    # Jika cache tidak valid atau tidak ada, process ulang
    if not processed_docs or not vectorizer or not check_cache_valid(raw_docs):
        # Preprocess
        raw_documents = list(raw_docs.values())
        document_ids = list(raw_docs.keys())
        
        processed_docs = preprocess_kumpulan_dokumen(raw_documents)
        save_to_cache(processed_docs, "processed_docs.pkl")
        
        # Build index
        vectorizer, doc_vectors = build_index(processed_docs)
        save_to_cache(vectorizer, "vectorizer.pkl")
        save_to_cache(doc_vectors, "doc_vectors.pkl")
        
        # Simpan raw data juga
        save_to_cache(raw_documents, "raw_documents.pkl")
        save_to_cache(document_ids, "document_ids.pkl")
        
        return True, {
            "raw_documents": raw_documents,
            "document_ids": document_ids,
            "processed_documents": processed_docs,
            "vectorizer": vectorizer,
            "doc_vectors": doc_vectors,
            "from_cache": False
        }
    else:
        # Load dari cache
        raw_documents = load_from_cache("raw_documents.pkl")
        document_ids = load_from_cache("document_ids.pkl")
        
        return True, {
            "raw_documents": raw_documents,
            "document_ids": document_ids,
            "processed_documents": processed_docs,
            "vectorizer": vectorizer,
            "doc_vectors": doc_vectors,
            "from_cache": True
        }

# =====================
# Global CSS (MATCH NEW DESIGN)
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

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #f8f9fa;
}
</style>
""", unsafe_allow_html=True)

# =====================
# Initialize Session State
# =====================
if 'system_loaded' not in st.session_state:
    st.session_state.system_loaded = False
    st.session_state.system_data = None
    st.session_state.load_message = ""

# =====================
# Auto-Load pada Startup
# =====================
if not st.session_state.system_loaded:
    success, result = auto_load_system("data")
    
    if success:
        st.session_state.system_loaded = True
        st.session_state.system_data = result
        cache_status = " (from cache)" if result["from_cache"] else " (fresh load)"
        st.session_state.load_message = f"✅ Sistem siap! {len(result['document_ids'])} dokumen{cache_status}"
    else:
        st.session_state.load_message = result

# =====================
# Sidebar
# =====================
with st.sidebar:
    st.title("⚙️ System Control")
    
    if st.session_state.system_loaded:
        # System Status
        st.success(st.session_state.load_message)
        
        # Statistics
        data = st.session_state.system_data
        st.markdown("### 📊 Statistics")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Documents", len(data["document_ids"]))
        with col2:
            st.metric("Vocabulary", len(data["vectorizer"].get_feature_names_out()))
        
        # Reload Button
        if st.button("🔄 Force Reload Documents"):
            # Clear cache
            cache_files = ["processed_docs.pkl", "vectorizer.pkl", "doc_vectors.pkl", 
                          "raw_documents.pkl", "document_ids.pkl", "doc_count.pkl"]
            cache_dir = os.path.join(current_dir, "cache")
            for file in cache_files:
                cache_path = os.path.join(cache_dir, file)
                if os.path.exists(cache_path):
                    os.remove(cache_path)
            
            st.session_state.system_loaded = False
            st.rerun()
        
        # Evaluation Section
        st.markdown("---")
        st.markdown("### 📈 Evaluation")
        
        test_query = st.text_input("Test Query for Evaluation", 
                                  value="machine learning")
        
        if st.button("🎯 Run Evaluation on Test Query"):
            if test_query:
                with st.spinner("Running evaluation..."):
                    processed_query = preprocess_query_pengguna(test_query)
                    
                    results, doc_ids, scores = search(
                        processed_query,
                        data["vectorizer"],
                        data["doc_vectors"]
                    )
                    
                    relevant_docs = doc_ids[:3]
                    eval_results = evaluate_system([doc_ids], [relevant_docs])
                    
                    eval_folder = os.path.join(current_dir, "evaluasi")
                    saved_file = auto_save_evaluation(
                        test_query, 
                        doc_ids[:10], 
                        relevant_docs, 
                        eval_results,
                        folder=eval_folder
                    )
                    
                    st.success(f"✅ Evaluation saved to {saved_file}")
                    
                    st.markdown("#### Evaluation Metrics")
                    for k, metrics in eval_results.items():
                        if k != 'MAP':
                            st.write(f"**K={k}**: Precision={metrics['precision_avg']:.3f}, "
                                   f"Recall={metrics['recall_avg']:.3f}, "
                                   f"F1={metrics['f1_avg']:.3f}")
                    
                    st.metric("MAP Score", eval_results.get('MAP', 0))
    else:
        st.warning("⚠️ System belum dimuat")
        st.info(st.session_state.load_message)
        
        # Show folder info
        data_folder = os.path.join(current_dir, "data")
        st.info(f"""
**🔍 Folder 'data' kosong:**

`{data_folder}`

**Tambahkan file .txt**
        """)
        
        if os.path.exists(data_folder):
            txt_files = [f for f in os.listdir(data_folder) if f.endswith('.txt')]
            st.info(f"📂 Folder 'data' ditemukan: {len(txt_files)} file .txt")
            
            if txt_files:
                st.write("**Dokumen yang ditemukan:**")
                for file in txt_files[:10]:
                    st.write(f"• {file}")
                if len(txt_files) > 10:
                    st.write(f"... dan {len(txt_files) - 10} lainnya")

# =====================
# Header (MATCH NEW DESIGN)
# =====================
# Try to load logo
logo_path = os.path.join(current_dir, "assets", "logo.png")
if os.path.exists(logo_path):
    logo_base64 = load_base64_image(logo_path)
    st.markdown(f"""
    <div class="header-container">
        <img src="data:image/png;base64,{logo_base64}" class="header-logo" />
        <div class="header-title">Douggle</div>
    </div>
    <div class="subtitle">
        Search and explore academic knowledge
    </div>
    """, unsafe_allow_html=True)
else:
    # Fallback without logo
    st.markdown(f"""
    <div class="header-container">
        <div class="header-title">🟠 Douggle</div>
    </div>
    <div class="subtitle">
        Search and explore academic knowledge
    </div>
    """, unsafe_allow_html=True)

# =====================
# Main Content
# =====================
if not st.session_state.system_loaded:
    # Show instructions when system not loaded
    st.warning("⚠️ Menunggu dokumen...")
    
    data_folder = os.path.join(current_dir, "data")
    st.info(f"""
**Instruksi:**

1. Pastikan folder `data` berisi file .txt
2. Lokasi: `{data_folder}`
3. File akan otomatis diproses saat pertama kali
4. Hasil preprocessing disimpan di cache untuk percepatan
5. Evaluasi otomatis tersimpan di folder `evaluasi/`
    """)
    
    if os.path.exists(data_folder):
        txt_files = [f for f in os.listdir(data_folder) if f.endswith('.txt')]
        st.write(f"📂 Folder 'data' ditemukan: {len(txt_files)} file .txt")
        
        if txt_files:
            st.write("**Dokumen yang ditemukan:**")
            for i, file in enumerate(txt_files[:5], 1):
                st.write(f"• {file}")
            if len(txt_files) > 5:
                st.write(f"... dan {len(txt_files) - 5} lainnya")
    
    if st.button("🔄 Coba Load Ulang", use_container_width=True):
        st.rerun()
    
    st.stop()

# System loaded - show search interface
data = st.session_state.system_data

# =====================
# Search Bar (MATCH NEW DESIGN)
# =====================
st.markdown('<div class="search-wrapper">', unsafe_allow_html=True)
query = st.text_input(
    "",
    placeholder="Search research papers, methods, or topics...",
    key="main_search"
)
st.markdown('</div>', unsafe_allow_html=True)

# =====================
# Layout: Filter + Results (MATCH NEW DESIGN)
# =====================
col_filter, col_results = st.columns([1, 3], gap="large")

# -------- Filter (Left Sidebar) --------
with col_filter:
    st.markdown('<div class="filter-box">', unsafe_allow_html=True)
    st.markdown("### Filter Results")
    max_docs = st.slider("Number of documents", 1, 20, 10)
    min_score = st.slider("Minimum score", 0.0, 1.0, 0.1, 0.05)
    st.markdown('</div>', unsafe_allow_html=True)

# -------- Results (Right Content) --------
with col_results:
    if not query.strip():
        st.info("Start by typing a query above.")
    else:
        with st.spinner("🔍 Searching..."):
            # Process query
            processed_query = preprocess_query_pengguna(query)
            
            # Search
            results, doc_ids, scores = search(
                processed_query,
                data["vectorizer"],
                data["doc_vectors"]
            )
            
            # Filter by min_score
            filtered_results = [
                (doc_ids[i], scores[i]) 
                for i in range(len(doc_ids)) 
                if scores[i] >= min_score
            ]
            
            found_count = len(filtered_results)
            
            if found_count == 0:
                st.warning(f"No documents found with score ≥ {min_score}. Try lowering the minimum score.")
            else:
                st.success(f"Found **{found_count}** documents (showing top {min(max_docs, found_count)})")
                
                # Display results with new card design
                display_count = min(max_docs, found_count)
                for i in range(display_count):
                    doc_idx, score = filtered_results[i]
                    
                    # Get document info
                    title = data['document_ids'][doc_idx]
                    snippet = data['raw_documents'][doc_idx][:200] + "..."
                    word_count = len(data['raw_documents'][doc_idx].split())
                    
                    # Display card
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-title">📄 {title}</div>
                        <div class="result-meta">
                            Similarity score: {score:.4f} • {word_count} words
                        </div>
                        <div class="result-snippet">{snippet}</div>
                    </div>
                    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("*Douggle IR System v2.0 | Information Retrieval with TF-IDF & Cosine Similarity*", unsafe_allow_html=True)