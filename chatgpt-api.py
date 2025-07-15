import os
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage


# # 初始化模型
# chat = ChatOpenAI(
#     model="gpt-4o-mini",
#     api_key=os.getenv("OPENAI_API_KEY"),
# )

# try:
#     # 发出简单请求
#     response = chat([HumanMessage(content="你好，GPT，现在能听到我说话吗？")])
#     print("✅ GPT 响应成功：\n", response.content)
# except Exception as e:
#     print("❌ GPT 请求失败：\n", str(e))

# try:
#     # 发出简单请求
#     response = chat([HumanMessage(content="你好，能不能教一下我python的常用库呢？")])
#     print("✅ GPT 响应成功：\n", response.content)
# except Exception as e:
#     print("❌ GPT 请求失败：\n", str(e))



from openai import OpenAI 

client=ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

response=client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role":"user","content":"请说明api的具体用途"}
    ]
)

print(response)



