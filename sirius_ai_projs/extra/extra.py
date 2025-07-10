




# import os
# import sys
# import logging
# from crewai import Agent, Task, Crew, Process
# from crewai.tools import tool
# from crewai import LLM
# # from langchain_openai import ChatOpenAI
# from langchain_ollama import OllamaLLM




# # -------------------------------
# # Setup Logging
# # -------------------------------
# logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
# def checkpoint(msg):
#     logging.info(f"🔵 CHECKPOINT: {msg}")


# # -------------------------------
# # Custom Tools for Each Agent
# # -------------------------------
# @tool("Generate Permuted User Data")
# def agent1_tool() -> str:
#     """Run Agent 1 to generate user data permutations from input."""
#     checkpoint(" Agent 1 Tool: Importing run_agent1 from agent1 module...")
#     try:
#         from agent1 import run_agent1
#         checkpoint(" Agent 1 Tool: Successfully imported run_agent1.")
#     except Exception as e:
#         checkpoint(f" Agent 1 Tool: Import failed with error: {e}")
#         raise

#     try:
#         checkpoint(" Agent 1 Tool: Running run_agent1()...")
#         run_agent1()
#         checkpoint(" Agent 1 Tool: run_agent1() completed successfully.")
#     except Exception as e:
#         checkpoint(f" Agent 1 Tool: Execution failed with error: {e}")
#         raise

#     return "Agent 1 completed"




# @tool("Search and Scrape User Info")
# def agent2_tool() -> str:
#     """Run Agent 2 to perform search and scrape using SerpAPI and ScrapeWebsiteTool."""
#     checkpoint(" Agent 2 Tool: Importing run_agent2 from agent2 module...")
#     try:
#         from agent2 import run_agent2
#         checkpoint(" Agent 2 Tool: Successfully imported run_agent2.")
#     except Exception as e:
#         checkpoint(f" Agent 2 Tool: Import failed with error: {e}")
#         raise

#     try:
#         checkpoint(" Agent 2 Tool: Running run_agent2()...")
#         run_agent2()
#         checkpoint(" Agent 2 Tool: run_agent2() completed successfully.")
#     except Exception as e:
#         checkpoint(f" Agent 2 Tool: Execution failed with error: {e}")
#         raise

#     return "Agent 2 completed"



# @tool("Summarize AML Findings")
# def agent3_tool() -> str:
#     """Run Agent 3 to summarize AML content from scraped web data."""
#     checkpoint(" Agent 3 Tool: Importing run_agent3 from agent3 module...")
#     try:
#         from agent3 import run_agent3
#         checkpoint(" Agent 3 Tool: Successfully imported run_agent3.")
#     except Exception as e:
#         checkpoint(f" Agent 3 Tool: Import failed with error: {e}")
#         raise

#     try:
#         checkpoint(" Agent 3 Tool: Running run_agent3()...")
#         run_agent3()
#         checkpoint("Agent 3 Tool: run_agent3() completed successfully.")
#     except Exception as e:
#         checkpoint(f" Agent 3 Tool: Execution failed with error: {e}")
#         raise

#     return " Agent 3 completed"


# llm = LLM(
#     model= "ollama/llama3.2:1b",
#     base_url="http://localhost:11434"
# )

# # -------------------------------
# # Define Agents
# # -------------------------------
# checkpoint("Defining agents...")

# try:
#     agent1 = Agent(
#         role="Permutator",
#         goal="Generate realistic variations of user identity data",
#         backstory="An expert in LLMs and data anonymization.",
#         tools=[agent1_tool],
#         default_tool=agent1_tool,  # 🔧 Force tool execution
#         allow_delegation=False,
#         llm=llm,
#          verbose=True
#     )
#     checkpoint(" Agent 1 defined.")
# except Exception as e:
#     checkpoint(f" Failed to define Agent 1: {e}")
#     raise

# try:
#     agent2 = Agent(
#         role="AML Web Investigator",
#         goal="Search online platforms and extract suspicious content about users",
#         backstory="A specialist in search and digital evidence collection.",
#         tools=[agent2_tool],
#         default_tool=agent2_tool,  # 🔧 Force tool execution
#         allow_delegation=False,
#         llm=llm,
#         verbose=True
#     )
#     checkpoint(" Agent 2 defined.")
# except Exception as e:
#     checkpoint(f" Failed to define Agent 2: {e}")
#     raise

# try:
#     agent3 = Agent(
#         role="AML Summarizer",
#         goal="Extract and summarize financial crime and fraud indicators",
#         backstory="An LLM agent skilled at reviewing and summarizing large data dumps.",
#         tools=[agent3_tool],
#         default_tool=agent3_tool,  # 🔧 Force tool execution
#          allow_delegation=False,
#          llm=llm,
#          verbose=True
#     )
#     checkpoint(" Agent 3 defined.")
# except Exception as e:
#     checkpoint(f"Failed to define Agent 3: {e}")
#     raise


