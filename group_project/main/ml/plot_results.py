import pandas as pd
import matplotlib.pyplot as plt

# Load model results
results = pd.read_csv("model_results.csv")

# Create bar chart
plt.figure(figsize=(8, 5))

plt.bar(results["Model"], results["Accuracy"])

plt.title("Comparison of Machine Learning Models")

plt.xlabel("Models")

plt.ylabel("Accuracy (%)")

plt.ylim(0, 100)

# Display values above bars
for i, value in enumerate(results["Accuracy"]):
    plt.text(i, value + 1, f"{value:.2f}%", ha="center")

plt.tight_layout()

# Save graph
plt.savefig("model_accuracy.png", dpi=300)

print("Graph saved successfully!")