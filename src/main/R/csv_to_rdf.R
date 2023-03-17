#!/usr/bin/Rscript
library(tidyr)
library(dplyr)
library(jsonlite)
library(stringr)
library(data.table)
library(yaml)

#setwd('/home/gehau/git/codelijst-testrepo/src/main/R')
#setwd('/Users/pieter/work/svn/codelijst-testrepo/src/main/R')

to_jsonld <- function(dataframe) {
  # lees context
  context <- jsonlite::read_json(jsonld_source_pad)
  # jsonld constructie
  df_in_list <- list('@graph' = dataframe, '@context' = context)
  df_in_json <- toJSON(df_in_list, auto_unbox=TRUE)
  return(df_in_json)
}

collapse_df_on_pipe <- function(df) {
  # group by
  df <- df %>%
    rename("id" = "@id")
  df3 <-  df %>%
    select(id) %>%
    distinct()
  for(col in colnames(df)) {   # for-loop over columns
    if ( col != 'id') {
      df4 <- df %>% select(id, col)
      names(df4)[2] <- 'naam' # hack, geef de tweede kolom een vaste naam, summarize werkt niet met variabele namen
      df2 <- df4 %>% group_by(id) %>%
        summarize(naam = paste(sort(unique(naam)),collapse="|"))
      names(df2)[2] <- col # wijzig kolom met naam 'naam' terug naar variabele naam
      df3 <- merge(df3, df2, by = "id")
    }
  }
  return(df3)
}

expand_df_on_pipe <- function(dataframe) {
  # fix voor vctrs_error_incompatible in pubchem column
  df <- dataframe %>%
    mutate_all(list(~ str_c("", .)))
  # verdubbel rijen met pipe separator
  for(col in colnames(df)) {   # for-loop over columns
    df <- df %>%
      separate_rows(col, sep = "\\|")%>%
      distinct()
  }
  return(df)
}

rename_columns <- function(df) {
  # rename columns
  df <- df %>%
    rename("@id" = uri,
           "@type" = type)
  return(df)
}

members_from_collection  <- function(df) {
  # members van collection uit "inverse" relatie
  collections <- na.omit(distinct(df['collection']))
  for (col in as.list(collections$collection)) {
    medium <- subset(df, collection == col ,
                     select=c(uri, collection))
    medium_members <- as.list(medium["uri"])
    df2 <- data.frame(col, medium_members)
    names(df2) <- c("uri","member")
    df <- bind_rows(df, df2)
  }
  return(df)
}

hasTopConcept_from_topConceptOf  <- function(df) {
  # hasTopConcept relatie uit inverse relatie
  schemes <- na.omit(distinct(df['topConceptOf']))
  for (scheme in as.list(schemes$topConceptOf)) {
    topconceptof <- subset(df, topConceptOf == scheme ,
                           select=c(uri, topConceptOf))
    hastopconcept <- as.list(topconceptof["uri"])
    df2 <- data.frame(scheme, hastopconcept)
    names(df2) <- c("uri","hasTopConcept")
    df <- bind_rows(df, df2)
  }
  return(df)
}

narrower_from_broader  <- function(df) {
  # narrower uit "inverse" relatie broader
  broaders <- na.omit(distinct(df['broader']))
  for (broad in as.list(broaders$broader)) {
    relation <- subset(df, broader == broad ,
                       select=c(uri, broader))
    narrowers <- as.list(relation["uri"])
    df2 <- data.frame(broad, narrowers)
    names(df2) <- c("uri","narrower")
    df <- bind_rows(df, df2)
  }
  return(df)
}

## Start script

# PARSE CONFIG AND SET CONFIG VAR

config = yaml.load_file("config.yml")

dataset_distributie_pad = config$skos$distributie_pad
distributie_naam = config$skos$distributie_naam
jsonld_source_pad = config$skos$jsonld_source
csv_source_pad = config$skos$csv_source

# lees csv
df <- read.csv(file = csv_source_pad, sep=",", na.strings=c("","NA"))

df <- expand_df_on_pipe(df)%>%
  members_from_collection()%>%
  hasTopConcept_from_topConceptOf()%>%
  narrower_from_broader()%>%
  rename_columns()

csv_distributie <- paste(dataset_distributie_pad, distributie_naam, ".csv", sep="")
write.csv(collapse_df_on_pipe(df),csv_distributie, row.names = FALSE)

# write volledig geexpandeerde csv, ter controle, deze wordt niet aan versiebeheer toegevoegd
test_distributie <- paste(dataset_distributie_pad, "temp_test_separate_rows.csv", sep="")
write.csv(df,test_distributie, row.names = FALSE)

# bewaar jsonld
tmp_file <- tempfile(fileext = ".jsonld")

write(to_jsonld(df), tmp_file)

### CLEAN RDF

# serialiseer jsonld naar mooie turtle en mooie jsonld
# hiervoor dienen jena cli-tools geinstalleerd, zie README.md
ttl_distributie <- paste(dataset_distributie_pad, distributie_naam, ".ttl", sep="")
jsonld_distributie <- paste(dataset_distributie_pad, distributie_naam, ".jsonld", sep="")

riot_cmd <- paste("riot --formatted=TURTLE ", tmp_file, " > ", ttl_distributie)
system(riot_cmd)

riot_cmd <- paste("riot --formatted=JSONLD ", ttl_distributie, " > ", jsonld_distributie)
system(riot_cmd)
#system("shacl v --shapes ../resources/be/vlaanderen/omgeving/data/id/ontology/chemische-stof-ap-constraints/chemische-stof-ap-constraints.ttl --data ../resources/be/vlaanderen/omgeving/data/id/conceptscheme/testrepo/testrepo.ttl")



