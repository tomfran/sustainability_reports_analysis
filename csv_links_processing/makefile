SCORE=

run: 
	@python3.8 main.py

clean:
	@rm -rf src/__pycache__
	@echo "Unnecessary stuff removed"

setup:
	@mkdir data

help:
	@echo -e "\n\
\033[1mCSV-PROCESSING\033[0m\n\n\
\033[1mCOMMANDS\033[0m\n\n\
\t1. \033[1mmake run\033[0m : run the program, find results in data\n\
\tThe pdfs links to analyze must be places in data/pdf_links.csv\n\
\tResults are stored in data/filtered_pdf_links.csv, and data/stats.csv\n\n\
\t2. \033[1mmake clean\033[0m : remove python cache\n\n\
\t3. \033[1mmake setup\033[0m : create the necessary folders\n\n\
\t4. \033[1mmake copy\033[0m  : copy the result in a new file, speficy name with SCORE=<name>\n\n\
\t5. \033[1mmake all\033[0m   : run and copy\n\n\
\t6. \033[1mmake help\033[0m  : show this help message \n\n"

copy:
	cp data/stats.csv data/$(SCORE).csv

all:
	make run && make copy