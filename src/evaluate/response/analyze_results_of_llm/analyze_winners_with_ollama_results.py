import json
from collections import defaultdict

def analyze_results(file_path):
    total_count = 0
    overall_winner_count = defaultdict(int)
    criteria_winner_count = defaultdict(lambda: defaultdict(int))  # criteria -> answer -> count

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                result = json.loads(line)
                total_count += 1

                # Count overall winner
                overall = result.get("Overall Winner", {})
                winner = overall.get("Winner", "")
                if winner:
                    overall_winner_count[winner] += 1

                # Count each criteria
                for criterion, value in result.items():
                    if criterion == "Overall Winner":
                        continue
                    winner = value.get("Winner", "")
                    if winner:
                        criteria_winner_count[criterion][winner] += 1

            except json.JSONDecodeError as e:
                print(f"❌ Error parsing JSON on line {total_count + 1}: {e}")

    # Print summary
    print(f"✅ Processed {total_count} results\n")
    print("🏆 Overall Winner Counts:")
    for answer, count in overall_winner_count.items():
        print(f" - {answer}: {count} times")

    print("\n📊 Criteria Breakdown:")
    for criterion, winners in criteria_winner_count.items():
        print(f"\n🔹 {criterion}")
        for answer, count in winners.items():
            print(f"   - {answer}: {count} times")


if __name__ == "__main__":
    analyze_results("./data/response_of_LLM/125_responses_eval_qwen2_revert.jsonl")