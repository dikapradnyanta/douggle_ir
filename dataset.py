# dataset.py (Modul 1 - Dataset - Improved Version)
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatasetManager:
    """
    Modul ini bertanggung jawab untuk pengumpulan dan pemuatan dataset mentah.
    Sesuai aturan Index 1, modul ini tidak melakukan preprocessing apa pun.
    """
    def __init__(self, folder_path="data"):
        self.folder_path = folder_path
        self.documents = {}
        self.errors = []

    def load_documents(self):
        """
        Memuat seluruh dokumen dari folder dataset.
        Output: Dictionary dengan nama file sebagai ID dan isi teks sebagai value.
        """
        if not os.path.exists(self.folder_path):
            error_msg = f"Error: Folder '{self.folder_path}' tidak ditemukan."
            logger.error(error_msg)
            return error_msg

        txt_files = [f for f in os.listdir(self.folder_path) if f.endswith(".txt")]
        
        if not txt_files:
            warning_msg = f"Warning: Folder '{self.folder_path}' tidak memiliki file .txt"
            logger.warning(warning_msg)
            return warning_msg

        loaded_count = 0
        empty_files = []
        
        for filename in txt_files:
            file_path = os.path.join(self.folder_path, filename)
            try:
                # Check file size
                file_size = os.path.getsize(file_path)
                if file_size == 0:
                    empty_files.append(filename)
                    logger.warning(f"⚠️ {filename} is empty (0 bytes)")
                    continue
                
                # Read file
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if content.strip():  # Skip empty content
                        self.documents[filename] = content
                        loaded_count += 1
                        logger.info(f"✅ Loaded: {filename} ({file_size} bytes)")
                    else:
                        empty_files.append(filename)
                        logger.warning(f"⚠️ {filename} has no content after stripping")
                        
            except UnicodeDecodeError:
                error = f"Encoding error in {filename}, trying with different encoding"
                logger.error(error)
                self.errors.append(error)
                
                # Try with different encoding
                try:
                    with open(file_path, 'r', encoding='latin-1') as file:
                        content = file.read()
                        if content.strip():
                            self.documents[filename] = content
                            loaded_count += 1
                            logger.info(f"✅ Loaded with latin-1: {filename}")
                except Exception as e:
                    self.errors.append(f"Failed to load {filename}: {str(e)}")
                    
            except Exception as e:
                error = f"Failed to read {filename}: {str(e)}"
                logger.error(error)
                self.errors.append(error)
        
        # Summary
        logger.info(f"\n{'='*50}")
        logger.info(f"📊 LOADING SUMMARY")
        logger.info(f"{'='*50}")
        logger.info(f"✅ Successfully loaded: {loaded_count} documents")
        if empty_files:
            logger.warning(f"⚠️ Empty files found: {len(empty_files)}")
            for f in empty_files[:5]:  # Show first 5
                logger.warning(f"   - {f}")
            if len(empty_files) > 5:
                logger.warning(f"   ... and {len(empty_files)-5} more")
        if self.errors:
            logger.error(f"❌ Errors encountered: {len(self.errors)}")
        logger.info(f"{'='*50}\n")
        
        return self.documents

    def get_metadata(self):
        """
        Menghasilkan metadata statistik dari dataset yang dimuat.
        """
        if not self.documents:
            return "Dataset belum dimuat atau kosong."

        num_docs = len(self.documents)
        total_words = sum(len(content.split()) for content in self.documents.values())
        avg_length = total_words / num_docs if num_docs > 0 else 0
        
        # Calculate min and max document length
        doc_lengths = [len(content.split()) for content in self.documents.values()]
        min_length = min(doc_lengths) if doc_lengths else 0
        max_length = max(doc_lengths) if doc_lengths else 0

        metadata = {
            "Jumlah Dokumen": num_docs,
            "Total Kata": total_words,
            "Panjang Rata-rata (kata)": round(avg_length, 2),
            "Panjang Minimum (kata)": min_length,
            "Panjang Maximum (kata)": max_length,
            "Format File": ".txt",
            "Status": "Siap untuk Preprocessing" if num_docs > 0 else "Kosong"
        }
        
        if self.errors:
            metadata["Errors"] = len(self.errors)
        
        return metadata

    def get_document_list(self):
        """Return list of loaded document names"""
        return list(self.documents.keys())

    def get_document(self, doc_id):
        """Get specific document by ID"""
        return self.documents.get(doc_id, None)

# Demonstrasi penggunaan mandiri untuk pengecekan kualitas
if __name__ == "__main__":
    manager = DatasetManager(folder_path="data")
    raw_data = manager.load_documents()
    
    print("\n" + "="*60)
    print("🔍 DOUGGLE: Dataset Metadata")
    print("="*60)
    
    stats = manager.get_metadata()
    if isinstance(stats, dict):
        for key, value in stats.items():
            print(f"{key:30s}: {value}")
    else:
        print(stats)
    
    print("="*60)
    
    # Show sample documents
    if isinstance(raw_data, dict) and raw_data:
        print("\n📄 Sample Documents (first 3):")
        for i, (doc_id, content) in enumerate(list(raw_data.items())[:3]):
            preview = content[:150].replace('\n', ' ')
            print(f"\n{i+1}. {doc_id}")
            print(f"   Preview: {preview}...")
            print(f"   Length: {len(content.split())} words")

# Function wrapper untuk kemudahan import
def load_documents(folder_path="data"):
    """
    Fungsi utama untuk memuat dokumen dengan lebih mudah.
    Langsung dipanggil dari app.py tanpa perlu instantiate class.
    """
    manager = DatasetManager(folder_path=folder_path)
    return manager.load_documents()