"""
@fileoverview This module defines the ResearcherNode class, which is responsible for conducting research
by performing searches using the Tavily API. It processes sub-queries to gather relevant documents
and stores them in a unified 'documents' attribute within the research state.
"""

from langchain_core.messages import AIMessage
from tavily import AsyncTavilyClient
import os
import asyncio
from datetime import datetime
from typing import List

from ..classes import ResearchState, TavilyQuery

class ResearcherNode:
    """
    Represents the research node in the research workflow.

    Attributes:
        tavily_client (AsyncTavilyClient): An asynchronous client for interacting with the Tavily API.
    """

    def __init__(self):
        """
        Initializes the ResearcherNode with a Tavily API client.
        """
        self.tavily_client = AsyncTavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    async def tavily_search(self, sub_queries: List[TavilyQuery]):
        """
        Perform searches for each sub-query using the Tavily search tool concurrently.

        Args:
            sub_queries (List[TavilyQuery]): A list of sub-queries to be searched.

        Returns:
            List[dict]: A list of search results for each sub-query.
        """
        async def perform_search(itm):
            """
            Perform a single search with error handling.

            Args:
                itm (TavilyQuery): A single sub-query item.

            Returns:
                List[dict]: The search results for the given sub-query.
            """
            try:
                query_with_date = f"{itm.query} {datetime.now().strftime('%m-%Y')}"
                response = await self.tavily_client.search(query=query_with_date, topic="general", max_results=7)
                return response['results']
            except Exception as e:
                print(f"Error occurred during search for query '{itm.query}': {str(e)}")
                return []

        print("🔍 Starting Tavily search for sub-queries...")
        search_tasks = [perform_search(itm) for itm in sub_queries]
        search_responses = await asyncio.gather(*search_tasks)

        print("✅ Tavily search completed.")
        search_results = []
        for response in search_responses:
            search_results.extend(response)

        return search_results

    async def research(self, state: ResearchState):
        """
        Conducts a Tavily Search and stores all documents in a unified 'documents' attribute.

        Args:
            state (ResearchState): The current state of the research process.

        Returns:
            dict: The result of the research, including messages and documents.
        """
        msg = "🚀 Conducting Tavily Search for the specified company...\n"
        state['documents'] = {}

        print("🚀 Initiating research process...")
        research_node = ResearcherNode()
        response = await research_node.tavily_search(state['sub_questions'].sub_queries)

        print("📄 Processing search results...")
        for doc in response:
            url = doc.get('url')
            if url and url not in state['documents']:
                state['documents'][url] = doc

        print("📚 Research process completed.")
        return {"messages": [AIMessage(content=msg)], "documents": state['documents']}

    async def run(self, state: ResearchState):
        """
        Executes the research process and returns the result.

        Args:
            state (ResearchState): The current state of the research process.

        Returns:
            dict: The result of the research, including messages and documents.
        """
        print("🏃‍♂️ Running the research node...")
        result = await self.research(state)
        print("🎉 Research node execution finished.")
        return result