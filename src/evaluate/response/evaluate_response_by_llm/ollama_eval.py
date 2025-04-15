import asyncio
import re
import json
from lightrag.llm.ollama import ollama_model_complete

async def batch_eval_ollama(query_file, result1_file, result2_file, output_file_path):
    # Read the list of questions from the file
    with open(query_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Regex to extract the question content and remove quotes if present
    queries = [
        re.findall(r"Question \d+: (.+)", line.strip())[0].replace('"', '')
        for line in lines if line.strip()
    ]

    with open(result1_file, "r") as f:
        answers1 = json.load(f)
    answers1 = [i["response"] for i in answers1]

    with open(result2_file, "r") as f:
        answers2 = json.load(f)
    answers2 = [i["response"] for i in answers2]

    output = []
    
    for i, (query, answer1, answer2) in enumerate(zip(queries, answers1, answers2)):
        sys_prompt = """
        ---Role---
        You are an expert tasked with evaluating two answers to the same question based on three criteria: **Comprehensiveness**, **Diversity**, and **Empowerment**.
        """

        prompt = f"""
        You will evaluate two answers to the same question based on three criteria: **Comprehensiveness**, **Diversity**, and **Empowerment**.

        - **Comprehensiveness**: How much detail does the answer provide to cover all aspects and details of the question?
        - **Diversity**: How varied and rich is the answer in providing different perspectives and insights on the question?
        - **Empowerment**: How well does the answer help the reader understand and make informed judgments about the topic?

        For each criterion, choose the better answer (either Answer 1 or Answer 2) and explain why. Then, select an overall winner based on these three categories.

        Here is the question:
        {query}

        Here are the two answers:

        **Answer 1:**
        {answer1}

        **Answer 2:**
        {answer2}

        Evaluate both answers using the three criteria listed above and provide detailed explanations for each criterion.

        Output your evaluation in the following JSON format:

        {{
            "Comprehensiveness": {{
                "Winner": "[Answer 1 or Answer 2]",
                "Explanation": "[Provide explanation here]"
            }},
            "Empowerment": {{
                "Winner": "[Answer 1 or Answer 2]",
                "Explanation": "[Provide explanation here]"
            }},
            "Overall Winner": {{
                "Winner": "[Answer 1 or Answer 2]",
                "Explanation": "[Summarize why this answer is the overall winner based on the three criteria]"
            }}
        }}
        """

        print(f"Processing Question {i+1}/{len(queries)}")
        
        try:
            result = await ollama_model_complete(
                prompt=prompt,
                system_prompt=sys_prompt,
                stream=False,
                format="json"
            )
            output.append(json.loads(result))
        except Exception as e:
            print(f"❌ Error on Question {i}: {e}")
            output.append({"error": str(e)})

        # Ghi sau mỗi 10 dòng
        if i % 10 == 0 or i == len(queries):
            with open(output_file_path, "a", encoding="utf-8") as f:
                for entry in output:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            output = []  # reset buffer

    print(f"✅ Finished evaluating {len(queries)} questions.")


if __name__ == "__main__":
    query_file = "./data/questions/125_questions_for_compare.txt"
    result1_file = "./data/response_of_LLM/125_responses_tikiAI.json"
    result2_file = "./data/response_of_LLM/125_responses_libraAI.json"
    output_file_path = "./data/response_of_LLM/125_responses_eval_qwen2_revert.jsonl"
    asyncio.run(batch_eval_ollama(query_file, result1_file, result2_file, output_file_path))
