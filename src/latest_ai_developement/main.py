#!/usr/bin/env python
from crew import LatestAiDevelopmentCrew

def run():
    inputs = {
        "topic": "Anti Money Laundering",
        "user_data": {
            "name": "Vijay",
            "phone": "1234567890",
            "paytm_link": "paytm.me/xyz",
            "country": "India",
            "age": "35",
            "email": "vijay@example.com"
        },
        "num_permutations": 5
    }
    result = LatestAiDevelopmentCrew().crew().kickoff(inputs=inputs)
    print("\\n✅ Final Result:")
    print(result)

if __name__ == "__main__":
    run()


