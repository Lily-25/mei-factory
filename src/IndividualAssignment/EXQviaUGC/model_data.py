import json
import os
import pandas as pd

from src.IndividualAssignment.utiles.llm_api import get_deepseek_obj
llm = get_deepseek_obj

class EXQPromptConstructor:
    def __init__(self):
        self.base_prompt = """角色：你是一名专业的用户体验量化分析师，精通使用Klaus & Maklan (2013)提出的EXQ模型。

任务：根据用户提供的文本评价和图片描述，对"自动驾驶服务"进行用户体验质量评估。

模型框架：请严格按照EXQ模型的四个核心维度进行分析：
1. 服务体验（Service Experience）：关注服务的核心功能、可靠性与问题解决能力。服务是否如承诺般可靠、有效地完成了任务？
2. 时刻惊喜（Moment of Surprise）：关注服务是否创造了超越常规的、令人惊喜或愉悦的积极时刻。
3. 产品体验（Product Experience）：关注作为"产品"本身的易用性、界面设计、舒适度及技术流畅性。
4. 目标达成（Goal Achievement）：关注服务在多大程度上帮助用户实现了其深层的个人目标与价值。

输入数据：
- 文本评价：{text_review}
- 图片描述：{image_description}

输出要求：
- 以纯JSON格式输出，无需任何额外解释。
- JSON结构必须完全遵循以下示例：

{json_format_example}

评分规则：
- 所有分数均为 -5 到 +5 之间的整数。
- -5至-1：负面（-5=极度糟糕，-1=略有不足）
- 0：中性/未提及
- +1至+5：正面（+1=略有积极，+5=极度出色）
- comprehensive_score（综合得分）是该维度下所有sub_scores的算术平均值（四舍五入取整）。
- comprehensive_scores_summary中的每个分数，直接对应其下方同名维度中的 comprehensive_score 值。
- rationale（评分依据）必须直接引用或紧密关联输入数据中的文本和图片信息，清晰说明打分的来源。避免主观臆断。"""

        self.json_format = {
            "exq_analysis": {
                "comprehensive_scores_summary": {
                    "service_experience": 0,
                    "moment_of_surprise": 0,
                    "product_experience": 0,
                    "goal_achievement": 0
                },
                "service_experience": {
                    "comprehensive_score": 0,
                    "sub_scores": {
                        "reliability": 0,
                        "effectiveness": 0,
                        "problem_resolution": 0
                    },
                    "rationale": ""
                },
                "moment_of_surprise": {
                    "comprehensive_score": 0,
                    "sub_scores": {
                        "positive_surprise": 0,
                        "delight": 0,
                        "memorability": 0
                    },
                    "rationale": ""
                },
                "product_experience": {
                    "comprehensive_score": 0,
                    "sub_scores": {
                        "ease_of_use": 0,
                        "comfort": 0,
                        "interface_design": 0
                    },
                    "rationale": ""
                },
                "goal_achievement": {
                    "comprehensive_score": 0,
                    "sub_scores": {
                        "efficiency_gain": 0,
                        "peace_of_mind": 0,
                        "value_alignment": 0
                    },
                    "rationale": ""
                }
            }
        }

    def construct_prompt(self, text_review, image_description):
        """
            构造EXQ分析prompt

            Args:
                text_review (str): 用户文本评价
                image_description (str): 图片描述

            Returns:
                str: 完整的prompt字符串
            """
        json_example = json.dumps(self.json_format, indent=2, ensure_ascii=False)

        prompt = self.base_prompt.format(
            text_review=text_review,
            image_description=image_description,
            json_format_example=json_example
        )

        return prompt

    def batch_construct_prompts(self, data_list):
        """
            批量构造prompts

            Args:
                data_list (list): 包含多个字典的列表，每个字典包含text_review和image_description

            Returns:
                dict: 以数据ID为key，prompt为value的字典
            """
        prompts = {}
        for i, data in enumerate(data_list):
            prompt_id = f"prompt_{i + 1:03d}"
            prompts[prompt_id] = self.construct_prompt(
                data['text_review'],
                data['image_description']
            )
        return prompts

    def save_prompts(self, prompts, output_dir="output_prompts"):
        """
            保存prompts到文件

            Args:
                prompts (dict): 由batch_construct_prompts返回的prompts字典
                output_dir (str): 输出目录
            """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for prompt_id, prompt_content in prompts.items():
            filename = f"{prompt_id}.txt"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(prompt_content)

            print(f"已保存: {filepath}")


def rate_with_exq_model():
    # 初始化构造器
    constructor = EXQPromptConstructor()

    df = pd.read_csv('data/mid/data_from_dianping.csv')
    response_list = []
    rate_list = []
    for row in df.itertuples():

          single_prompt = constructor.construct_prompt(row.driving_text_content, row.driving_picture_topic)
          try:
              response = llm.complete(single_prompt)
              rate_list.append(json.loads(response.text)['exq_analysis']['comprehensive_scores_summary'])
              response_list.append(json.loads(response.text))
          except Exception as e:
              print(e)
              pass

    df = pd.DataFrame(rate_list)
    df.to_csv('data/output/review_from_dianping.csv')

    with open('data/output/review_from_dianping.txt', 'w', encoding='utf-8') as f:
        for item in response_list:
            json_str = json.dumps(item, ensure_ascii=False, indent=2)
            f.write(json_str)


def read_concatenated_json(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

        # 方法1：使用栈平衡法解析
        start_index = 0
        stack = []

        for i, char in enumerate(content):
            if char == '{':
                stack.append(char)
            elif char == '}':
                if stack:
                    stack.pop()
                if not stack:  # 栈为空，表示一个完整的JSON对象结束
                    try:
                        json_str = content[start_index:i + 1]
                        obj = json.loads(json_str)
                        data.append(obj)
                        start_index = i + 1  # 下一个对象开始位置
                    except json.JSONDecodeError:
                        # 如果解析失败，继续寻找下一个
                        start_index = i + 1

        return data

def combine_raw_and_rate_data():
    raw_df = pd.read_csv('data/mid/data_from_dianping.csv', index_col=0)
    rate_df = pd.read_csv('data/output/review_from_dianping.csv', index_col=0)
    explain_df = pd.DataFrame(read_concatenated_json('data/output/review_from_dianping.txt'))

    df = pd.concat([raw_df, rate_df, explain_df], axis=1)
    df.to_csv('data/output/rate_result.csv')



if __name__ == "__main__":
    combine_raw_and_rate_data()