"""
@fileoverview This module defines the ManualSelectionNode class, which facilitates the manual selection
of document clusters identified during the research process. It allows users to choose the appropriate
cluster for the target company via a WebSocket interface or through a manual input in a studio environment.
"""

from langchain_core.messages import AIMessage
from langgraph.errors import NodeInterrupt
from ..classes import ResearchState

class ManualSelectionNode:
    """
    Represents the manual selection node in the research workflow.

    Methods:
        manual_cluster_selection(state, websocket): Handles the manual selection of clusters either via WebSocket
        or through a studio environment.
        run(state, websocket=None): Executes the manual cluster selection process.
    """

    async def manual_cluster_selection(self, state: ResearchState, websocket):
        """
        Facilitates the manual selection of document clusters.

        Args:
            state (ResearchState): The current state of the research process, including document clusters.
            websocket: The WebSocket connection for real-time communication with the frontend.

        Returns:
            dict: A dictionary containing messages about the selection process and the chosen cluster index.
        """
        clusters = state['document_clusters']
        print("🔍 Identifying clusters for manual selection...")
        msg = "Multiple clusters were identified. Please review the options and select the correct cluster for the target company.\n\n"
        msg += "Enter '0' if none of these clusters match the target company.\n"

        if websocket:
            print("🌐 WebSocket connection established. Sending cluster options to the frontend...")
            # Send cluster options to the frontend via WebSocket
            await websocket.send_text(msg)

            # Wait for user selection from WebSocket
            while True:
                try:
                    print("⏳ Waiting for user selection via WebSocket...")
                    selection_text = await websocket.receive_text()
                    selected_cluster_index = int(selection_text) - 1

                    if selected_cluster_index == -1:
                        msg = "No suitable cluster found. Trying to cluster again.\n"
                        print("🔄 No suitable cluster selected. Re-clustering...")
                        await websocket.send_text(msg)
                        return {"messages": [AIMessage(content=msg, is_manual_selection=True)], "chosen_cluster": selected_cluster_index}
                    elif 0 <= selected_cluster_index < len(clusters):
                        chosen_cluster = clusters[selected_cluster_index]
                        msg = f"You selected cluster '{chosen_cluster.company_name}' as the correct cluster."
                        print(f"✅ Cluster '{chosen_cluster.company_name}' selected.")
                        await websocket.send_text(msg)
                        return {"messages": [AIMessage(content=msg, is_manual_selection=True)], "chosen_cluster": selected_cluster_index}
                    else:
                        print("❌ Invalid choice received. Prompting user again...")
                        await websocket.send_text("Invalid choice. Please enter a number corresponding to the listed clusters or '0' to re-cluster.")
                except ValueError:
                    print("⚠️ Invalid input received. Prompting user again...")
                    await websocket.send_text("Invalid input. Please enter a valid number.")
        else:
            print("🖥️ No WebSocket connection. Manual selection needed in studio environment. Re-clustering...")
            # Handle selection for studio, attempt to cluster again for now
            msg = "Manual selection needed, trying to cluster again.\n"
            return {"messages": [AIMessage(content=msg, is_manual_selection=True)], "chosen_cluster": -1}

    async def run(self, state: ResearchState, websocket=None):
        """
        Executes the manual cluster selection process.

        Args:
            state (ResearchState): The current state of the research process.
            websocket: Optional; The WebSocket connection for real-time communication with the frontend.

        Returns:
            dict: The result of the manual cluster selection, including messages and the chosen cluster index.
        """
        print("🏃‍♂️ Running the manual cluster selection process...")
        result = await self.manual_cluster_selection(state, websocket)
        print("🎉 Manual cluster selection process completed.")
        return result
