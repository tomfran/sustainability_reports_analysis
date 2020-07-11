# Python PDF OCR

Python PDF-OCR project.  
The goal of this project is to extract text from a pdf file for further analysis.
The pdfs comes from companies, so data is organized in comanies folders containing pdf files.

## Setup

After cloning run `make setup` to create the required folders and to install dependencies.  
Use `make help` to see all the make rules.

## Paths

Pdf files are placed inside `data/pdf/company_folder/pdfs_files`  
Converted text is inside `data/converted/[company_name]/[pdf_name]`  

## How does it work?

### PDF to image conversion

The first step is to convert PDF files into images, the library used is [pdf2image](https://github.com/Belval/pdf2image).

### Paragraph detection

Pdf files can sometimes have multiple columns or small paragraphs in a page.  
When analyzing a page, the ocr library does not recognize those areas and simply parses the text as one line, ignoring the spaces between columns.
To improve ocr results the paragraphs are detected and cropped.

The paragraph detection is mainly an Image processing task.  
The library in use is [Open CV](https://opencv.org/).

The main steps are described below:
1. The pages are converted to greyscale images;
2. The images are [thresholded](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html) to make text pop, as the result is a white text on black background;
3. The thresholded images are then [dilated](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html) to merge adjacent words, thus paragraphs can be found;
4. The final step involves finding [contours](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contours_begin/py_contours_begin.html#contours-getting-started) to the previously merged paragraphs and crop them.

The result is then a set of paragraphs which can be analyzed.

### Text recognition

The last step of the conversion process is the text recognition.  
The library in use is [pyocr](https://gitlab.gnome.org/World/OpenPaperwork/pyocr).


## Known issues

The paragraph detection process is not perfect, it can sometimes identify non-existing paragraphs in, for instance, images.
Sometimes the text recognition phase can found some noise in the text, recognizing some additional letters or spaces.

## Notes

To speed up computation the main program uses a multithreading approach: single threads are used to find paragraphs and then text in a page.
The result is a faster computation, with a  tradeoff of higher CPU and RAM usage.

Developed and tested in a linux environment.
