import re
import json
import pandas as pd

from src.IndividualAssignment.utiles.llm_api import get_deepseek_obj
from src.Dissertation.taxonomy import (knowledge_retention_activities_taxonomy,industry_taxonomy,collins_based_tacit_knowledge_taxonomy,digital_technology_taxonomy,SECI_taxonomy)
llm = get_deepseek_obj()

def parse_document(doc_text):
    """将单个文档文本解析为字典"""
    lines = doc_text.strip().split('\n')
    doc_dict = {}

    dict_mapping = {
        'Publication date' : 'Publication year',
        'Language': 'Language of publication',
    }

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 检查是否包含冒号，并且冒号不在行首（避免 URL 中的 : 被误判）
        if ':' in line and not line.startswith(':'):
            # 只分割第一个冒号（防止 Abstract 或 Links 中的冒号干扰）
            key, value = line.split(':', 1)
            key = key.strip()

            if len(key.split()) > 5:
                continue

            value = value.strip()
            if key and value:
                if key in dict_mapping.keys():
                    key = dict_mapping[key]
                doc_dict[key] = value
    return doc_dict


def sort_paper_from_ProQuest(cmd, indexes):
    for index in indexes:
        input_file = f'./data/papers/{cmd}/ProQuestDocuments-{index}.txt'
        output_file = f'./data/papers/{cmd}/ProQuestDocuments-{index}.json'
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用下划线分隔符分割文档（支持前后空白）
        # 注意：你的分隔符是 60 个或更多下划线（实际是 120+），我们用正则匹配
        separator = r'\n_{60,}\s*\n'
        raw_docs = re.split(separator, content)

        # 过滤空文档
        raw_docs = [doc.strip() for doc in raw_docs if doc.strip()]

        # 解析每个文档为字典
        all_docs = []
        for doc in raw_docs:
            parsed = parse_document(doc)
            if parsed:  # 只保留非空字典
                all_docs.append(parsed)

        # 保存为 JSON 文件
        with open(output_file, 'w', encoding='utf-8') as out_f:
            json.dump(all_docs, out_f, ensure_ascii=False, indent=2)

        print(f"成功解析 {len(all_docs)} 个文档，已保存至 {output_file}")


