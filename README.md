# Travel Planner with Tavily and Langgraph

The **Travel Planner** is an open-source tool designed for creating detailed travel itineraries. Built with **Tavily’s `search` and `extract` capabilities** and powered by **LangGraph**, it delivers precise, real-time travel insights in a structured format. Ideal for trip planning, destination research, and itinerary management, this tool leverages advanced AI-driven workflows to provide comprehensive, reliable travel plans for data-driven decision-making.

## Table of Contents
1. [Overview](#overview)
2. [Key Workflow Features](#key-workflow-features)
3. [Running the Tool Locally](#running-the-tool-locally)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Running the Application](#running-the-application)
4. [Running the Tool in LangGraph Studio](#running-the-tool-in-langgraph-studio)
5. [Customization](#customization)
6. [Future Directions](#future-directions)

---

## Overview

The **Travel Planner** is an open-source tool designed for creating detailed travel itineraries. Built with **Tavily’s search and extract capabilities** and powered by **LangGraph**, it gathers both general and targeted information, using feedback loops and optional human validation for accuracy. It is designed to handle complex scenarios, such as distinguishing similarly named companies or gathering data in sparsely documented fields, and can be easily adapted to other research domains.

---
![workflow](https://i.imgur.com/92E2kcj.jpeg)

---

## Key Workflow Features
1. **Establishing a Ground Truth with Tavily Extract**: Each session begins by setting a “ground truth” with Tavily’s `extract` tool, using a user-provided company name and URL. This foundational data anchors the subsequent search, ensuring all steps stay within accurate and verified data boundaries.
2. **Sub-Question Generation and Tavily Search**: The workflow dynamically generates specific research questions to drive Tavily’s `search`, focusing the retrieval on relevant, high-value information rather than conducting broad, unfocused searches.
3. **AI-Driven Document Clustering**: Retrieved documents are clustered based on relevance to the target company. This process, anchored by the ground truth, filters out unrelated content, a critical feature for similarly named companies or entities with minimal online presence.
4. **Human-on-the-Loop Validation**: In cases where clustering yields ambiguous results, optional human review allows for manual cluster selection, ensuring the data aligns accurately with the target entity.
5. **Document Curation and Enrichment with Tavily Extract**: Once the appropriate cluster is identified, Tavily’s `extract` further refines and enriches the content, adding substantial depth to the research. This step enhances the precision and comprehensiveness of the final output.
6. **Report Generation and Evaluation with Feedback Loops**: An LLM synthesizes the enriched data into a structured report. If gaps are detected, feedback loops prompt additional information gathering, enabling iterative improvements without restarting the entire workflow.
7. **Multi-Format Output**: The finalized report can be exported in PDF or Markdown formats, making it ready for easy sharing and integration.

---

## Running the Tool Locally

### Prerequisites

- Python 3.11 or later: [Python Installation Guide](https://www.tutorialsteacher.com/python/install-python)
- Tavily API Key - [Sign Up](https://tavily.com/)
- Anthropic API Key - [Sign Up](https://console.anthropic.com/settings/keys)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/danielleyahalom/company-researcher.git
   cd company-researcher
   ```

2. **Create a Virtual Environment**:

   To avoid dependency conflicts, it's recommended to create and activate a virtual environment using `venv`:

   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate       # Windows
   ```

3. **Set Up API Keys**:
   Configure your OpenAI and Tavily API keys as environment variables or place them in a `.env` file:

   ```bash
   export TAVILY_API_KEY={Your Tavily API Key here}
   export ANTHROPIC_API_KEY={Your Anthropic API Key here}
   ```

4. **Install Dependencies**:

   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**:

   ```bash
   python app.py
   ```

6. **Open the App in Your Browser**:

   ```bash
   http://localhost:5000
   ```

---

## Running the Tool in LangGraph Studio

---
<div align="center">
  <img src="https://i.imgur.com/FEAUhNW.png" alt="Langgraph Studio" height="500">
</div>

---

**LangGraph Studio** enables visualization, debugging, and real-time interaction with the Company Researcher's workflow. Here’s how to set it up:

### Prerequisites

1. **Download LangGraph Studio**:
   - For macOS, download the latest `.dmg` file for LangGraph Studio from [here](https://langgraph-studio.vercel.app/api/mac/latest) or visit the [releases page](https://github.com/langchain-ai/langgraph-studio/releases).
   - **Note**: Currently, only macOS is supported.

2. **Install Docker**:
   - Ensure [Docker Desktop](https://docs.docker.com/engine/install/) is installed and running. LangGraph Studio requires Docker Compose version 2.22.0 or higher.

### Setting Up in LangGraph Studio

1. **Clone the Repository**:
      ```bash
      git clone https://github.com/danielleyahalom/company-researcher.git
      cd company_researcher
      ```
   - **Note**: This repository includes all required files except for the `.env` file, which you need to create to store your API keys.

2. **Configure the Environment**:
   - Create a `.env` file in the root directory to store your API keys:
      ```bash
      touch .env
      ```
   - Add your API keys to the `.env` file:
      ```bash
      TAVILY_API_KEY={Your Tavily API Key here}
      ANTHROPIC_API_KEY={Your Anthropic API Key here}
      ```

3. **Ensure LangGraph Configuration Files Are in Place**:
   - The repository includes `langgraph.json` and `langgraph_entry.py`, defining the entry point and configuration for LangGraph Studio.

4. **Start LangGraph Studio**:
   - Open LangGraph Studio and select the `company_researcher` directory from the dashboard.

5. **Running the Workflow in Studio**:
   - Visualize each step of the workflow, make real-time edits, and monitor the workflow’s state.
   - **Important Note**: If a cluster cannot be automatically selected, the tool will attempt to re-cluster instead.

LangGraph Studio provides a hands-on approach to refining the workflow, enhancing both development efficiency and output reliability.

---

## Customization

The tool’s modular structure makes it adaptable to various research applications:

- **Modify Prompts**: Adjust prompts in question generation or report synthesis for different research needs.
- **Extend Workflow Nodes**: Add, remove, or modify nodes to focus on specific types of analysis.
- **Customize Output Formats**: Tailor output formats (e.g., CSS for PDF styling) to suit organizational standards.

---

## Future Directions

This adaptable workflow can be fine-tuned for a range of applications beyond company research:

- **Market Analysis**: Apply the workflow to track trends, competitors, and emerging tech.
- **Lead Generation**: Compile detailed profiles on potential clients for targeted outreach.
- **Ongoing Knowledge Bases**: Build continuously updated research repositories in fields like law, finance, or healthcare.

This tool exemplifies how AI-driven workflows, backed by precise data extraction and real-time search, can reshape research and analysis across domains.