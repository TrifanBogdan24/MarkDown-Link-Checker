#!/usr/bin/env python3
import typing
import sys
import os
import re



exit_code=0


regular_expressions = {
    # 📄 REGEX for MarkDown file extension (file name ends with `.md`)
    'rgx_md_file_extension': r'.*\.md$',

    # 🖼️ REGEX for MarkDown images: ![alt text](path)
    'rgx_md_img': r'\!\[.*\]\([^)]*\)',

    # 🔗 REGEX for MarkDown links: [text](path)
    'rgx_md_link_pattern_1': r'[^\!]\[.*\]\([^)]*\)',
    'rgx_md_link_pattern_2': r'^\[.*\]\([^)]*\)',

    # 🌐 REGEX for URLs in MarkDown: <https://google.com>, "https://google.com", 'http://google.com'
    'rgx_md_url_pattern_1': r'<https?://[^ ]*>',
    'rgx_md_url_pattern_2': r'"https?://[^ ]*"',
    'rgx_md_url_pattern_3': r"'https?://[^ ]*'",

    # 🖼️ REGEX for HTML images (`img` tag)
    'rgx_html_img_pattern_1': r'<img.*src[ \t]*=[ \t]*".*".*>',
    'rgx_html_img_pattern_2': r"<img.*src[ \t]*=[ \t]*'.*'.*>",

    # 🔗 REGEX for HTML links (`href` tag)
    'rgx_html_href_pattern_1': r'href[ \t]*=[ \t]*".*"',
    'rgx_html_href_pattern_2': r"href[ \t]*=[ \t]*'.*'"
}



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
        print(f"{path}")

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
            print(f"ERROR: Invalid argument. {path} is neither a regular file or a directory.", file=sys.stderr)
            exit_code=255

    return md_file_paths


def main() -> None:
    md_file_paths = iterate_cmd_args_and_get_md_files()
    

    print("MarkDown files:")
    [print(file) for file in md_file_paths]


if __name__ == "__main__":
    main()



