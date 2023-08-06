# Scraping DSL

Project that is using textX to define and interpret DSL in order to generate and run Scrapy project for scraping various types of items and storing it in the MongoDB.

The project currently supports scraping top 250 movies from imdb, councils at otvoreniparlament.rs , and all the products from gigatron and winwin website. (You can find all the examples in the examples folder)

# Prerequisites:

        1. Python 2.7+

        2. Python modules installed:

                Jinja2           2.10

                pydot            1.2.4

                pymongo          3.7.1

                Scrapy           1.5.0

                textX            1.7.1

        3. MongoDB database installed (with default settings)

# Item to be scrapped:

For each item there is:

1. Definition of product with properties and css selectors for each property under examples\domain_name\types\type_name.sdt file.

2. Configuration file (.py file) for properties that include more complex manipulation of the tag content under examples\domain_name\types\type_name.py file.

# DSL example:

Main DSL query is defined under examples\domain_name\type_program.sdq file.

Example (movie_program.sdq):

>find Movie where cast = &#39;Morgan Freeman&#39;

All the examples are under examples folder. (together with type definition and configuration files)

# How to run:

_\*Code expects all the files regarding the grammar definition to be under dsl/language folder and type definition, configuration and main DSL query in the examples/domain_name folder._

In dsl/generate.py file you define the scraping item and the domain:
>  # DEFINE THE TYPE AND THE DOMAIN OF THE SCRAPING ITEM
    domain = "imdb"
    type = "movie"
>

_\*Currently supported types are: movie, poslanik and most of the products on winwin and gigatron (laptop, mobilni\_telefon, frizider, televizor etc)_

Run generate.py and check the output folder. The scrapy is automatically run.

# Project structure:

- Templates are located at dsl/templates folder
- Generator is in the main dsl folder (with .py extension)
- Language files are in the dsl/language folder.
- Generated Scrapy project is in the dsl/output folder.

# License:

MIT
