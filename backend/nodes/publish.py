
"""
@fileoverview This module defines the PublishNode class, which is responsible for formatting and saving
research reports in either PDF or Markdown format. It utilizes utility functions to convert Markdown content
to PDF and manages the output directory for storing the generated reports.
"""

import os
from datetime import datetime
from langchain_core.messages import AIMessage
from ..utils.utils import generate_pdf_from_md
from ..classes import ResearchState

class PublishNode:
    """
    Represents the publish node in the research workflow.

    Attributes:
        output_dir (str): The directory where the generated reports will be saved.
    """

    def __init__(self, output_dir="reports"):
        """
        Initializes the PublishNode with a specified output directory.

        Args:
            output_dir (str): The directory to save the generated reports. Defaults to "reports".
        """
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"📁 Created output directory at '{self.output_dir}'")
        else:
            print(f"📂 Output directory '{self.output_dir}' already exists.")

    async def markdown_to_pdf(self, markdown_content: str, output_path: str):
        """
        Converts Markdown content to a PDF file.

        Args:
            markdown_content (str): The content in Markdown format to be converted.
            output_path (str): The file path where the PDF will be saved.

        Raises:
            Exception: If the PDF generation fails.
        """
        try:  
            print(f"📝 Converting Markdown to PDF at '{output_path}'...")
            generate_pdf_from_md(markdown_content, output_path)
            print(f"✅ PDF successfully generated at '{output_path}'")
        except Exception as e:
            print(f"❌ Failed to generate PDF: {str(e)}")
            raise Exception(f"Failed to generate PDF: {str(e)}")

    async def format_output(self, state: ResearchState):
        """
        Formats the research report based on the specified output format and saves it.

        Args:
            state (ResearchState): The current state of the research process, including the report content.

        Returns:
            dict: A dictionary containing a message about the saved report.
        """
        report = state["report"]
        output_format = state.get("output_format", "pdf")  # Default to PDF

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_base = f"{self.output_dir}/{state['company']}_Weekly_Report_{timestamp}"
        print(f"🕒 Timestamp for report: {timestamp}")

        if output_format == "pdf":
            pdf_file_path = f"{file_base}.pdf"
            print(f"🔄 Formatting report as PDF...")
            await self.markdown_to_pdf(markdown_content=report, output_path=pdf_file_path)
            formatted_report = f"📥 PDF report saved at {pdf_file_path}"
        else:
            markdown_file_path = f"{file_base}.md"
            print(f"🔄 Formatting report as Markdown...")
            with open(markdown_file_path, "w") as md_file:
                md_file.write(report)
            print(f"✅ Markdown report saved at '{markdown_file_path}'")
            formatted_report = f"📥 Markdown report saved at {markdown_file_path}"

        return {"messages": [AIMessage(content=formatted_report)]}

    async def run(self, state: ResearchState):
        """
        Executes the report formatting and saving process.

        Args:
            state (ResearchState): The current state of the research process.

        Returns:
            dict: The result of the report formatting, including messages about the saved report.
        """
        print("🚀 Starting the report formatting and saving process...")
        result = await self.format_output(state)
        print("🎉 Report formatting and saving process completed.")
        return result

