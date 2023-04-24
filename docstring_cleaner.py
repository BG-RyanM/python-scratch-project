import argparse

"""
A script that goes through a list of Python source files and finds triple-quote docstrings
that can be compressed down to a single line. The source file is modified accordingly.

Generate a list of source files with:
$ find $PWD -type f -name "*.py" > all_py_files.txt

Run the program with:
$ python docstring_cleaner.py --file_list all_py_files.txt
(might need to copy all_py_files.txt to appropriate folder first)
"""


def process_all_files(file_list_file):
    """
    Process all source code files listed in a text file.
    :param file_list_file: the text file, one full file path per line
    :return:
    """
    file = open(file_list_file, "r")
    file_list = file.readlines()
    file.close()
    for f_path in file_list:
        process_file(f_path.strip())


def process_file(file_path):
    """
    Process a single Python source file, writing it out again.
    :param file_path: full path of source file
    """
    # If the file is this one, skip it
    if file_path.find("docstring_cleaner.py") != -1:
        return
    print("Processing file:", file_path)
    file = open(file_path, "r")
    read_lines = file.readlines()
    file.close()

    out_lines = parse_file(read_lines)

    file = open(file_path, "w")
    file.writelines(out_lines)
    file.close()


def parse_file(lines):
    """
    Parse a Python source file, given all the lines of text in it.
    :param lines: list of text lines
    :return: list of text lines, but with compressed docstrings where appropriate
    """
    out_lines = []
    open_quotes_line_num = -1
    for idx, line in enumerate(lines):
        # How many triple quotes are on this line?
        count = line.count('"""')
        if count == 1 and open_quotes_line_num == -1:
            # Found a line with opening triple quotes
            open_quotes_line_num = idx
        elif count == 1 and open_quotes_line_num != -1:
            # Found a line with closing triple quotes
            mashed_lines = mash_lines(lines[open_quotes_line_num : idx + 1])
            out_lines.extend(mashed_lines)
            open_quotes_line_num = -1
        elif open_quotes_line_num == -1:
            # An ordinary line
            out_lines.append(line)
    if open_quotes_line_num != -1:
        # Something went wrong, just output file as it is
        return [line for line in lines]
    return out_lines


def mash_lines(lines):
    """
    Given a list of consecutive text lines that make up a docstring, attempt to
    compress them down to a single line.
    :param lines: list of text line
    :return: compressed lines, given as a list. Might be unchanged source lines.
    """
    if len(lines) > 3:
        # Not a docstring to compress into one line
        return [line for line in lines]

    out_str = ""
    for idx, line in enumerate(lines):
        # Don't strip whitespace characters preceding first line
        out_str += line.strip() if idx > 0 else line.strip("\n")
    out_str += "\n"
    return [out_str]


parser = argparse.ArgumentParser(description="Script to compress docstrings")
parser.add_argument("--file_list", required=True)
args = parser.parse_args()

process_all_files(args.file_list)
