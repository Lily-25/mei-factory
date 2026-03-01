import pandas as pd

from Dissertation.literature_review_tools.llm_mgmt.deepseek_api_interface import batch_extract as batch_extract_by_deepseek

class AssessPapers:

    """use LLM to judge the relevance of the papers. The principles are as follows:
    - use Deepseek to assess the relevance between topics discussed in papers and knowledge retention
    - review the result, and make a thread to choose highly relevant papers.
    """

    def __init__(self):
        pass

    @staticmethod
    def assess_relevance_by_deepseek():
        input_file = "../data/papers/midput/semi_structured_papers.json"
        output_file = "../data/papers/midput/ssp_extract_relevance_deepseek"
        cmd = "Cmd_Ext_Relevance"

        batch_extract_by_deepseek(input_file, output_file, cmd, count=1000)

    @staticmethod
    def select_papers_by_relevance():
        input_file = "../data/papers/midput/ssp_extract_relevance_deepseek.csv"
        output_file = "../data/papers/midput/ssp_extract_relevance"

        df = pd.read_csv(input_file)

        filtered_df = df[(df['relevance'] > 0.5) | (df['approaches'].apply(len) > 2)]

        cols_to_drop = ['challenges',
                        'methods',
                        'findings',
                        'knowledge_flows',
                        'tacit_knowledge_types',
                        'approaches']
        filtered_df = filtered_df.drop(columns=cols_to_drop)

        filtered_df.to_csv(f'{output_file}.csv', index=None)
        filtered_df.to_json(f'{output_file}.json', orient='records')


if __name__ == '__main__':
    # AssessPapers.assess_relevance_by_deepseek()
    AssessPapers.select_papers_by_relevance()