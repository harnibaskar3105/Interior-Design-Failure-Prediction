import pandas as pd
import random

# Define options
budgets = [50000, 100000, 150000, 200000, 250000, 300000, 400000, 500000, 600000, 700000, 800000, 900000]
room_sizes = ["small", "medium", "large"]
materials = ["Wood", "PVC", "Marble"]
lightings = ["low", "medium", "high"]

data = []

# Function to determine failure logically
def determine_failure(budget, room, material, lighting):
    # Low budget + marble → HIGH RISK
    if budget <= 200000 and material == "Marble":
        return 1
    # Very low budget + any large room → HIGH RISK
    if budget <= 150000 and room == "large":
        return 1
    # Low budget + high lighting → HIGH RISK
    if budget <= 150000 and lighting == "high":
        return 1
    # Medium budget + small/medium room → LOW RISK
    if budget >= 300000 and material != "PVC":
        return 0
    # Otherwise, default
    return 0

# Generate dataset
for i in range(200):
    budget = random.choice(budgets)
    room = random.choice(room_sizes)
    material = random.choice(materials)
    lighting = random.choice(lightings)
    failure = determine_failure(budget, room, material, lighting)
    data.append([budget, room, material, lighting, failure])

# Create DataFrame
df = pd.DataFrame(data, columns=["budget", "room_size", "material", "lighting", "failure"])

# Save to CSV
df.to_csv("interior_design_fixed.csv", index=False)

print("✅ Dataset generated: interior_design_fixed.csv")
print(df.head(20))
