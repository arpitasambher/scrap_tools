# import os
# import requests
# from typing import Optional
# from langchain.llms.base import LLM

# class OpenRouterLLM(LLM):
#     """Custom LLM wrapper for OpenRouter API with detailed debugging and CrewAI compatibility."""

#     api_key: str = os.getenv("OPENROUTER_API_KEY")

#     @property
#     def _llm_type(self) -> str:
#         return "openrouter"


#     def _call(self, prompt: str, stop: Optional[list] = None) -> str:
#         try:
#             prompt = str(prompt)
#             print("\n[CHECKPOINT] Entered OpenRouterLLM._call()")
#             print(f"[INPUT] Prompt length: {len(prompt)} characters")
#             print(f"[INPUT] Stop tokens: {stop}")

#             if not self.api_key:
#                 print("[ERROR] OPENROUTER_API_KEY missing.")
#                 return "Error: Missing API Key"

#             url = "https://openrouter.ai/api/v1/chat/completions"
#             headers = {
#                 "Authorization": f"Bearer {self.api_key}",
#                 "Content-Type": "application/json"
#             }
#             payload = {
#                 "model": "meta-llama/llama-3-8b-instruct",
#                 "messages": [{"role": "user", "content": prompt}],
#             }

#             print("[CHECKPOINT] Sending request to OpenRouter API...")
#             response = requests.post(url, headers=headers, json=payload, timeout=60)
#             print(f"[DEBUG] HTTP Status: {response.status_code}")

#             if response.status_code == 200:
#                 data = response.json()
#                 if "choices" in data and len(data["choices"]) > 0:
#                     content = data["choices"][0]["message"]["content"]
#                     print(f"[OUTPUT] Response length: {len(content)} chars")
#                     return content[:2000]  # Limit size if needed
#                 else:
#                     return "Error: Invalid response structure"
#             else:
#                 print(f"[ERROR] API returned {response.status_code}")
#                 return f"Error: API {response.status_code} {response.text[:300]}"
#         except Exception as e:
#             print(f"[CRITICAL ERROR] {e}")
#             return f"Error: {str(e)}"





import os
import time
import requests
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

# class OpenRouterLLM(LLM):
#     """Custom LLM wrapper for OpenRouter API with detailed debugging and CrewAI compatibility."""

#     api_key: str = os.getenv("OPENROUTER_API_KEY")

#     @property
#     def _llm_type(self) -> str:
#         return "openrouter"

#     def _call(self, prompt: str, stop: Optional[list] = None) -> str:
#         try:
#             print("\n[CHECKPOINT] OpenRouterLLM called")
#             if not self.api_key:
#                 return "Error: Missing OPENROUTER_API_KEY"

#             url = "https://openrouter.ai/api/v1/chat/completions"
#             headers = {
#                 "Authorization": f"Bearer {self.api_key}",
#                 "Content-Type": "application/json"
#             }
#             payload = {
#                 "model": "meta-llama/llama-3-8b-instruct",
#                 "messages": [{"role": "user", "content": str(prompt)}]
#             }

#             response = requests.post(url, headers=headers, json=payload, timeout=60)
#             if response.status_code == 200:
#                 data = response.json()
#                 return data["choices"][0]["message"]["content"] if "choices" in data else "Error: Bad API response"
#             else:
#                 return f"Error: {response.status_code} - {response.text}"
#         except Exception as e:
#             return f"Error: {str(e)}"

from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai import LLM


# llm = LLM(
#     model="openrouter/meta-llama/llama-3.3-70b-instruct:free",
#     base_url="https://openrouter.ai/api/v1",
#     api_key='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',
#     # stream=True,
# )

# llm = LLM(
#     model="openrouter/deepseek/deepseek-r1",
#     base_url="https://openrouter.ai/api/v1",
#     api_key="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",
#     stream=True 
# )

# llm = LLM(
#     model="ollama/llama3.2:1b",
#     base_url="http://localhost:11434"
# )
GEMINI_API_KEY="AIzaSyDhbckEeDbDdZKQ-R83T81llxi62yN3Ta8"
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
        file_path (str, optional): File path for storing output. Defaults to  permuted_user_data.json "".

    Returns:
        list: A list of generated permutations.
    """
    print("[CHECKPOINT] Entered permutation_tool")
    print(f"[INPUT] user_inputs: {user_data}, num_permutations: {num_permutations}")
    start_time = time.time()

    result = generate_permutations(user_data, num_permutations)

    print(f"[OUTPUT] Generated {len(result)} permutations")
    print(f"[TIME] permutation_tool completed in {time.time() - start_time:.2f}s")
    print("[CHECKPOINT] Exiting permutation_tool")
    return result


# @tool("query_tool")
# def query_tool():
#     """
#     Self-contained tool that loads permutations from file and generates AML queries.
#     """
#     import json, time
#     print("[CHECKPOINT] Entered query_tool")
    
