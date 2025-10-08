import pandas as pd
import json
from src.IndividualAssignment.utiles.llm_api import get_deepseek_obj

llm = get_deepseek_obj()

prompt_parallel_review  = {
    'zh': """
请你扮演一个专业的商业分析专家，专注于技术创新领域. 在"龙灵山生态公园自动驾驶主题景区项目"网络调研问卷的同行评审任务中，需要你发挥你的专业知识和正直的职业操守对以下两位大模型的对问卷中问题的调研结果进行匿名评审。

以下调查问卷的背景
******
针对"龙灵山生态公园自动驾驶主题景区项目"完成一份网络调研问卷。根据用户提供的调研问题清单，对“龙灵山生态公园2020年引入无人驾驶技术创新”后续发展进行分析。分析过程中请谨记：
问卷反馈信息：
  - `score`：问题评分，范围-5到5。
  - `reasoning`：打分原因，基于网络信息的中肯总结，明确列出优势、劣势或不确定性，并注明引用来源的文章标题和发布时间。
评分标准：
   - 【-5, -3】：显著落后于行业水平，存在明显短板或问题。
   - 【-2, 0】：略低于或基本达到行业基准，但无突出优势。
   - 【1, 3】：部分环节表现优于行业平均水平，具备一定特色。
   - 【4, 5】：在技术、模式或用户体验上具有行业领先优势。
******

你的任务是基于以下标准，为每位代表的回答分别打分（1-10分，10分为最高），并提供具体的评审理由。

评审标准：
- 准确性：回答是否基于可靠信息，是否存在事实错误或误导性内容。
- 完整性：是否全面覆盖了问题的核心要点，有无遗漏关键信息。
- 逻辑性：回答的结构是否清晰，论证是否合理，逻辑是否严密。
- 可溯源：引用参考的信息真实可靠。

需评审的回答：
问题：{question}
代表A的回答：{answer_from_A}
代表B的回答：{answer_from_B}

你的任务：
分别对代表A和代表B的回答进行打分（1-10分）。
为每个打分提供详细的理由，结合评审标准逐条分析其优点和不足。
在评审结束时，总结两个回答的整体表现，并提出该问卷调研问题的建议评分【-5，5】。
请确保评审过程客观、公正，避免个人偏好影响判断。

评分标准：
9-10: 优秀：完全准确、完整、逻辑强、可溯源
7-8: 良好：基本准确， minor issues
5-6: 中等：一些错误或遗漏
3-4: 差： significant errors
1-2: 极差：完全错误

输出要求：
- 格式：严格按照JSON数组格式输出，不要包含Markdown。
- 内容：每个问题对应一个对象，按顺序包含且仅包含以下两个字段：
  - `A Score`：整数，范围1-10。
  - `B Score`：整数，范围1-10。
  - `Recommend Score`：整数，范围【-5，5】。
  - `reasoning`：字符串，基于网络信息的中肯总结，明确列出优势、劣势或不确定性，并注明引用来源的文章标题和发布时间

请直接基于网络信息进行分析，不要美化结果。请现在开始分析
""",
    'en': ""
}

def generate_extraction_prompt(question,
                               answer_from_A,
                               answer_from_B,
                               lang='zh'):
    """生成信息抽取的prompt"""
    template = prompt_parallel_review[lang]
    return template.format(question = question,
                           answer_from_A=answer_from_A,
                           answer_from_B=answer_from_B)

def construct_review_prompt():
    file_path_a = 'data/input/qwen.json'
    file_path_b = 'data/input/ernie.json'
    file_path_c = 'data/input/deepseek.json'

    json_a = pd.read_json(file_path_a)
    json_b = pd.read_json(file_path_b)
    json_c = pd.read_json(file_path_c)

    df = pd.read_csv('IndividualAssignment/SWOT/data/framework/Introduce_innovation.csv', sep='\t')

    question_list = []
    a_list = []
    b_list = []
    c_list = []
    prompt_a_list = []
    prompt_b_list = []
    prompt_c_list = []

    for index in range(len(json_a)):
        a_score = json_a.iloc[index].to_json(force_ascii=False)
        b_score = json_b.iloc[index].to_json(force_ascii=False)
        c_score = json_c.iloc[index].to_json(force_ascii=False)
        question = df.iloc[index]['Survey Question']

        question_list.append(question)
        a_list.append(a_score)
        b_list.append(b_score)
        c_list.append(c_score)

        prompt = generate_extraction_prompt(question,
                                            b_score,
                                            c_score)

        prompt_a_list.append(prompt)
        prompt = generate_extraction_prompt(question,
                                            a_score,
                                            c_score)

        prompt_b_list.append(prompt)
        prompt = generate_extraction_prompt(question,
                                            a_score,
                                            b_score)

        prompt_c_list.append(prompt)


    review_prompt_df = pd.DataFrame({'question':question_list,
                                     'qwen': a_list,
                                     'ernie': b_list,
                                     'deepseek': b_list,
                                     'prompt_qwen': prompt_a_list,
                                     'prompt_ernie': prompt_b_list,
                                     'prompt_deepseek': prompt_c_list})
    review_prompt_df.to_csv('data/mid/review_prompt.csv')

def rate_as_reviewer(reviewers=['deepseek']):

    construct_review_prompt()
    df = pd.read_csv('data/mid/review_prompt.csv', index_col=0)

    for reviewer in reviewers:
        try:
            tag_prompt = f'prompt_{reviewer}'
            tag_outcome = f'outcome_{reviewer}'
            tag_filename = f'data/mid/review_{reviewer}.csv'

            outcome_list = []

            for _, row in df.iterrows():
                response = llm.complete(row[tag_prompt])
                response_json = json.loads(response.text)

                outcome_list.append(response_json)

            df[tag_outcome] = outcome_list

            df.to_csv(tag_filename)
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':

    rate_as_reviewer()
