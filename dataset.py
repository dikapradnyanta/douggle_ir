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
        """
        if not os.path.exists(self.folder_path):
            return f"Error: Folder '{self.folder_path}' tidak ditemukan."

        for filename in os.listdir(self.folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.folder_path, filename)
                try:
                    # Menggunakan encoding utf-8 untuk membaca file
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read().strip() # Menghapus spasi kosong di awal/akhir
                        if content:
                            self.documents[filename] = content
                        else:
                            print(f"Peringatan: File {filename} kosong!")
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
    # 1. Inisialisasi manager (Pastikan nama folder sesuai, yaitu "data")
    manager = DatasetManager(folder_path="data")
    
    # 2. EKSEKUSI PEMBACAAN FILE (PENTING: Harus dipanggil agar data masuk ke memori)
    manager.load_documents()
    
    print("--- Douggle: Dataset Metadata ---")
    
    # 3. Hitung dan ambil statistik
    stats = manager.get_metadata()
    
    # 4. Cetak hasil
    if isinstance(stats, dict):
        for key, value in stats.items():
            print(f"{key}: {value}")
    else:
        print(stats)