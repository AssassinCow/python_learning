import os
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage


# 初始化模型
chat = ChatOpenAI(
    model="gpt-4o-mini",
    api_key="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",
)

try:
    # 发出简单请求
    response = chat([HumanMessage(content="你好，GPT，现在能听到我说话吗？")])
    print("✅ GPT 响应成功：\n", response.content)
except Exception as e:
    print("❌ GPT 请求失败：\n", str(e))



# from openai import OpenAI 

# client=OpenAI(
#     api_key="sk-0093f362e6ed48849f7549ea636bd49f",
#     base_url="https://api.deepseek.com",
# )

# response=client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role":"user","content":"请说明api的具体用途"}
#     ]
# )

# print(response)


