"""
@fileoverview This module defines essential data structures for the research workflow.
It includes classes for handling Tavily search inputs, document clustering, and report evaluation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class TravelQuery(BaseModel):
    """
    Represents a single query for Tavily's travel search tool.

    Attributes:
        query (str): The travel search query.
    """
    query: str = Field(description="The travel search query.")

class TravelSearchInput(BaseModel):
    """
    Defines the input schema for Tavily's travel search tool using a multi-query approach.

    Attributes:
        sub_queries (List[TravelQuery]): A set of sub-queries that can be answered in isolation.
    """
    sub_queries: List[TravelQuery] = Field(description="A set of sub-queries that can be answered in isolation.")

class TravelOptionCluster(BaseModel):
    """
    Represents a cluster of travel options related to a specific destination.

    Attributes:
        destination_name (str): The name or identifier of the destination these options belong to.
        options (List[str]): A list of URLs relevant to the identified destination.
    """
    destination_name: str = Field(
        ...,
        description="The name or identifier of the destination these options belong to."
    )
    options: List[str] = Field(
        ...,
        description="A list of URLs relevant to the identified destination."
    )

class DocumentClusters(BaseModel):
    """
    Represents a collection of document clusters.

    Attributes:
        clusters (List[DocumentCluster]): List of document clusters.
    """
    clusters: List[DocumentCluster] = Field(default_factory=list, description="List of document clusters.")

class ReportEvaluation(BaseModel):
    """
    Represents the evaluation of a report.

    Attributes:
        grade (int): Overall grade of the report on a scale from 1 to 3 (1 = needs improvement, 3 = complete and thorough).
        critical_gaps (Optional[List[str]]): List of critical gaps to address if the grade is 1.
    """
    grade: int = Field(
        ..., 
        description="Overall grade of the report on a scale from 1 to 3 (1 = needs improvement, 3 = complete and thorough)."
    )
    critical_gaps: Optional[List[str]] = Field(
        None, 
        description="List of critical gaps to address if the grade is 1."
    )
