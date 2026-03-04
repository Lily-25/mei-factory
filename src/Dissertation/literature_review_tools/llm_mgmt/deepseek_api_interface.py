import json
import pandas as pd

from utils.llm_api import get_deepseek_chat_obj,get_deepseek_r1_obj
from Dissertation.literature_review_tools.llm_mgmt.prompt_generator import LiteratureReviewPrompt


class DeepSeekAPI:
    def __init__(self, model_name):
        if model_name == "Chat":
            self.model_func = get_deepseek_chat_obj
        else:
            self.model_func = get_deepseek_r1_obj

    def extract(self, prompt: str) -> dict:

        try:
            response = self.model_func(prompt)
            result = json.loads(response)
            return result
        except Exception as e:
            print(f"Error processing abstract: {e}")
            return {"challenges": ""}


    def batch_extract(self, input_file, output_file, cmd, count = 1):

        with open(input_file,
                  'r',
                  encoding='utf-8') as f:
            documents = json.load(f)

        enhanced_docs = []

        try:
            for i, doc in enumerate(documents):

                if count:
                    count = count -1
                else:
                    break

                print(f'Processing abstract: {i+1}/{len(documents)}')

                abstract = doc.get("Abstract", "")
                if not abstract.strip():
                    print(f"Document {i + 1}: No abstract found.")
                    doc.update({"challenges": ""})
                else:
                    extracted = self.extract(LiteratureReviewPrompt(abstract).get_prompt(cmd))
                    doc.update(extracted)
                enhanced_docs.append(doc)

        except Exception as e:
            print(f"Error processing abstract: {e}")
            pass

        with open(f'{output_file}.json', 'w', encoding='utf-8') as f:
            json.dump(enhanced_docs, f, ensure_ascii=False, indent=2)

        print(f"Processed {len(enhanced_docs)} documents. Saved to {output_file}")

        (pd.DataFrame(enhanced_docs).fillna("other").to_csv(f'{output_file}.csv', index=None))

if __name__ == '__main__':

    input_file = "./data/papers/midput/semi_structured_papers.json"
    output_file = "./data/papers/midput/ssp_abstract_extract_deepseek"
    cmd = "Cmd_Ext_Activity_Deepseek"

    DeepSeekAPI(model_name='Reasoner').batch_extract(input_file, output_file, cmd)

