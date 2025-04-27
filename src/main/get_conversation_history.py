import json
import os

def get_conversation_history(WORKING_DIR: str, mode: str, history_turns: int = 3):
    cache_file_path = f"{WORKING_DIR}/kv_store_llm_response_cache.json"
    
    if (not WORKING_DIR or not mode or not os.path.exists(cache_file_path)):
        return []
    
    # Load data from file
    with open(cache_file_path, "r", encoding="utf-8") as f:
        cache_data = json.load(f)

    conversations = []

    # Combine entries from selected mode
    all_entries = list(cache_data.get(mode, {}).values())

    # Filter only entries with cache_type == "query"
    for entry in all_entries:
        if entry.get("cache_type") == "query":
            prompt = entry.get("original_prompt", "").strip()
            reply = entry.get("return", "").strip()

            conversations.append((prompt, reply))

    # Get the history_turns most recent conversations (from the end)
    recent_conversations = conversations[-history_turns:]

    # Convert to conversation_history format
    conversation_history = []
    for prompt, reply in recent_conversations:
        conversation_history.append({"role": "user", "content": prompt})
        conversation_history.append({"role": "assistant", "content": reply})

    return conversation_history

if __name__ == "__main__":
    WORKING_DIR = "./dickens_ollama"
    mode = "hybrid"
    history_turns = 2
    conversation_history = get_conversation_history(WORKING_DIR, mode, history_turns)
    print(conversation_history)