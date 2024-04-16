import pandas as pd
import json
    
def clean_df(df: pd.DataFrame):
    original_columns = df.columns.tolist()
    original_indices = {col: idx for idx, col in enumerate(original_columns)}

    # Identify columns containing JSON data
    json_columns = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, str) and x.startswith("{") and x.endswith("}")).any()]
    list_columns = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, str) and x.startswith("[") and x.endswith("]")).any()]

    # Expand columns containing JSON data into multiple columns
    new_columns = {}
    for col in json_columns:
        new_cols = df[col].apply(lambda x: {} if pd.isna(x) else json.loads(x.replace("'", "\""))).apply(pd.Series).add_prefix(col + '(').add_suffix(")")
        new_columns[col] = new_cols.columns.tolist()
        df = pd.concat([df.drop([col], axis=1), new_cols], axis=1)
        
    for col in list_columns:
        df[col] = df[col].apply(lambda x: "" if pd.isna(x) else x[1:-1])

    # Reorder the expanded columns based on the original order
    for col, new_cols in new_columns.items():
        original_idx = original_indices[col]
        for new_col in new_cols[::-1]:
            df.insert(original_idx + 1, new_col, df.pop(new_col))

    # Remove empty columns and replace NaNs with empty strings
    df.replace({pd.NA: ''}, inplace=True)
    df.dropna(axis=1, how='all', inplace=True)

    return df
