import io
import json
import cv2
import requests

api_key = open("./utils/key.txt", 'r').read()


def parse_image(filepath: str) -> str:
    """parses the given image and returns the text read from it

    Args:
        filepath (str): path of the file to be scanned

    Returns:
        str: text extracted from the given image
    """
    img = cv2.imread(filepath)
    height, width, _ = img.shape

    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".jpg", img, [1, 90])
    file_bytes = io.BytesIO(compressedimage)

    result = requests.post(url_api,
                           files={"screenshot.jpg": file_bytes},
                           data={"apikey": api_key,
                                 "language": "eng"})
    result = result.content.decode()
    result = json.loads(result)

    parsed_results = result.get("ParsedResults")[0]
    text_detected = parsed_results.get("ParsedText")

    return text_detected
