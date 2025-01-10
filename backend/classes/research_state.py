"""
@fileoverview This module defines the research state and its associated input and output states
for the research workflow. It includes data structures for managing the research process, 
such as company information, document handling, and report evaluation.
"""

from langgraph.graph import add_messages
from langchain_core.messages import AnyMessage
from typing import TypedDict, List, Annotated, Dict, Union
from .classes import TravelQuery, TravelSearchInput, TravelOptionCluster, ReportEvaluation

class TravelState(TypedDict):
    """
    Represents the state of the travel planning process.

    Attributes:
        destination (str): The name of the destination being planned.
        travel_dates (str): The dates associated with the travel.
        initial_documents (Dict[str, Dict[Union[str, int], Union[str, float]]]): Initial set of documents.
        sub_questions (TravelSearchInput): Sub-questions for the travel planning.
        documents (Dict[str, Dict[Union[str, int], Union[str, float]]]): Documents collected during planning.
        travel_option_clusters (List[TravelOptionCluster]): Clusters of related travel options.
        chosen_option (int): Index of the chosen travel option cluster.
        itinerary (str): The generated itinerary.
        eval (ReportEvaluation): Evaluation of the itinerary.
        output_format (str): Desired format of the output itinerary.
        messages (Annotated[list[AnyMessage], add_messages]): Messages related to the travel planning process.
    """
    destination: str 
    travel_dates: str
    initial_documents: Dict[str, Dict[Union[str, int], Union[str, float]]]
    sub_questions: TravelSearchInput
    documents: Dict[str, Dict[Union[str, int], Union[str, float]]]
    travel_option_clusters: List[TravelOptionCluster]
    chosen_option: int
    itinerary: str
    eval: ReportEvaluation
    output_format: str
    messages: Annotated[list[AnyMessage], add_messages]

class InputState(TypedDict):
    """
    Represents the input state for initiating research.

    Attributes:
        company (str): The name of the company to research.
        company_url (str): The URL associated with the company.
    """
    company: str
    company_url: str

class OutputState(TypedDict):
    """
    Represents the output state after research completion.

    Attributes:
        report (str): The final report generated from the research.
    """
    report: str