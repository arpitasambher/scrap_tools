import os
import time
import requests
import json
import random
import numpy as np  # Required for RL math
from typing import Optional, List, Dict
from langchain.llms.base import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool
import sys

# Mock imports if paths don't exist for the sake of the example
sys.path.insert(0, r"C:\users\hp\Desktop\siriusai\rock\final\utils")
try:
    from utils.permutation import generate_permutations
    from utils.queries import generate_queries
    from utils.search import run_search
    from utils.scraper import scrape_all
    from utils.summarizer import summarize
except ImportError:
    # Fallback mocks to ensure code runs if utils are missing
    def generate_permutations(data, n): return [{"name": data.get("name", "John Doe")}] * int(n)
    def generate_queries(perms, queries_per_identity=10): return [{"query": f"{p['name']} fraud", "type": "fraud"} for p in perms]
    def run_search(queries, limit=15): return [{"title": "Result", "snippet": "suspicious activity", "link": "http://example.com"}]
    def scrape_all(): return "Scraped content containing evidence of money laundering and fraud."
    def summarize(topic): return "Subject was involved in significant money laundering schemes."

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GEMINI_API_KEY = "AIzaSyBZLs0ZnQJHgCBJEotsRECDRQfr31Vj-SI" # Ensure this is secure in production
llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
    api_key=GEMINI_API_KEY,
)

# ============================================================================
#  1. REINFORCEMENT LEARNING ENGINE (Q-Learning / Bandit)
# ============================================================================

