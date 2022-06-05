import re
import os
import tempfile
from pdf2image import convert_from_path
from rich import print
from rich.progress import track
from .ocr import parse_image


def grep_all(filepath: str, pattern: str) -> str:
    """returns all the lines containing the given pattern

    Args:
        filepath (str): path of the file to be scanned
        pattern (str): regex pattern to be searched in the given file

    Returns:
        str: string made up of lines matching the pattern
    """
    grep_list = []
    images = convert_from_path(filepath)

    for i in range(len(images)):

        temp = tempfile.NamedTemporaryFile()
        images[i].save(temp.name, 'JPEG')
        text = parse_image(temp.name)

        for line in text.split('\n'):
            if re.search(pattern, line):
                grep_list.append(line)
    grep_str = '\n'.join(grep_list)

    return grep_str


def find(text: str, pattern: str) -> list:
    """returns a list of dictionary containing line number and the matched line 

    Args:
        text (str): text to be searched for the pattern
        pattern (str): regex pattern to be searched in the given text

    Returns:
        list: list of dictionary containing line number and the matched line 
    """
    occurances = []
    for lno, line in enumerate(text.split('\n')):
        if re.search(pattern, line):
            occurances.append(
                {'lno': f"[italic magenta]Line {str(lno)}: [/italic magenta]",
                 'line': line})
    return occurances


def display_location(filepath: str, pattern: str):
    """displays the line number 

    Args:
        filepath (str): path of the file to be scanned
        pattern (str): regex pattern to be searched in the given file
    """
    images = convert_from_path(filepath)

    for i in track(range(len(images)), description="Progress: "):

        temp = tempfile.NamedTemporaryFile()
        images[i].save(temp.name, 'JPEG')
        occurances = find(parse_image(temp.name), pattern)

        if occurances:
            print(f"[bold red]\nPage {i+1}: [/bold red]")
            for occurance in occurances:
                line_num = occurance["lno"]
                line_list = re.split(f'({pattern})', occurance["line"])
                line_list[1] = "[bold green on blue]" + \
                    f"{line_list[1]}" + "[/bold green on blue]"
                line = ''.join(line_list)
                print(line_num + line)

        temp.close()


def pdf_to_text(filepath: str, pattern: str):
    """converts pdf file to text file

    Args:
        filepath (str): path of the file to be scanned
        pattern (str): regex pattern to be searched in the given file
    """
    images = convert_from_path(filepath)
    f = open(os.path.splitext(filepath)[0] + '-text.txt', 'w')

    for i in range(len(images)):
        temp = tempfile.NamedTemporaryFile()
        images[i].save(temp.name, 'JPEG')
        text = parse_image(temp.name)
        f.write(f"Page {i+1}\n\n" + text)
        temp.close()

    f.close()
