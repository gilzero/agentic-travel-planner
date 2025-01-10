"""
@fileoverview This module defines the EnrichDocsNode class, which is responsible for curating and enriching
documents based on the selected cluster. It utilizes the Tavily Extract service to enhance document content
with more detailed information.
"""

from langchain_core.messages import AIMessage
from tavily import AsyncTavilyClient
import os
from ..classes import ResearchState

class EnrichDocsNode:
    """
    Represents the node responsible for curating and enriching documents in the research workflow.

    Attributes:
        tavily_client (AsyncTavilyClient): An asynchronous client for interacting with the Tavily API.
    """

    def __init__(self):
        """
        Initializes the EnrichDocsNode with a Tavily API client.
        """
        self.tavily_client = AsyncTavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    async def curate(self, state: ResearchState):
        """
        Curates and enriches documents based on the selected cluster.

        Args:
            state (ResearchState): The current state of the research process, including document clusters and documents.

        Returns:
            dict: A dictionary containing messages about the enrichment process and the updated documents.
        """
        print("🔍 Starting document curation and enrichment process...")
        chosen_cluster_index = state['chosen_cluster']
        clusters = state['document_clusters']
        chosen_cluster = clusters[chosen_cluster_index]
        print(f"📂 Selected cluster for enrichment: '{chosen_cluster.company_name}'")

        msg = f"🚀 Enriching documents for selected cluster '{chosen_cluster.company_name}'...\n"

        # Filter `documents` to include only those in the chosen cluster
        selected_docs = {url: state['documents'][url] for url in chosen_cluster.cluster if url in state['documents']}
        print(f"📑 Number of documents selected for enrichment: {len(selected_docs)}")

        # Limit to first 15 URLs 
        urls_to_extract = list(selected_docs.keys())[:15]
        print(f"🔗 URLs to be enriched (limited to 15): {urls_to_extract}")

        # Enrich the content using Tavily Extract
        try:
            print("🛠️ Extracting content using Tavily Extract...")
            extracted_content = await self.tavily_client.extract(urls=urls_to_extract)
            enriched_docs = {}
            
            # Update `documents` with enriched content from Tavily Extract
            for item in extracted_content["results"]:
                url = item['url']
                if url in selected_docs:
                    enriched_docs[url] = {
                        **selected_docs[url],  # Existing doc data
                        "raw_content": item.get("raw_content", ""),
                        "extracted_details": item.get("details", {}),
                    }
            print("✅ Document enrichment completed successfully.")
            state['documents'] = enriched_docs  # Update documents with enriched data

        except Exception as e:
            print(f"❌ Error during Tavily Extract: {str(e)}")
            msg += f"Error occurred during Tavily Extract: {str(e)}\n"
            msg += f"Extracted URLs: {urls_to_extract}\n"  # Log the urls_to_extract if error

        return {"messages": [AIMessage(content=msg)], "documents": state['documents']}
    
    async def run(self, state: ResearchState):
        """
        Executes the document curation and enrichment process.

        Args:
            state (ResearchState): The current state of the research process.

        Returns:
            dict: The result of the document enrichment, including messages and the updated documents.
        """
        print("🏃‍♂️ Running the enrichment node...")
        result = await self.curate(state)
        print("🎉 Enrichment process completed.")
        return result