from http.client import responses

import pandas as pd
import json

from src.IndividualAssignment.utiles.llm_api import get_deepseek_obj
llm = get_deepseek_obj

prompt_extraction_keyword = {
    'zh': "你是一个专业的信息抽取助手。请从以下用户评价中，严格准确地抽取出指定的关键信息。对自动驾驶相关的描述最大程度保持用户原始描述"
          "**抽取字段说明：**"
          "- **User Level（用户级别）**：提取用户自称的或评价中提到的级别，如'Lv5'、'Lv4'、等。如果没有提及，则返回空字符串 ''。"
          "- **Date（评价时间）**：提取评价中明确提到的时间、日期或相对时间（如'昨天'、'上周'、'2023年国庆'）。将其规范化为 YYYY-MM-DD 格式。如果无法确定具体日期，则返回空字符串 ''。"
          "- **Text Content（文本评价内容）**：这是评价的核心文本，需要完整提取。请去除问候语、无关的感叹词等，保留对产品/服务本身的核心描述。"
          "- **Self-driving Text Content（自动驾驶相关文本评价内容）**：这是文本评价中关于自动驾驶相关的描述，需要完整提取。请去除问候语、无关的感叹词等，保留对自动驾驶产品/服务本身的核心描述。"
          "- **Picture Topic（图片分享）**：如果评价中提到分享了图片或图片内容（例如'拍了张照片'、'上图是...'），请用一句话总结图片的主题或内容（例如：'展示产品开裂的细节'）。如果没有提及，则返回空字符串 ''。"
          "- **Self-driving Picture Topic（图片分享）**：如果评价中提到分享了图片或图片内容（例如'拍了张照片'、'上图是...'），请用检查其中是否有关于自动驾驶相关的内容，如果有请提取相关描述；如果没有提及，则返回空字符串 ''。"
          ""
          "**输出要求：**"
          "- **只输出一个纯粹的 JSON 对象**，不要有任何额外的解释、前缀或后缀。"
          "- JSON 结构必须严格按照以下键（key）的顺序和名称：`user_level`, `date`, `text_content`, `driving_text_content`,`picture_topic`,`driving_picture_topic`"
          ""
          "现在，请处理以下用户评价："
          "【评价开始】"
          "{review_text}"  # 使用明确的变量名
          "【评价结束】",
    'en': ""
}


def generate_extraction_prompt(review_text, lang='zh'):
    """生成信息抽取的prompt"""
    template = prompt_extraction_keyword[lang]
    return template.format(review_text=review_text)


def split_large_file_to_blocks(file_path):
    """
    逐行读取大文件并按'==='分割，内存效率更高
    """
    blocks = []
    current_block = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # 如果遇到分隔行
                if line.strip().startswith('==='):
                    # 如果当前block有内容，保存它
                    if current_block:
                        blocks.append(''.join(current_block).strip())
                        current_block = []
                else:
                    current_block.append(line)

            # 添加最后一个block
            if current_block:
                blocks.append(''.join(current_block).strip())

        return blocks
    except Exception as e:
        print(f"读取文件时出错：{e}")
        return []


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

def prepare_structure_review(file_name):
    # 使用示例
    user_review_list = split_large_file_to_blocks(file_name)
    response_list = []
    for user_review in user_review_list:
        prompt = generate_extraction_prompt(user_review)
        try:
            response = llm.complete(prompt)
            response_list.append(json.loads(response.text))
        except Exception as e:
            print(e)
            pass

    df = json_to_dataframe(response_list)
    df.to_csv('data/mid/data_from_dianping.csv')

if __name__ == '__main__':
    prepare_structure_review('data/input/data_from_dianping.txt')