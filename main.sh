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

        # Check if the file path ends with .md
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
for file in "${MarkDown_files[@]}" ; do
    echo "$file"
done

exit $exit_code
