
from llama_index.llms.deepseek import DeepSeek

deepseek_key = ""

def get_deepseek_obj():
    llm = DeepSeek(model="deepseek-chat", api_key=deepseek_key)
    return llm