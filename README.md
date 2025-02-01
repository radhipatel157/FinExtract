# Financial Data Extraction Pipeline

This project is financial data extraction pipeline designed to process PDFs into structured financial data. The pipeline uses image processing, OCR, and AI models to detect, extract, and filter financial tables before final processing with the Langflow API && AI model.

## Features
- Converts PDF pages into images.
- Detects and crops images containing tables.
- Converts cropped table images into CSV files.
- Merges CSV data into a single text file.
- Uses Langflow API and Llama AI model for advanced filtering and extraction.

## Approaches

### Approach 1: Simple Flow
1. **Environment Setup**
   - Install all required libraries.
2. **PDF to Images**
   - Convert the entire PDF into images.
3. **Table Detection & Cropping**
   - Select images containing tables and crop them.
4. **Image to CSV Conversion**
   - Convert cropped images into CSV files.
5. **Merge CSV Files**
   - Merge all CSV files into a single text file.
6. **Langflow API Processing**
   - Input the text file into Langflow API for further data extraction.

### Approach 2: Short Flow
1. **Environment Setup**
   - Install all required libraries.
2. **PDF to Images (Page-wise)**
   - Convert the PDF into images on a page-by-page basis.
3. **Filter Pages with Tables**
   - Identify and retain only those pages containing tables.
4. **OCR on Selected Pages**
   - Perform OCR on filtered pages and convert them into text.
5. **Further Image Processing**
   - Convert cropped table images into CSV files.
6. **Advanced Filtering with Llama AI**
   - Use Llama AI to filter only the necessary cropped images using OCR text data.
7. **Merge CSV to Text**
   - Combine selected CSV files into a single text file for further processing.
8. **Chunk Text for Processing**
   - Split the text file into manageable chunks due to token limits.
9. **Prediction and Output**
   - Use Langflow API for final financial data extraction.

## Instructions to Upload and Run the Code in Google Colab

1. **Download the Jupyter Notebook Files:**
   - Download the two `.ipynb` files from this repository.

2. **Upload the Files to Google Colab:**
   - Go to [Google Colab](https://colab.research.google.com/).
   - Click on the **File** menu, then select **Upload notebook**.
   - Upload the `.ipynb` files you downloaded from this repository.

3. **Run the Code:**
   - Once the notebooks are uploaded, you can start running the code cells by clicking on each cell and pressing **Shift + Enter**.
   - Ensure that all dependencies are installed (as listed in the **Dependencies** section) by running the required installation commands in the first cell of each notebook.
   


## Dependencies
Here’s a list of dependencies you can add to your GitHub README file:

## Dependencies
- Python 3.x
- OpenCV
- Pillow
- NumPy
- pandas
- TensorFlow
- PaddlePaddle GPU
- PaddleOCR
- pdf2image
- Poppler-utils
- layoutparser
- pytesseract
- llama-index
- langflow
- argparse
- requests
- protobuf


