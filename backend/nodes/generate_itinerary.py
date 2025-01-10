"""
@fileoverview This module defines the GenerateNode class, which is responsible for generating a Markdown report
based on the research state. It utilizes the ChatAnthropic model to create a structured report with inline citations
and a citations section.
"""

from datetime import datetime
from langchain_core.messages import AIMessage
from langchain_anthropic import ChatAnthropic
from ..classes import ResearchState

class GenerateItineraryNode:
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

    async def generate_itinerary(self, state: TravelState):
        """
        Generates a Markdown itinerary based on the current travel state.

        Args:
            state (TravelState): The current state of the travel planning process.

        Returns:
            dict: A dictionary containing messages about the itinerary generation and the itinerary content.
        """
        print("🗂️ Preparing to generate itinerary...")
        itinerary_title = f"Travel Itinerary for {state['destination']}"
        itinerary_date = datetime.now().strftime('%B %d, %Y')

        prompt = f"""
        You are an expert travel planner tasked with creating a detailed itinerary for a trip to **{state['destination']}**. Write the itinerary in Markdown format, but **do not include a title**. Each section must be written in well-structured paragraphs, not lists or bullet points.
        Ensure the itinerary includes:
        - **Inline citations** as Markdown hyperlinks directly in the main sections (e.g., Visit the famous Eiffel Tower ([Official Site](https://eiffeltower.com))).
        - A **Citations Section** at the end that lists all URLs used.

        ### Itinerary Structure:
        1. **Overview**:
            - High-level overview of the destination, key attractions, and travel dates.
            - Include any notable events or festivals happening during the travel dates.

        2. **Daily Schedule**:
            - Detailed plan for each day, including activities, dining options, and transportation.
            - Include timings and any necessary reservations.

        3. **Accommodation Details**:
            - Information on where to stay, including hotel names, addresses, and contact information.

        4. **Travel Tips**:
            - Important travel tips, local customs, and safety information.

        5. **Citations**:
            - Ensure every source cited in the itinerary is listed in the text as Markdown hyperlinks.
            - Also include a list of all URLs as Markdown hyperlinks in this section.

        ### Documents to Base the Itinerary On:
        {state['documents']}
        """

        messages = [("system", "Your task is to generate a Markdown itinerary."), ("human", prompt)]

        try:
            print("🚀 Sending prompt to ChatAnthropic model...")
            response = await self.model.ainvoke(messages)
            print("✅ Response received from model.")
            markdown_content = self.extract_markdown_content(response.content)
            full_itinerary = f"# {itinerary_title}\n\n*{itinerary_date}*\n\n{markdown_content}"
            print("📄 Itinerary generated successfully!")
            print("🖨️ Final Itinerary:\n" + "="*40 + f"\n{full_itinerary}\n" + "="*40)
            return {"messages": [AIMessage(content=f"Itinerary generated successfully!\n{full_itinerary}")], "itinerary": full_itinerary}
        except Exception as e:
            error_message = f"Error generating itinerary: {str(e)}"
            print(f"❌ {error_message}")
            return {
                "messages": [AIMessage(content=error_message)],
                "itinerary": f"# Error Generating Itinerary\n\n*{itinerary_date}*\n\n{error_message}"
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