def standardize_country(country_str):

    """
    Standardizes a country string to a canonical name.
    Args:
        country_str (str): The raw country string from the data.

    Returns:
        str: The standardized country name.
    """
    if pd.isna(country_str) or country_str == 'other':
        return country_str

    # Normalize the string: remove extra spaces, convert to title case for easier matching
    normalized = re.sub(r'\s+', ' ', country_str.strip()).title()

    # Handle specific cases for the United States
    us_patterns = [
        r'^U\.?S\.?A?\.?$',
        r'^United\s+States.*',
        r'^Un\s+Ited\s+States$',
        r'^Unite\s?D\s+States$',
        r'^Unit\s+Ed\s+States$',
        r'^United\s+Stat\s+Es$',
        r'^Usa$'
    ]
    for pattern in us_patterns:
        if re.match(pattern, normalized, re.IGNORECASE):
            return "United States"

    # Handle specific cases for the United Kingdom
    uk_patterns = [
        r'^U\.?K\.?$',
        r'^United\s+Kingdom.*',
        r'^Uni\s+Ted\s+Kingdom$',
        r'^United\s+Kingd\s+Om$',
        r'^England$',
        r'^Scotland$',
        r'^Wales$',
        r'^Northern\s+Ireland$',
        r'^Birmingham$',  # A major city in England
        r'^East\s+Sussex$',  # A county in England
        r'^Adapazari$',
        # This seems like a Turkish city, but in your data it's listed under UK. We'll keep it as UK per your data's context.
    ]
    for pattern in uk_patterns:
        if re.match(pattern, normalized, re.IGNORECASE):
            return "United Kingdom"

    # Handle specific cases for the Netherlands
    nl_patterns = [
        r'^Netherland[s]?$',
        r'^Nether\s+Lands$',
        r'^Netherl\s+Ands$',
        r'^The\s+Netherlands$'
    ]

    for pattern in nl_patterns:
        if re.match(pattern, normalized, re.IGNORECASE):
            return "Netherlands"

    # Handle Canada
    if re.match(r'^(Canada|Can)$', normalized, re.IGNORECASE):
        return "Canada"

    # Handle other specific countries that appear in your data
    # For these, we mostly just correct the casing
    known_countries = {
        'Japan': 'Japan',
        'Italy': 'Italy',
        'France': 'France',
        'Germany': 'Germany',
        'India': 'India',
        'Switzerland': 'Switzerland',
        'Australia': 'Australia',
        'Singapore': 'Singapore',
        'China (Republic : 1949- )': 'China',
        'South Africa': 'South Africa',
        'New Zealand': 'New Zealand',
        'Turkey': 'Turkey',
        'Malaysia': 'Malaysia',
        'Colombia': 'Colombia',
        'Brazil': 'Brazil',
        'Spain': 'Spain',
        'Portugal': 'Portugal',
        'Denmark': 'Denmark',
        'Austria': 'Austria',
        'Belgium': 'Belgium',
        'Norway': 'Norway',
        'Ireland': 'Ireland',
        'Israel': 'Israel',
        'Taiwan': 'China',
        'Hong Kong': 'China',
        'Korea (South)': 'Korea (South)',
        'Russia': 'Russia',
        'Ukraine': 'Ukraine',
        'Romania': 'Romania',
        'Bulgaria': 'Bulgaria',
        'Hungary': 'Hungary',
        'Czech Republic': 'Czech Republic',
        'Poland': 'Poland',
        'Greece': 'Greece',
        'Pakistan': 'Pakistan',
        'Lithuania': 'Lithuania',
        'Croatia': 'Croatia',
        'Slovenia': 'Slovenia',
        'Bosnia And Herzegovina': 'Bosnia And Herzegovina',
        'Mumbai': 'India',  # Mumbai is a city in India
        'Chandigarh': 'India',  # Chandigarh is a city in India
        'Punjab': 'India',  # Punjab is a state in India
        'Victoria': 'Australia',  # Victoria is a state in Australia
        'Princeton': 'United States',  # Princeton is a city in the US
        'Bridgetown': 'Barbados',  # Bridgetown is the capital of Barbados
        'Vilnius': 'Lithuania',  # Vilnius is the capital of Lithuania
    }

    # Check if the normalized string matches a known country key
    for key, value in known_countries.items():
        if normalized == key.title():
            return value

    # If none of the above, return the original string (or its title case)
    return normalized

def build_dataframe(cmd, indexes):

    enhanced_docs = []
    for index in indexes:
        json_file = f'./data/papers/{cmd}/ProQuestDocuments-{index}.json'

        with open(json_file, 'r', encoding='utf-8') as f:
            documents = json.load(f)

        for i, doc in enumerate(documents):
            enhanced_docs.append(doc)

    df = pd.DataFrame(enhanced_docs).fillna("other")

    # Apply logic
    cols_to_drop = [
        col for col in df.columns
        if df[col].dropna().nunique() == 2 and 'other' in df[col].dropna().unique()
    ]

    print("Columns to drop:", cols_to_drop)  # Output: ['A', 'E']

    df_cleaned = df.drop(columns=cols_to_drop)
    df_cleaned.to_csv(f'./data/papers/{cmd}/ProQuestDocuments-original-fields.csv')

    print(list(df_cleaned.columns))
    columns_to_keep = ['Title',
               'Author',
               'Abstract',
               'Publication title',
               'Country of publication',
               'Publication year',
               'Source type',
               'Language of publication',
               'DOI',
               'Database',
               'Document type',
                       'Research method',
                       'Methodology'
               ]

    df_final = df[columns_to_keep].copy()
    df_final['Country of publication'] = df_final['Country of publication'].apply(standardize_country)

    df_final = df_final.drop_duplicates(subset=['Title'])

    df_final.to_csv(f'./data/papers/{cmd}/ProQuestDocuments-selected-fields.csv', index=None)
    df_final.to_json(f'./data/papers/{cmd}/ProQuestDocuments-selected-fields.json', orient='records')


def extract_challenge_method_findings(prompt: str) -> dict:

    try:
        response = llm.complete(prompt)
        result = json.loads(response.text)
        return result
    except Exception as e:
        print(f"Error processing abstract: {e}")
        return {"challenges": ""}

