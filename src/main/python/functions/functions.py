import json
import pandas as pd

def string_split(x: str) :
    try:
        return  x.split('|')
    except:
        return x

'''expand_df_on_pipe(df: pd.DataFrame) -> pd.DataFrame
    This function takes a dataframe and expands it on the pipe character.
    It does this by splitting the string on the pipe character and then
    exploding the dataframe.
    
    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to be expanded.
        
    Returns
    -------
    pd.DataFrame
        The expanded dataframe.'''

def expand_df_on_pipe(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        df[col] = df[col].apply(lambda x: string_split(x))
        df = df.explode(col)
    return df.drop_duplicates()

''' def rename_columns(df: pd.DataFrame) -> pd.DataFrame
Rename columns in a dataframe.

Parameters
----------
df : pd.DataFrame
    The dataframe to rename columns in.

Returns
-------
pd.DataFrame
    The dataframe with renamed columns.'''

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={"uri": "@id", "type": "@type"})

'''def members_from_collection(df: pd.DataFrame) -> pd.DataFrame:
    This function takes a dataframe as input and returns a dataframe.
    The input dataframe should have a column 'collection' with the uri's of the collections.
    The output dataframe will have a column 'member' with the uri's of the members of the collections.
    The output dataframe will have a column 'type' with the type of the collection.
    The output dataframe will have a column 'uri' with the uri of the collection.
'''
def members_from_collection(df: pd.DataFrame) -> pd.DataFrame:
    # members van collection uit "inverse" relatie
    collections = df['collection'].dropna().unique()
    for col in collections:
        medium = df[df['collection'] == col][['uri', 'collection']]
        medium_members = medium['uri'].tolist()
        df2 = pd.DataFrame({'type': 'skos:Collection','uri': col, 'member': medium_members})
        df = pd.concat([df, df2])
    return df

'''
def hasTopConcept_from_topConceptOf(df: pd.DataFrame) -> pd.DataFrame:
    This function takes a dataframe as input and returns a dataframe with the hasTopConcept relation.
    The hasTopConcept relation is derived from the topConceptOf relation.
    The function takes the topConceptOf relation and creates a hasTopConcept relation for each scheme.
    The hasTopConcept relation is added to the dataframe.
    
    Parameters
    ----------
    df : pd.DataFrame
        The dataframe with the topConceptOf relation.
        
    Returns
    -------
    pd.DataFrame
        The dataframe with the hasTopConcept relation.
'''
def hasTopConcept_from_topConceptOf(df: pd.DataFrame) -> pd.DataFrame:
    # hasTopConcept relatie uit inverse relatie
    schemes = df[df['topConceptOf'].notnull()]['topConceptOf'].unique()
    for scheme in schemes:
        topconceptof = df[df['topConceptOf'] == scheme][['uri', 'topConceptOf']]
        hastopconcept = topconceptof['uri'].tolist()
        df2 = pd.DataFrame({'type': 'skos:Concept','uri': scheme, 'hasTopConcept': hastopconcept})
        df = pd.concat([df, df2])
    return df

'''
def narrower_from_broader(df: pd.DataFrame) -> pd.DataFrame:
    This function takes a dataframe with a column 'broader' and returns a dataframe with a column 'narrower'
    The 'narrower' column is created by taking the 'broader' column and reversing the relationship.
    The 'narrower' column contains the uri's of the concepts that are narrower than the concept in the 'broader' column.
    The 'narrower' column is then added to the original dataframe.
    
    Parameters
    ----------
    df : pd.DataFrame
        A dataframe with a column 'broader'
        
    Returns
    -------
    pd.DataFrame
        A dataframe with a column 'narrower'
        
    # 1. Select all rows with a broader value
    # 2. Remove duplicates
    # 3. For each broader value
    # 4. Select all rows with that broader value
    # 5. Select the uri and broader values
    # 6. Select the uri values
    # 7. Create a new dataframe with the broader value as uri and the uri values as narrower
    # 8. Add the new dataframe to the original dataframe
    # 9. Return the new dataframe
'''
def narrower_from_broader(df: pd.DataFrame) -> pd.DataFrame:
    # narrower uit "inverse" relatie broader
    broaders = df[['broader']].dropna()
    broaders = broaders.drop_duplicates()
    for broad in broaders['broader']:
        relation = df[df['broader'] == broad][['uri','broader']]
        narrowers = relation['uri']
        df2 = pd.DataFrame({'type': 'skos:Concept','uri':broad, 'narrower':narrowers})
        df = pd.concat([df, df2])
    return df

'''
def to_jsonld(df: pd.DataFrame, context: dict) -> str:
Convert a pandas DataFrame to JSON-LD.

Parameters
----------
df : pd.DataFrame
    The DataFrame to convert.
context : dict
    A JSON-LD context.

Returns
-------
str
    A JSON-LD string.
'''

def to_jsonld(df: pd.DataFrame, context: dict) -> str:
    result = df.to_json(orient="table")
    data = json.loads(result)['data']
    df_in_list = {'@graph': data, '@context': context}
    df_in_json = json.dumps(df_in_list, ensure_ascii=False)
    return df_in_json
