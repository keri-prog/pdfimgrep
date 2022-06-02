import io
import json
import cv2
import numpy as np
import requests

api_key = open("key.txt", 'r').read()


def parse_image(filepath: str):
    """_summary_

    Args:
        filepath (str): filepath of the file to be read 

    Returns:
        _type_: _description_
    """
    img = cv2.imread(filepath)
    height, width, _ = img.shape

    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".jpg", img, [1, 90])
    file_bytes = io.BytesIO(compressedimage)

    result = requests.post(url_api,
              files = {"screenshot.jpg": file_bytes},
              data = {"apikey": api_key,
                      "language": "eng"})
    result = result.content.decode()
    result = json.loads(result)

    parsed_results = result.get("ParsedResults")[0]
    text_detected = parsed_results.get("ParsedText")
    
    return text_detected