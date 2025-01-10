"""
File: graph.py
Description: This module defines the Graph class, which sets up and manages a research workflow using a state graph.
The workflow consists of various nodes that represent different stages of the research process, from initial grounding
to publishing the final report. The class also handles asynchronous execution of the workflow and provides progress updates.
"""

from langchain_core.messages import SystemMessage, AIMessage
from functools import partial
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver

# Import research state class
from backend.classes.research_state import ResearchState, InputState, OutputState

# Import node classes
from backend.nodes import (
    InitialGroundingNode, 
    SubQuestionsNode, 
    ResearcherNode, 
    ClusterNode, 
    ManualSelectionNode, 
    EnrichDocsNode, 
    GenerateNode,
    EvaluationNode,
    PublishNode
)
from backend.utils.routing_helper import (
    route_based_on_cluster, 
    route_after_manual_selection, 
    should_continue_research,
    route_based_on_evaluation
)

class Graph:
    """
    The Graph class initializes and manages a research workflow using a state graph.
    It sets up nodes representing different stages of the research process and handles
    the execution of the workflow asynchronously.
    """
    def __init__(self, company=None, url=None, output_format="pdf", websocket=None):
        """
        Initializes the Graph with a research state, nodes, and a workflow.

        Args:
            company (str, optional): The name of the company for the research.
            url (str, optional): The URL associated with the company.
            output_format (str, optional): The desired output format for the report.
            websocket (WebSocket, optional): WebSocket for real-time communication.
        """
        # Initial setup of ResearchState and messages
        self.messages = [
            SystemMessage(content="You are an expert researcher ready to begin the information gathering process.")
        ]

        # Initialize ResearchState
        self.state = ResearchState(
            company=company,
            company_url=url,
            output_format=output_format,
            messages=self.messages
        )
        
        # Initialize nodes as attributes
        self.initial_search_node = InitialGroundingNode()
        self.sub_questions_node = SubQuestionsNode()
        self.researcher_node = ResearcherNode()
        self.cluster_node = ClusterNode()
        self.manual_selection_node = ManualSelectionNode()
        self.curate_node = EnrichDocsNode()
        self.generate_node = GenerateNode()
        self.evaluation_node = EvaluationNode()
        self.publish_node = PublishNode()

        # Initialize workflow for the graph
        self.workflow = StateGraph(ResearchState, input=InputState, output=OutputState)

        # Add nodes to the workflow
        self.workflow.add_node("initial_grounding", self.initial_search_node.run)
        self.workflow.add_node("sub_questions_gen", self.sub_questions_node.run)
        self.workflow.add_node("research", self.researcher_node.run)
        self.workflow.add_node("cluster", self.curried_node(self.cluster_node.run))
        self.workflow.add_node("manual_cluster_selection", self.curried_node(self.manual_selection_node.run))
        self.workflow.add_node("enrich_docs", self.curate_node.run)               
        self.workflow.add_node("generate_report", self.curried_node(self.generate_node.run))
        self.workflow.add_node("eval_report", self.evaluation_node.run)
        self.workflow.add_node("publish", self.publish_node.run)

        # Add edges to the graph
        self.workflow.add_edge("initial_grounding", "sub_questions_gen")
        self.workflow.add_edge("sub_questions_gen", "research")
        self.workflow.add_edge("research", "cluster")
        self.workflow.add_conditional_edges("cluster", route_based_on_cluster)
        self.workflow.add_conditional_edges("manual_cluster_selection", route_after_manual_selection)
        self.workflow.add_conditional_edges("enrich_docs", should_continue_research)
        self.workflow.add_edge("generate_report", "eval_report")
        self.workflow.add_conditional_edges("eval_report", route_based_on_evaluation)

        # Set start and end nodes
        self.workflow.set_entry_point("initial_grounding")
        self.workflow.set_finish_point("publish")

        self.memory = MemorySaver()
        self.websocket = websocket

    async def run(self, progress_callback=None):
        """
        Compiles and executes the workflow asynchronously, providing progress updates.

        Args:
            progress_callback (callable, optional): A callback function to handle progress updates.
        """
        # Compile the graph
        graph = self.workflow.compile(checkpointer=self.memory)
        thread = {"configurable": {"thread_id": "2"}}

        # Execute the graph asynchronously and send progress updates
        async for s in graph.astream(self.state, thread, stream_mode="values"):
            if "messages" in s and s["messages"]:  # Check if "messages" exists and is non-empty
                message = s["messages"][-1]
                output_message = message.content if hasattr(message, "content") else str(message)
                if progress_callback and not getattr(message, "is_manual_selection", False):
                    await progress_callback(output_message)

    def curried_node(self, node_run_method):
        """
        Wraps a node's run method to handle websocket communication.

        Args:
            node_run_method (callable): The run method of a node.

        Returns:
            callable: A wrapped asynchronous function for the node.
        """
        async def wrapper(state):
            return await node_run_method(state, self.websocket)
        return wrapper

    def compile(self):
        """
        Compiles the workflow for use in langgraph studio.

        Returns:
            StateGraph: The compiled state graph.
        """
        # Use a consistent thread ID for state persistence
        thread = {"configurable": {"thread_id": "2"}}

        # Compile the workflow with checkpointer and interrupt configuration
        graph = self.workflow.compile(
            checkpointer=self.memory
            # interrupt_before=["manual_cluster_selection"]
        )
        return graph
