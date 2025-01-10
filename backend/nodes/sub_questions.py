"""
@fileoverview This module defines the SubQuestionsNode class, responsible for generating sub-questions
based on initial search data. It utilizes a language model to create specific questions that aid in
understanding the company being researched.
"""

from langchain_core.messages import AIMessage
from langchain_anthropic import ChatAnthropic
from ..classes import ResearchState, TavilySearchInput

class SubQuestionsNode:
    """
    Represents the sub-questions generation node in the research workflow.

    Attributes:
        model (ChatAnthropic): A language model used to generate sub-questions.
    """

    def __init__(self) -> None:
        """
        Initializes the SubQuestionsNode with a language model.
        """
        self.model = ChatAnthropic(
            model="claude-3-5-haiku-20241022",
            temperature=0
        )
     
    async def generate_sub_questions(self, state: ResearchState):
        """
        Generates sub-questions based on the initial search results.

        Args:
            state (ResearchState): The current state of the research process, including company information.

        Returns:
            dict: A dictionary containing messages, generated sub-questions, and initial documents.
        """
        try:
            msg = "🤔 Generating sub-questions based on the initial search results...\n"
            
            if 'sub_questions_data' not in state:
                state['sub_questions_data'] = []
                
            prompt = f"""
            You are an expert researcher focusing on company analysis to generate a report.
            Your task is to generate 4 specific sub-questions that will provide a thorough understanding of the company: '{state['company']}'.
            
            ### Key Areas to Explore:
            - **Company Background**: Include history, mission, headquarters location, CEO, and number of employees.
            - **Products and Services**: Focus on main offerings, unique features, and target customer segments.
            - **Market Position**: Address competitive standing, market reach, and industry impact.
            - **Financials**: Seek recent funding, revenue milestones, financial performance, and growth indicators.

            Use the initial information provided from the company's website below to keep questions directly relevant to **{state['company']}**.

            Official URL: {state['company_url']}
            Initial Company Information:
            {state["initial_documents"]}
            
            Ensure questions are clear, specific, and well-aligned with the company's context.
            """
            
            messages = ["system","Your task is to generate sub-questions based on the initial search results.",
                ("human",f"{prompt}")]

            sub_questions = await self.model.with_structured_output(TavilySearchInput).ainvoke(messages)

            # Print the generated sub-questions in a more human-friendly format
            print("Generated Sub-Questions:")
            for i, query in enumerate(sub_questions.sub_queries, start=1):
                print(f"Sub-Question {i}: {query.query}")

            
        except Exception as e:
            msg = f"An error occurred during sub-question generation: {str(e)}"
            return {"messages": [AIMessage(content=msg)], "sub_questions": None, "initial_documents": state['initial_documents']}
            
        return {"messages": [AIMessage(content=msg)], "sub_questions": sub_questions, "initial_documents": state['initial_documents']}
            
    async def run(self, state: ResearchState):
        """
        Executes the sub-question generation process and returns the result.

        Args:
            state (ResearchState): The current state of the research process.

        Returns:
            dict: The result of the sub-question generation, including messages and sub-questions.
        """
        result = await self.generate_sub_questions(state)
        return result