#!/usr/bin/env python3
import typing
from enum import Enum
import sys
import os
import re        # regular expressions
import requests  # for testing HTTP/HTTPS connections


exit_code=0



regular_expressions = {
    # 📄 REGEX for MarkDown file extension (file name ends with `.md`)
    'rgx_md_file_extension': r'.*\.md$',

    # 🖼️ REGEX for MarkDown images: ![alt text](path)
    'rgx_md_img': r'\!\[.*\]\([^)]*\)',

    # 🔗 REGEX for MarkDown links: [text](path)
    'rgx_md_link_pattern_1': r'[^\!]\[.*\]\([^#][^)]*\)',
    'rgx_md_link_pattern_2': r'^\[.*\]\([^#][^)]*\)',

    # 🌐 REGEX for URLs in MarkDown: <https://google.com>, "https://google.com", 'http://google.com'
    'rgx_md_url_pattern_1': r'<https?://[^ ]*>',
    'rgx_md_url_pattern_2': r'"https?://[^ ]*"',
    'rgx_md_url_pattern_3': r"'https?://[^ ]*'",

    # 🖼️ REGEX for HTML images (`img` tag)
    'rgx_html_img_pattern_1': r'<img.*src[ \t]*=[ \t]*".*".*>',
    'rgx_html_img_pattern_2': r"<img.*src[ \t]*=[ \t]*'.*'.*>",

    # 🔗 REGEX for HTML links (`href` tag)
    'rgx_html_href_url_pattern_1': r'href[ \t]*=[ \t]*"https?://[^ ]*"',
    'rgx_html_href_url_pattern_2': r"href[ \t]*=[ \t]*'https?://[^ ]*'"
}




class colors:


  '''
  Code from: https://www.geeksforgeeks.org/print-colors-python-terminal/
  
  Colors class:reset all colors with colors.reset; two
  sub classes fg for foreground
  and bg for background; use as colors.subclass.colorname.
  i.e. colors.fg.red or colors.bg.greenalso, the generic bold, disable,
  underline, reverse, strike through,
  and invisible work with the main class i.e. colors.bold'''
  reset = '\033[0m'
  bold = '\033[01m'
  disable = '\033[02m'
  underline = '\033[04m'
  reverse = '\033[07m'
  strikethrough = '\033[09m'
  invisible = '\033[08m'

  class fg:
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'






def scan_directory_for_md_files(path: str, md_file_paths: list[str]) -> list[str]:
    """
    Iterates recursively the directory given by the first argument
    and appends the relative path to all MarkDown files (having the extension '.md')
    to the list contained by the second argument.

    The function returns the list with the appended file paths.
    """
    directories = []
    rgx = regular_expressions['rgx_md_file_extension']
    
    for dentry in os.listdir(path):

        rel_path = os.path.join(path, dentry)

        if os.path.isdir(rel_path):
            directories.append(rel_path)
        elif os.path.isfile(rel_path) and re.search(rgx, rel_path) is not None:
            md_file_paths.append(rel_path)
    
    for directory in directories:
        scan_directory_for_md_files(directory, md_file_paths)
    
    return md_file_paths



def iterate_cmd_args_and_get_md_files() -> list[str]:
    
    paths = []

    if len(sys.argv) == 1:
        # No arguments were provided to the script
        # Scanning the current working directory for MarkDown file
        paths = ['.']
    else:
        paths = [sys.argv[i] for i in range(1, len(sys.argv))]
    

    # Removing duplicated arguments
    paths = list(set(paths))
    

    md_file_paths = []

    
    for path in paths:

        if os.path.isfile(path):
            # Regular file
            rgx = regular_expressions['rgx_md_file_extension']
            
            if re.search(rgx, path) is not None:
                md_file_paths.append(path)
            else:
                print(f"ERROR: Invalid argument.", file=sys.stderr)
                print(f"      {path} is not a MarkDown file.", file=sys.stderr)
                print(f"       It doesn't have the '.md' extension.", file=sys.stderr)
                exit_code=255
                continue
        elif os.path.isdir(path):
            # Directory
            scan_directory_for_md_files(path, md_file_paths)
        else:
            print(f"ERROR: Invalid argument.", file=sys.stderr)
            print(f"      {path} is neither a regular file or a directory.", file=sys.stderr)
            exit_code=255
            continue
    return md_file_paths


def match_rgx_md_img_against_file(file_path):
    """
    Returned format:
    file_path:line:column:pattern
    """
    rgx = regular_expressions['rgx_md_img']
    


    # Open the file and read line by line
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            # Find all matches of the regex in the current line
            for match in re.finditer(rgx, line):
                start_column = match.start() + 1
                pattern = match.group(0)
                print("🖼️  ", end='')
                print(f"{colors.fg.purple}{file_path}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.green}{line_num}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.blue}{start_column}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.yellow}{pattern}{colors.reset}")
                # matches.append(f"{file_path}:{line_num}:{start_column}:{pattern}")
    




def match_rgx_md_link_pattern_1_against_file(file_path):
    """
    Returned format:
    file_path:line:column:pattern
    """
    rgx = regular_expressions['rgx_md_link_pattern_1']
    


    # Open the file and read line by line
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            # Find all matches of the regex in the current line
            for match in re.finditer(rgx, line):
                start_column = match.start() + 1
                pattern = match.group(0)
                print("🔗  ", end='')
                print(f"{colors.fg.purple}{file_path}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.green}{line_num}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.blue}{start_column}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.yellow}{pattern}{colors.reset}")
    
    



