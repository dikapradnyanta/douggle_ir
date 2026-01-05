import json
import os
from datetime import datetime

def precision_at_k(retrieved_docs, relevant_docs, k):
    """Calculate precision@k"""
    if k == 0:
        return 0.0
    retrieved_k = retrieved_docs[:k]
    relevant_count = sum(1 for doc in retrieved_k if doc in relevant_docs)
    return relevant_count / k

def recall_at_k(retrieved_docs, relevant_docs, k):
    """Calculate recall@k"""
    if not relevant_docs or len(relevant_docs) == 0:
        return 0.0
    retrieved_k = retrieved_docs[:k]
    relevant_count = sum(1 for doc in retrieved_k if doc in relevant_docs)
    return relevant_count / len(relevant_docs)

def f1_score_at_k(precision, recall):
    """Calculate F1-Score@k"""
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

def mean_average_precision(retrieved_docs_list, relevant_docs_list):
    """Calculate Mean Average Precision (MAP)"""
    average_precisions = []
    
    for retrieved_docs, relevant_docs in zip(retrieved_docs_list, relevant_docs_list):
        precision_values = []
        relevant_found = 0
        
        for k in range(1, len(retrieved_docs) + 1):
            if retrieved_docs[k-1] in relevant_docs:
                relevant_found += 1
                precision_at_k = relevant_found / k
                precision_values.append(precision_at_k)
        
        if not precision_values:
            average_precisions.append(0.0)
        else:
            average_precisions.append(sum(precision_values) / len(relevant_docs))
    
    return sum(average_precisions) / len(average_precisions) if average_precisions else 0.0

def evaluate_system(retrieved_docs_list, relevant_docs_list, k_values=[1, 3, 5, 10]):
    """
    Evaluate system comprehensively
    Returns: dict with metrics for each k
    """
    results = {}
    
    for k in k_values:
        precision_list = []
        recall_list = []
        f1_list = []
        
        for retrieved_docs, relevant_docs in zip(retrieved_docs_list, relevant_docs_list):
            precision = precision_at_k(retrieved_docs, relevant_docs, k)
            recall = recall_at_k(retrieved_docs, relevant_docs, k)
            f1 = f1_score_at_k(precision, recall)
            
            precision_list.append(precision)
            recall_list.append(recall)
            f1_list.append(f1)
        
        results[k] = {
            "precision_avg": round(sum(precision_list) / len(precision_list), 4) if precision_list else 0.0,
            "recall_avg": round(sum(recall_list) / len(recall_list), 4) if recall_list else 0.0,
            "f1_avg": round(sum(f1_list) / len(f1_list), 4) if f1_list else 0.0,
        }
    
    # Calculate MAP
    map_score = mean_average_precision(retrieved_docs_list, relevant_docs_list)
    results['MAP'] = round(map_score, 4)
    
    return results

def auto_save_evaluation(query, retrieved_docs, relevant_docs, metrics, folder="evaluasi"):
    """
    Auto-save evaluation results to folder
    """
    # Create folder if not exists
    os.makedirs(folder, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{folder}/evaluation_{timestamp}.json"
    
    # Prepare data
    eval_data = {
        "timestamp": timestamp,
        "query": query,
        "retrieved_docs": retrieved_docs,
        "relevant_docs": relevant_docs,
        "metrics": metrics,
        "summary": {
            "num_retrieved": len(retrieved_docs),
            "num_relevant": len(relevant_docs),
            "relevant_in_top_10": sum(1 for doc in retrieved_docs[:10] if doc in relevant_docs)
        }
    }
    
    # Save to file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(eval_data, f, indent=2, ensure_ascii=False)
    
    return filename

def load_evaluations(folder="evaluasi"):
    """
    Load all evaluations from folder
    """
    if not os.path.exists(folder):
        return []
    
    evaluations = []
    for file in os.listdir(folder):
        if file.endswith('.json'):
            filepath = os.path.join(folder, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    evaluations.append(data)
            except:
                continue
    
    return sorted(evaluations, key=lambda x: x['timestamp'], reverse=True)

# Demo mode
if __name__ == "__main__":
    # Example usage
    retrieved = list(range(10))
    relevant = [1, 3, 5, 7, 9]
    
    metrics = evaluate_system([retrieved], [relevant])
    
    print("Evaluation Results:")
    for k, m in metrics.items():
        if k != 'MAP':
            print(f"K={k}: Precision={m['precision_avg']}, Recall={m['recall_avg']}, F1={m['f1_avg']}")
    print(f"MAP: {metrics['MAP']}")
    
    # Auto save example
    saved_file = auto_save_evaluation("test query", retrieved, relevant, metrics)
    print(f"\nSaved to: {saved_file}")