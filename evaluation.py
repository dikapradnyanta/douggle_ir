def precision_at_k(retrieved_docs, relevant_docs, k):
    if k == 0:
        return 0.0
    retrieved_k = retrieved_docs[:k]
    relevant_count = sum(1 for doc in retrieved_k if doc in relevant_docs)
    return relevant_count / k


def recall_at_k(retrieved_docs, relevant_docs, k):
    if not relevant_docs:
        return 0.0
    retrieved_k = retrieved_docs[:k]
    relevant_count = sum(1 for doc in retrieved_k if doc in relevant_docs)
    return relevant_count / len(relevant_docs)


def evaluate_system(retrieved_docs, relevant_docs, k):
    precision = precision_at_k(retrieved_docs, relevant_docs, k)
    recall = recall_at_k(retrieved_docs, relevant_docs, k)
    return {
        "precision": precision,
        "recall": recall
    }


if __name__ == "__main__":
    retrieved = ["D1", "D2", "D3", "D4", "D5"]
    relevant = ["D2", "D4"]
    k = 3

    result = evaluate_system(retrieved, relevant, k)
    print("Evaluation Result:", result)