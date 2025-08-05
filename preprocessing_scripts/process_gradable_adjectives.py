import json
from collections import defaultdict
import os
import pandas as pd

if __name__ == "__main__":
    with open("unified/raw_data/gradable_adjective.tsv", "r") as f:
        df = pd.read_csv(f, sep='\t')
        print(df)
    
        # Add Scale ID column starting from 1
        # Get unique scales and create mapping
        unique_scales = df['Scale'].unique()
        scale_to_id = {scale: i+1 for i, scale in enumerate(unique_scales)}
        
        # Add Scale ID column based on unique scales
        df.insert(0, 'Scale ID', df['Scale'].map(scale_to_id))

        # Save to CSV
        df.to_csv('unified/gradable_adjectives.csv', index=True)
        print('saved into gradable_adjectives.csv')
