#!/usr/bin/env bash




# Function to scan directory for Markdown files
function scan_directory_for_md_files() {
    local nr_args=$#

    if [[ $nr_args -ne 2 ]] ; then
        # Printing to STDERR
        echo >&2 "ERR: The function should be provided 2 arguments:"
        echo >&2 "- A path to a directory"
        echo >&2 "- A list of file paths"
        return 1
    fi

    local DIR=$1
    local -n md_file_paths=$2  # Use nameref to reference and modify the original array

    if [[ ! -d $DIR ]] ; then
        echo >&2 "ERR: The path $DIR is not a directory or doesn't exist."
        return 1
    fi

    # Append found files to the array
    while IFS= read -r file ; do
        md_file_paths+=("$file")
    done < <(find "$DIR" -name "*.md" -type f)
}

exit_code=0


nr_args=$#
paths=()

if [[ $nr_args -eq 0 ]] ; then
    echo "No arguments (paths) were provided."
    echo "Scanning the current working directory for MarkDown files ('.md')"
    paths=(".")
else
    paths=("$@")   # Command line arguments
fi

MarkDown_files=()

for path in "${paths[@]}" ; do
    if [[ ! -e $path ]] ; then
        # Path doesn't exists
        # Printing to STDERR
        echo >&2 "ERR: Path $path does not exist."
        echo >&2 "The script expects a path to a directory/file/symbolic link."
        exit_code=255
        continue
    elif [[ -h $path || -f $path ]]; then
        # Path to a regular file (`-f`) or a symbolic link (`-h`)
        echo "$path"  # ../ITC-Sheets/REGEX/README.md

        # Check if the file path ends with '.md' (REGEX)
        if [[ ! "$path" =~ .*\.md$ ]]; then
            # Printing to STDERR
            echo >&2 "ERR: The file $path is not a Markdown file, it doesn't have the '.md' extension."
            exit_code=255
        else
            MarkDown_files+=("$path")
        fi
        continue
    elif [[ -d $path ]] ; then
        # Path to a directory
        scan_directory_for_md_files "$path" MarkDown_files
        continue
    else
        # Printing to STDERR
        echo >&2 "ERR: Invalid path $path."
        echo >&2 "The script expects a path to a directory/file/symbolic link."
        exit_code=255
    fi
done



# Print the Markdown files found
echo "Markdown files found:"
for md_file in "${MarkDown_files[@]}" ; do
    
    # 🖼️ REGEX for MarkDown images: ![alt text](path)
    rgx_md_img='\!\[.*\]\([^)]*\)'

    # 🔗 REGEX for MarkDown links: [text](path)
    rgx_md_link_1='[^\!]\[.*\]\([^)]*\)'
    rgx_md_link_2='^\[.*\]\([^)]*\)'

    # 🌐 REGEX for URLs in MarkDown: <https://google.com>, "https://google.com", 'http://google.com'
    rgx_md_url_1='<https?://[^ ]*>'
    rgx_md_url_2='"https?://[^ ]*"'
    rgx_md_url_3="'https?://[^ ]*'"
    
    # 🖼️ REGEX for HTML images (`img` tag)
    rgx_html_img_1='<img.*src[ \t]*=[ \t]*".*".*>'
    rgx_html_img_2="<img.*src[ \t]*=[ \t]*'.*'.*>"

    # 🔗 REGEX for HTML links (`href` tag)
    rgx_html_href_1='href[ \t]*=[ \t]*".*"'
    rgx_html_href_2="href[ \t]*=[ \t]*'.*'"




    # Problem: how to print each matched pattern on a single line    
    rg --vimgrep --only-matching "$rgx_md_img" "$md_file"

    rg --vimgrep --only-matching  -e "$rgx_md_link_1" -e "$rgx_md_link_2"  "$md_file"

    rg --vimgrep --only-matching -e "$rgx_md_url_1"  -e "$rgx_md_url_2"  -e "$rgx_md_url_3"  "$md_file"

    rg --vimgrep --only-matching -e "$rgx_html_img_1" -e "$rgx_html_img_2"  "$md_file"

    rg --vimgrep --only-matching -e "$rgx_html_href_1" -e "$rgx_html_href_2"  "$md_file"



done

exit $exit_code
