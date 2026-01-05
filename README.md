# 🔍 Douggle IR System

**Information Retrieval System** berbasis TF-IDF dan Cosine Similarity dengan cache system otomatis.

---

## 📋 Daftar Isi
- [Fitur Utama](#-fitur-utama)
- [Arsitektur Sistem](#-arsitektur-sistem)
- [Instalasi](#-instalasi)
- [Cara Penggunaan](#-cara-penggunaan)
- [Struktur Folder](#-struktur-folder)
- [Cara Kerja Sistem](#-cara-kerja-sistem)
- [Evaluasi](#-evaluasi)
- [Troubleshooting](#-troubleshooting)
- [Kontribusi](#-kontribusi)

---

## ✨ Fitur Utama

- ✅ **Auto-load Documents**: Otomatis memuat dokumen dari folder `data/`
- 🚀 **Cache System**: Menyimpan hasil preprocessing untuk percepatan
- 🔍 **TF-IDF Search**: Pencarian berbasis Term Frequency-Inverse Document Frequency
- 📊 **Evaluation Metrics**: Precision@K, Recall@K, F1-Score, MAP
- 🎨 **Modern UI**: Interface berbasis Streamlit yang responsif
- 🇮🇩 **Indonesian Support**: Preprocessing dengan Sastrawi (stemming & stopwords)
- 💾 **Persistent Results**: Hasil evaluasi tersimpan otomatis

---

## 🏗️ Arsitektur Sistem

```
┌─────────────────────────────────────────────────┐
│              USER INTERFACE (Streamlit)         │
│                    app.py                       │
└──────────────────┬──────────────────────────────┘
                   │
       ┌───────────┼───────────┬──────────────┐
       │           │           │              │
       ▼           ▼           ▼              ▼
  ┌────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │Dataset │  │Preprocess│  │Retrieval │  │Evaluation│
  │Module  │  │Module    │  │Module    │  │Module    │
  └────────┘  └──────────┘  └──────────┘  └──────────┘
       │           │             │              │
       └───────────┴─────────────┴──────────────┘
                   │
              ┌────▼─────┐
              │  Cache   │
              │ (Pickle) │
              └──────────┘
```

---

## 📦 Instalasi

### 1. Clone atau Download Repository
```bash
git clone https://github.com/yourusername/douggle-ir.git
cd douggle-ir
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate Sample Data (Optional)
Jika folder `data/` kosong atau file-nya 0 KB:
```bash
python generate_sample_data.py
```

### 4. Run Application
```bash
streamlit run app.py
```

---

## 🚀 Cara Penggunaan

### **Step 1: Persiapkan Data**
1. Buat folder `data/` (jika belum ada)
2. Taruh file `.txt` berisi dokumen
3. Format: UTF-8 encoding
4. Minimal 1 dokumen

### **Step 2: Jalankan Sistem**
```bash
streamlit run app.py
```

### **Step 3: Cari Dokumen**
1. Masukkan query di search box
2. Atur parameter:
   - **Top K**: Jumlah hasil yang ditampilkan
   - **Min Score**: Skor minimum relevansi (0.0 - 1.0)
3. Klik tombol "🔍 Search"

### **Step 4: Lihat Hasil**
Sistem akan menampilkan:
- Nama dokumen
- Skor relevansi
- Preview isi dokumen
- Panjang dokumen (jumlah kata)

### **Step 5: Evaluasi (Optional)**
1. Buka sidebar → "📈 Evaluation"
2. Masukkan test query
3. Klik "🎯 Run Evaluation on Test Query"
4. Hasil tersimpan di folder `evaluasi/`

---

## 📁 Struktur Folder

```
douggle_ir/
│
├── app.py                      # Main application (Streamlit UI)
├── dataset.py                  # Module untuk load documents
├── preprocessing.py            # Module untuk text cleaning
├── retrieval.py                # Module untuk TF-IDF & search
├── evaluation.py               # Module untuk metrics evaluation
├── requirements.txt            # Python dependencies
├── generate_sample_data.py     # Script generate data sample
├── README.md                   # Documentation (this file)
│
├── data/                       # ← Taruh file .txt di sini
│   ├── doc01.txt
│   ├── doc02.txt
│   └── ...
│
├── cache/                      # Auto-generated cache folder
│   ├── processed_docs.pkl
│   ├── vectorizer.pkl
│   ├── doc_vectors.pkl
│   └── ...
│
└── evaluasi/                   # Auto-generated evaluation results
    ├── evaluation_20260105_143022.json
    └── ...
```

---

## ⚙️ Cara Kerja Sistem

### **1. Data Loading (dataset.py)**
```python
load_documents(folder_path="data")
```
- Scan folder `data/` untuk file `.txt`
- Load semua dokumen ke memory
- Return: `{filename: content}`

### **2. Preprocessing (preprocessing.py)**
```python
preprocess_kumpulan_dokumen(raw_documents)
```
Tahapan:
1. **Lowercase**: "Machine Learning" → "machine learning"
2. **Remove Punctuation**: "Hello, World!" → "Hello World"
3. **Remove Numbers**: "Python3" → "Python"
4. **Stopword Removal**: "yang di dari" → (dihapus)
5. **Stemming**: "pembelajaran" → "ajar"

### **3. Indexing (retrieval.py)**
```python
build_index(processed_docs)
```
- Membangun TF-IDF matrix
- Setiap dokumen → vector numerik
- Menyimpan vocabulary (kata unik)

### **4. Searching (retrieval.py)**
```python
search(query, vectorizer, doc_vectors)
```
- Query → vector numerik
- Hitung Cosine Similarity dengan semua dokumen
- Ranking berdasarkan skor (tertinggi ke terendah)

### **5. Evaluation (evaluation.py)**
```python
evaluate_system(retrieved_docs_list, relevant_docs_list)
```
Metrics yang dihitung:
- **Precision@K**: Berapa banyak hasil yang relevan dari K hasil teratas?
- **Recall@K**: Berapa banyak dokumen relevan yang ditemukan dari total dokumen relevan?
- **F1-Score@K**: Harmonic mean dari Precision dan Recall
- **MAP**: Mean Average Precision untuk semua query

---

## 📊 Evaluasi

### Contoh Output Evaluasi:
```json
{
  "timestamp": "20260105_143022",
  "query": "machine learning",
  "retrieved_docs": [0, 5, 12, 8, 3, ...],
  "relevant_docs": [0, 5, 12],
  "metrics": {
    "1": {
      "precision_avg": 1.0,
      "recall_avg": 0.333,
      "f1_avg": 0.5
    },
    "3": {
      "precision_avg": 1.0,
      "recall_avg": 1.0,
      "f1_avg": 1.0
    },
    "MAP": 0.8333
  }
}
```

### Interpretasi Metrics:
- **Precision@3 = 1.0**: Semua 3 hasil teratas relevan
- **Recall@3 = 1.0**: Semua dokumen relevan ditemukan di top-3
- **MAP = 0.8333**: Kualitas ranking sangat baik

---

## 🐛 Troubleshooting

### **Problem 1: File 0 KB / Empty**
**Symptom**: 
```
⚠️ Folder 'data' kosong. Tambahkan file .txt
```

**Solution**:
1. Jalankan: `python generate_sample_data.py`
2. Atau manual: copy-paste text ke file `.txt` di folder `data/`
3. Pastikan encoding UTF-8

---

### **Problem 2: Import Error Sastrawi**
**Symptom**:
```
ModuleNotFoundError: No module named 'Sastrawi'
```

**Solution**:
```bash
pip install Sastrawi
```

---

### **Problem 3: Cache Tidak Valid**
**Symptom**: Sistem tidak load dokumen baru

**Solution**:
1. Klik "🔄 Force Reload Documents" di sidebar
2. Atau manual: hapus folder `cache/`

---

### **Problem 4: Streamlit Error**
**Symptom**:
```
streamlit: command not found
```

**Solution**:
```bash
pip install streamlit
# atau
python -m streamlit run app.py
```

---

## 🔧 Konfigurasi Lanjutan

### Custom Stopwords
Edit file `preprocessing.py`:
```python
custom_stopwords = stopword_remover.get_stop_words() + ['custom', 'words']
stop_factory = StopWordRemoverFactory().set_stop_words(custom_stopwords)
```

### Custom TF-IDF Parameters
Edit file `retrieval.py`:
```python
vectorizer = TfidfVectorizer(
    max_features=5000,      # Max vocabulary size
    min_df=2,               # Min document frequency
    max_df=0.8,             # Max document frequency
    ngram_range=(1, 2)      # Unigrams and bigrams
)
```

---

## 🤝 Kontribusi

Contributions are welcome! Silakan:
1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

MIT License - feel free to use this project for educational purposes.

---

## 👨‍💻 Author

**Douggle IR Team**
- Information Retrieval System Project
- Built with ❤️ using Python & Streamlit

---

## 📚 Referensi

- [TF-IDF Wikipedia](https://en.wikipedia.org/wiki/Tf–idf)
- [Scikit-learn TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [Sastrawi - Indonesian NLP](https://github.com/sastrawi/sastrawi)
- [Streamlit Documentation](https://docs.streamlit.io)

---

## 🎯 Roadmap

- [ ] Add support for PDF files
- [ ] Multi-language support
- [ ] Advanced query expansion
- [ ] Real-time indexing
- [ ] REST API endpoint
- [ ] Docker containerization
- [ ] Cloud deployment guide

---

**Last Updated**: January 5, 2026