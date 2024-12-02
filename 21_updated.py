import cv2
import numpy as np
import difflib
import json
from paddleocr import PaddleOCR

reference_numbers = ["61S012", "DIN62FE", "DE 31 2G SMAW"]

ocr_engine = PaddleOCR(
    det_model_dir="ocr_models/ch_PP-OCRv4_det_infer",
    rec_model_dir="ocr_models/ch_PP-OCRv4_rec_infer",
    cls_model_dir="ocr_models/ch_ppocr_mobile_v2.0_cls_infer",
    rec_char_dict_path="ocr_models/ppocr_keys_v1.txt",
    use_angle_cls=False,
    lang="en",
    det_db_box_thresh=0.3,
    drop_score=0.2
)

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return processed_img

def calculate_match_score(text, ref_numbers):
    
    scores = {ref: difflib.SequenceMatcher(None, text, ref).ratio() for ref in ref_numbers}
    return scores

def ocr_text(image):
    ocr_result = ocr_engine.ocr(image, cls=False)
    return ocr_result[0][0][1][0].strip() if ocr_result and ocr_result[0] else ""

def process_image(image_path):
    image = cv2.imread(image_path)
    preprocessed_image = preprocess_image(image)

    original_text = ocr_text(preprocessed_image)
    flipped_image = cv2.flip(preprocessed_image, 0)
    flipped_text = ocr_text(flipped_image)

    
    original_scores = calculate_match_score(original_text, reference_numbers)
    flipped_scores = calculate_match_score(flipped_text, reference_numbers)

    
    best_match_original = max(original_scores, key=original_scores.get)
    best_match_flipped = max(flipped_scores, key=flipped_scores.get)

    original_best_score = original_scores[best_match_original]
    flipped_best_score = flipped_scores[best_match_flipped]

    threshold = 0.75

    
    if original_best_score >= threshold and flipped_best_score >= threshold:
        
        if original_best_score >= flipped_best_score:
            best_match_reference = best_match_original
            flip_status = "unflipped"
        else:
            best_match_reference = best_match_flipped
            flip_status = "flipped"
    elif original_best_score >= threshold:
        best_match_reference = best_match_original
        flip_status = "unflipped"
    elif flipped_best_score >= threshold:
        best_match_reference = best_match_flipped
        flip_status = "flipped"
    else:
        best_match_reference = "No match"
        flip_status = "unflipped"

    result = {
        "flip_status": flip_status,
        "best_match_reference": best_match_reference,
        "texts": {
            "original_text": original_text,
            "flipped_text": flipped_text
        }
    }
    return result

image_path = r"C:\Users\sruth\Desktop\filtered_images\merged_region_0.png"
result = process_image(image_path)
print(json.dumps(result, indent=4))
