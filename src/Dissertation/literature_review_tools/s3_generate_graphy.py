import json

from llm_mgmt.gemini_api_interface import batch_extract as batch_extract_by_gemini
from llm_mgmt.qwen_api_interface import batch_extract as batch_extract_by_qwen
from utils.translator import translate_with_truncation
import pandas as pd
import uuid
import itertools
import ast


class GraphyGenerator:

    def __init__(self):
        pass

    @staticmethod
    def generate_activity_by_gemini(count=1):
        input_file = "../data/papers/midput/ssp_abstract_extract.json"
        output_file = "../data/papers/midput/ssp_extract_activities"
        cmd = "Cmd_Ext_Activity"

        batch_extract_by_gemini(input_file, output_file, cmd, count=count)

    @staticmethod
    def generate_activity_by_qwen(count=1):
        input_file = "../data/papers/midput/ssp_extract_relevance.json"
        output_file = "../data/papers/midput/ssp_extract_activities_qwen"
        cmd = "Cmd_Ext_Activity"

        batch_extract_by_qwen(input_file, output_file, cmd, count=count)

    @staticmethod
    def combine_activities():
        input_file = "../data/papers/midput/ssp_extract_activities_qwen.csv"
        output_file = "../data/papers/midput/ssp_extract_activities"

        df = pd.read_csv(input_file)

        df['uuid'] = [str(uuid.uuid4()) for _ in range(len(df))]

        # waiting for multiple LLMs

        df.to_csv(f'{output_file}.csv', index=False)
        df.to_json(f'{output_file}.json', orient='records')

    @staticmethod
    def generate_graphy():
        input_file = "../data/papers/midput/ssp_extract_activities.csv"
        output_extract_file = "../data/papers/output/ssp_extract_activities.csv"
        output_activity_file = "../data/papers/output/activity_combinations.csv"

        df = pd.read_csv(input_file)

        relation_rows = []
        activity_node_rows = []
        tech_node_rows = []
        selected_uuid = []
        for i, item in df.iterrows():
            industries = ast.literal_eval(item['industries'])
            activities = ast.literal_eval(item["activities"])

            selected_uuid_flag = False
            for activity in activities:
                if not len(activity["technologies"]) or not len(activity["activity_name"]):
                    continue

                selected_uuid_flag = True
                if len(activity["knowledge_flows"]) == 4:
                    activity["knowledge_flows"] = ['']
                kf_list = activity["knowledge_flows"] if len(activity["knowledge_flows"]) > 0 else ['']

                if len(activity["tacit_knowledge_types"]) == 4:
                    activity["tacit_knowledge_types"] = ['']
                tkt_list = activity["tacit_knowledge_types"]
                tech_list = activity["technologies"]

                activity_node_rows.append({
                    "Label": "KR_Activities",
                    "Name": activity['activity_name']})

                for tech in tech_list:
                    tech_node_rows.append({
                    "Label": "Digital_Tech",
                    "Name": tech})

                # 生成笛卡尔积
                for kf, tkt, tech in itertools.product(kf_list, tkt_list, tech_list):
                    relation_rows.append({
                        "uuid": item["uuid"],
                        'division': industries['division'],
                        'majorGroup': industries['majorGroup'],
                        "activity_name": activity["activity_name"],
                        "knowledge_flows": kf,
                        "tacit_knowledge_types": tkt,
                        "technologies": tech
                    })

            if selected_uuid_flag:
                selected_uuid.append(item['uuid'])

        df[df['uuid'].isin(selected_uuid)].to_csv(output_extract_file, index=False)

        df_activities = pd.DataFrame(relation_rows)
        df_activities.to_csv(output_activity_file, index=False)

        graphy_dir = "../data/graph/"

        df_activity_nodes = pd.DataFrame(activity_node_rows)
        df_activity_nodes.dropna(subset=['Name'], inplace=True)
        df_activity_nodes['count'] = df_activity_nodes.groupby(list(df_activity_nodes.columns))['Name'].transform('size')
        df_activity_nodes = df_activity_nodes.drop_duplicates()
        df_activity_nodes.to_csv(f'{graphy_dir}/activity_nodes.csv', index=False, sep='\t')

        df_tech_nodes = pd.DataFrame(tech_node_rows)
        df_tech_nodes.dropna(subset=['Name'], inplace=True)
        df_tech_nodes['count'] = df_tech_nodes.groupby(list(df_tech_nodes.columns))['Name'].transform('size')
        df_tech_nodes = df_tech_nodes.drop_duplicates()
        df_tech_nodes.to_csv(f'{graphy_dir}/tech_nodes.csv', index=False, sep='\t')

        activity_and_seci = []
        activity_and_tk = []
        activity_and_tech = []

        for i, item in df_activities.iterrows():

            if not len(item['activity_name']):
                continue

            if len(item['knowledge_flows']):
                activity_and_seci.append({
                    'Src_Label': 'KR_Activities',
                    'Src_Name': item['activity_name'],
                    'Dst_Label': 'SECI',
                    'Dst_Name': item['knowledge_flows'],
                    'Relationship': 'knowledge_flows'
                })

            if len(item['tacit_knowledge_types']):
                activity_and_tk.append({
                    'Src_Label': 'KR_Activities',
                    'Src_Name': item['activity_name'],
                    'Dst_Label': 'TK_Taxonomy',
                    'Dst_Name': item['tacit_knowledge_types'],
                    'Relationship': 'tacit_knowledge_types'
                })

            if len(item['technologies']):
                activity_and_tech.append({
                    'Src_Label': 'KR_Activities',
                    'Src_Name': item['activity_name'],
                    'Dst_Label': 'Digital_Tech',
                    'Dst_Name': item['technologies'],
                    'Relationship': 'activity_and_tech'
                })

        df_activity_and_seci = pd.DataFrame(activity_and_seci)
        df_activity_and_seci = df_activity_and_seci.drop_duplicates()
        df_activity_and_seci.to_csv(f'{graphy_dir}/activity_and_seci.csv', index=False, sep='\t')

        df_activity_and_tk = pd.DataFrame(activity_and_tk)
        df_activity_and_tk = df_activity_and_tk.drop_duplicates()
        df_activity_and_tk.to_csv(f'{graphy_dir}/activity_and_tk.csv', index=False, sep='\t')

        df_activity_and_tech = pd.DataFrame(activity_and_tech)
        df_activity_and_tech = df_activity_and_tech.drop_duplicates()
        df_activity_and_tech.to_csv(f'{graphy_dir}/activity_and_tech.csv', index=False, sep='\t')

    @staticmethod
    def generate_review_template():
        extract_file = "../data/papers/output/ssp_extract_activities.csv"

        df = pd.read_csv(extract_file)

        translate_list = []
        for i, item in df.iterrows():
            text = translate_with_truncation(item['Abstract'])
            print(text)
            translate_list.append(text)

        df['Abstract_zh'] = translate_list

        df.to_csv(extract_file, index=False)


if __name__ == '__main__':
    #GraphyGenerator.generate_activity_by_qwen(count=1000)
    #GraphyGenerator.combine_activities()
    #GraphyGenerator.generate_graphy()
    GraphyGenerator.generate_review_template()

