import re
import tempfile
from pdf2image import convert_from_path
from rich import print
from rich.progress import track
from .ocr import parse_image


def grep_all(filepath: str, pattern: str):
    """_summary_

    Args:
        filepath (str): _description_
        pattern (str): _description_

    Returns:
        _type_: _description_
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
            occurances.append(
                {'lno': f"[italic magenta]Line {str(lno)}: [/italic magenta]",
                 'line': line})
    return occurances


def display_location(filepath: str, pattern: str):
    """_summary_

    Args:
        filepath (str): _description_
        pattern (str): _description_
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
                line_list[1] = "[bold green on blue]" + f"{line_list[1]}"+ "[/bold green on blue]"
                line = ''.join(line_list)
                print(line_num + line)

        temp.close()


def pdf_to_text(filepath: str, pattern: str):
    """_summary_

    Args:
        filepath (str): _description_
        pattern (str): _description_
    """
    images = convert_from_path(filepath)
    f = open(filepath.split('.')[0] + '-text.txt', 'w')

    for i in range(len(images)):
        temp = tempfile.NamedTemporaryFile()
        images[i].save(temp.name, 'JPEG')
        text = parse_image(temp.name, pattern)
        f.write(f"Page {i+1}\n\n" + text)
        temp.close()

    f.close()

