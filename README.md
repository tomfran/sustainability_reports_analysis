# Sustainability reports analysis

The goal of this repository is to find and analyze sustainability reports published on companies sites.

## Process

The steps are as follows:
1. The first task is to find useful documents from a list of pdf links for each website.
2. After finding eligible links, the pdfs are downloaded and their text is extracted using an ocr repository.
3. An elastic index is then created with companies information and the pdf text, with entities and top entities extracted from the corps of the files.
4. With the index containing all relevant information the analysis phase can begin.

...