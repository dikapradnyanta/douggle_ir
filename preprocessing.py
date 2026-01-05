import os
import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory


stem_factory = StemmerFactory()
stemmer = stem_factory.create_stemmer()

stop_factory = StopWordRemoverFactory()
stopword_remover = stop_factory.create_stop_word_remover()



def preprocess_satu_teks(text):
    """Membersihkan satu teks secara mendalam."""
    if not isinstance(text, str): return ""
    
    
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\d+', '', text)
    
    
    text = stopword_remover.remove(text)
    
    
    text = stemmer.stem(text)
    
    return text

def preprocess_kumpulan_dokumen(list_dokumen):
    """Memproses list dokumen secara massal."""
    return [preprocess_satu_teks(doc) for doc in list_dokumen]

def preprocess_query_pengguna(query):
    """Menjamin hasil query konsisten dengan indeks dokumen."""
    return preprocess_satu_teks(query)



if __name__ == "__main__":
    file_input = 'data.txt' 
    file_output = 'dokumen_siap_indeks.txt'
    
    if os.path.exists(file_input):
       
        with open(file_input, 'r', encoding='utf-8') as f:
            dokumen_mentah = f.readlines()
        
        print(f"⏳ Memproses {len(dokumen_mentah)} baris dokumen...")
        
        
        hasil_bersih = preprocess_kumpulan_dokumen(dokumen_mentah)
        
        
        with open(file_output, 'w', encoding='utf-8') as f:
            for baris in hasil_bersih:
                f.write(baris + '\n')
        
        print(f"✅ Selesai! Hasil disimpan di '{file_output}'")
    else:
        print(f"❌ File '{file_input}' tidak ditemukan. Silakan buat file tersebut dahulu.")