#!/bin/bash

# Transform csv, ../resources/be/vlaanderen/omgeving/data/id/conceptscheme/chemische_stof/chemische_stof.csv
# to jsonld, /tmp/chemische_stof.jsonld
Rscript ../R/csv_to_json.R

# Make formatted jsonld ant turtle
riot --formatted=TURTLE /tmp/chemische_stof.jsonld   > '../resources/be/vlaanderen/omgeving/data/id/conceptscheme/chemische_stof/chemische_stof.ttl'
riot --formatted=JSONLD '../resources/be/vlaanderen/omgeving/data/id/conceptscheme/chemische_stof/chemische_stof.ttl'   > '../resources/be/vlaanderen/omgeving/data/id/conceptscheme/chemische_stof/chemische_stof.jsonld' 

