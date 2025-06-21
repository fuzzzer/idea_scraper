import os

def collect_py_files_content(directory, output_file):
    # Check if the input directory exists
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the output file in write mode
    with open(output_file, 'w', encoding='utf-8') as outfile:
        file_count = 0  # Track how many .py files we find
        # Walk through the directory recursively
        for root, dirs, files in os.walk(directory):
            print(f"Entering directory: {root}")  # Debug: print each directory entered
            for file in files:
                if file.endswith('.py') and not file.endswith('.g.py'):
                    file_count += 1
                    # Get the full file path
                    file_path = os.path.join(root, file)
                    print(f"Found py file: {file_path}")  # Debug: print each .py file found
                    # Read the content of the py file and write it to the output file
                    with open(file_path, 'r', encoding='utf-8') as py_file:
                        content = py_file.read()
                        outfile.write(f"// Content from: {file_path}\n\n")
                        outfile.write(content)
                        outfile.write("\n\n")  # Add spacing between files

        # Summary of the process
        if file_count == 0:
            print("No .py files found.")
        else:
            print(f"Successfully processed {file_count} .py files.")

if __name__ == "__main__":
    # Get the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Use relative path from script's directory
    lib_folder = os.path.join(script_dir, '../reddit_scraper')
    output_txt_file = os.path.join(script_dir, 'outputs/reddit_scraper.txt')

    # Collect all .py file contents and write them to the output file
    collect_py_files_content(lib_folder, output_txt_file)
