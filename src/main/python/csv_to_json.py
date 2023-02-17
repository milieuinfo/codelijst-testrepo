import json
import pandas as pd
from functions.functions import *
from rdflib import Graph, plugin
import os

#g = Graph()
#g.parse("/tmp/test.jsonld")

context = json.load(open("../resources/source/test_context.json"))
df = pd.read_csv("../resources/source/test_source.csv", sep=",", na_values=["", "NA"])
df = expand_df_on_pipe(df)
df = members_from_collection(df)
df = hasTopConcept_from_topConceptOf(df)
df = narrower_from_broader(df)
df = rename_columns(df)
df = df.drop_duplicates()


jsonld = to_jsonld(df, context)
with open("/tmp/test.jsonld", "w") as f:
    f.write(jsonld)
os.system("riot --formatted=TURTLE /tmp/test.jsonld > ../resources/be/vlaanderen/omgeving/data/id/conceptscheme/test/test.ttl")
os.system("riot --formatted=JSONLD ../resources/be/vlaanderen/omgeving/data/id/conceptscheme/test/test.ttl > ../resources/be/vlaanderen/omgeving/data/id/conceptscheme/test/test.jsonld")