# # -------------------------------
# # Define Tasks
# # -------------------------------
# checkpoint("Defining tasks...")

# try:
#     task1 = Task(
#         description="Generate 15 realistic permutations of user data by accepting manual input.",
#         expected_output="A JSON file named permuted_user_data27.json",
#         agent=agent1,
#           tool=agent1_tool, 
#         force_tool=True 
#     )
#     checkpoint(" Task 1 defined.")
# except Exception as e:
#     checkpoint(f"Failed to define Task 1: {e}")
#     raise

# try:
#     task2 = Task(
#         description="Search Google for AML-related results for each user and scrape the top 10 links.",
#         expected_output="A file output27.json with scraped content or error per link.",
#         agent=agent2,
#           tool=agent2_tool, 
#         force_tool=True  
#     )
#     checkpoint(" Task 2 defined.")
# except Exception as e:
#     checkpoint(f"Failed to define Task 2: {e}")
#     raise

# try:
#     task3 = Task(
#         description="Summarize the AML-related findings from the scraped web pages.",
#         expected_output="A summary.txt file with highlights of each relevant web page.",
#         agent=agent3,
#           tool=agent3_tool, 
#         force_tool=True  
#     )
#     checkpoint(" Task 3 defined.")
# except Exception as e:
#     checkpoint(f"Failed to define Task 3: {e}")
#     raise


# # -------------------------------
# # Run Crew Sequentially
# # -------------------------------
# checkpoint(" Assembling Crew...")

# try:
    
#     crew = Crew(
#         agents=[agent1, agent2, agent3],
#         tasks=[task1, task2, task3],
#         process=Process.sequential,
#         verbose=False,
#         memory=False
#     )
#     checkpoint(" Crew assembled successfully.")
# except Exception as e:
#     checkpoint(f" Failed to assemble Crew: {e}")
#     raise


# # -------------------------------
# # Launching Execution
# # -------------------------------
# # if __name__ == "__main__":
# #     print("🔧 Testing tools directly...\n")

# #     print(agent1_tool.run())  # Correct usage
# #     print(agent2_tool.run())
# #     print(agent3_tool.run())

# #     print("\n✅ All tools executed directly.")


# if __name__ == "__main__":
#     checkpoint(" Launching full CrewAI pipeline...")
#     try:
#         result = crew.kickoff()
#         checkpoint(" All agents completed!")
#         print("\n Final Crew Result:", result)
#     except Exception as e:
#         checkpoint(f" Crew execution failed: {e}")
#         raise







import os
import sys
import logging
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from crewai import LLM
# from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM




# -------------------------------
# Setup Logging
# -------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
def checkpoint(msg):
    logging.info(f"🔵 CHECKPOINT: {msg}")


# -------------------------------
# Custom Tools for Each Agent
# -------------------------------
@tool("Generate Permuted User Data")
def agent1_tool() -> str:
    """Run Agent 1 to generate user data permutations from input."""
    checkpoint(" Agent 1 Tool: Importing run_agent1 from agent1 module...")
    try:
        # from agent1 import run_agent1
        from agent1 import generate_permutations
        checkpoint(" Agent 1 Tool: Successfully imported run_agent1.")
    except Exception as e:
        checkpoint(f" Agent 1 Tool: Import failed with error: {e}")
        raise

    try:
        checkpoint(" Agent 1 Tool: Running run_agent1()...")
        # run_agent1()
        generate_permutations(input_data={"name": "Vijay Mallaya", "phone": "94748494"}, num_permutations=15)
        checkpoint(" Agent 1 Tool: run_agent1() completed successfully.")
    except Exception as e:
        checkpoint(f" Agent 1 Tool: Execution failed with error: {e}")
        raise

    return "Agent 1 completed"




@tool("Search and Scrape User Info")
def agent2_tool() -> str:
    """Run Agent 2 to perform search and scrape using SerpAPI and ScrapeWebsiteTool."""
    checkpoint(" Agent 2 Tool: Importing run_agent2 from agent2 module...")
    try:
        from agent2 import run_agent2
        checkpoint(" Agent 2 Tool: Successfully imported run_agent2.")
    except Exception as e:
        checkpoint(f" Agent 2 Tool: Import failed with error: {e}")
        raise

    try:
        checkpoint(" Agent 2 Tool: Running run_agent2()...")
        run_agent2()
        checkpoint(" Agent 2 Tool: run_agent2() completed successfully.")
    except Exception as e:
        checkpoint(f" Agent 2 Tool: Execution failed with error: {e}")
        raise

    return "Agent 2 completed"



