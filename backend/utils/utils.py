
"""
@fileoverview This module provides utilities for generating PDFs from Markdown content.
It includes classes and functions for handling PDF creation, content sanitization, and
Markdown parsing to ensure proper formatting and character handling.
"""

import re
from fpdf import FPDF


class CustomPDF(FPDF):
    """
    A custom PDF class extending FPDF to set default margins and add a footer.
    """
    def __init__(self):
        """
        Initializes the CustomPDF with specific margins and auto page break settings.
        """
        super().__init__()
        self.set_left_margin(25)
        self.set_right_margin(25)
        self.set_auto_page_break(auto=True, margin=25)

    def footer(self):
        """
        Adds a footer to each page with the current page number.
        """
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def sanitize_content(content):
    """
    Sanitizes the content by encoding and decoding to handle special characters consistently.

    Args:
        content (str): The content to sanitize.

    Returns:
        str: The sanitized content.
    """
    return content.encode('utf-8', 'ignore').decode('utf-8')

def replace_problematic_characters(content):
    """
    Replaces problematic Unicode characters with more common equivalents.

    Args:
        content (str): The content in which to replace characters.

    Returns:
        str: The content with replaced characters.
    """
    replacements = {
        '\u2013': '-',  # en dash to hyphen
        '\u2014': '--',  # em dash to double hyphen
        '\u2018': "'",   # left single quote to apostrophe
        '\u2019': "'",   # right single quote to apostrophe
        '\u201c': '"',   # left double quote to double quote
        '\u201d': '"',   # right double quote to double quote
        '\u2026': '...', # ellipsis
        '\u2022': '*',   # bullet
        '\u2122': 'TM'   # trademark symbol
    }
    for char, replacement in replacements.items():
        content = content.replace(char, replacement)
    return content

def generate_pdf_from_md(content, filename='output.pdf'):
    """
    Generates a PDF from Markdown content.

    Args:
        content (str): The Markdown content to convert to PDF.
        filename (str, optional): The name of the output PDF file. Defaults to 'output.pdf'.

    Returns:
        str: A message indicating the result of the PDF generation.
    """
    try:
        pdf = CustomPDF()
        pdf.add_page()
        pdf.set_font('Arial', '', 12)

        # Sanitize and replace problematic characters in content
        content = sanitize_content(content)
        content = replace_problematic_characters(content)

        lines = content.split('\n')
        for line in lines:
            if line.startswith('#'):
                header_level = min(line.count('#'), 4)
                header_text = re.sub(r'\*{2,}', '', line.strip('# ').strip())
                pdf.set_font('Arial', 'B', 18 - header_level * 2)
                pdf.ln(8 if header_level == 1 else 5)
                pdf.multi_cell(0, 10, header_text)
                pdf.set_font('Arial', '', 12)
            else:
                process_markdown_line(pdf, line)
                pdf.ln(8)

        pdf.output(filename)
        return f"PDF generated: {filename}"

    except Exception as e:
        return f"Error generating PDF: {e}"

def process_markdown_line(pdf, line):
    """
    Parses a line for Markdown styling, including bold, italics, and links.

    Args:
        pdf (CustomPDF): The PDF object to write to.
        line (str): The line of text to process.
    """
    parts = re.split(r'(\*\*.*?\*\*|\*.*?\*|\[.*?\]\(.*?\)|https?://\S+)', line)
    for part in parts:
        if re.match(r'\*\*.*?\*\*', part):  # Bold
            text = part.strip('*')
            pdf.set_font('Arial', 'B', 12)
            pdf.write(10, text)
        elif re.match(r'\*.*?\*', part):  # Italics
            text = part.strip('*')
            pdf.set_font('Arial', 'I', 12)
            pdf.write(10, text)
        elif re.match(r'\[.*?\]\(.*?\)', part):  # Markdown link
            display_text = re.search(r'\[(.*?)\]', part).group(1)
            url = re.search(r'\((.*?)\)', part).group(1)
            pdf.set_text_color(0, 0, 255)
            pdf.set_font('Arial', 'U', 12)
            pdf.write(10, display_text, url)
            pdf.set_text_color(0, 0, 0)  # Reset color
            pdf.set_font('Arial', '', 12)
        elif re.match(r'https?://\S+', part):  # Plain URL
            url = part
            pdf.set_text_color(0, 0, 255)
            pdf.set_font('Arial', 'U', 12)
            pdf.write(10, url, url)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Arial', '', 12)
        else:
            pdf.set_font('Arial', '', 12)
            pdf.write(10, part)

