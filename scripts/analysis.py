import json
import pandas as pd
import argparse
import os

def analyze_one_concept(concept_path):
    # normal first 
    # Load results from json file
    fp = f"results/{concept_path}_normal.json"
    with open(fp, "r") as f:
        results = json.load(f)

    # Create dataframe from results
    df = pd.DataFrame()
    for file_name, result in results.items():
        row = {
            "file_name": file_name,
            "question": result["question"],
            "answer": result["answer"],
        }
        # Add token probabilities
        for token, prob in result["token_probs"].items():
            row[f"prob_{token}"] = prob
        
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    print(f"\nAnalyzing {fp}:")
    print(f"Total samples: {len(df)}")
    print("\nAnswer distribution:")
    print(df["answer"].value_counts())
    print("\nMean token probabilities:")
    prob_cols = [col for col in df.columns if col.startswith("prob_")]
    print(df[prob_cols].mean().sort_values(ascending=False))

    # Create bar plot of probabilities for A and B
    import matplotlib.pyplot as plt
    import numpy as np

    # Extract probabilities for A and B answers
    prob_A = df['prob_A'].fillna(0).values
    prob_B = df['prob_B'].fillna(0).values

    # Set up the plot
    plt.figure(figsize=(12, 6))
    
    # Calculate x positions for bars
    x = np.arange(len(df))  # Use unit spacing for clearer grouping
    width = 0.35  # Width of bars
    
    # Create bars side by side
    plt.bar(x - width/2, prob_A, width, label='Metric', color='skyblue')
    plt.bar(x + width/2, prob_B, width, label='Imperial', color='lightcoral')

    # Customize plot
    plt.xlabel('Sample')
    plt.ylabel('Probability')
    plt.title('Probability Distribution of Metric vs Imperial Answers')
    plt.legend()
    
    # Set x-ticks at each sample point with file names
    file_names = [os.path.splitext(name)[0] for name in df['file_name']]
    plt.xticks(x, file_names, rotation=45, ha='right')

    # Add grid for better readability
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Add value labels on top of each bar
    for i in range(len(df)):
        plt.text(i - width/2, prob_A[i], f'{prob_A[i]:.2f}', 
                ha='center', va='bottom')
        plt.text(i + width/2, prob_B[i], f'{prob_B[i]:.2f}',
                ha='center', va='bottom')

    # Set y-axis limits to ensure labels are visible
    plt.ylim(0, 1.2)

    # Adjust layout and display
    plt.tight_layout()
    
    # Save plot
    save_dir = "figures"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    plt.savefig(f"{save_dir}/{concept_path}_probs_normal.png")
    plt.close()

    print(f"\nProbability plot saved as {save_dir}/{concept_path}_probs_normal.png")

    fp = f"results/{concept_path}_flip.json"
    with open(fp, "r") as f:
        results_flip = json.load(f)

    df_flip = pd.DataFrame()
    for file_name, result in results_flip.items():
        row = {
            "file_name": file_name,
            "question": result["question"],
            "answer": result["answer"],
        }
        # Add token probabilities
        for token, prob in result["token_probs"].items():
            row[f"prob_{token}"] = prob
        
        df_flip = pd.concat([df_flip, pd.DataFrame([row])], ignore_index=True)

    # Create bar plot for flipped results
    plt.figure(figsize=(12, 6))
    
    # Get probabilities for A and B answers
    prob_A = []
    prob_B = []
    
    for _, row in df_flip.iterrows():
        # Get all probability columns
        prob_cols = [col for col in row.index if col.startswith('prob_')]
        # Sort by probability value in descending order
        probs = sorted([(col, row[col]) for col in prob_cols], key=lambda x: x[1], reverse=True)
        # Take top two probabilities
        prob_A.append(probs[0][1])
        prob_B.append(probs[1][1])

    x = np.arange(len(df_flip))
    width = 0.35

    plt.bar(x - width/2, prob_A, width, label='Imperial', color='lightcoral')
    plt.bar(x + width/2, prob_B, width, label='Metric', color='skyblue')

    plt.xlabel('Sample')
    plt.ylabel('Probability')
    plt.title('Probability Distribution of Metric vs Imperial Answers (Flipped)')
    plt.legend()
    
    # Set x-ticks at each sample point with file names
    file_names = [os.path.splitext(name)[0] for name in df_flip['file_name']]
    plt.xticks(x, file_names, rotation=45, ha='right')

    # Add grid for better readability
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Add value labels on top of each bar
    for i in range(len(df_flip)):
        plt.text(i - width/2, prob_A[i], f'{prob_A[i]:.2f}', 
                ha='center', va='bottom')
        plt.text(i + width/2, prob_B[i], f'{prob_B[i]:.2f}',
                ha='center', va='bottom')

    # Set y-axis limits to ensure labels are visible
    plt.ylim(0, 1.2)

    # Adjust layout and display
    plt.tight_layout()
    
    # Save plot
    plt.savefig(f"{save_dir}/{concept_path}_probs_flip.png")
    plt.close()

    print(f"Flipped probability plot saved as {save_dir}/{concept_path}_probs_flip.png")

    




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    concept_paths = {
        "time_googlegen": "assets/1_time/googlegen",
        "time_camera": "assets/1_time/camera",
        "quantifiers_battery": "assets/2_quantifiers/battery",
        "quantifiers_eggs": "assets/2_quantifiers/eggs", 
        "temperature_googlegen": "assets/4_1_temperature/googlegen",
        "temperature_camera": "assets/4_1_temperature/camera",
        "distance": "assets/4_2_distance",
        "speed": "assets/4_3_speed",
        "size": "assets/4_4_size",
        "price": "assets/4_5_price"
    }

    binary_concepts = ["temperature_googlegen", "temperature_camera", "distance", "speed", "size", "price"]

    parser.add_argument("--concept", type=str, default="size")

    parser.add_argument("--eval_type", type=str, default="loc_thailand")
    

    args = parser.parse_args()

    analyze_one_concept(args.concept)

