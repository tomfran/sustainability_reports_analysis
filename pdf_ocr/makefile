run: 
	@python3.8 main.py

clean:
	@make -s clean_images && make -s clean_texts && make -s clean_cache
	@echo "Done."
	
clean_images:
	@rm -rf data/images/*
	@echo "Images removed"
	
clean_texts:
	@rm -rf data/converted/*
	@echo "Texts removed"

clean_cache:
	@rm -rf src/__pycache__
	@echo "pycache removed"

setup:
	@mkdir -p data/converted data/images data/pdf
	@echo "Folders created."
	@pip3 install -r requirements.txt
	@echo Installed dependencies

help:
	@echo -e "\n\
\033[1mPDF-OCR\033[0m\n\n\
\033[1mMAIN COMMANDS\033[0m\n\n\
\t1. \033[1mmake run\033[0m : convert the pdf files to text;\n\
\tThe pdf files need to be placed inside data/pdf.\n\n\
\t2. \033[1mmake clean\033[0m : remove all converted images, \n\ttexts and pycache.\n\n\
\t3. \033[1mmake setup\033[0m : create the necessary folders and \n\tinstall dependencies.\n\
\tThis might need sudo priviledges to run pip3 install.\n\n\
\033[1mOTHER COMMANDS\033[0m\n\n\
\t1. \033[1mmake clean_images\033[0m : remove converted images. \n\n\
\t2. \033[1mmake clean_texts\033[0m : remove converted texts. \n\n\
\t3. \033[1mmake clean_cache\033[0m : remove pycache. \n\n\
\033[1mPATHS\033[0m\n\n\
\t1. \033[1mdata/pdf\033[0m : pdf files path, \n\tplace here the pdfs to be converted.\n\n\
\t2. \033[1mdata/images/[pdf_name]\033[0m : converted images path.\n\n\
\t3. \033[1mdata/converted/[pdf_name]\033[0m : converted text path, \n\tstores the result of the ocr routine.\n\n"


