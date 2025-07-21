
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff
from crew import LatestAiDevelopmentCrew
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()



def run():
    print("📝 Please enter the following user data:\n")

    user_data = {
        "name": input("Name: "),
        "phone": input("Phone number: "),
        "paytm_link": input("Paytm link: "),
        "country": input("Country: "),
        "age": input("Age: "),
        "email": input("Email: ")
    }

    while True:
        try:
            num_permutations = int(input("🔢 Number of permutations: "))
            break
        except ValueError:
            print("❌ Please enter a valid integer.")

    inputs = {
        "topic": "Anti Money Laundering",
        "user_data": user_data,
        "num_permutations": num_permutations
    }

    result = LatestAiDevelopmentCrew().crew().kickoff(inputs=inputs)

    print("\n✅ Final Result:")
    print(result)


if __name__ == "__main__":
    run()


