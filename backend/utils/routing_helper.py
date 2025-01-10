"""
@fileoverview This module provides routing helper functions for the research workflow.
These functions determine the next step in the workflow based on the current state,
such as cluster selection, manual selection, document count, and evaluation grade.
"""

from typing import Literal
from ..classes import ResearchState
from langchain_core.messages import AIMessage

def route_based_on_cluster(state: ResearchState) -> Literal["enrich_docs", "manual_cluster_selection"]:
    """
    Determines the next step based on the chosen cluster.

    Args:
        state (ResearchState): The current state of the research.

    Returns:
        Literal["enrich_docs", "manual_cluster_selection"]: The next step in the workflow.
    """
    if state.get('chosen_cluster') is not None:
        return "enrich_docs"
    return "manual_cluster_selection"

def route_after_manual_selection(state: ResearchState) -> Literal["enrich_docs", "cluster"]:
    """
    Determines the next step after manual cluster selection.

    Args:
        state (ResearchState): The current state of the research.

    Returns:
        Literal["enrich_docs", "cluster"]: The next step in the workflow.
    """
    if state.get('chosen_cluster') >= 0:
        return "enrich_docs"
    return "cluster"

def should_continue_research(state: ResearchState) -> Literal["research", "generate_report"]:
    """
    Decides whether to continue research or generate a report based on document count.

    Args:
        state (ResearchState): The current state of the research.

    Returns:
        Literal["research", "generate_report"]: The next step in the workflow.
    """
    min_doc_count = 2  # Minimum threshold for documents
    if len(state["documents"]) < min_doc_count:
        return "research"
    return "generate_report"

def route_based_on_evaluation(state: ResearchState) -> Literal["research", "publish"]:
    """
    Routes the workflow based on the evaluation grade of the report.

    Args:
        state (ResearchState): The current state of the research.

    Returns:
        Literal["research", "publish"]: The next step in the workflow.
    """
    evaluation = state.get("eval")
    return "research" if evaluation.grade == 1 else "publish"
