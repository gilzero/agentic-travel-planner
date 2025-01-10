"""
@fileoverview This module defines the InitialGroundingNode class, responsible for initiating the research process
by extracting base content from a provided company URL using the Tavily API. It sets up the initial documents
for further research and analysis.
"""

from langchain_core.messages import AIMessage
from tavily import AsyncTavilyClient
import os

from ..classes import ResearchState


class InitialGroundingNode:
    """
    Represents the initial grounding node in the research workflow.

    Attributes:
        tavily_client (AsyncTavilyClient): An asynchronous client for interacting with the Tavily API.
    """

    def __init__(self) -> None:
        """
        Initializes the InitialGroundingNode with a Tavily API client.
        """
        self.tavily_client = AsyncTavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        print("🚀 InitialGroundingNode initialized with Tavily API client.")

    async def initial_search(self, state: ResearchState):
        """
        Performs an initial search to extract base content from the provided company URL.

        Args:
            state (ResearchState): The current state of the research process, including company information.

        Returns:
            dict: A dictionary containing messages and the initial documents extracted.
        """
        msg = f"🔎 Initiating initial grounding for company '{state['company']}'...\n"
        print(f"🔍 Starting initial search for company: {state['company']}")

        urls = [state['company_url']]
        state['initial_documents'] = {}
        
        try:
            search_results = await self.tavily_client.extract(urls=urls)
            print(f"✅ Successfully retrieved search results for {state['company']}.")
            for item in search_results["results"]:
                url = item['url']
                raw_content = item["raw_content"]
                state['initial_documents'][url] = {'url': url, 'raw_content': raw_content}
                print(f"📄 Document extracted from URL: {url}")
                
        except Exception as e:
            error_msg = f"❌ Error occurred during Tavily Extract request: {e}"
            print(error_msg)
        
        return {"messages": [AIMessage(content=msg)], "initial_documents": state['initial_documents']}
    
    async def run(self, state: ResearchState):
        """
        Executes the initial search and returns the result.

        Args:
            state (ResearchState): The current state of the research process.

        Returns:
            dict: The result of the initial search, including messages and initial documents.
        """
        print("🏃‍♂️ Running the initial search process...")
        result = await self.initial_search(state)
        print("🏁 Initial search process completed.")
        return result