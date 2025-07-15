# import os
# import yaml
# from crewai import Agent, Crew, Process, Task
# from crewai.project import CrewBase, agent, crew, task
# from tools.openrouter_tool import OpenRouterLLMTool
# from tools.serpapi_tool import SerpApiTool
# from tools.scraper_tool import ScraperTool
# from models import AMLReport
# from utils.permutation import generate_permutations
# from utils.queries import generate_queries
# from utils.search import run_search
# from utils.scraper import scrape_all
# from utils.summarizer import summarize

# def load_yaml(path):
#     with open(path, "r") as f:
#         return yaml.safe_load(f)

# CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")
# import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# @CrewBase
# class LatestAiDevelopmentCrew():
#     """AML Crew"""

#     agents_config = os.path.join(BASE_DIR, "config", "agents.yaml")
#     tasks_config = os.path.join(BASE_DIR, "config", "tasks.yaml")

# # class LatestAiDevelopmentCrew():
# #     """AML Crew"""
# # #     agents_config = load_yaml(os.path.join(CONFIG_DIR, "agents.yaml"))
# # #     tasks_config = load_yaml(os.path.join(CONFIG_DIR, "tasks.yaml"))
# #     agents_config = "config/agents.yaml"
# #     tasks_config = "config/tasks.yaml"

#     @agent
#     def researcher(self) -> Agent:
#         return Agent(
#             config=self.agents_config["researcher"],
#             tools=[OpenRouterLLMTool(), SerpApiTool(), ScraperTool()],
#             verbose=True
#         )

#     @agent
#     def reporting_analyst(self) -> Agent:
#         return Agent(
#             config=self.agents_config["reporting_analyst"],
#             tools=[OpenRouterLLMTool()],
#             verbose=True
#         )

#     @task
#     def research_task(self) -> Task:
#         return Task(
#             config=self.tasks_config["research_task"],
#             agent=self.researcher(),
#             execute=lambda inputs: self._run_research(inputs)
#         )

#     @task
#     def reporting_task(self) -> Task:
#         return Task(
#             config=self.tasks_config["reporting_task"],
#             agent=self.reporting_analyst(),
#             output_json=AMLReport,
#             execute=lambda inputs: self._run_reporting(inputs)
#         )

#     @crew
#     def crew(self) -> Crew:
#         return Crew(
#             agents=self.agents,
#             tasks=self.tasks,
#             process=Process.sequential,
#             verbose=2
#         )

#     def _run_research(self, inputs):
#         topic = inputs.get("topic")
#         user_data = inputs.get("user_data")
#         num = inputs.get("num_permutations")

#         perms = generate_permutations(user_data, num)
#         queries = generate_queries(perms, 10)
#         run_search(limit=30)
#         scrape_all()
#         return {"status": "Research done", "topic": topic}

#     def _run_reporting(self, inputs):
#         topic = inputs.get("topic")
#         summary = summarize(topic)
#         return AMLReport(topic=topic, total_permutations=inputs["num_permutations"], total_queries=10, summary=summary)




import os
import time
import yaml
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.openrouter_tool import OpenRouterLLMTool
from tools.serpapi_tool import SerpApiTool
from tools.scraper_tool import ScraperTool
from models import AMLReport
from utils.permutation import generate_permutations
from utils.queries import generate_queries
from utils.search import run_search
from utils.scraper import scrape_all
from utils.summarizer import summarize
from tools.openrouter_llm import OpenRouterLLM

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@CrewBase
class LatestAiDevelopmentCrew():
    """AML Crew"""

    agents_config = os.path.join(BASE_DIR, "config", "agents.yaml")
    tasks_config = os.path.join(BASE_DIR, "config", "tasks.yaml")

    # -------------------------
    # Agents
    # -------------------------
    @agent
    def researcher(self) -> Agent:
        print("[CHECKPOINT] Initializing Researcher Agent...")
        return Agent(
            config=self.agents_config["researcher"],
            tools=[SerpApiTool(), ScraperTool()],
            verbose=True,
            llm=OpenRouterLLM()
        )

    @agent
    def reporting_analyst(self) -> Agent:
        print("[CHECKPOINT] Initializing Reporting Analyst Agent...")
        return Agent(
            config=self.agents_config["reporting_analyst"],
            tools=[],
            verbose=True,
            llm=OpenRouterLLM() 
        )

    # -------------------------
    # Tasks
    # -------------------------
    @task
    def research_task(self) -> Task:
        print("[CHECKPOINT] Creating Research Task...")
        return Task(
            config=self.tasks_config["research_task"],
            agent=self.researcher(),
            execute=lambda inputs: self._run_research(inputs)
        )

    @task
    def reporting_task(self) -> Task:
        print("[CHECKPOINT] Creating Reporting Task...")
        return Task(
            config=self.tasks_config["reporting_task"],
            agent=self.reporting_analyst(),
            output_json=AMLReport,
            execute=lambda inputs: self._run_reporting(inputs)
        )

    # -------------------------
    # Crew Assembly
    # -------------------------
    @crew
    def crew(self) -> Crew:
        print("[CHECKPOINT] Building Crew with sequential process...")
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=2
        )

    # -------------------------
    # Task Logic with Logs
    # -------------------------
    def _run_research(self, inputs):
        print("[TASK] Research Task Started...")
        start_time = time.time()

        try:
            topic = inputs.get("topic")
            user_data = inputs.get("user_data")
            num = inputs.get("num_permutations")
            print(f"[INFO] Topic: {topic}, Permutations: {num}")

            # Step 1: Generate permutations
            print("[STEP 1] Generating permutations...")
            perms = generate_permutations(user_data, num)
            print(f"[STEP 1 ✅] Generated {len(perms)} permutations")

            # Step 2: Generate queries
            print("[STEP 2] Generating queries...")
            queries = generate_queries(perms, 10)
            print(f"[STEP 2 ✅] Generated {len(queries)} queries")

            # Step 3: Search
            print("[STEP 3] Running SerpAPI search...")
            run_search(limit=30)
            print("[STEP 3 ✅] Search complete")

            # Step 4: Scraping
            print("[STEP 4] Scraping search results...")
            scrape_all()
            print("[STEP 4 ✅] Scraping complete")

            print(f"[TASK ✅] Research completed in {round(time.time() - start_time, 2)}s")
            return {"status": "Research done", "topic": topic}

        except Exception as e:
            print(f"[ERROR] Research Task Failed: {str(e)}")
            return {"status": "FAILED", "error": str(e)}

    def _run_reporting(self, inputs):
        print("[TASK] Reporting Task Started...")
        start_time = time.time()

        try:
            topic = inputs.get("topic")
            print(f"[INFO] Summarizing for topic: {topic}")

            # Step 1: Summarize
            summary = summarize(topic)
            print(f"[STEP ✅] Summary created")

            print(f"[TASK ✅] Reporting completed in {round(time.time() - start_time, 2)}s")
            return AMLReport(
                topic=topic,
                total_permutations=inputs.get("num_permutations", 0),
                total_queries=10,
                summary=summary
            )

        except Exception as e:
            print(f"[ERROR] Reporting Task Failed: {str(e)}")
            return {"status": "FAILED", "error": str(e)}