#     try:
#         with open(r"scrap_tools\final\output\permuted_user_data.json", "r") as f:
#             permutations = json.load(f)
#             print(permutations)
#     except Exception as e:
#         print(f"[ERROR] Failed to load permutations: {e}")
 
#     print(f"[INPUT] permutations count: {len(permutations)}")
#     start_time = time.time()
 
#     result = generate_queries(permutations, queries_per_identity=10)
 
#     print(f"[OUTPUT] Generated {len(result)} queries")
#     print(f"[TIME] query_tool completed in {time.time() - start_time:.2f}s")
#     print("[CHECKPOINT] Exiting query_tool")
#     return result

@CrewBase
class LatestAiDevelopmentCrew():


    """AML Crew with Tool-based Agents"""
    
    agents: List[BaseAgent]
    tasks: List[Task]

#     agents_config = os.path.join(BASE_DIR, "config", "agents.yaml")
#     tasks_config = os.path.join(BASE_DIR, "config", "tasks.yaml")
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ========================
    # Tools
    # ========================

#     @tool("permutation_tool")
#     def permutation_tool(self, user_inputs: dict, file_path: str = ""):
#         """
#         Generate permutations for AML based on user inputs.

#         Args:
#             user_inputs (dict): Dictionary containing user input values for AML.
#             file_path (str, optional): File path for storing output. Defaults to  permuted_user_data.json "".

#         Returns:
#             list: A list of generated permutations.
#         """
#         print("[CHECKPOINT] Entered permutation_tool")
#         print(f"[INPUT] user_inputs: {user_inputs}, file_path: {file_path}")
#         start_time = time.time()

#         result = generate_permutations(user_inputs, user_inputs.get("num_permutations", 5))

#         print(f"[OUTPUT] Generated {len(result)} permutations")
#         print(f"[TIME] permutation_tool completed in {time.time() - start_time:.2f}s")
#         print("[CHECKPOINT] Exiting permutation_tool")
#         return result

#     @tool("query_tool")
#     def query_tool(self, permutations: list):
#         """
#         Generate AML-related queries from provided permutations.

#         Args:
#             permutations (list): A list of permutations generated earlier.

#         Returns:
#             list: A list of generated queries based on permutations.
#         """
#         print("[CHECKPOINT] Entered query_tool")
#         print(f"[INPUT] permutations count: {len(permutations)}")
#         start_time = time.time()

#         result = generate_queries(permutations, queries_per_identity=10)

#         print(f"[OUTPUT] Generated {len(result)} queries")
#         print(f"[TIME] query_tool completed in {time.time() - start_time:.2f}s")
#         print("[CHECKPOINT] Exiting query_tool")
#         return result

#     @tool("search_tool")
#     def search_tool(self):
#         """
#         Perform a web search using SerpAPI and store results.

#         Returns:
#             dict: Status of search operation.
#         """
#         print("[CHECKPOINT] Entered search_tool")
#         start_time = time.time()

#         print("[INFO] Running run_search with limit=30")
#         run_search(limit=30)

#         print("[OUTPUT] Search Completed")
#         print(f"[TIME] search_tool completed in {time.time() - start_time:.2f}s")
#         print("[CHECKPOINT] Exiting search_tool")
#         return {"status": "Search Completed"}

#     @tool("scraping_tool_calling")
#     def scraping_tool(self):
#         """
#         Scrape data from previously collected URLs.

#         Returns:
#             dict: Status of scraping operation.
#         """
#         print("[CHECKPOINT] Entered scraping_tool")
#         start_time = time.time()

#         print("[INFO] Running scrape_all()")
#         scrape_all()

#         print("[OUTPUT] Scraping Completed")
#         print(f"[TIME] scraping_tool completed in {time.time() - start_time:.2f}s")
#         print("[CHECKPOINT] Exiting scraping_tool")
#         return {"status": "Scraping Completed"}

#     @tool("summarizer_tool_calling")
#     def summarizer_tool(self, topic: str):
#         """
#         Summarize collected data into a structured AML report.

#         Args:
#             topic (str): The main topic to summarize.

#         Returns:
#             str: A summarized text report.
#         """
#         print("[CHECKPOINT] Entered summarizer_tool")
#         print(f"[INPUT] topic: {topic}")
#         start_time = time.time()

#         print("[INFO] Running summarize()")
#         result = summarize(topic)

#         print(f"[OUTPUT] Summary length: {len(result)} characters")
#         print(f"[TIME] summarizer_tool completed in {time.time() - start_time:.2f}s")
#         print("[CHECKPOINT] Exiting summarizer_tool")
#         return result




    @agent
    def permutation_agent(self) -> Agent:
        print("[CHECKPOINT] Creating permutation_agent")
        
        return Agent(
            config=self.agents_config['permutation_agent'],
            tools=[permutation_tool],
            verbose=True,
            llm=llm
        )
    # @agent
    # def query_agent(self) -> Agent:
    #     print("[CHECKPOINT] Creating query_agent")
    #     return Agent(
    #         config=self.agents_config['query_agent'],
    #         tools=[query_tool],
    #         verbose=True,
    #         llm=llm
    #     )

