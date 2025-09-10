import pandas as pd
import numpy as np
import os

# Load the ML dataset
print("Loading ML dataset...")
df = pd.read_csv("Edge-IIoTset dataset/Selected dataset for ML and DL/ML-EdgeIIoT-dataset.csv")

print("=" * 80)
print("COMPREHENSIVE EDGE-IIOTSET DATASET ANALYSIS")
print("=" * 80)

# Basic Statistics
print(f"\n1. DATASET OVERVIEW")
print("-" * 50)
print(f"• Total Records: {len(df):,}")
print(f"• Total Features: {len(df.columns)}")
print(f"• Memory Usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")

# Attack Distribution
print(f"\n2. ATTACK TYPE DISTRIBUTION")
print("-" * 50)
attack_dist = df['Attack_type'].value_counts()
for attack, count in attack_dist.items():
    percentage = (count / len(df)) * 100
    print(f"• {attack}: {count:,} ({percentage:.1f}%)")

# Label Distribution
print(f"\n3. ATTACK LABEL DISTRIBUTION")
print("-" * 50)
label_dist = df['Attack_label'].value_counts()
for label, count in label_dist.items():
    percentage = (count / len(df)) * 100
    label_name = "Attack" if label == 1 else "Normal"
    print(f"• {label_name} (Label {label}): {count:,} ({percentage:.1f}%)")

# Data Quality
print(f"\n4. DATA QUALITY")
print("-" * 50)
print(f"• Missing values: {df.isnull().sum().sum()}")
print(f"• Duplicate rows: {df.duplicated().sum()}")

# Feature Analysis
numeric_cols = df.select_dtypes(include=[np.number]).columns
categorical_cols = df.select_dtypes(include=['object']).columns
print(f"• Numeric features: {len(numeric_cols)}")
print(f"• Categorical features: {len(categorical_cols)}")

# Attack Categories
print(f"\n5. ATTACK CATEGORIES")
print("-" * 50)
ddos_attacks = ['DDoS_UDP', 'DDoS_ICMP', 'DDoS_TCP']
web_attacks = ['XSS', 'SQL_injection', 'Password']
network_attacks = ['MITM', 'Port_Scanning', 'Fingerprinting']
malware_attacks = ['Ransomware', 'Backdoor']
recon_attacks = ['Vulnerability_scanner']

categories = {
    'DDoS Attacks': ddos_attacks,
    'Web Attacks': web_attacks,
    'Network Attacks': network_attacks,
    'Malware': malware_attacks,
    'Reconnaissance': recon_attacks
}

for category, attacks in categories.items():
    total_count = sum(attack_dist.get(attack, 0) for attack in attacks)
    percentage = (total_count / len(df)) * 100
    print(f"• {category}: {total_count:,} ({percentage:.1f}%)")

# Dataset Characteristics
print(f"\n6. DATASET CHARACTERISTICS")
print("-" * 50)
print("• Strengths:")
print("  - Comprehensive IoT sensor coverage")
print("  - Realistic attack scenarios")
print("  - Large dataset size")
print("  - Multiple data formats")
print("  - Academic research ready")

# Class Imbalance
normal_count = label_dist.get(0, 0)
attack_count = label_dist.get(1, 0)
imbalance_ratio = attack_count / normal_count if normal_count > 0 else 0
print(f"\n• Class Imbalance:")
print(f"  - Attack:Normal ratio = {imbalance_ratio:.2f}:1")
print(f"  - Normal: {normal_count:,} ({normal_count/len(df)*100:.1f}%)")
print(f"  - Attack: {attack_count:,} ({attack_count/len(df)*100:.1f}%)")

# Use Cases
print(f"\n7. RECOMMENDED USE CASES")
print("-" * 50)
print("• Intrusion Detection Systems")
print("• Anomaly Detection")
print("• Federated Learning")
print("• Network Security Research")
print("• IoT Behavior Analysis")
print("• ML/DL Model Training")

# Technical Recommendations
print(f"\n8. TECHNICAL RECOMMENDATIONS")
print("-" * 50)
print("• Handle mixed data types")
print("• Use stratified sampling")
print("• Consider class imbalance")
print("• Implement proper validation")
print("• Feature engineering needed")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
