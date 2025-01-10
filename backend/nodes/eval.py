"""
@fileoverview This module defines the EvaluationNode class, which is responsible for evaluating
the quality of a generated report. It uses the ChatAnthropic model to assign a grade to the report
based on its completeness, accuracy, and depth of information. If the report is found lacking,
it identifies critical gaps and suggests additional sub-queries to address these gaps.
"""

from langchain_core.messages import AIMessage
from ..classes import ResearchState, TavilySearchInput, TavilyQuery, ReportEvaluation
from langchain_anthropic import ChatAnthropic

class EvaluationNode:
    """
    Represents the evaluation node in the research workflow.

    Attributes:
        model (ChatAnthropic): An instance of the ChatAnthropic model used for evaluating the report.
    """

    def __init__(self):
        """
        Initializes the EvaluationNode with a specified ChatAnthropic model.
        """
        self.model = ChatAnthropic(
            model="claude-3-5-haiku-20241022",
            temperature=0
        )
        print("🔍 EvaluationNode initialized with ChatAnthropic model.")

    async def evaluate_report(self, state: ResearchState):
        """
        Evaluates the generated report by assigning an overall grade from 1 to 3.
        If the grade is 1, identifies critical gaps in the report and suggests additional sub-queries.

        Args:
            state (ResearchState): The current state of the research process, including the report content.

        Returns:
            dict: A dictionary containing messages about the evaluation, the evaluation result,
                  and any new sub-questions if critical gaps are identified.
        """
        print("📝 Preparing to evaluate the report...")
        prompt = f"""
            You have created a report on '{state['company']}' based on the gathered information.
            Grade the report on a scale of 1 to 3 based on completeness, accuracy, and depth of information:
            - **3** indicates a thorough and well-supported report with no major gaps.
            - **2** indicates adequate coverage, but could be improved.
            - **1** indicates significant gaps or missing essential sections.

            If the grade is 1, specify any critical gaps that need addressing.
            
            Here is the report for evaluation:
            {state['report']}
        """

        # Invoke the model for report evaluation
        print("🚀 Sending report to ChatAnthropic model for evaluation...")
        messages = ["system", "Your task is to evaluate a report on a scale of 1 to 3.",
                    ("human", f"{prompt}")]
        evaluation = await self.model.with_structured_output(ReportEvaluation).ainvoke(messages)
        print("✅ Evaluation received from model.")

        # Determine if additional questions are needed based on grade
        if evaluation.grade == 1:
            msg = f"❌ The report received a grade of 1. Critical gaps identified: {', '.join(evaluation.critical_gaps or ['None specified'])}"
            print("⚠️ Critical gaps found. Generating additional sub-queries...")
            # Create new sub-questions for critical gaps
            new_sub_queries = [
                TavilyQuery(query=f"Gather information on {gap} for {state['company']}", topic="general", days=30)
                for gap in evaluation.critical_gaps or []
            ]
            if 'sub_questions' in state:
                state['sub_questions'].sub_queries.extend(new_sub_queries)
            else:
                state['sub_questions'] = TavilySearchInput(sub_queries=new_sub_queries)
            print(f"🔍 Suggested additional sub-queries: {[query.query for query in new_sub_queries]}")
            return {"messages": [AIMessage(content=msg)], "eval": evaluation, "sub_questions": state['sub_questions']}
        else:
            msg = f"✅ The report received a grade of {evaluation.grade}/3 and is marked as complete."
            print("🎉 Report evaluation completed successfully.")
            return {"messages": [AIMessage(content=msg)], "eval": evaluation}

    async def run(self, state: ResearchState):
        """
        Executes the report evaluation process.

        Args:
            state (ResearchState): The current state of the research process.

        Returns:
            dict: The result of the report evaluation, including messages and any new sub-questions if applicable.
        """
        print("🏃‍♂️ Running the evaluation process...")
        result = await self.evaluate_report(state)
        print("🎉 Evaluation process completed.")
        return result
