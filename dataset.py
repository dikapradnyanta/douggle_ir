import os

class DatasetManager:
    """
    Modul ini bertanggung jawab untuk pengumpulan dan pemuatan dataset mentah.
    Sesuai aturan Index 1, modul ini tidak melakukan preprocessing apa pun[cite: 36].
    """
    def __init__(self, folder_path="data"):
        self.folder_path = folder_path
        self.documents = {}

    def load_documents(self):
        """
        Memuat seluruh dokumen dari folder dataset.
        Output: Dictionary dengan nama file sebagai ID dan isi teks sebagai value.
        """
        if not os.path.exists(self.folder_path):
            return f"Error: Folder '{self.folder_path}' tidak ditemukan."

        for filename in os.listdir(self.folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.folder_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        self.documents[filename] = file.read()
                except Exception as e:
                    print(f"Gagal membaca {filename}: {e}")
        
        return self.documents

    def get_metadata(self):
        """
        Menghasilkan metadata statistik dari dataset yang dimuat.
        """
        if not self.documents:
            return "Dataset belum dimuat atau kosong."

        num_docs = len(self.documents)
        # Menghitung panjang rata-rata dokumen berdasarkan jumlah kata 
        total_words = sum(len(content.split()) for content in self.documents.values())
        avg_length = total_words / num_docs if num_docs > 0 else 0

        metadata = {
            "Jumlah Dokumen": num_docs,
            "Panjang Rata-rata (kata)": round(avg_length, 2),
            "Format File": ".txt",
            "Status": "Siap untuk Preprocessing"
        }
        return metadata

# Demonstrasi penggunaan mandiri untuk pengecekan kualitas [cite: 37]
if __name__ == "__main__":
    manager = DatasetManager(folder_path="data")
    raw_data = manager.load_documents()
    
    print("--- Douggle: Dataset Metadata ---")
    stats = manager.get_metadata()
    if isinstance(stats, dict):
        for key, value in stats.items():
            print(f"{key}: {value}")
    else:
        print(stats)

# Function wrapper untuk kemudahan import
def load_documents(folder_path="data"):
    """
    Fungsi utama untuk memuat dokumen dengan lebih mudah.
    Langsung dipanggil dari app.py tanpa perlu instantiate class.
    """
    manager = DatasetManager(folder_path=folder_path)
    return manager.load_documents()