class RLOptimizer:
    """
    A simple Q-Learning/Bandit manager that learns which query keywords
    yield the best AML results over time.
    """
    def __init__(self, state_file="rl_brain.json"):
        self.state_file = os.path.join("output", state_file)
        self.epsilon = 0.2  # Exploration rate (20% random actions)
        self.alpha = 0.1    # Learning rate
        self.gamma = 0.9    # Discount factor
        
        # Define the "Arms" (Actions) - Types of AML queries
        self.actions = ["fraud", "money_laundering", "terrorism", "arrest", "sanctions", "corruption"]
        
        self.q_table = self.load_brain()

    def load_brain(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        # Initialize Q-values to 0.0
        return {action: 0.0 for action in self.actions}

    def save_brain(self):
        if not os.path.exists("output"):
            os.makedirs("output")
        with open(self.state_file, 'w') as f:
            json.dump(self.q_table, f, indent=4)

    def choose_action(self) -> str:
        """Epsilon-Greedy Action Selection"""
        if random.uniform(0, 1) < self.epsilon:
            print("[RL] Exploring: Choosing random keyword.")
            action = random.choice(self.actions)
        else:
            # Exploiting: Choose max Q value
            print("[RL] Exploiting: Choosing best performing keyword.")
            action = max(self.q_table, key=self.q_table.get)
        
        print(f"[RL] Selected Query Focus: {action.upper()} (Current Score: {self.q_table[action]:.2f})")
        return action

    def learn(self, action: str, reward: float):
        """Update Q-Table based on reward"""
        old_value = self.q_table.get(action, 0.0)
        # Q-learning update rule (simplified for 1-step bandit)
        new_value = old_value + self.alpha * (reward - old_value)
        self.q_table[action] = new_value
        self.save_brain()
        print(f"[RL] Updated Brain: {action} new score -> {new_value:.2f}")

# Initialize the RL Brain
rl_brain = RLOptimizer()

# ============================================================================
#  2. MODIFIED TOOLS WITH RL INTEGRATION
# ============================================================================

@tool("permutation_tool")
def permutation_tool(user_data: dict, num_permutations: str):
    """Generate permutations for AML based on user inputs."""
    print("[CHECKPOINT] Entered permutation_tool")
    start_time = time.time()
    result = generate_permutations(user_data, num_permutations)
    
    # Save user data for later context if needed
    with open(os.path.join("output", "permuted_data.json"), "w") as f:
        json.dump(result, f)
        
    print(f"[TIME] permutation_tool completed in {time.time() - start_time:.2f}s")
    return result


@tool("query_tool")
def query_tool():
    """
    Loads permutations and generates AML queries. 
    USES RL TO PRIORITIZE SPECIFIC KEYWORDS.
    """
    print("[CHECKPOINT] Entered query_tool")
    
    try:
        file_path = os.path.join("output", "permuted_data.json")
        with open(file_path, "r") as f:
            permutations = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load permutations: {e}")
        return []

    # --- RL INTEGRATION ---
    # Ask the RL Brain which keyword category to prioritize for this run
    priority_keyword = rl_brain.choose_action()
    # ----------------------

    print(f"[INFO] RL Agent selected priority strategy: {priority_keyword}")

    # Generate standard queries (assuming generate_queries returns a list of dicts)
    raw_queries = generate_queries(permutations, queries_per_identity=20)
    
    # Filter or Boost queries based on RL selection
    # Assuming raw_queries contains strings, we append the priority keyword if not present
    # Or if generate_queries returns objects, we filter them.
    
    final_query_list = []
    
    # Logic: We ensure the RL-selected keyword is appended to the queries
    # and we tag them so we know what action caused this result
    for item in raw_queries:
        # If item is a dict from utils
        q_text = item.get('query', '') if isinstance(item, dict) else str(item)
        
        # Inject RL keyword into the query string for better targeting
        enhanced_query = f"{q_text} {priority_keyword}"
        
        final_query_list.append({
            "query": enhanced_query,
            "rl_action": priority_keyword # Track which action generated this
        })

    # Save intended queries
    with open(os.path.join("output", "queries_data.json"), "w") as f:
        json.dump(final_query_list, f)

    return final_query_list


@tool("search_tool")
def search_tool():
    """Perform a web search using SerpAPI."""
    print("[CHECKPOINT] Entered search_tool")
    try:
        file_path = os.path.join("output", "queries_data.json")
        with open(file_path, "r") as f:
            queries = json.load(f)
        
        # Extract just the string for the search engine
        query_texts = [q["query"] for q in queries]
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

    result = run_search(query_texts, limit=15)
    return result


@tool("scraping_tool")
def scraping_tool():
    """Scrape data from collected URLs."""
    print("[CHECKPOINT] Entered scraping_tool")
    result = scrape_all()
    return result


@tool("summarizer_and_reward_tool")
def summarizer_and_reward_tool(topic: str):
    """
    Summarize collected data AND calculate RL Reward.
    """
    print("[CHECKPOINT] Entered summarizer_and_reward_tool")
    
    # 1. Run the standard summarization
    summary_text = summarize(topic)

    # 2. --- RL REWARD CALCULATION ---
    print("[RL] Calculating Reward based on finding...")
    
    reward = 0.0
    
    # Define "High Value" words - if these appear, the query strategy was good
    high_value_triggers = ["guilty", "convicted", "arrested", "sentence", "prison", "fine", "laundering"]
    medium_value_triggers = ["alleged", "accused", "investigation", "court", "charges"]
    
    lower_summary = summary_text.lower()
    
    for word in high_value_triggers:
        if word in lower_summary:
            reward += 2.0
            
    for word in medium_value_triggers:
        if word in lower_summary:
            reward += 0.5

    # Penalize if the summary says "No information found"
    if "no relevant information" in lower_summary or len(summary_text) < 50:
        reward -= 1.0

    print(f"[RL] Calculated Reward: {reward}")

    # 3. Retrieve which action we took (from the saved queries file)
    try:
        with open(os.path.join("output", "queries_data.json"), "r") as f:
            queries = json.load(f)
            # We assume the batch used the same RL action
            if queries:
                action_taken = queries[0].get("rl_action", "fraud")
                
                # UPDATE THE BRAIN
                rl_brain.learn(action_taken, reward)
    except Exception as e:
        print(f"[RL ERROR] Could not update brain: {e}")

    return summary_text


# ============================================================================
#  3. CREW DEFINITION
# ============================================================================

@CrewBase
class LatestAiDevelopmentCrew():
    """AML Crew with Tool-based Agents and RL Optimization"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def permutation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['permutation_agent'],
            tools=[permutation_tool],
            verbose=True,
            llm=llm
        )
        
    @agent
    def query_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['query_agent'],
            tools=[query_tool], # Uses RL inside
            verbose=True,
            llm=llm
        )

    @agent
    def search_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["search_agent"],
            tools=[search_tool],
            verbose=True,
            llm=llm
        )

    @agent
    def scraping_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["scraping_agent"],
            tools=[scraping_tool],
            verbose=True,
            llm=llm
        )

    @agent
    def summarizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["summarizer_agent"],
            tools=[summarizer_and_reward_tool], # Calculates Reward
            verbose=True,
            llm=llm
        )

    # Tasks Definition
    @task
    def permutation_task(self) -> Task:
        return Task(config=self.tasks_config["permutation_task"])

    @task
    def query_task(self) -> Task:
        return Task(config=self.tasks_config["query_task"])

    @task
    def search_task(self) -> Task:
        return Task(config=self.tasks_config["search_task"])

    @task
    def scraping_task(self) -> Task:
        return Task(config=self.tasks_config["scraping_task"])

    @task
    def summarizer_task(self) -> Task:
        return Task(config=self.tasks_config["summarizer_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.permutation_agent(),
                self.query_agent(),
                self.search_agent(),
                self.scraping_agent(),
                self.summarizer_agent()
            ],
            tasks=[
                self.permutation_task(),
                self.query_task(),
                self.search_task(),
                self.scraping_task(),
                self.summarizer_task()
            ],
            process=Process.sequential,
            verbose=True
        )


if __name__ == "__main__":
    print("## Starting AML Crew with Reinforcement Learning ##")
    
    # Optional: Run in a loop to simulate "Training Episodes"
    # In a real scenario, you run this once per request, but the "brain.json" persists
    
    inputs = {'topic': 'AML Investigation', 'user_data': {'name': 'John Doe'}, 'num_permutations': '5'}
    
    # Run the crew
    crew_instance = LatestAiDevelopmentCrew()
    result = crew_instance.crew().kickoff(inputs=inputs)
    
    print("\n################################################")
    print("## Final Result ##")
    print("################################################\n")
    print(result)
