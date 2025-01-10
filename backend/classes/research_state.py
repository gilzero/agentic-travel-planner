"""
@fileoverview This module defines the research state and its associated input and output states
for the research workflow. It includes data structures for managing the research process, 
such as company information, document handling, and report evaluation.
"""

from langgraph.graph import add_messages
from langchain_core.messages import AnyMessage
from typing import TypedDict, List, Annotated, Dict, Union
from .classes import TavilySearchInput, DocumentCluster, ReportEvaluation

class ResearchState(TypedDict):
    """
    Represents the state of the research process.

    Attributes:
        company (str): The name of the company being researched.
        company_url (str): The URL associated with the company.
        initial_documents (Dict[str, Dict[Union[str, int], Union[str, float]]]): Initial set of documents.
        sub_questions (TavilySearchInput): Sub-questions for the research.
        documents (Dict[str, Dict[Union[str, int], Union[str, float]]]): Documents collected during research.
        document_clusters (List[DocumentCluster]): Clusters of related documents.
        chosen_cluster (int): Index of the chosen document cluster.
        report (str): The generated report.
        eval (ReportEvaluation): Evaluation of the report.
        output_format (str): Desired format of the output report.
        messages (Annotated[list[AnyMessage], add_messages]): Messages related to the research process.
    """
    company: str 
    company_url: str
    initial_documents: Dict[str, Dict[Union[str, int], Union[str, float]]]
    sub_questions: TavilySearchInput
    documents: Dict[str, Dict[Union[str, int], Union[str, float]]]
    document_clusters: List[DocumentCluster]
    chosen_cluster: int
    report: str
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