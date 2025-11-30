import json

input_file = "./ground_truth.json"
output_file = "./ground_truth_retrieval.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

retrieval_gt = []

for item in data:
    query = item.get("query")
    source_id = item.get("meta", {}).get("source_id")

    if not query or not source_id:
        continue

    retrieval_gt.append({
        "query": query,
        "expected_context_ids": [str(source_id)]
    })

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(retrieval_gt, f, ensure_ascii=False, indent=4)

print("✅ DONE! File ground_truth_retrieval.json đã được tạo.")
