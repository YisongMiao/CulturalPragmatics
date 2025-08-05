import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import tempfile

def read_csv_safely(file_path):
    """Read CSV file with proper encoding handling"""
    # Try common encodings in order of likelihood
    encodings_to_try = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252', 'utf-8-sig']
    
    for encoding in encodings_to_try:
        try:
            df = pd.read_csv(file_path, encoding=encoding, quotechar='"', escapechar='\\')
            print(f"Successfully read with encoding: {encoding}")
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error with {encoding}: {e}")
            continue
    
    raise ValueError(f"Could not read {file_path} with any of the attempted encodings")

def read_chinese_csv_robust(file_path):
    """Read Chinese CSV file with robust encoding handling for mixed/corrupted files"""
    print(f"Reading Chinese file: {file_path}")
    
    # First try the simple approach with gbk
    try:
        df = pd.read_csv(file_path, encoding='gbk', quotechar='"', escapechar='\\', on_bad_lines='skip')
        print(f"Successfully read with gbk encoding (skipping bad lines)")
        return df
    except Exception as e:
        print(f"Failed with gbk: {e}")
    
    # Try reading line by line and reconstructing for corrupted files
    try:
        lines = []
        with open(file_path, 'rb') as f:
            for i, line in enumerate(f):
                try:
                    decoded_line = line.decode('gbk')
                    lines.append(decoded_line)
                except UnicodeDecodeError:
                    try:
                        decoded_line = line.decode('latin-1')
                        lines.append(decoded_line)
                    except:
                        print(f"Skipping corrupted line {i+1}")
                        continue
        
        # Reconstruct the CSV
        content = ''.join(lines)
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.csv', delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        
        df = pd.read_csv(tmp_path, encoding='utf-8', quotechar='"', escapechar='\\')
        os.unlink(tmp_path)
        print(f"Successfully read with line-by-line reconstruction")
        return df
    except Exception as e:
        print(f"Failed with line-by-line reconstruction: {e}")
    
    # Fall back to the general method
    return read_csv_safely(file_path)

def analyze_data(df):
    """Analyze the Target and Source columns"""
    print(f"\nDataset Overview:")
    print(f"Total samples: {len(df)}")
    
    # Analyze Target column
    print(f"\nTarget Analysis:")
    target_counts = df['Target'].value_counts()
    print(f"Number of unique targets: {df['Target'].nunique()}")
    print(f"Top 5 most common targets:")
    print(target_counts.head())
    print(f"Percentage with target: {(df['Target'].notna().sum() / len(df)) * 100:.1f}%")
    
    # Analyze Source column  
    print(f"\nSource Analysis:")
    source_counts = df['Source'].value_counts()
    print(f"Number of unique sources: {df['Source'].nunique()}")
    print(f"Top 5 most common sources:")
    print(source_counts.head())
    print(f"Percentage with source: {(df['Source'].notna().sum() / len(df)) * 100:.1f}%")
    
    # Analyze Target-Source pairs
    print(f"\nTarget-Source Pair Analysis:")
    pair_counts = df.groupby(['Target', 'Source']).size().sort_values(ascending=False)
    print(f"Number of unique target-source pairs: {len(pair_counts)}")
    print(f"Top 5 most common target-source pairs:")
    print(pair_counts.head())

