"""
@fileoverview This module defines the GenerateNode class, which is responsible for generating a Markdown report
based on the research state. It utilizes the ChatAnthropic model to create a structured report with inline citations
and a citations section.
"""

from datetime import datetime
from langchain_core.messages import AIMessage
from langchain_anthropic import ChatAnthropic
from ..classes import ResearchState

class GenerateNode:
    """
    Represents the node responsible for generating a Markdown report in the research workflow.

    Attributes:
        model (ChatAnthropic): An instance of the ChatAnthropic model used for generating the report.
    """

    def __init__(self):
        """
        Initializes the GenerateNode with a specified ChatAnthropic model.
        """
        self.model = ChatAnthropic(
            model="claude-3-5-haiku-20241022",
            temperature=0
        )
        print("📝 GenerateNode initialized with ChatAnthropic model.")

    def extract_markdown_content(self, content):
        """
        Extracts the Markdown content from the given text, removing any extra preamble or conversational text.

        Args:
            content (str): The text content from which to extract Markdown.

        Returns:
            str: The extracted Markdown content.
        """
        print("🔍 Extracting Markdown content from response...")
        start_index_hash = content.find("#")
        start_index_bold = content.find("**")
        
        if start_index_hash != -1 and (start_index_bold == -1 or start_index_hash < start_index_bold):
            return content[start_index_hash:].strip()
        elif start_index_bold != -1:
            return content[start_index_bold:].strip()
        else:
            return content.strip()

    async def generate_report(self, state: ResearchState):
        """
        Generates a Markdown report based on the current research state.

        Args:
            state (ResearchState): The current state of the research process.

        Returns:
            dict: A dictionary containing messages about the report generation and the report content.
        """
        print("🗂️ Preparing to generate report...")
        report_title = f"Weekly Report on {state['company']}"
        report_date = datetime.now().strftime('%B %d, %Y')

        prompt = f"""
        You are an expert researcher tasked with writing a fact-based report on recent developments for the company **{state['company']}**. Write the report in Markdown format, but **do not include a title**. Each section must be written in well-structured paragraphs, not lists or bullet points.
        Ensure the report includes:
        - **Inline citations** as Markdown hyperlinks directly in the main sections (e.g., Company X is an innovative leader in AI ([LinkedIn](https://linkedin.com))).
        - A **Citations Section** at the end that lists all URLs used.

        ### Report Structure:
        1. **Executive Summary**:
            - High-level overview of the company, its services, location, employee count, and achievements.
            - Make sure to include the general information necessary to understand the company well including any notable achievements.

        2. **Leadership and Vision**:
            - Details on the CEO and key team members, their experience, and alignment with company goals.
            - Any personnel changes and their strategic impact.

        3. **Product and Service Overview**:
            - Summary of current products/services, features, updates, and market fit.
            - Include details from the company's website, tools, or new integrations.

        4. **Financial Performance**:
            - For public companies: key metrics (e.g., revenue, market cap).
            - For startups: funding rounds, investors, and milestones.

        5. **Recent Developments**:
            - New product enhancements, partnerships, competitive moves, or market entries.

        6. **Citations**:
            - Ensure every source cited in the report is listed in the text as Markdown hyperlinks.
            - Also include a list of all URLs as Markdown hyperlinks in this section.

        ### Documents to Base the Report On:
        {state['documents']}
        """

        messages = [("system", "Your task is to generate a Markdown report."), ("human", prompt)]

        try:
            print("🚀 Sending prompt to ChatAnthropic model...")
            response = await self.model.ainvoke(messages)
            print("✅ Response received from model.")
            markdown_content = self.extract_markdown_content(response.content)
            full_report = f"# {report_title}\n\n*{report_date}*\n\n{markdown_content}"
            print("📄 Report generated successfully!")
            print("🖨️ Final Report:\n" + "="*40 + f"\n{full_report}\n" + "="*40)
            return {"messages": [AIMessage(content=f"Report generated successfully!\n{full_report}")], "report": full_report}
        except Exception as e:
            error_message = f"Error generating report: {str(e)}"
            print(f"❌ {error_message}")
            return {
                "messages": [AIMessage(content=error_message)],
                "report": f"# Error Generating Report\n\n*{report_date}*\n\n{error_message}"
            }

    async def run(self, state: ResearchState, websocket):
        """
        Executes the report generation process and sends a status message via WebSocket if provided.

        Args:
            state (ResearchState): The current state of the research process.
            websocket: The WebSocket connection for real-time communication with the frontend.

        Returns:
            dict: The result of the report generation, including messages and the report content.
        """
        print("🏃‍♂️ Running the report generation process...")
        if websocket:
            await websocket.send_text("⌛️ Generating report...")
        result = await self.generate_report(state)
        print("🎉 Report generation process completed.")
        return result