def match_rgx_md_link_pattern_2_against_file(file_path):
    """
    Returned format:
    file_path:line:column:pattern
    """
    rgx = regular_expressions['rgx_md_link_pattern_2']
    


    # Open the file and read line by line
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            # Find all matches of the regex in the current line
            for match in re.finditer(rgx, line):
                start_column = match.start() + 1
                pattern = match.group(0)
                print("🔗  ", end='')
                print(f"{colors.fg.purple}{file_path}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.green}{line_num}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.blue}{start_column}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.yellow}{pattern}{colors.reset}")
    
    




def match_rgx_md_url_pattern_1_against_file(file_path):
    """
    Returned format:
    file_path:line:column:pattern
    """
    rgx = regular_expressions['rgx_md_url_pattern_1']
    


    # Open the file and read line by line
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            # Find all matches of the regex in the current line
            for match in re.finditer(rgx, line):
                start_column = match.start() + 1
                pattern = match.group(0)
                print("🌐  ", end='')
                print(f"{colors.fg.purple}{file_path}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.green}{line_num}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.blue}{start_column}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.yellow}{pattern}{colors.reset}")
    
    






def match_rgx_md_url_pattern_2_against_file(file_path):
    """
    Returned format:
    file_path:line:column:pattern
    """
    rgx = regular_expressions['rgx_md_url_pattern_2']


    # Open the file and read line by line
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            # Find all matches of the regex in the current line
            for match in re.finditer(rgx, line):
                start_column = match.start() + 1
                pattern = match.group(0)
                print("🌐  ", end='')
                print(f"{colors.fg.purple}{file_path}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.green}{line_num}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.blue}{start_column}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.yellow}{pattern}{colors.reset}")
    





def match_rgx_md_url_pattern_3_against_file(file_path):
    """
    Returned format:
    file_path:line:column:pattern
    """
    rgx = regular_expressions['rgx_md_url_pattern_3']
    


    # Open the file and read line by line
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            # Find all matches of the regex in the current line
            for match in re.finditer(rgx, line):
                start_column = match.start() + 1
                pattern = match.group(0)
                print("🌐  ", end='')
                print(f"{colors.fg.purple}{file_path}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.green}{line_num}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.blue}{start_column}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.yellow}{pattern}{colors.reset}")
    
    



def match_rgx_html_img_pattern_1_against_file(file_path):
    """
    Returned format:
    file_path:line:column:pattern
    """
    rgx = regular_expressions['rgx_html_img_pattern_1']
    


    # Open the file and read line by line
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            # Find all matches of the regex in the current line
            for match in re.finditer(rgx, line):
                start_column = match.start() + 1
                pattern = match.group(0)
                print("🖼️  ", end='')
                print(f"{colors.fg.purple}{file_path}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.green}{line_num}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.blue}{start_column}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.yellow}{pattern}{colors.reset}")
    
    




def match_rgx_html_img_pattern_2_against_file(file_path):
    """
    Returned format:
    file_path:line:column:pattern
    """
    rgx = regular_expressions['rgx_html_img_pattern_2']
    


    # Open the file and read line by line
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            # Find all matches of the regex in the current line
            for match in re.finditer(rgx, line):
                start_column = match.start() + 1
                pattern = match.group(0)
                print("🖼️  ", end='')
                print(f"{colors.fg.purple}{file_path}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.green}{line_num}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.blue}{start_column}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.yellow}{pattern}{colors.reset}")
    
    



def match_rgx_html_href_url_pattern_1_against_file(file_path):
    """
    Returned format:
    file_path:line:column:pattern
    """
    rgx = regular_expressions['rgx_html_href_url_pattern_1']
    


    # Open the file and read line by line
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            # Find all matches of the regex in the current line
            for match in re.finditer(rgx, line):
                start_column = match.start() + 1
                pattern = match.group(0)
                print("🔗  ", end='')
                print(f"{colors.fg.purple}{file_path}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.green}{line_num}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.blue}{start_column}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.yellow}{pattern}{colors.reset}")
    
    



def match_rgx_html_href_url_pattern_2_against_file(file_path):
    """
    Returned format:
    file_path:line:column:pattern
    """
    rgx = regular_expressions['rgx_html_href_url_pattern_2']
    


    # Open the file and read line by line
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            # Find all matches of the regex in the current line
            for match in re.finditer(rgx, line):
                start_column = match.start() + 1
                pattern = match.group(0)
                print("🔗  ", end='')
                print(f"{colors.fg.purple}{file_path}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.green}{line_num}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.blue}{start_column}{colors.fg.cyan}:", end='')
                print(f"{colors.fg.yellow}{pattern}{colors.reset}")
    
    


def main() -> None:
    md_file_paths = iterate_cmd_args_and_get_md_files()
    


    print("MarkDown files:")
    [print(colors.fg.purple, f"{file}", colors.reset) for file in md_file_paths]

    
    for path in md_file_paths:
        print(f"MarkDown images in {path}:")
        match_rgx_md_img_against_file(path)
        print()
        print(f"MarkDown links in {path}:") 
        match_rgx_md_link_pattern_1_against_file(path)
        match_rgx_md_link_pattern_2_against_file(path)
        print()
        print(f"MarkDown URLs in {path}:") 
        match_rgx_md_url_pattern_1_against_file(path)
        match_rgx_md_url_pattern_2_against_file(path)
        match_rgx_md_url_pattern_3_against_file(path)
        print()
        print(f"HTML images in {path}:") 
        match_rgx_html_img_pattern_1_against_file(path)
        match_rgx_html_img_pattern_2_against_file(path)
        print()
        print(f"HTML 'href' URLs in {path}:") 
        match_rgx_html_href_url_pattern_1_against_file(path)
        match_rgx_html_href_url_pattern_2_against_file(path)
        print()

if __name__ == "__main__":
    main()