@tool("Summarize AML Findings")
def agent3_tool() -> str:
    """Run Agent 3 to summarize AML content from scraped web data."""
    checkpoint(" Agent 3 Tool: Importing run_agent3 from agent3 module...")
    try:
        from agent3 import run_agent3
        checkpoint(" Agent 3 Tool: Successfully imported run_agent3.")
    except Exception as e:
        checkpoint(f" Agent 3 Tool: Import failed with error: {e}")
        raise

    try:
        checkpoint(" Agent 3 Tool: Running run_agent3()...")
        run_agent3()
        checkpoint("Agent 3 Tool: run_agent3() completed successfully.")
    except Exception as e:
        checkpoint(f" Agent 3 Tool: Execution failed with error: {e}")
        raise

    return " Agent 3 completed"


llm = LLM(
    model= "ollama/llama3.2:1b",
    base_url="http://localhost:11434"
)

# -------------------------------
# Define Agents
# -------------------------------
checkpoint("Defining agents...")

try:
    agent1 = Agent(
        role="Permutator",
        goal="Generate realistic variations of user identity data",
        backstory="An expert in LLMs and data anonymization.",
        tools=[agent1_tool],
        default_tool=agent1_tool,  # 🔧 Force tool execution
        allow_delegation=False,
        llm=llm,
        verbose=True
    )
    checkpoint(" Agent 1 defined.")
except Exception as e:
    checkpoint(f" Failed to define Agent 1: {e}")
    raise

try:
    agent2 = Agent(
        role="AML Web Investigator",
        goal="Search online platforms and extract suspicious content about users",
        backstory="A specialist in search and digital evidence collection.",
        tools=[agent2_tool],
        default_tool=agent2_tool,  # 🔧 Force tool execution
        allow_delegation=False,
        llm=llm,
        verbose=True
    )
    checkpoint(" Agent 2 defined.")
except Exception as e:
    checkpoint(f" Failed to define Agent 2: {e}")
    raise

try:
    agent3 = Agent(
        role="AML Summarizer",
        goal="Extract and summarize financial crime and fraud indicators",
        backstory="An LLM agent skilled at reviewing and summarizing large data dumps.",
        tools=[agent3_tool],
        default_tool=agent3_tool,  # 🔧 Force tool execution
         allow_delegation=False,
         llm=llm,
         verbose=True
    )
    checkpoint(" Agent 3 defined.")
except Exception as e:
    checkpoint(f"Failed to define Agent 3: {e}")
    raise


# -------------------------------
# Define Tasks
# -------------------------------
checkpoint("Defining tasks...")

try:
    task1 = Task(
        description="  you are an agent who use  the tool provided to you  Execute Agent ones  tool to generate 15 permuted user data entries and save as permuted_user_data27.json",

        expected_output=" the output of agent ones tool is a  JSON file named permuted_user_data27.json",
        agent=agent1,
          tool=agent1_tool, 
        force_tool=True 
    )
    checkpoint(" Task 1 defined.")
except Exception as e:
    checkpoint(f"Failed to define Task 1: {e}")
    raise

try:
    task2 = Task(
        description="you are an agent who use  the tool provided to you  for making  Google  search for AML-related results for each user and scrape the top 10 links.",
        expected_output=" agent2 tool must return a file output27.json with scraped content or error per link.",
        agent=agent2,
          tool=agent2_tool, 
        force_tool=True  
    )
    checkpoint(" Task 2 defined.")
except Exception as e:
    checkpoint(f"Failed to define Task 2: {e}")
    raise

try:
    task3 = Task(
        description="   you are an agent who use  the tool provided to you agent3 tool will Summarize the AML-related findings from the scraped web pages.",
        expected_output=" agent3 tool will return A summary.txt file with highlights of each relevant web page.",
        agent=agent3,
          tool=agent3_tool, 
        force_tool=True  
    )
    checkpoint(" Task 3 defined.")
except Exception as e:
    checkpoint(f"Failed to define Task 3: {e}")
    raise


# -------------------------------
# Run Crew Sequentially
# -------------------------------
checkpoint(" Assembling Crew...")

try:
    
    crew = Crew(
        agents=[agent1, agent2, agent3],
        tasks=[task1, task2, task3],
        process=Process.sequential,
        llm=llm,
        verbose=True,
        memory=False
    )
    checkpoint(" Crew assembled successfully.")
except Exception as e:
    checkpoint(f" Failed to assemble Crew: {e}")
    raise


# -------------------------------
# Launching Execution
# -------------------------------
# if __name__ == "__main__":
#     print("🔧 Testing tools directly...\n")

#     print(agent1_tool.run())  # Correct usage
#     print(agent2_tool.run())
#     print(agent3_tool.run())

#     print("\n✅ All tools executed directly.")


if __name__ == "__main__":
    checkpoint(" Launching full CrewAI pipeline...")
    try:
        result = crew.kickoff( inputs={"name" : " Vijay Mallaya " , "phone":"94748494"}) 
        checkpoint(" All agents completed!")
        print("\n Final Crew Result:", result)
    except Exception as e:
        checkpoint(f" Crew execution failed: {e}")
        raise


