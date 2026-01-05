# retrieval.py (Modul 3 - Indexing & Retrieval)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def build_index(processed_docs):
    """
    Fungsi untuk membangun indeks TF-IDF.
    Input: list of strings (dokumen hasil preprocessing dari Index 2)
    Output: vectorizer (objek TF-IDF) dan doc_vectors (matriks numerik)
    """
    # Menginisialisasi Vectorizer untuk mengubah teks menjadi angka
    vectorizer = TfidfVectorizer()
    
    # Menghitung bobot TF-IDF untuk seluruh koleksi dokumen
    doc_vectors = vectorizer.fit_transform(processed_docs)
    
    return vectorizer, doc_vectors

def search(query, vectorizer, doc_vectors):
    """
    Fungsi untuk mencari dokumen paling relevan berdasarkan query pengguna.
    Input: query (str), vectorizer (objek), doc_vectors (matriks)
    Output: results (ID & Skor), doc_ids (ID saja), scores (Skor saja)
    """
    # 1. Mengubah query menjadi representasi numerik menggunakan model yang sudah ada
    query_vector = vectorizer.transform([query])
    
    # 2. Menghitung nilai kemiripan menggunakan Cosine Similarity 
    # flatten() digunakan untuk mengubah matriks menjadi list sederhana
    cosine_scores = cosine_similarity(query_vector, doc_vectors).flatten()
    
    # 3. Menggabungkan ID dokumen (indeks) dengan skornya
    # Format: [(index_0, skor_0), (index_1, skor_1), ...]
    results_raw = list(enumerate(cosine_scores))
    
    # 4. Mengurutkan hasil dari skor tertinggi ke terendah (Ranking)
    results = sorted(results_raw, key=lambda x: x[1], reverse=True)
    
    # 5. Memisahkan ID dan Skor untuk kebutuhan output modul lain
    doc_ids = [res[0] for res in results]
    scores = [res[1] for res in results]
    
    return results, doc_ids, scores