if __name__ == "__main__":
    fp_test = 'MultiMM/data/EN_test.csv'
    fp_train = 'MultiMM/data/EN_train.csv'
    fp_val = 'MultiMM/data/EN_val.csv'
    
    # Check if all files exist
    for fp in [fp_train, fp_val]:
        if not os.path.exists(fp):
            print(f"File not found: {fp}")
            exit(1)
    
    # Read all files into one dataframe
    try:
        # df_test = read_csv_safely(fp_test)
        df_train = read_csv_safely(fp_train) 
        df_val = read_csv_safely(fp_val)
        
        # Combine into one dataframe
        df = pd.concat([df_train, df_val], ignore_index=True)
        print(f"\nCombined {len(df_train)} train, and {len(df_val)} validation samples")
        print(f"Total samples: {len(df)}")
        
    except Exception as e:
        print(f"Failed to read files: {e}")

    # Analyze metaphor occurrence distribution
    print("\nMetaphor Occurrence Analysis:")
    metaphor_counts = df['MetaphorOccurrence'].value_counts()
    print("Distribution of metaphor occurrences:")
    print(metaphor_counts)
    
    # Separate into metaphorical and non-metaphorical
    metaphorical = df[df['MetaphorOccurrence'] == 1]
    non_metaphorical = df[df['MetaphorOccurrence'] == 0]
    
    print(f"\nMetaphorical examples: {len(metaphorical)} ({len(metaphorical)/len(df)*100:.1f}%)")
    print(f"Non-metaphorical examples: {len(non_metaphorical)} ({len(non_metaphorical)/len(df)*100:.1f}%)")

    # Analyze metaphorical examples
    print("\n========== Analysis of Metaphorical Examples:")
    print("Target Analysis:")
    target_counts_metaphor = metaphorical['Target'].value_counts()
    print(f"Number of unique targets: {metaphorical['Target'].nunique()}")
    print(f"Top 5 most common targets:")
    print(target_counts_metaphor.head())
    print(f"Percentage with target: {(metaphorical['Target'].notna().sum() / len(metaphorical)) * 100:.1f}%")

    print("\nSource Analysis:")
    source_counts_metaphor = metaphorical['Source'].value_counts() 
    print(f"Number of unique sources: {metaphorical['Source'].nunique()}")
    print(f"Top 5 most common sources:")
    print(source_counts_metaphor.head())
    print(f"Percentage with source: {(metaphorical['Source'].notna().sum() / len(metaphorical)) * 100:.1f}%")

    print("\nTarget-Source Pair Analysis:")
    pair_counts_metaphor = metaphorical.groupby(['Target', 'Source']).size().sort_values(ascending=False)
    print(f"Number of unique target-source pairs: {len(pair_counts_metaphor)}")
    print(f"Top 5 most common target-source pairs:")
    print(pair_counts_metaphor.head())

    # Now analyze Chinese datasets
    print("\n========== Analysis of Chinese Datasets ==========")
    
    try:
        # Read Chinese datasets
        df_train_cn = read_chinese_csv_robust(fp_train.replace('EN', 'CN'))
        df_val_cn = read_chinese_csv_robust(fp_val.replace('EN', 'CN'))
        
        # Combine into one dataframe
        df_cn = pd.concat([df_train_cn, df_val_cn], ignore_index=True)
        print(f"\nCombined {len(df_train_cn)} train, and {len(df_val_cn)} validation samples")
        print(f"Total samples: {len(df_cn)}")
        
        # Test: Save a sample of Chinese text to verify encoding
        print("\nTesting Chinese character display:")
        sample_texts = df_cn['Text'].dropna().head(3).tolist()
        for i, text in enumerate(sample_texts):
            print(f"Sample {i+1}: {text[:50]}...")
        
        # Save sample to file to verify encoding
        with open('MultiMM/chinese_sample.txt', 'w', encoding='utf-8') as f:
            f.write("Chinese Sample Texts:\n")
            for i, text in enumerate(sample_texts):
                f.write(f"Sample {i+1}: {text}\n")
        print("Chinese sample saved to 'MultiMM/chinese_sample.txt'")
        
    except Exception as e:
        print(f"Failed to read Chinese files: {e}")
        
    # Analyze metaphor occurrence distribution
    print("\nMetaphor Occurrence Analysis:")
    metaphor_counts_cn = df_cn['MetaphorOccurrence'].value_counts()
    print("Distribution of metaphor occurrences:")
    print(metaphor_counts_cn)
    
    # Separate into metaphorical and non-metaphorical
    metaphorical_cn = df_cn[df_cn['MetaphorOccurrence'] == 1]
    non_metaphorical_cn = df_cn[df_cn['MetaphorOccurrence'] == 0]
    
    print(f"\nMetaphorical examples: {len(metaphorical_cn)} ({len(metaphorical_cn)/len(df_cn)*100:.1f}%)")
    print(f"Non-metaphorical examples: {len(non_metaphorical_cn)} ({len(non_metaphorical_cn)/len(df_cn)*100:.1f}%)")

    # Analyze metaphorical examples
    print("\n========== Analysis of Chinese Metaphorical Examples:")
    print("Target Analysis:")
    target_counts_metaphor_cn = metaphorical_cn['Target'].value_counts()
    print(f"Number of unique targets: {metaphorical_cn['Target'].nunique()}")
    print(f"Top 5 most common targets:")
    print(target_counts_metaphor_cn.head())
    print(f"Percentage with target: {(metaphorical_cn['Target'].notna().sum() / len(metaphorical_cn)) * 100:.1f}%")

    print("\nSource Analysis:")
    source_counts_metaphor_cn = metaphorical_cn['Source'].value_counts()
    print(f"Number of unique sources: {metaphorical_cn['Source'].nunique()}")
    print(f"Top 5 most common sources:")
    print(source_counts_metaphor_cn.head())
    print(f"Percentage with source: {(metaphorical_cn['Source'].notna().sum() / len(metaphorical_cn)) * 100:.1f}%")

    print("\nTarget-Source Pair Analysis:")
    pair_counts_metaphor_cn = metaphorical_cn.groupby(['Target', 'Source']).size().sort_values(ascending=False)
    print(f"Number of unique target-source pairs: {len(pair_counts_metaphor_cn)}")
    print(f"Top 5 most common target-source pairs:")
    print(pair_counts_metaphor_cn.head())