#!/usr/bin/env python3
"""
Comprehensive Analysis of Edge-IIoTset Dataset
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

def analyze_dataset_structure():
    """Analyze the overall dataset structure"""
    print("=" * 60)
    print("EDGE-IIOTSET DATASET STRUCTURE ANALYSIS")
    print("=" * 60)
    
    # Check file sizes and structure
    base_path = "Edge-IIoTset dataset"
    
    print("\n1. DATASET ORGANIZATION:")
    print("-" * 30)
    
    # Normal traffic analysis
    normal_path = os.path.join(base_path, "Normal traffic")
    normal_sensors = os.listdir(normal_path)
    print(f"Normal Traffic Sensors: {len(normal_sensors)}")
    for sensor in normal_sensors:
        sensor_path = os.path.join(normal_path, sensor)
        if os.path.isdir(sensor_path):
            files = os.listdir(sensor_path)
            csv_files = [f for f in files if f.endswith('.csv')]
            pcap_files = [f for f in files if f.endswith('.pcap')]
            print(f"  - {sensor}: {len(csv_files)} CSV, {len(pcap_files)} PCAP")
    
    # Attack traffic analysis
    attack_path = os.path.join(base_path, "Attack traffic")
    attack_files = os.listdir(attack_path)
    csv_attacks = [f for f in attack_files if f.endswith('.csv')]
    pcap_attacks = [f for f in attack_files if f.endswith('.pcap')]
    print(f"\nAttack Traffic: {len(csv_attacks)} CSV files, {len(pcap_attacks)} PCAP files")
    
    # ML datasets
    ml_path = os.path.join(base_path, "Selected dataset for ML and DL")
    ml_files = os.listdir(ml_path)
    print(f"\nML/DL Datasets: {len(ml_files)} files")
    for file in ml_files:
        file_path = os.path.join(ml_path, file)
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        print(f"  - {file}: {size_mb:.1f} MB")

def analyze_ml_datasets():
    """Analyze the preprocessed ML datasets"""
    print("\n" + "=" * 60)
    print("ML/DL DATASETS ANALYSIS")
    print("=" * 60)
    
    # Analyze ML dataset
    try:
        print("\n1. ML-EdgeIIoT-dataset.csv Analysis:")
        print("-" * 40)
        
        # Read sample to understand structure
        df_ml = pd.read_csv("Edge-IIoTset dataset/Selected dataset for ML and DL/ML-EdgeIIoT-dataset.csv", nrows=1000)
        
        print(f"Columns: {len(df_ml.columns)}")
        print(f"Sample rows: {len(df_ml)}")
        
        # Analyze attack types
        if 'Attack_type' in df_ml.columns:
            attack_counts = df_ml['Attack_type'].value_counts()
            print(f"\nAttack Types Distribution (sample):")
            for attack, count in attack_counts.items():
                print(f"  - {attack}: {count}")
        
        # Analyze data types
        print(f"\nData Types:")
        numeric_cols = df_ml.select_dtypes(include=[np.number]).columns
        categorical_cols = df_ml.select_dtypes(include=['object']).columns
        print(f"  - Numeric columns: {len(numeric_cols)}")
        print(f"  - Categorical columns: {len(categorical_cols)}")
        
        # Check for missing values
        missing_values = df_ml.isnull().sum()
        missing_cols = missing_values[missing_values > 0]
        print(f"\nMissing Values:")
        if len(missing_cols) > 0:
            for col, missing in missing_cols.items():
                print(f"  - {col}: {missing} ({missing/len(df_ml)*100:.1f}%)")
        else:
            print("  - No missing values in sample")
            
    except Exception as e:
        print(f"Error analyzing ML dataset: {e}")

def analyze_attack_types():
    """Analyze different attack types"""
    print("\n" + "=" * 60)
    print("ATTACK TYPES ANALYSIS")
    print("=" * 60)
    
    attack_path = "Edge-IIoTset dataset/Attack traffic"
    attack_files = [f for f in os.listdir(attack_path) if f.endswith('.csv')]
    
    print(f"\nFound {len(attack_files)} attack CSV files:")
    
    attack_stats = {}
    
    for attack_file in attack_files:
        try:
            attack_name = attack_file.replace('_attack.csv', '').replace('_', ' ')
            file_path = os.path.join(attack_path, attack_file)
            
            # Get file size
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            
            # Read sample to get row count
            df_sample = pd.read_csv(file_path, nrows=1000)
            total_rows = len(df_sample)
            
            attack_stats[attack_name] = {
                'file_size_mb': size_mb,
                'sample_rows': total_rows,
                'columns': len(df_sample.columns)
            }
            
            print(f"  - {attack_name}: {size_mb:.1f} MB, {total_rows} sample rows, {len(df_sample.columns)} columns")
            
        except Exception as e:
            print(f"  - {attack_file}: Error reading file - {e}")
    
    return attack_stats

def analyze_normal_traffic():
    """Analyze normal IoT sensor traffic"""
    print("\n" + "=" * 60)
    print("NORMAL TRAFFIC ANALYSIS")
    print("=" * 60)
    
    normal_path = "Edge-IIoTset dataset/Normal traffic"
    sensors = os.listdir(normal_path)
    
    sensor_stats = {}
    
    for sensor in sensors:
        sensor_path = os.path.join(normal_path, sensor)
        if os.path.isdir(sensor_path):
            csv_file = os.path.join(sensor_path, f"{sensor}.csv")
            if os.path.exists(csv_file):
                try:
                    # Get file size
                    size_mb = os.path.getsize(csv_file) / (1024 * 1024)
                    
                    # Read sample
                    df_sample = pd.read_csv(csv_file, nrows=1000)
                    
                    sensor_stats[sensor] = {
                        'file_size_mb': size_mb,
                        'sample_rows': len(df_sample),
                        'columns': len(df_sample.columns)
                    }
                    
                    print(f"  - {sensor}: {size_mb:.1f} MB, {len(df_sample)} sample rows, {len(df_sample.columns)} columns")
                    
                except Exception as e:
                    print(f"  - {sensor}: Error reading file - {e}")
    
    return sensor_stats

def analyze_data_quality():
    """Analyze data quality and characteristics"""
    print("\n" + "=" * 60)
    print("DATA QUALITY ANALYSIS")
    print("=" * 60)
    
    # Analyze a few sample files for data quality
    sample_files = [
        "Edge-IIoTset dataset/Attack traffic/MITM_attack.csv",
        "Edge-IIoTset dataset/Normal traffic/Temperature_and_Humidity/Temperature_and_Humidity.csv"
    ]
    
    for file_path in sample_files:
        if os.path.exists(file_path):
            try:
                print(f"\nAnalyzing: {os.path.basename(file_path)}")
                print("-" * 40)
                
                df = pd.read_csv(file_path, nrows=1000)
                
                print(f"Shape: {df.shape}")
                print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
                
                # Check for duplicates
                duplicates = df.duplicated().sum()
                print(f"Duplicate rows: {duplicates}")
                
                # Check data types
                print(f"Data types:")
                for dtype, count in df.dtypes.value_counts().items():
                    print(f"  - {dtype}: {count} columns")
                
                # Check for infinite values
                inf_cols = []
                for col in df.select_dtypes(include=[np.number]).columns:
                    if np.isinf(df[col]).any():
                        inf_cols.append(col)
                print(f"Columns with infinite values: {len(inf_cols)}")
                
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")

def generate_summary_report(attack_stats, sensor_stats):
    """Generate comprehensive summary report"""
    print("\n" + "=" * 60)
    print("COMPREHENSIVE SUMMARY REPORT")
    print("=" * 60)
    
    print("\n1. DATASET OVERVIEW:")
    print("-" * 20)
    print("• Dataset Name: Edge-IIoTset")
    print("• Purpose: IoT/IIoT Cybersecurity Dataset")
    print("• Format: CSV + PCAP files")
    print("• Use Cases: ML/DL for Intrusion Detection")
    
    print("\n2. DATA COMPOSITION:")
    print("-" * 20)
    print(f"• Normal Traffic Sensors: {len(sensor_stats)}")
    print(f"• Attack Types: {len(attack_stats)}")
    print("• Preprocessed ML Datasets: 2 (ML + DNN)")
    
    print("\n3. NORMAL TRAFFIC SENSORS:")
    print("-" * 30)
    for sensor, stats in sensor_stats.items():
        print(f"• {sensor}: {stats['file_size_mb']:.1f} MB, {stats['columns']} features")
    
    print("\n4. ATTACK TYPES:")
    print("-" * 15)
    for attack, stats in attack_stats.items():
        print(f"• {attack}: {stats['file_size_mb']:.1f} MB, {stats['columns']} features")
    
    print("\n5. DATASET STRENGTHS:")
    print("-" * 20)
    print("• Comprehensive coverage of IoT sensors")
    print("• Realistic attack scenarios")
    print("• Both raw and preprocessed data")
    print("• Multiple data formats (CSV + PCAP)")
    print("• Academic research ready")
    
    print("\n6. POTENTIAL USE CASES:")
    print("-" * 25)
    print("• Intrusion Detection System development")
    print("• Anomaly detection in IoT networks")
    print("• Federated learning experiments")
    print("• Network security research")
    print("• IoT device behavior analysis")
    
    print("\n7. RECOMMENDATIONS:")
    print("-" * 20)
    print("• Use preprocessed datasets for ML/DL experiments")
    print("• Combine normal and attack data for training")
    print("• Consider data imbalance between attack types")
    print("• Validate on real IoT environments")
    print("• Use PCAP files for network-level analysis")

if __name__ == "__main__":
    # Run comprehensive analysis
    analyze_dataset_structure()
    analyze_ml_datasets()
    attack_stats = analyze_attack_types()
    sensor_stats = analyze_normal_traffic()
    analyze_data_quality()
    generate_summary_report(attack_stats, sensor_stats)
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