def get_prompt(cmd, abstract):
    Prompt = {
        "Commands_1": f"""
You are an expert academic researcher. Please read the following abstract and extract such elements in JSON format:  
\- "challenges": the main problem or gap addressed  
\- "methods": the research methods used  
\- "activities": the knowledge retention approaches discussed, the scope of value: {knowledge_retention_activities_taxonomy}  
\- "findings": Key results or outcomes  
\- "industries": Industry or industries discussed, the scope of value: {industry_taxonomy}  
\- "tacit knowledge types": Tacit knowledge discussed, the scope of value: {collins_based_tacit_knowledge_taxonomy}  
\- "knowledge flows": SECI model discussed, the scope of value: {SECI_taxonomy}

Abstract:  
{abstract}  
Respond ONLY with a valid JSON object, no explanation and no prefix like 'json'
""",
        'Commands_2': f"""
You are an expert academic researcher. Please read the following abstract and extract such elements in JSON format:  
\- "challenges": the main problem or gap addressed  
\- "methods": the research methods used  
\- "activities": the knowledge retention approaches discussed, the scope of value: {knowledge_retention_activities_taxonomy}  
\- "technologies": Digital technologies discussed, the scope of value: {digital_technology_taxonomy}  
\- "findings": Key results or outcomes  
\- "industries": Industry or industries discussed, the scope of value: {industry_taxonomy}  
\- "tacit knowledge types": Tacit knowledge discussed, the scope of value: {collins_based_tacit_knowledge_taxonomy}  

Abstract:  
{abstract}  
    
Respond ONLY with a valid JSON object, no explanation and no prefix like 'json'"""
    }
    return Prompt[cmd]

def batch_extract_challenge_method_findings(cmd):

    output_json_path = f'data/papers/{cmd}/ProQuestDocuments-extract.json'
    with open(f'data/papers/{cmd}/ProQuestDocuments-selected-fields.json',
              'r',
              encoding='utf-8') as f:
        documents = json.load(f)

    enhanced_docs = []

    try:
        count = 293
        for i, doc in enumerate(documents):
            abstract = doc.get("Abstract", "")
            if not abstract.strip():
                print(f"Document {i + 1}: No abstract found.")
                doc.update({"challenges": ""})
            else:
                extracted = extract_challenge_method_findings(get_prompt(cmd, abstract))
                doc.update(extracted)
            enhanced_docs.append(doc)

            if count:
                count = count -1
            else:
                break
    except Exception as e:
        print(f"Error processing abstract: {e}")
        pass

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(enhanced_docs, f, ensure_ascii=False, indent=2)

    print(f"Processed {len(enhanced_docs)} documents. Saved to {output_json_path}")


if __name__ == '__main__':

    indexes = [293]
    cmd = "Commands_2"

    # sort_paper_from_ProQuest(cmd,indexes)

    # build_dataframe(cmd, indexes)

    # batch_extract_challenge_method_findings(cmd)

    output_json_path = f'data/papers/Commands_2/ProQuestDocuments-extract.json'
    with open(output_json_path,
              'r',
              encoding='utf-8') as f:
        documents = json.load(f)

    df = pd.DataFrame(documents).fillna("other")

    # Define the columns to check
    columns_to_check = ['methods', 'activities', 'technologies', 'findings', 'industries', 'tacit knowledge types']

    # Filter out rows where ALL specified columns are 'other'
    df = df[~(df[columns_to_check] == 'other').all(axis=1)]

    df.to_csv(f'data/papers/Commands_2/ProQuestDocuments-extract.csv')

    df_exploded = (
        df
        .explode('industries', ignore_index=True)
        .explode('activities', ignore_index=True)
        .explode('technologies', ignore_index=True)
        .explode('tacit knowledge types', ignore_index=True)
    )

    # Step 3: 按三列分组并计数
    result = (
        df_exploded
        .groupby(['industries', 'activities', 'technologies', 'tacit knowledge types'], as_index=False)
        .size()
        .rename(columns={'size': 'count'})
        .sort_values('count', ascending=False)
        .reset_index(drop=True)
    )

    # 可选：重命名列以提高可读性
    result = result.rename(columns={
        'industries': 'industry',
        'activities': 'activity',
        'technologies': 'technology',
        'tacit knowledge types': 'tacit knowledge types'
    })
    result.to_csv('data/papers/Commands_2/ProQuestDocuments-extract-3d.csv', index=False)
