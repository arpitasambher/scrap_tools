import os
from datetime import date
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# CrewAI core
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# Ollama (correct import for LangChain >= 0.3.1)
from langchain_ollama import OllamaLLM

# Get today's date for CVE filter
today = date.today()
current_date = today.strftime("%B %d, %Y")

# ✅ Correct model call for Ollama
ollama_mistral = OllamaLLM(
    model="ollama/mistral:latest",
    temperature=0.2
)

# ✅ Serper tool — API key is loaded automatically from .env
search_tool = SerperDevTool()

# Agent 1: Researcher
researcher = Agent(
    role='researcher',
    goal='Uncover very detailed information about new CVEs that came out today',
    backstory='You are a top cybersecurity researcher tracking daily threats.',
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=ollama_mistral
)

# Agent 2: Newsletter Writer
writer = Agent(
    role='cybersecurity newsletter writer',
    goal='Write a structured and detailed cybersecurity newsletter',
    backstory='You summarize critical CVEs for a global audience in clear, technical English.',
    verbose=True,
    allow_delegation=False,
    llm=ollama_mistral
)

# Task 1: Research CVEs
task1 = Task(
    description=f'Gather data about new Critical CVEs from today\'s date: {current_date}',
    agent=researcher,
    expected_output='A bulleted list of today\'s most critical CVEs'
)

# Task 2: Write newsletter
task2 = Task(
    description='Write a compelling, structured newsletter summarizing each CVE from Task 1',
    agent=writer,
    expected_output='Markdown-formatted cybersecurity newsletter'
)

# Assemble and run the Crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    verbose=True,  # must be boolean!
)

result = crew.kickoff()

print("\n\n📄 FINAL RESULT:\n")
print(result)
