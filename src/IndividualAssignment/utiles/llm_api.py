
from llama_index.llms.deepseek import DeepSeek

deepseek_key = "sk-"

def get_deepseek_obj():
    llm = DeepSeek(model="deepseek-chat", api_key=deepseek_key)
    return llm

import google.generativeai as genai
genai.configure(api_key="")

def get_gemini_obj():
    llm = genai.GenerativeModel("gemini-2.5-flash")
    return llm