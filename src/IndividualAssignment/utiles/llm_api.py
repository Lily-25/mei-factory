
from llama_index.llms.deepseek import DeepSeek

deepseek_key = "sk-0021798633cc402880f809e83b285ede"

def get_deepseek_obj():
    llm = DeepSeek(model="deepseek-chat", api_key=deepseek_key)
    return llm

import google.generativeai as genai
genai.configure(api_key="AIzaSyAORjARWWKJgHYqo3CTIVPeIu2Yg5qI550")

def get_gemini_obj():
    llm = genai.GenerativeModel("gemini-2.5-flash")
    return llm