#     @agent
#     def query_agent(self) -> Agent:
#         print("[CHECKPOINT] Creating query_agent")
#         return Agent(
#             config={
#                 **self.agents_config["query_agent"],
#                 "goal": self.agents_config["query_agent"]["goal"] +
#                         " Use the `query_tool` to create queries based on permutations."
#             },
#             tools=[self.query_tool],
#             verbose=True,
#             llm=llm
#         )






#     @agent
#     def search_agent(self) -> Agent:
#         print("[CHECKPOINT] Creating search_agent")
#         return Agent(
#             config={
#                 **self.agents_config["search_agent"],
#                 "goal": self.agents_config["search_agent"]["goal"] +
#                         " Use the `search_tool` to perform searches."
#             },
#             tools=[self.search_tool],
#             verbose=True,
#             llm=llm
#         )

#     @agent
#     def scraping_agent(self) -> Agent:
#         print("[CHECKPOINT] Creating scraping_agent")
#         return Agent(
#             config={
#                 **self.agents_config["scraping_agent"],
#                 "goal": self.agents_config["scraping_agent"]["goal"] +
#                         " Use the `scraping_tool` to extract data from URLs."
#             },
#             tools=[self.scraping_tool],
#             verbose=True,
#             llm=llm
#         )

#     @agent
#     def summarizer_agent(self) -> Agent:
#         print("[CHECKPOINT] Creating summarizer_agent")
#         return Agent(
#             config={
#                 **self.agents_config["summarizer_agent"],
#                 "goal": self.agents_config["summarizer_agent"]["goal"] +
#                         " Use the `summarizer_tool` to generate AML-focused summaries."
#             },
#             tools=[self.summarizer_tool],
#             verbose=True,
#             llm=llm
#         )

    @task
    def permutation_task(self) -> Task:
        print("[CHECKPOINT] Creating permutation_task")
        return Task(
            config=self.tasks_config["permutation_task"]
        )

    # @task
    # def query_task(self) -> Task:
    #     print("[CHECKPOINT] Creating query_task")
    #     return Task(
    #         config=self.tasks_config['query_task']
    #     )

#     @task
#     def query_task(self) -> Task:
#         print("[CHECKPOINT] Creating query_task")
#         return Task(
#             config={
#                 **self.tasks_config["query_task"],
#                 "description": self.tasks_config["query_task"]["description"] +
#                                " You must use the provided `query_tool` to create search queries."
#             },
#             agent=self.query_agent(),
#             execute=lambda inputs: self.query_tool(inputs.get("permutations", []))
#         )

#     @task
#     def search_task(self) -> Task:
#         print("[CHECKPOINT] Creating search_task")
#         return Task(
#             config={
#                 **self.tasks_config["search_task"],
#                 "description": self.tasks_config["search_task"]["description"] +
#                                " Use the `search_tool` to find relevant URLs."
#             },
#             agent=self.search_agent(),
#             execute=lambda _: self.search_tool()
#         )

#     @task
#     def scraping_task(self) -> Task:
#         print("[CHECKPOINT] Creating scraping_task")
#         return Task(
#             config={
#                 **self.tasks_config["scraping_task"],
#                 "description": self.tasks_config["scraping_task"]["description"] +
#                                " Use the `scraping_tool` to extract content from these URLs."
#             },
#             agent=self.scraping_agent(),
#             execute=lambda _: self.scraping_tool()
#         )

#     @task
#     def summarizer_task(self) -> Task:
#         print("[CHECKPOINT] Creating summarizer_task")
#         return Task(
#             config={
#                 **self.tasks_config["summarizer_task"],
#                 "description": self.tasks_config["summarizer_task"]["description"] +
#                                " Use the `summarizer_tool` to compile AML-focused summaries."
#             },
#             agent=self.summarizer_agent(),
#             output_json=AMLReport,
#             execute=lambda inputs: AMLReport(
#                 topic=inputs.get("topic"),
#                 total_permutations=inputs.get("num_permutations", 0),
#                 total_queries=10,
#                 summary=self.summarizer_tool(inputs.get("topic"))
#             )
#         )


        # ========================
        # Crew Assembly
        # ========================



    # @crew
    # def crew(self) -> Crew:
    #     print("[CHECKPOINT] Assembling Crew")
    #     print(f"[INFO] Agents count: {len(self.agents)}, Tasks count: {len(self.tasks)}")
    #     return Crew(
    #         agents=self.agents,
    #         tasks=self.tasks,
    #         process=Process.sequential,
    #         verbose=True
    #     )




    # Create Crew for a single agent
    @crew
    def crew(self) -> Crew:
        print("[CHECKPOINT] Assembling Crew")
        print(f"[INFO] Agents count: {len(self.agents)}, Tasks count: {len(self.tasks)}")
        single_agent = self.permutation_agent()
        single_task = self.permutation_task()
        return Crew(
            agents=[single_agent],
            tasks=[single_task],
            process=Process.sequential,
            verbose=True,
        )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    























    
    


