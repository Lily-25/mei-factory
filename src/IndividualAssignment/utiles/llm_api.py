
from llama_index.llms.deepseek import DeepSeek

deepseek_key = "sk-0021798633cc402880f809e83b285ede"

def get_deepseek_obj():
    llm = DeepSeek(model="deepseek-chat", api_key=deepseek_key)
    return llm