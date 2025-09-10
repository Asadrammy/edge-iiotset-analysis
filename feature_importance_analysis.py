#!/usr/bin/env python3
"""
Feature Importance Analysis for Edge-IIoTset Dataset
Identifying Important Columns for Threat Identification
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings('ignore')

def analyze_feature_importance():
    """Analyze feature importance for threat identification"""
    
    print("🔍 Loading Edge-IIoTset Dataset for Feature Analysis...")
    
    # Load dataset
    df = pd.read_csv("Edge-IIoTset dataset/Selected dataset for ML and DL/ML-EdgeIIoT-dataset.csv")
    
    print(f"✅ Dataset loaded: {len(df):,} records, {len(df.columns)} features")
    
    # Basic dataset info
    print(f"\n📊 Dataset Overview:")
    print(f"  - Total Records: {len(df):,}")
    print(f"  - Total Features: {len(df.columns)}")
    print(f"  - Target Classes: {df['Attack_type'].nunique()}")
    print(f"  - Class Distribution:")
    for attack_type, count in df['Attack_type'].value_counts().head(10).items():
        print(f"    • {attack_type}: {count:,} ({count/len(df)*100:.1f}%)")
    
    # Separate features and target
    target_column = 'Attack_type'
    feature_columns = [col for col in df.columns if col not in [target_column, 'Attack_label']]
    
    print(f"\n🎯 Target Variable: {target_column}")
    print(f"🔧 Feature Variables: {len(feature_columns)}")
    
    # Data preprocessing
    print(f"\n🔄 Preprocessing Data...")
    
    # Handle mixed data types
    df_processed = df.copy()
    
    # Convert mixed type columns to numeric where possible
    for col in feature_columns:
        if df_processed[col].dtype == 'object':
            # Try to convert to numeric
            df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
    
    # Fill missing values
    df_processed = df_processed.fillna(0)
    
    # Prepare features and target
    X = df_processed[feature_columns]
    y = df_processed[target_column]
    
    # Encode target variable
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    print(f"✅ Data preprocessed successfully")
    print(f"  - Features shape: {X.shape}")
    print(f"  - Target shape: {y_encoded.shape}")
    
    # Feature Selection Analysis
    print(f"\n📈 Performing Feature Importance Analysis...")
    
    # 1. Random Forest Feature Importance
    print(f"\n1️⃣ Random Forest Feature Importance:")
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X, y_encoded)
    
    # Get feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': rf.feature_importance_
    }).sort_values('importance', ascending=False)
    
    print(f"   Top 20 Most Important Features:")
    for i, (_, row) in enumerate(feature_importance.head(20).iterrows(), 1):
        print(f"   {i:2d}. {row['feature']:<30} {row['importance']:.4f}")
    
    # 2. Statistical Feature Selection (F-test)
    print(f"\n2️⃣ Statistical Feature Selection (F-test):")
    selector_f = SelectKBest(score_func=f_classif, k=20)
    X_selected_f = selector_f.fit_transform(X, y_encoded)
    
    f_scores = pd.DataFrame({
        'feature': feature_columns,
        'f_score': selector_f.scores_
    }).sort_values('f_score', ascending=False)
    
    print(f"   Top 20 Features by F-score:")
    for i, (_, row) in enumerate(f_scores.head(20).iterrows(), 1):
        print(f"   {i:2d}. {row['feature']:<30} {row['f_score']:.2f}")
    
    # 3. Mutual Information
    print(f"\n3️⃣ Mutual Information Feature Selection:")
    mi_scores = mutual_info_classif(X, y_encoded, random_state=42)
    
    mi_df = pd.DataFrame({
        'feature': feature_columns,
        'mi_score': mi_scores
    }).sort_values('mi_score', ascending=False)
    
    print(f"   Top 20 Features by Mutual Information:")
    for i, (_, row) in enumerate(mi_df.head(20).iterrows(), 1):
        print(f"   {i:2d}. {row['feature']:<30} {row['mi_score']:.4f}")
    
    # Combine all methods for comprehensive ranking
    print(f"\n🎯 Comprehensive Feature Ranking:")
    
    # Normalize scores
    feature_importance['rf_norm'] = feature_importance['importance'] / feature_importance['importance'].max()
    f_scores['f_norm'] = f_scores['f_score'] / f_scores['f_score'].max()
    mi_df['mi_norm'] = mi_df['mi_score'] / mi_df['mi_score'].max()
    
    # Merge all scores
    combined_scores = feature_importance.merge(f_scores, on='feature').merge(mi_df, on='feature')
    combined_scores['combined_score'] = (
        combined_scores['rf_norm'] * 0.4 + 
        combined_scores['f_norm'] * 0.3 + 
        combined_scores['mi_norm'] * 0.3
    )
    
    combined_scores = combined_scores.sort_values('combined_score', ascending=False)
    
    print(f"   Top 25 Most Important Features (Combined Score):")
    for i, (_, row) in enumerate(combined_scores.head(25).iterrows(), 1):
        print(f"   {i:2d}. {row['feature']:<30} {row['combined_score']:.4f}")
    
    # Categorize features by domain
    print(f"\n📋 Feature Categories for Threat Identification:")
    
    # Network-related features
    network_features = [f for f in feature_columns if any(keyword in f.lower() for keyword in 
                       ['ip', 'tcp', 'udp', 'port', 'connection', 'packet', 'protocol', 'network'])]
    
    # HTTP-related features
    http_features = [f for f in feature_columns if any(keyword in f.lower() for keyword in 
                    ['http', 'request', 'response', 'uri', 'method', 'content'])]
    
    # DNS-related features
    dns_features = [f for f in feature_columns if any(keyword in f.lower() for keyword in 
                   ['dns', 'query', 'name', 'type'])]
    
    # MQTT-related features
    mqtt_features = [f for f in feature_columns if any(keyword in f.lower() for keyword in 
                    ['mqtt', 'topic', 'message', 'proto'])]
    
    # Modbus-related features
    modbus_features = [f for f in feature_columns if any(keyword in f.lower() for keyword in 
                      ['mbtcp', 'modbus', 'trans', 'unit'])]
    
    # ICMP-related features
    icmp_features = [f for f in feature_columns if any(keyword in f.lower() for keyword in 
                    ['icmp', 'checksum', 'seq', 'timestamp'])]
    
    # ARP-related features
    arp_features = [f for f in feature_columns if any(keyword in f.lower() for keyword in 
                   ['arp', 'hw', 'proto'])]
    
    # Time-related features
    time_features = [f for f in feature_columns if any(keyword in f.lower() for keyword in 
                    ['time', 'delta', 'stream'])]
    
    print(f"\n🌐 Network Features ({len(network_features)}):")
    for feature in network_features[:10]:
        print(f"   • {feature}")
    
    print(f"\n🌍 HTTP Features ({len(http_features)}):")
    for feature in http_features[:10]:
        print(f"   • {feature}")
    
    print(f"\n🔍 DNS Features ({len(dns_features)}):")
    for feature in dns_features[:10]:
        print(f"   • {feature}")
    
    print(f"\n📡 MQTT Features ({len(mqtt_features)}):")
    for feature in mqtt_features[:10]:
        print(f"   • {feature}")
    
    print(f"\n⚙️ Modbus Features ({len(modbus_features)}):")
    for feature in modbus_features[:10]:
        print(f"   • {feature}")
    
    print(f"\n📊 ICMP Features ({len(icmp_features)}):")
    for feature in icmp_features[:10]:
        print(f"   • {feature}")
    
    print(f"\n🔗 ARP Features ({len(arp_features)}):")
    for feature in arp_features[:10]:
        print(f"   • {feature}")
    
    print(f"\n⏰ Time Features ({len(time_features)}):")
    for feature in time_features[:10]:
        print(f"   • {feature}")
    
    # Model Performance with Top Features
    print(f"\n🎯 Model Performance Analysis:")
    
    # Test with different numbers of top features
    top_features_counts = [10, 20, 30, 50]
    
    for n_features in top_features_counts:
        top_features = combined_scores.head(n_features)['feature'].tolist()
        X_top = X[top_features]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_top, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Train model
        rf_top = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        rf_top.fit(X_train, y_train)
        
        # Evaluate
        accuracy = rf_top.score(X_test, y_test)
        print(f"   Top {n_features:2d} features: Accuracy = {accuracy:.4f}")
    
    # Generate recommendations
    print(f"\n💡 Recommendations for Threat Identification:")
    
    top_15_features = combined_scores.head(15)['feature'].tolist()
    
    print(f"\n🎯 Top 15 Most Important Features for Threat Detection:")
    for i, feature in enumerate(top_15_features, 1):
        print(f"   {i:2d}. {feature}")
    
    print(f"\n📋 Feature Selection Strategy:")
    print(f"   1. Use top 15-20 features for optimal performance")
    print(f"   2. Focus on network and protocol-specific features")
    print(f"   3. Include both statistical and behavioral features")
    print(f"   4. Consider feature correlation to avoid redundancy")
    
    print(f"\n🔍 Key Threat Indicators:")
    print(f"   • Network Protocol Anomalies (TCP, UDP, ICMP)")
    print(f"   • HTTP Request Patterns")
    print(f"   • DNS Query Behaviors")
    print(f"   • Connection Timing Patterns")
    print(f"   • Packet Size and Frequency")
    
    # Save results
    results = {
        'top_features': top_15_features,
        'feature_importance': combined_scores.head(25).to_dict('records'),
        'feature_categories': {
            'network': network_features,
            'http': http_features,
            'dns': dns_features,
            'mqtt': mqtt_features,
            'modbus': modbus_features,
            'icmp': icmp_features,
            'arp': arp_features,
            'time': time_features
        },
        'recommendations': {
            'optimal_features': 20,
            'min_features': 15,
            'max_features': 30
        }
    }
    
    import json
    with open('feature_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Analysis complete! Results saved to 'feature_analysis_results.json'")
    
    return results

if __name__ == "__main__":
    results = analyze_feature_importance()
