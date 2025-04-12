import json

# Đọc dữ liệu từ 2 file JSON
with open('./data/response_of_LLM/125_responses_tikiAI.json', 'r', encoding='utf-8') as f1:
    libra_data = json.load(f1)

with open('./data/response_of_LLM/125_responses_libraAI.json', 'r', encoding='utf-8') as f2:
    tiki_data = json.load(f2)

# Gộp dữ liệu theo chỉ số (giả định 2 file có cùng thứ tự câu hỏi)
merged_data = []
for idx, (libra, tiki) in enumerate(zip(libra_data, tiki_data), start=1):
    merged_data.append({
        "number": idx,
        "question": libra["question"], 
        "answer_tiki": libra["response"],
        "answer_libra": tiki["response"]
    })

# Ghi ra file mới
with open('./data/response_of_LLM/merged_responses.json', 'w', encoding='utf-8') as outfile:
    json.dump(merged_data, outfile, ensure_ascii=False, indent=2)

print("Đã gộp dữ liệu thành công vào merged_responses.json")