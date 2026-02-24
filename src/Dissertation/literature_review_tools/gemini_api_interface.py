import json
import pandas as pd

from src.IndividualAssignment.utiles.llm_api import get_gemini_obj
from src.Dissertation.literature_review_tools.prompt_generator import LiteratureReviewPrompt

llm = get_gemini_obj()


def extract_challenge_method_findings(prompt: str) -> dict:
    try:
        response = llm.generate_content(prompt)
        result = json.loads(response.text)
        return result
    except Exception as e:
        print(f"Error processing abstract: {e}")
        return {"challenges": ""}


def batch_extract_challenge_method_findings(input_file, output_file, cmd):
    with open(input_file,
              'r',
              encoding='utf-8') as f:
        documents = json.load(f)

    enhanced_docs = []

    try:
        count = 1000
        for i, doc in enumerate(documents):

            if count:
                count = count - 1
            else:
                break

            abstract = doc.get("Abstract", "")
            if not abstract.strip():
                print(f"Document {i + 1}: No abstract found.")
                doc.update({"challenges": ""})
            else:
                extracted = extract_challenge_method_findings(LiteratureReviewPrompt(abstract).get_prompt(cmd))
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
    input_file = "../data/papers/midput/semi_structured_papers.json"
    output_file = "../data/papers/midput/ssp_abstract_extract_gemini"
    cmd = "Cmd_Ext_Activity_Gemini"

    batch_extract_challenge_method_findings(input_file, output_file, cmd)
