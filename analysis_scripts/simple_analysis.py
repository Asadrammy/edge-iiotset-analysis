import pandas as pd
import numpy as np
import os

print("=" * 60)
print("EDGE-IIOTSET DATASET ANALYSIS")
print("=" * 60)

# 1. Dataset Structure
print("\n1. DATASET STRUCTURE:")
print("-" * 20)

base_path = "Edge-IIoTset dataset"
normal_path = os.path.join(base_path, "Normal traffic")
attack_path = os.path.join(base_path, "Attack traffic")
ml_path = os.path.join(base_path, "Selected dataset for ML and DL")

# Count files
normal_sensors = [d for d in os.listdir(normal_path) if os.path.isdir(os.path.join(normal_path, d))]
attack_files = [f for f in os.listdir(attack_path) if f.endswith('.csv')]
ml_files = os.listdir(ml_path)

print(f"Normal Traffic Sensors: {len(normal_sensors)}")
print(f"Attack Types: {len(attack_files)}")
print(f"ML/DL Datasets: {len(ml_files)}")

# 2. File Sizes
print("\n2. FILE SIZES:")
print("-" * 15)

# ML datasets
for file in ml_files:
    file_path = os.path.join(ml_path, file)
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    print(f"{file}: {size_mb:.1f} MB")

# 3. Sample Data Analysis
print("\n3. SAMPLE DATA ANALYSIS:")
print("-" * 25)

# Analyze ML dataset
try:
    print("\nML-EdgeIIoT-dataset.csv:")
    df_ml = pd.read_csv(os.path.join(ml_path, "ML-EdgeIIoT-dataset.csv"), nrows=1000)
    print(f"  Columns: {len(df_ml.columns)}")
    print(f"  Sample rows: {len(df_ml)}")
    
    if 'Attack_type' in df_ml.columns:
        attack_counts = df_ml['Attack_type'].value_counts()
        print(f"  Attack types in sample:")
        for attack, count in attack_counts.items():
            print(f"    - {attack}: {count}")
    
    # Data types
    numeric_cols = df_ml.select_dtypes(include=[np.number]).columns
    categorical_cols = df_ml.select_dtypes(include=['object']).columns
    print(f"  Numeric columns: {len(numeric_cols)}")
    print(f"  Categorical columns: {len(categorical_cols)}")
    
except Exception as e:
    print(f"Error reading ML dataset: {e}")

# 4. Attack Types Analysis
print("\n4. ATTACK TYPES:")
print("-" * 15)

for attack_file in attack_files[:5]:  # Analyze first 5 attacks
    try:
        attack_name = attack_file.replace('_attack.csv', '').replace('_', ' ')
        file_path = os.path.join(attack_path, attack_file)
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        
        df_sample = pd.read_csv(file_path, nrows=100)
        print(f"  {attack_name}: {size_mb:.1f} MB, {len(df_sample)} sample rows")
        
    except Exception as e:
        print(f"  {attack_file}: Error - {e}")

# 5. Normal Traffic Analysis
print("\n5. NORMAL TRAFFIC SENSORS:")
print("-" * 30)

for sensor in normal_sensors[:5]:  # Analyze first 5 sensors
    try:
        csv_file = os.path.join(normal_path, sensor, f"{sensor}.csv")
        if os.path.exists(csv_file):
            size_mb = os.path.getsize(csv_file) / (1024 * 1024)
            df_sample = pd.read_csv(csv_file, nrows=100)
            print(f"  {sensor}: {size_mb:.1f} MB, {len(df_sample)} sample rows")
        else:
            print(f"  {sensor}: CSV file not found")
    except Exception as e:
        print(f"  {sensor}: Error - {e}")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
