





import os
import time
import requests
import json, time
from typing import Optional
from langchain.llms.base import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool
# from models import AMLReport
import sys
sys.path.insert(0, 'scrap_tools/final/utils')

from utils.permutation import generate_permutations
from utils.queries import generate_queries
from utils.search import run_search
from utils.scraper import scrape_all
from utils.summarizer import summarize


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai import LLM


GEMINI_API_KEY="AIzaSyBZLs0ZnQJHgCBJEotsRECDRQfr31Vj-SI"
llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
    api_key=GEMINI_API_KEY,
)

@tool("permutation_tool")
def permutation_tool(user_data: dict, num_permutations: str):
    """
    Generate permutations for AML based on user inputs.

    Args:
        user_inputs (dict): Dictionary containing user input values for AML.
        file_path (str, optional): File path for storing output. Defaults to  permuted_data.json "".

    Returns:
        list: A list of generated permutations.
    """
    print("[CHECKPOINT] Entered permutation_tool")
    print(f"[INPUT] user_inputs: {user_data}, num_permutations: {num_permutations}")
    start_time = time.time()

    result = generate_permutations(user_data, num_permutations)
    print("RESULT :/n" )
    print(result)
    print(f"[OUTPUT] Generated {len(result)} permutations")
    print(f"[TIME] permutation_tool completed in {time.time() - start_time:.2f}s")
    print("[CHECKPOINT] Exiting permutation_tool")
    return result


@tool("query_tool")
def query_tool():
    """
    Self-contained tool that loads permutations from file and generates AML queries.
    """
    print("[CHECKPOINT] Entered query_tool")
    
    try:
        file_path = os.path.join("output", "permuted_data.json")
        with open(file_path, "r") as f:
            permutations = json.load(f)
            print(permutations)
    except Exception as e:
        print(f"[ERROR] Failed to load permutations: {e}")
 
    print(f"[INPUT] permutations count: {len(permutations)}")
    start_time = time.time()
 
    result = generate_queries(permutations, queries_per_identity=10)
 
    print(f"[OUTPUT] Generated {len(result)} queries")
    print(f"[TIME] query_tool completed in {time.time() - start_time:.2f}s")
    print("[CHECKPOINT] Exiting query_tool")
    return result


@tool("search_tool")
def search_tool():
    """
    Perform a web search using SerpAPI and store results.

    Returns:
        dict: Status of search operation.
    """
    print("[CHECKPOINT] Entered search_tool")
    try:
        file_path = os.path.join("output", "queries_data.json")
        with open(file_path, "r") as f:
            queries = json.load(f)
            print(queries)
        query_list = [q["query"] for q in queries]
        
    except Exception as e:
        print(f"[ERROR] Failed to load queries: {e}")
        return {"status": "error", "message": str(e)}
 
    print(f"[INPUT] permutations count: {len(query_list)}")
    start_time = time.time()

    print("[INFO] Running run_search with limit=30")
    result=run_search(query_list,limit=15)

    print("[OUTPUT] Search Completed")
    print(f"[TIME] search_tool completed in {time.time() - start_time:.2f}s")
    print("[CHECKPOINT] Exiting search_tool")
    return result
    
    
@tool("scraping_tool")
def scraping_tool():
    """
    Scrape data from previously collected URLs.

    Returns:
        dict: Status of scraping operation.
    """
    print("[CHECKPOINT] Entered scraping_tool")

    start_time = time.time()

    print("[INFO] Running scrape_all()")
    result=scrape_all()

    print("[OUTPUT] Scraping Completed")
    print(f"[TIME] scraping_tool completed in {time.time() - start_time:.2f}s")
    print("[CHECKPOINT] Exiting scraping_tool")
    return result


@tool("summarizer_tool")
def summarizer_tool(topic: str):
    """
    Summarize collected data into a structured AML report.

    Args:
        topic (str): The main topic to summarize.

    Returns:
        str: A summarized text report.
    """
    print("[CHECKPOINT] Entered summarizer_tool")
    print(f"[INPUT] topic: {topic}")
    start_time = time.time()

    print("[INFO] Running summarize()")
    result = summarize(topic)

    print(f"[OUTPUT] Summary length: {len(result)} characters")
    print(f"[TIME] summarizer_tool completed in {time.time() - start_time:.2f}s")
    print("[CHECKPOINT] Exiting summarizer_tool")
    return result                  

@CrewBase
class LatestAiDevelopmentCrew():

    """AML Crew with Tool-based Agents"""
    
    agents: List[BaseAgent]
    tasks: List[Task]


    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    



    @agent
    def permutation_agent(self) -> Agent:
        print("[CHECKPOINT] Creating permutation_agent")
        
        return Agent(
            config=self.agents_config['permutation_agent'],
            tools=[permutation_tool],
            verbose=True,
            llm=llm
        )
    @agent
    def query_agent(self) -> Agent:
        print("[CHECKPOINT] Creating query_agent")
        return Agent(
            config=self.agents_config['query_agent'],
            tools=[query_tool],
            verbose=True,
            llm=llm
        )

    @agent
    def search_agent(self) -> Agent:
        print("[CHECKPOINT] Creating search_agent")
        return Agent(
            config=self.agents_config["search_agent"],
            tools=[search_tool],
            verbose=True,
            llm=llm
        )

    @agent
    def scraping_agent(self) -> Agent:
        print("[CHECKPOINT] Creating scraping_agent")
        return Agent(
            config=self.agents_config["scraping_agent"],
            tools=[scraping_tool],
            verbose=True,
            llm=llm
        )

    @agent
    def summarizer_agent(self) -> Agent:
        print("[CHECKPOINT] Creating summarizer_agent")
        return Agent(
            config=self.agents_config["summarizer_agent"],
            tools=[summarizer_tool],
            verbose=True,
            llm=llm
        )

    @task
    def permutation_task(self) -> Task:
        print("[CHECKPOINT] Creating permutation_task")
        return Task(
            config=self.tasks_config["permutation_task"]
        )

    @task
    def query_task(self) -> Task:
        print("[CHECKPOINT] Creating query_task")
        return Task(
            config=self.tasks_config["query_task"]
        )


    @task
    def search_task(self) -> Task:
        print("[CHECKPOINT] Creating search_task")
        return Task(
            config=self.tasks_config["search_task"],
        )

    @task
    def scraping_task(self) -> Task:
        print("[CHECKPOINT] Creating scraping_task")
        return Task(
            config=self.tasks_config["scraping_task"],
        )

    @task
    def summarizer_task(self) -> Task:
        print("[CHECKPOINT] Creating summarizer_task")
        return Task(
            config=self.tasks_config["summarizer_task"],
            )



       


    @crew
    def crew(self) -> Crew:
        print("[CHECKPOINT] Assembling Crew")
        print(f"[INFO] Agents count: {len(self.agents)}, Tasks count: {len(self.tasks)}")
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )





    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    























    
    


