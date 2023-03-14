# codelijst-testrepo

## Samenvatting

De codelijst 'testrepo' is een template om een nieuw codelijst project op te zetten. \

## Gebruik

```
cd /tmp
git clone https://github.com/milieuinfo/codelijst-testrepo.git
cd codelijst-testrepo
jupyter-notebook
```
- open create_new_codelist_project.ipynb in de notebook
- vervang 'whatever' door de naam van je codelijst (geen spaties etc.)
- run de notebook
- het nieuwe project is aangemaakt onder /tmp/codelijst-...
- Voeg een definitie van een nieuwe code toe aan $PROJECT_HOME/src/main/resources/source/codelijst_source.csv
- maak project aan in github
- push naar github

### csv naar rdf
```
cd $PROJECT_HOME/src/main/bash
bash 01_csv_to_rfd.sh
```

## Dependencies

**_RDF tools:_**

In dit project worden twee jena cli-tools gebruikt: riot en sparql.
Sparql wordt gebruikt om het rdf-formaat om te zetten naar csv, riot wordt gebruikt om de rdf-formaten om te zetten, e.i. json-ld naar turtle.
- Lees eerst [deze documentatie](https://jena.apache.org/documentation/tools/index.html).
- Installeer de jena [binaries](https://dlcdn.apache.org/jena/binaries/).
Bijvoorbeeld:
```
curl -O https://dlcdn.apache.org/jena/binaries/apache-jena-4.6.0.tar.gz
tar -xf apache-jena-4.6.0.tar.gz -C /opt
echo 'export PATH="/opt/apache-jena-4.6.0/bin:$PATH"' >> ~/.bashrc
. ~/.bashrc
```

**_R:_**

Met behulp van de tidyverse bibliotheek in R wordt de csv omgezet naar jsonld.
```
sudo apt install r-base build-essential r-cran-jsonlite r-cran-tidyr r-cran-dplyr
```
