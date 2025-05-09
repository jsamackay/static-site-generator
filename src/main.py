from textnode import TextNode, TextType
from markdown_blocks import markdown_to_html_node
import os
import sys
import shutil


def main():
    # Default basepath to "/" if not provided
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_directory("static", "docs")
    generate_pages_recursive(
        "content/",
        "template.html",
        "docs/",
        basepath
    )


def copy_directory(source, destination):
    """
    Recursively copies all contents from the source directory to the destination directory.
    Deletes all contents of the destination directory before copying.
    Logs each file and directory being copied.
    """
    # Ensure the source directory exists
    if not os.path.exists(source):
        raise FileNotFoundError(f"Source directory '{source}' does not exist.")

    # Delete all contents of the destination directory
    if os.path.exists(destination):
        shutil.rmtree(destination)
        print(f"Deleted all contents of '{destination}'.")

    # Recreate the destination directory
    os.makedirs(destination)
    print(f"Created destination directory '{destination}'.")

    # Walk through the source directory
    for root, dirs, files in os.walk(source):
        # Compute the relative path from the source directory
        relative_path = os.path.relpath(root, source)
        # Compute the corresponding destination path
        dest_path = os.path.join(destination, relative_path)

        # Create directories in the destination
        for dir_name in dirs:
            dir_path = os.path.join(dest_path, dir_name)
            os.makedirs(dir_path, exist_ok=True)
            print(f"Created directory: {dir_path}")

        # Copy files to the destination
        for file_name in files:
            src_file = os.path.join(root, file_name)
            dest_file = os.path.join(dest_path, file_name)
            shutil.copy2(src_file, dest_file)
            print(f"Copied file: {src_file} -> {dest_file}")

def extract_title(markdown):
    """
    Extracts the title from the markdown content.
    The title is expected to be the first line of the markdown.
    """
    if len(markdown.strip()) == 0:
        raise Exception("Markdown content is empty")
    lines = markdown.split("\n")
    if len(lines) == 0:
        raise Exception("Markdown content is empty")
    return lines[0].strip("# ").strip()

def generate_page(from_path, template_path, dest_path, base_path):
    """
    Reads content from the source file (from_path) and the template file (template_path),
    and prepares to generate the final page at the destination (dest_path).
    """
    # Read content from the source file
    with open(from_path, "r", encoding="utf-8") as from_file:
        from_content = from_file.read()
        print(f"Read content from {from_path}")

    # Read content from the template file
    with open(template_path, "r", encoding="utf-8") as template_file:
        template_content = template_file.read()
        print(f"Read content from {template_path}")

    html = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)
    
    # Replace placeholders in the template with actual content
    html = template_content.replace("{{ Content }}", html)
    html = html.replace("{{ Title }}", title)
    html = html.replace("href=\"/", f"href=\"{base_path}")
    html = html.replace("src=\"/", f"src=\"{base_path}")
    # Write the final HTML to the destination file
    with open(dest_path, "w", encoding="utf-8") as dest_file:
        dest_file.write(html)
        print(f"Wrote content to {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    """
    Recursively generates pages from markdown files in the source directory (from_path)
    using the template file (template_path) and saves them to the destination directory (dest_path).
    """
    # Ensure the destination directory exists
    os.makedirs(dest_dir_path, exist_ok=True)
    print(f"Created destination directory '{dest_dir_path}'.")

    # Walk through the source directory
    for root, dirs, files in os.walk(dir_path_content):
        # Compute the relative path from the source directory
        relative_path = os.path.relpath(root, dir_path_content)
        # Compute the corresponding destination path
        dest_path = os.path.join(dest_dir_path, relative_path)

        # Create directories in the destination
        for dir_name in dirs:
            dir_path = os.path.join(dest_path, dir_name)
            os.makedirs(dir_path, exist_ok=True)
            print(f"Created directory: {dir_path}")

        # Process markdown files
        for file_name in files:
            if file_name.endswith(".md"):
                src_file = os.path.join(root, file_name)
                dest_file = os.path.join(dest_path, file_name.replace(".md", ".html"))
                generate_page(src_file, template_path, dest_file, base_path)

main()
