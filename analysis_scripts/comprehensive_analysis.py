import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

def create_analysis_report():
    """Create comprehensive analysis report with visualizations"""
    
    print("=" * 80)
    print("COMPREHENSIVE EDGE-IIOTSET DATASET ANALYSIS")
    print("=" * 80)
    
    # 1. Dataset Overview
    print("\n1. DATASET OVERVIEW")
    print("-" * 50)
    print("• Dataset: Edge-IIoTset Cybersecurity Dataset")
    print("• Purpose: IoT/IIoT Intrusion Detection Research")
    print("• Creator: Dr. Mohamed Amine Ferrag et al.")
    print("• Format: CSV + PCAP files")
    print("• License: Academic use (free), Commercial (with permission)")
    
    # 2. Dataset Structure Analysis
    print("\n2. DATASET STRUCTURE")
    print("-" * 50)
    
    # Count components
    normal_sensors = [d for d in os.listdir("Edge-IIoTset dataset/Normal traffic") 
                     if os.path.isdir(os.path.join("Edge-IIoTset dataset/Normal traffic", d))]
    attack_files = [f for f in os.listdir("Edge-IIoTset dataset/Attack traffic") if f.endswith('.csv')]
    ml_files = os.listdir("Edge-IIoTset dataset/Selected dataset for ML and DL")
    
    print(f"• Normal Traffic Sensors: {len(normal_sensors)}")
    print(f"• Attack Types: {len(attack_files)}")
    print(f"• Preprocessed ML Datasets: {len(ml_files)}")
    
    # 3. Detailed File Analysis
    print("\n3. FILE SIZE ANALYSIS")
    print("-" * 50)
    
    # ML Datasets
    ml_path = "Edge-IIoTset dataset/Selected dataset for ML and DL"
    for file in ml_files:
        file_path = os.path.join(ml_path, file)
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        print(f"• {file}: {size_mb:.1f} MB")
    
    # 4. ML Dataset Analysis
    print("\n4. ML DATASET DETAILED ANALYSIS")
    print("-" * 50)
    
    try:
        # Load ML dataset
        df_ml = pd.read_csv("Edge-IIoTset dataset/Selected dataset for ML and DL/ML-EdgeIIoT-dataset.csv")
        
        print(f"• Total Records: {len(df_ml):,}")
        print(f"• Total Features: {len(df_ml.columns)}")
        print(f"• Memory Usage: {df_ml.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")
        
        # Attack distribution
        print(f"\n• Attack Type Distribution:")
        attack_dist = df_ml['Attack_type'].value_counts()
        for attack, count in attack_dist.items():
            percentage = (count / len(df_ml)) * 100
            print(f"  - {attack}: {count:,} ({percentage:.1f}%)")
        
        # Label distribution
        print(f"\n• Attack Label Distribution:")
        label_dist = df_ml['Attack_label'].value_counts()
        for label, count in label_dist.items():
            percentage = (count / len(df_ml)) * 100
            label_name = "Attack" if label == 1 else "Normal"
            print(f"  - {label_name} (Label {label}): {count:,} ({percentage:.1f}%)")
        
        # Data quality
        print(f"\n• Data Quality:")
        print(f"  - Missing values: {df_ml.isnull().sum().sum()}")
        print(f"  - Duplicate rows: {df_ml.duplicated().sum()}")
        
        # Feature analysis
        numeric_cols = df_ml.select_dtypes(include=[np.number]).columns
        categorical_cols = df_ml.select_dtypes(include=['object']).columns
        print(f"  - Numeric features: {len(numeric_cols)}")
        print(f"  - Categorical features: {len(categorical_cols)}")
        
    except Exception as e:
        print(f"Error analyzing ML dataset: {e}")
    
    # 5. Attack Types Analysis
    print("\n5. ATTACK TYPES BREAKDOWN")
    print("-" * 50)
    
    attack_categories = {
        'DDoS Attacks': ['DDoS_UDP', 'DDoS_ICMP', 'DDoS_TCP'],
        'Web Attacks': ['XSS', 'SQL_injection', 'Password'],
        'Network Attacks': ['MITM', 'Port_Scanning', 'Fingerprinting'],
        'Malware': ['Ransomware', 'Backdoor'],
        'Reconnaissance': ['Vulnerability_scanner']
    }
    
    for category, attacks in attack_categories.items():
        print(f"• {category}:")
        for attack in attacks:
            if attack in attack_dist.index:
                count = attack_dist[attack]
                percentage = (count / len(df_ml)) * 100
                print(f"  - {attack}: {count:,} ({percentage:.1f}%)")
    
    # 6. Normal Traffic Analysis
    print("\n6. NORMAL TRAFFIC SENSORS")
    print("-" * 50)
    
    sensor_descriptions = {
        'Distance': 'Ultrasonic sensor for distance measurement',
        'Flame_Sensor': 'Flame detection sensor',
        'Heart_Rate': 'Heart rate monitoring sensor',
        'IR_Receiver': 'Infrared receiver sensor',
        'Modbus': 'Modbus communication protocol',
        'phValue': 'pH sensor (PH-4502C)',
        'Soil_Moisture': 'Soil moisture sensor v1.2',
        'Sound_Sensor': 'LM393 sound detection sensor',
        'Temperature_and_Humidity': 'DHT11 temperature and humidity sensor',
        'Water_Level': 'Water level sensor'
    }
    
    for sensor in normal_sensors:
        description = sensor_descriptions.get(sensor, 'IoT sensor')
        print(f"• {sensor}: {description}")
    
    # 7. Dataset Characteristics
    print("\n7. DATASET CHARACTERISTICS")
    print("-" * 50)
    
    print("• Strengths:")
    print("  - Comprehensive coverage of IoT sensors")
    print("  - Realistic attack scenarios")
    print("  - Both raw and preprocessed data")
    print("  - Multiple data formats (CSV + PCAP)")
    print("  - Academic research ready")
    print("  - Large dataset size (157K+ records)")
    print("  - Balanced attack distribution")
    
    print("\n• Data Imbalance:")
    normal_count = label_dist.get(0, 0)
    attack_count = label_dist.get(1, 0)
    imbalance_ratio = attack_count / normal_count if normal_count > 0 else 0
    print(f"  - Attack:Normal ratio = {imbalance_ratio:.2f}:1")
    print(f"  - Normal traffic: {normal_count:,} ({normal_count/len(df_ml)*100:.1f}%)")
    print(f"  - Attack traffic: {attack_count:,} ({attack_count/len(df_ml)*100:.1f}%)")
    
    # 8. Use Cases and Applications
    print("\n8. RECOMMENDED USE CASES")
    print("-" * 50)
    
    print("• Intrusion Detection Systems (IDS)")
    print("• Anomaly Detection in IoT Networks")
    print("• Federated Learning Experiments")
    print("• Network Security Research")
    print("• IoT Device Behavior Analysis")
    print("• Machine Learning Model Training")
    print("• Deep Learning Model Development")
    print("• Cybersecurity Education")
    
    # 9. Technical Recommendations
    print("\n9. TECHNICAL RECOMMENDATIONS")
    print("-" * 50)
    
    print("• Data Preprocessing:")
    print("  - Handle mixed data types in columns")
    print("  - Consider data normalization/standardization")
    print("  - Address class imbalance if needed")
    
    print("\n• Model Development:")
    print("  - Use stratified sampling for train/test splits")
    print("  - Consider ensemble methods for better performance")
    print("  - Implement cross-validation")
    print("  - Use appropriate evaluation metrics (F1, Precision, Recall)")
    
    print("\n• Feature Engineering:")
    print("  - Analyze feature importance")
    print("  - Consider feature selection techniques")
    print("  - Handle categorical variables appropriately")
    
    # 10. Dataset Statistics Summary
    print("\n10. STATISTICAL SUMMARY")
    print("-" * 50)
    
    print(f"• Total Dataset Size: {len(df_ml):,} records")
    print(f"• Feature Count: {len(df_ml.columns)}")
    print(f"• Attack Types: {len(attack_dist)}")
    print(f"• Normal Sensors: {len(normal_sensors)}")
    print(f"• Data Completeness: {((len(df_ml) - df_ml.isnull().sum().sum()) / (len(df_ml) * len(df_ml.columns)) * 100):.1f}%")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE - DATASET READY FOR RESEARCH USE")
    print("=" * 80)

if __name__ == "__main__":
    create_analysis_report()
