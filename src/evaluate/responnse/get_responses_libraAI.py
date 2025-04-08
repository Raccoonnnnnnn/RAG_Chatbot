import requests
import json
import time
import re


def query_api_and_save(query_file, result1_file, mode="hybrid", top_k=5):
    url = "http://localhost:8000/query"
    headers = {"Content-Type": "application/json"}

    # Read the list of questions from the file
    with open(query_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Regex to extract the question content and remove quotes if present
    queries = [
        re.findall(r"Question \d+: (.+)", line.strip())[0].replace('"', '')
        for line in lines if line.strip()
    ]

    results = []
    successful_count = 0

    for idx, query in enumerate(queries, start=1):
        payload = {
            "query": query,
            "mode": mode,
            "top_k": top_k
        }

        print(f"Sending request {idx}: {query}")
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            api_result = response.json()

            results.append(api_result)
            successful_count += 1
            print(f"✓ Received response for question {idx}")

            # Save every 10 successful responses
            if successful_count % 10 == 0:
                with open(result1_file, "w", encoding="utf-8") as out_f:
                    json.dump(results, out_f, ensure_ascii=False, indent=4)
                print(f"💾 Auto-saved after {successful_count} successful responses")

        except requests.exceptions.RequestException as e:
            print(f"✗ Error on request {idx}: {e}")
            results.append({"result": f"ERROR: {str(e)}"})

        time.sleep(0.5)  # Optional: delay between requests

    # Final save to ensure all data is written
    with open(result1_file, "w", encoding="utf-8") as out_f:
        json.dump(results, out_f, ensure_ascii=False, indent=4)

    print(f"\n✅ All responses saved to {result1_file}")


if __name__ == "__main__":
    query_api_and_save(
        query_file="./data/questions/125_questions_for_compare.txt",        
        result1_file="./data/response_of_LLM/125_responses_libraAI.json"
        # query_file="./data/questions/45_questions_for_accuracy.txt",        
        # result1_file="./data/response_of_LLM/45_responses_libraAI.json"
    )