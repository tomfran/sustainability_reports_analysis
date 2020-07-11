clean_ocr:
	@cd pdf_ocr && make -s clean

run:
	@python3.8 main.py