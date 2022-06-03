import re
import tempfile
from pdf2image import convert_from_path
from rich import print
from rich.text import Text
from rich.console import Console
from rich.progress import track
from rich.theme import Theme
from rich.highlighter import RegexHighlighter
from ocr import parse_image


class CustomRegExHighlighter(RegexHighlighter):

    def __init__(self, pattern):
        super().__init__()
        highlights = [re.compile(f"(?P<pattern>{pattern})")]
        base_style = "regex"


def grep(text: str, pattern: str):
    """_summary_

    Args:
        text (str): _description_
        pattern (str): _description_

    Returns:
        _type_: _description_
    """
    grep_list = []

    for lno, line in enumerate(text.split('\n')):
        if re.search(pattern, line):
            grep_list.append(line)
    grep_str = '\n'.join(grep_list)

    return grep_str


def find(text: str, pattern: str):
    """_summary_

    Args:
        text (str): _description_
        pattern (str): _description_

    Returns:
        _type_: _description_
    """
    occurances = []
    for lno, line in enumerate(text.split('\n')):
        if re.search(pattern, line):
            occurances.append({'lno': f"Line: {str(lno)}: ", 'line': line})
    return occurances


def display_location(filepath: str, pattern: str):
    images = convert_from_path(filepath)
    theme = Theme({"regex.pattern": "bold magenta"})
    console = Console(highlighter=CustomRegExHighlighter(pattern), theme=theme)

    for i in track(range(len(images)), description="Progress: "):

        temp = tempfile.NamedTemporaryFile()
        images[i].save(temp.name, 'JPEG')
        occurances = find(parse_image(temp.name), pattern)
        
        if occurances:
            print(f"\nPage {i+1}: ")
            for occurance in occurances:
                print(occurance["lno"] + occurance["line"])
        
        print()
        temp.close()


def pdf_to_text(filepath: str, pattern: str):
    images = convert_from_path(filepath)
    f = open(filepath.split('.')[0] + '-text.txt', 'w')

    for i in range(len(images)):
        temp = tempfile.NamedTemporaryFile()
        images[i].save(temp.name, 'JPEG')
        text = parse_image(temp.name, pattern)
        f.write(f"Page {i+1}\n\n" + text)
        temp.close()

    f.close()


display_location(
    "/home/kushojha/pdfimgrep/CSE2010_ADVANCED-C-PROGRAMMING_ETH_1.0_57_CSE2010_59 ACP_32.pdf", "Module")
