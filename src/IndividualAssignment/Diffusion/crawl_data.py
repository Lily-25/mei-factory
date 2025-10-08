import pandas as pd
import json
from src.IndividualAssignment.utiles.llm_api import get_deepseek_obj

llm = get_deepseek_obj

prompt_extraction_keyword = {
    'zh': """角色：你是一位严谨的商业分析专家，专注于技术创新领域。现在需要你针对"武汉自动驾驶技术创新扩散"完成一份网络调研问卷。

任务：根据用户提供的调研问题清单，对“武汉自动驾驶技术创新扩散”后续发展进行分析。分析过程中请谨记：
1. 客观中立：严格基于公开的网络信息进行分析，禁止任何形式的美化或主观臆断。如信息不足或存在争议，请在理由中明确说明。
2. 引用要求：所有reasoning中引用的网络信息必须注明具体的文章标题和发布时间。
3. 评分基准：以当前同类智慧景区项目为基准进行对比。
4. 评分标准：
   - 【-5, -3】：显著落后于行业水平，存在明显短板或问题。
   - 【-2, 0】：略低于或基本达到行业基准，但无突出优势。
   - 【1, 3】：部分环节表现优于行业平均水平，具备一定特色。
   - 【4, 5】：在技术、模式或用户体验上具有行业领先优势。

输入数据：调研问题清单
{questionnaire_list}

输出要求：
- 格式：严格按照JSON数组格式输出，不要包括Markdown。
- 内容：每个问题对应一个对象，按顺序包含且仅包含以下两个字段：
  - `score`：整数，范围-5到5。
  - `reasoning`：基于网络信息的中肯总结，明确列出优势、劣势或不确定性，并注明引用来源的文章标题和发布时间。JSON格式输出，其中包含
    - `advantages`： 项目优势
    - `disadvantages`： 项目劣势
    - `unknown factors`： 没有检索到的信息
    - `reference`： 引用来源的文章标题和发布时间
    
请直接基于网络信息进行分析，不要美化结果。请现在开始分析""",
    'en': ""
}


def generate_extraction_prompt(questionnaire_list, lang='zh'):
    """生成信息抽取的prompt"""
    template = prompt_extraction_keyword[lang]
    return template.format(questionnaire_list=questionnaire_list)


def json_to_dataframe(json_data_list):
    """
    将JSON数据列表转换为DataFrame
    """
    # 如果输入是单个JSON对象，转换为列表
    if isinstance(json_data_list, dict):
        json_data_list = [json_data_list]

    # 创建DataFrame
    df = pd.DataFrame(json_data_list)
    return df

def crawl_unverified_answer(file_path, model_type='DeepSeek'):
    # 使用示例

    prompt = generate_extraction_prompt(get_questionnaire_list(file_path))
    print(f'enter crawl_unverified_answer with \n'
          f'file_path : {file_path},\n'
          f'model_type : {model_type},\n'
          f'prompt : {prompt}')

    try:

        if model_type == 'DeepSeek':
            response = llm.complete(prompt)
            response_json = json.loads(response.text)
            with open('data/input/deepseek.json', 'w', encoding='utf-8') as f:
                json.dump(response_json, f, indent=4, ensure_ascii=False)

            df = json_to_dataframe(response_json)
            df.to_csv('data/input/data_search_by_deepseek.csv')

        elif model_type == 'ERNIE':
            df = pd.read_json('data/input/ernie.json')
            df.to_csv('data/input/data_search_by_ernie.csv')

            pass

        elif model_type == 'ChatGPT':
            pass

        elif model_type == 'Qwen':
            df = pd.read_json('data/input/qwen.json')
            df.to_csv('data/input/data_search_by_qwen.csv')

        else:
            pass

    except Exception as e:
        print(e)
        pass


def get_questionnaire_list(file_path):

    df = pd.read_csv(file_path, sep='\t')

    return '\n'.join(df['Survey Question'].tolist())

if __name__ == '__main__':
    file_path = 'data/framework/diffusion_questionnaire'

    crawl_unverified_answer(file_path, model_type='')

