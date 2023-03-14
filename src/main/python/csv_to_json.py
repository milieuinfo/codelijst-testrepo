import json
import pandas as pd
from functions.functions import *
from rdflib import Graph, plugin
import os

#g = Graph()
#g.parse("/tmp/test.jsonld")

context = json.load(open("../resources/source/codelijst_context.json"))
df = pd.read_csv("../resources/source/codelijst_source.csv", sep=",", na_values=["", "NA"])
df = expand_df_on_pipe(df)
df = members_from_collection(df)
df = hasTopConcept_from_topConceptOf(df)
df = narrower_from_broader(df)
df = rename_columns(df)
df = df.drop_duplicates()


jsonld = to_jsonld(df, context)
with open("/tmp/testrepo.jsonld", "w") as f:
    f.write(jsonld)
os.system("riot --formatted=TURTLE /tmp/testrepo.jsonld > ../resources/be/vlaanderen/omgeving/data/id/conceptscheme/testrepo/testrepo.ttl")
os.system("riot --formatted=JSONLD ../resources/be/vlaanderen/omgeving/data/id/conceptscheme/testrepo/testrepo.ttl > ../resources/be/vlaanderen/omgeving/data/id/conceptscheme/testrepo/testrepo.jsonld")
