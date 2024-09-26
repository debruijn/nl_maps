# Modifications
This file describes the modifications that I have made from the source files in this folder.

## Municipalities
The `nl_municipalities.png` file follows the `LICENSE_MUNICIPALITIES` license, which states that the original source 
data comes from [Centraal Bureau voor de Statistiek](http://www.cbs.nl) and is free to be used as long as proper 
attribution to the copyright holder CBS. There are no requirements to mention the changes you have done, but for the
purpose of this file, this is included anyway.

Starting at the source data from CBS:
- Prior to the work in this repository, the modifications done have been described as 'Source: Gemeentengrenzen 2016, 
with manual tweaking for the merges of municipalities in 2017, 2018, 2019, 2021 and (up to) 2024.'
  - This has been published on [Wikipedia](https://commons.wikimedia.org/wiki/File:Nederland_gemeenten_2024.svg)
  - Authors: CBS and Kadaster. SVG generated by Ellywa and adapted by Husky and Gpvos and Commonpike.
- Some clean-up in that SVG file was done to remove floating borders and small islands.
- The resultant SVG has been exported as PNG into `nl_municipalties.png`.

## Provinces
The `nl_provinces.png` file follows the `LICENSE_ISLANDS_PROVINCES' license, which requires to also give attribution and
indicate changes that have been made.

- The source of this file can be found on [Wikipedia](https://commons.wikimedia.org/wiki/File:Netherlands_provinces_map_blank.svg), 
and is own work from Gust Justice.
- From this source-file, the BES islands have been split into their own file (see below) and from the remainder some
small islands have been removed.
- The resultant SVG has been exported as PNG into `nl_provinces.png`.

## Islands
The `bes_islands.png` file follows the `LICENSE_ISLANDS_PROVINCES' license, which requires to also give attribution and
indicate changes that have been made.

- The source of this file can be found on [Wikipedia](https://commons.wikimedia.org/wiki/File:Netherlands_provinces_map_blank.svg), 
and is own work from Gust Justice.
- From this source-file, the European part has been split into its own file (see above). From the BES islands, the
borders have been removed. Saba and Sint Eustatius have been increased in size to make them more visible. 
- The resultant SVG has been exported as PNG into `bes_islands.png`.