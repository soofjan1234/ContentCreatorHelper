from google import genai

# 设置API密钥
api_key = "AIzaSyCAxd3Zf0Xuh4_FEkqg7PJ-1ue3CK4tw44" 

# 1. 创建客户端时直接传入 API Key
client = genai.Client(api_key=api_key)

try:
    # 调用模型生成内容
    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents="Explain how AI works in a few words",
    )
    
    # 打印结果
    print("API调用成功！")
    print("生成的内容:")
    print(response.text)
except Exception as e:
    print(f"API调用失败: {str(e)}")
