import sys
import os.path
import re
import hashlib

def convert_markdown_to_html(input_filename, output_filename):
    with open(input_filename, 'r') as input_file:
        markdown_content = input_file.read()
        html_content = process_markdown(markdown_content)
    
    with open(output_filename, 'w') as output_file:
        output_file.write(html_content)

def process_markdown(markdown_content):
    lines = markdown_content.split("\n")
    html_lines = []
    inside_paragraph = False
    md5_pattern = re.compile(r'\[\[(.*?)\]\]')
    remove_c_pattern = re.compile(r'\(\((.*?)\)\)')

    for line in lines:
        if line.strip():
            if not inside_paragraph:
                inside_paragraph = True
                html_lines.append("<p>")
            
            # Process MD5 and remove 'c' within the line
            line = md5_pattern.sub(lambda x: hashlib.md5(x.group(1).encode('utf-8')).hexdigest(), line)
            line = remove_c_pattern.sub(lambda x: x.group(1).replace('c', '', flags=re.IGNORECASE), line)
            
            html_lines.append(f"    {line}")
        else:
            if inside_paragraph:
                inside_paragraph = False
                html_lines.append("</p>")
            html_lines.append(line)
    
    if inside_paragraph:
        html_lines.append("</p>")
    
    return "\n".join(html_lines)

if len(sys.argv) < 3:
    sys.stderr.write("Usage: ./markdown2html.py <input_file> <output_file>\n")
    sys.exit(1)

input_filename = sys.argv[1]
output_filename = sys.argv[2]

if not os.path.exists(input_filename):
    sys.stderr.write(f"Missing {input_filename}\n")
    sys.exit(1)

convert_markdown_to_html(input_filename, output_filename)
sys.exit(0)

