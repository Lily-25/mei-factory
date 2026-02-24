import json
import pandas as pd


def visualization():
    input_json_path = f'../data/papers/midput/ssp_abstract_extract_deepseek.json'
    with open(input_json_path,
              'r',
              encoding='utf-8') as f:
        documents = json.load(f)

    df = pd.DataFrame(documents).fillna("other")

    # Define the columns to check
    columns_to_check = ['methods', 'correlation', 'activities', 'technologies', 'findings', 'industries', 'tacit knowledge types']

    # Filter out rows where ALL specified columns are 'other'
    df = df[~(df[columns_to_check] == 'other').all(axis=1)]

    df.to_csv(f'../data/papers/midput/ssp_abstract_extract_deepseek.csv')

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
        .groupby(['activities', 'technologies', 'tacit knowledge types'], as_index=False)
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
    result.to_csv('../data/papers/midput/ssp_abstract_extract_3d.csv', index=False)

if __name__ == '__main__':
    visualization()