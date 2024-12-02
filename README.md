# OCR Text Matching and Flip Detection

## Overview
This repository provides a pipeline to **detect flipped text** and match extracted text against a predefined set of **reference numbers** using OCR. The solution integrates **PaddleOCR** for text recognition, preprocessing for enhanced text clarity, and similarity matching using **difflib** to determine the closest reference match.

## Key Features
- **OCR-Based Text Extraction**: Extracts text from images using PaddleOCR.
- **Preprocessing**: Applies adaptive thresholding for better OCR results.
- **Flip Detection**: Compares OCR results from the original and flipped images to determine orientation.
- **Text Matching**: Uses similarity scoring to match extracted text against a set of reference numbers.
- **Threshold-Based Decision**: Ensures reliable matching using a configurable similarity threshold.

## Workflow
1. **Preprocessing**:
   - Converts the image to grayscale and applies adaptive thresholding to enhance text clarity.
2. **OCR and Flip Detection**:
   - Extracts text from the original and vertically flipped versions of the image.
   - Compares similarity scores for both orientations to determine the flip status.
3. **Text Matching**:
   - Calculates similarity scores between extracted text and reference numbers.
   - Identifies the best match above a similarity threshold (default: 0.75).
4. **Output**:
   - Returns flip status, best matching reference number, and OCR results from both orientations.


