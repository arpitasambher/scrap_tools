import json
import os

def generate_permutations(user_data, num):
    """Generate mock permutations for testing."""
    permutations = []
    for i in range(num):
        new_data = user_data.copy()
        new_data["name"] = f"{user_data['name']}_{i}"
        new_data["phone"] = user_data["phone"][:-1] + str(i)
        permutations.append(new_data)

    os.makedirs("output", exist_ok=True)
    with open("output/permuted_user_data.json", "w") as f:
        json.dump(permutations, f, indent=2)
    print(f"[UTIL] ✅ Saved {len(permutations)} permutations")
    return permutations
