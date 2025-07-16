import openai
import numpy as np
import json
import time
import random
import os
from collections import defaultdict
from hashlib import md5

openai.api_key = "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"

global_theorems = []
inference_tasks = []
theorem_embeddings = {}
theorem_usage = defaultdict(int)
theorem_hashes = set()


def create_embedding(text):
    try:
        response = openai.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response['data'][0]['embedding']
    except Exception as e:
        print("Embedding failed:", e)
        return None


def is_similar_to_existing_theorem(new_theorem, threshold=0.9):
    if not global_theorems:
        return False

    h = md5(new_theorem['description'].encode('utf-8')).hexdigest()
    if h in theorem_hashes:
        return True

    new_embedding = create_embedding(new_theorem['description'])
    if new_embedding is None:
        return True  

    for embedding in theorem_embeddings.values():
        denom = np.linalg.norm(new_embedding) * np.linalg.norm(embedding)
        similarity = 0 if denom < 1e-6 else np.dot(new_embedding, embedding) / denom
        if similarity > threshold:
            return True
    return False


def add_theorem(theorem):
    if not is_similar_to_existing_theorem(theorem):
        global_theorems.append(theorem)
        embedding = create_embedding(theorem['description'])
        if embedding is not None:
            theorem_embeddings[theorem['id']] = embedding
            theorem_usage[theorem['id']] = 0
            h = md5(theorem['description'].encode('utf-8')).hexdigest()
            theorem_hashes.add(h)


def select_theorems_for_gpt(k=3):
    if not global_theorems:
        return []
    usage = np.array([theorem_usage[t['id']] for t in global_theorems])
    temperature = 0.8
    norm_usage = (usage - usage.min()) / (usage.max() - usage.min() + 1e-8)
    preference = 1.0 - norm_usage
    weights = np.exp(preference / temperature)
    weights /= weights.sum()
    idxs = np.random.choice(len(global_theorems), size=min(k, len(global_theorems)), replace=False, p=weights)
    selected = [global_theorems[i] for i in idxs]
    for t in selected:
        theorem_usage[t['id']] += 1
    return selected


def generate_theorem_with_gpt():
    prompt = "Please generate a concise mathematical theorem suitable for mathematical reasoning tasks. Only output the theorem statement, no explanation."
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            timeout=30
        )
        desc = response.choices[0].message.content.strip().replace('\n', ' ')
        theorem = {"id": f"theorem_{len(global_theorems)}", "description": desc}
        add_theorem(theorem)
        print(f"Generated theorem {theorem['id']}")
        return [theorem]
    except Exception as e:
        print("Theorem generation failed:", e)
        return []


def generate_inference_task_with_gpt(task_id, theorems_for_gpt):
    if theorems_for_gpt:
        theorems_json = json.dumps(theorems_for_gpt, ensure_ascii=False, indent=2)
        prompt = (
            "Based on the following theorem library, generate a mathematical reasoning task, including premises (2-3 items), target_conclusion, "
            "and detailed inference_steps (each step includes step, applied_theorem_id, result). Theorem library:\n"
            + theorems_json +
            "\nPlease output in JSON format: {\"premises\": [...], \"target_conclusion\": \"...\", \"inference_steps\": [...] }"
        )
    else:
        prompt = (
            "Please generate a mathematical reasoning task, including premises (2-3 items), target_conclusion, "
            "and detailed inference_steps (each step includes step, applied_theorem_id, result). "
            "Please output in JSON format: {\"premises\": [...], \"target_conclusion\": \"...\", \"inference_steps\": [...] }"
        )
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            timeout=60
        )
        content = response.choices[0].message.content
        task_json = json.loads(content)
        for step in task_json.get("inference_steps", []):
            tid = step.get("applied_theorem_id")
            if tid and tid not in [t['id'] for t in global_theorems]:
                add_theorem({"id": tid, "description": step.get("result", "")})
        task = {
            "id": f"task_{task_id}",
            "premises": task_json["premises"],
            "target_conclusion": task_json["target_conclusion"],
            "inference_steps": task_json["inference_steps"]
        }
        inference_tasks.append(task)
        print(f"Generated reasoning task task_{task_id}")
        return True
    except json.JSONDecodeError as je:
        print("JSON decode error:", je)
        return False
    except Exception as e:
        print("Task generation failed:", e)
        return False

max_tasks = 500
max_fail = 10
fail_count = 0
task_id = 1

while len(inference_tasks) < max_tasks and fail_count < max_fail:
    try:
        if random.random() < 0.6:
            theorems_for_gpt = generate_theorem_with_gpt()
        else:
            theorems_for_gpt = select_theorems_for_gpt()

        success = generate_inference_task_with_gpt(task_id, theorems_for_gpt)
        if success:
            task_id += 1
            fail_count = 0
        else:
            fail_count += 1

        if task_id % 50 == 0:
            with open(f'dataset_checkpoint_{task_id}.json', 'w', encoding='utf-8') as f:
                json.dump({"global_theorems": global_theorems, "inference_tasks": inference_tasks}, f, indent=4, ensure_ascii=False)

        time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped by user.")
        break
    except Exception as e:
        print("Unexpected error:", e)
        fail_count += 1
        time.sleep(2)

output_data = {
    "global_theorems": global_theorems,
    "inference_tasks": inference_tasks
}

with open('dataset.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=4, ensure_ascii=False)

print("Reasoning dataset has been generated and saved as dataset.json")
