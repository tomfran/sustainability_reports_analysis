# CSV-links-processing

Simple program that finds probable sustainability pdf links in a pool of links.

## Setup

After cloning run `make setup` to create the required folders.  
Use `make help` to see all the make rules.

## Process

The main goal of this repository is to extract 2018 Sustainability reports from a pool of pdfs.
After processing the csv file, all links from each websites are evaluated, resulting in a list of eligible pdf files.

To evaluate a link, it is considered the name of the file, the path to that file, and the url of the page in which it has been found.

The stats can be found in the stats.csv file.