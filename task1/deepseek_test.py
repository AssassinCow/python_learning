import requests
import time
import json


API_URL = "https://api.deepseek.com/v1/chat/completions" 
API_KEY = "sk-0093f362e6ed48849f7549ea636bd49f"  

MODEL_NAME = "deepseek-chat"  
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

PROMPT_TEMPLATE = "请生成一个关于自然语言处理的基础知识点，第{}个。"

dataset = []

MAX_ITEMS = 20
SLEEP_BETWEEN_REQUESTS = 1.5  

def call_deepseek_api(prompt: str):
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return content.strip()
    except requests.exceptions.HTTPError as err:
        print(f"[错误] HTTP 请求失败：{err}")  
        return None
    except Exception as e:
        print(f"[异常] 其他错误：{e}")
        return None

for i in range(1, MAX_ITEMS + 1):
    prompt = PROMPT_TEMPLATE.format(i)
    print(f"[请求第 {i} 条数据] prompt: {prompt}")
    result = call_deepseek_api(prompt)

    if result:
        dataset.append({
            "id": i,
            "prompt": prompt,
            "response": result
        })
        print(f"[成功] 第 {i} 条完成：{result[:50]}...")
    else:
        print(f"[跳过] 第 {i} 条请求失败，跳过。")

    time.sleep(SLEEP_BETWEEN_REQUESTS)

output_file = "deepseek_dataset.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print(f"\n✅ 已生成数据集并保存到 {output_file}，共 {len(dataset)} 条数据。")
