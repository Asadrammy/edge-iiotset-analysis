import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import SelectKBest, f_classif
import json

print("🔍 Analyzing Edge-IIoTset Dataset Features for Threat Identification...")

# Load dataset
df = pd.read_csv("Edge-IIoTset dataset/Selected dataset for ML and DL/ML-EdgeIIoT-dataset.csv")
print(f"✅ Dataset loaded: {len(df):,} records, {len(df.columns)} features")

# Get feature columns (exclude target columns)
feature_columns = [col for col in df.columns if col not in ['Attack_type', 'Attack_label']]
print(f"🔧 Analyzing {len(feature_columns)} features")

# Data preprocessing
df_processed = df.copy()

# Handle mixed data types - convert to numeric where possible
for col in feature_columns:
    if df_processed[col].dtype == 'object':
        df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')

# Fill missing values
df_processed = df_processed.fillna(0)

# Prepare features and target
X = df_processed[feature_columns]
y = df_processed['Attack_type']

# Encode target variable
le = LabelEncoder()
y_encoded = le.fit_transform(y)

print(f"✅ Data preprocessed: {X.shape[0]} samples, {X.shape[1]} features")

# Random Forest Feature Importance
print(f"\n📈 Calculating Feature Importance...")
rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X, y_encoded)

# Get feature importance
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': rf.feature_importance_
}).sort_values('importance', ascending=False)

print(f"\n🎯 TOP 25 MOST IMPORTANT FEATURES FOR THREAT IDENTIFICATION:")
print("=" * 70)
for i, (_, row) in enumerate(feature_importance.head(25).iterrows(), 1):
    print(f"{i:2d}. {row['feature']:<35} {row['importance']:.4f}")

# Statistical Feature Selection (F-test)
print(f"\n📊 STATISTICAL FEATURE SELECTION (F-test):")
print("=" * 50)
selector_f = SelectKBest(score_func=f_classif, k=25)
X_selected_f = selector_f.fit_transform(X, y_encoded)

f_scores = pd.DataFrame({
    'feature': feature_columns,
    'f_score': selector_f.scores_
}).sort_values('f_score', ascending=False)

for i, (_, row) in enumerate(f_scores.head(25).iterrows(), 1):
    print(f"{i:2d}. {row['feature']:<35} {row['f_score']:.2f}")

# Categorize features by domain
print(f"\n📋 FEATURE CATEGORIES FOR THREAT IDENTIFICATION:")
print("=" * 55)

# Network-related features
network_features = [f for f in feature_columns if any(keyword in f.lower() for keyword in 
                   ['ip', 'tcp', 'udp', 'port', 'connection', 'packet', 'protocol'])]

# HTTP-related features
http_features = [f for f in feature_columns if any(keyword in f.lower() for keyword in 
                ['http', 'request', 'response', 'uri', 'method', 'content'])]

# DNS-related features
dns_features = [f for f in feature_columns if any(keyword in f.lower() for keyword in 
               ['dns', 'query', 'name', 'type'])]

# MQTT-related features
mqtt_features = [f for f in feature_columns if any(keyword in f.lower() for keyword in 
                ['mqtt', 'topic', 'message', 'proto'])]

# ICMP-related features
icmp_features = [f for f in feature_columns if any(keyword in f.lower() for keyword in 
                ['icmp', 'checksum', 'seq', 'timestamp'])]

# ARP-related features
arp_features = [f for f in feature_columns if any(keyword in f.lower() for keyword in 
               ['arp', 'hw', 'proto'])]

# Time-related features
time_features = [f for f in feature_columns if any(keyword in f.lower() for keyword in 
                ['time', 'delta', 'stream'])]

print(f"\n🌐 NETWORK FEATURES ({len(network_features)}):")
for feature in network_features:
    print(f"   • {feature}")

print(f"\n🌍 HTTP FEATURES ({len(http_features)}):")
for feature in http_features:
    print(f"   • {feature}")

print(f"\n🔍 DNS FEATURES ({len(dns_features)}):")
for feature in dns_features:
    print(f"   • {feature}")

print(f"\n📡 MQTT FEATURES ({len(mqtt_features)}):")
for feature in mqtt_features:
    print(f"   • {feature}")

print(f"\n📊 ICMP FEATURES ({len(icmp_features)}):")
for feature in icmp_features:
    print(f"   • {feature}")

print(f"\n🔗 ARP FEATURES ({len(arp_features)}):")
for feature in arp_features:
    print(f"   • {feature}")

print(f"\n⏰ TIME FEATURES ({len(time_features)}):")
for feature in time_features:
    print(f"   • {feature}")

# Get top 15 features for recommendations
top_15_features = feature_importance.head(15)['feature'].tolist()

print(f"\n💡 RECOMMENDATIONS FOR THREAT IDENTIFICATION:")
print("=" * 50)

print(f"\n🎯 TOP 15 MOST IMPORTANT FEATURES:")
for i, feature in enumerate(top_15_features, 1):
    print(f"   {i:2d}. {feature}")

print(f"\n📋 FEATURE SELECTION STRATEGY:")
print(f"   1. Use top 15-20 features for optimal performance")
print(f"   2. Focus on network and protocol-specific features")
print(f"   3. Include both statistical and behavioral features")
print(f"   4. Consider feature correlation to avoid redundancy")

print(f"\n🔍 KEY THREAT INDICATORS:")
print(f"   • Network Protocol Anomalies (TCP, UDP, ICMP)")
print(f"   • HTTP Request Patterns")
print(f"   • DNS Query Behaviors")
print(f"   • Connection Timing Patterns")
print(f"   • Packet Size and Frequency")

# Save results
results = {
    'top_features': top_15_features,
    'feature_importance': feature_importance.head(25).to_dict('records'),
    'feature_categories': {
        'network': network_features,
        'http': http_features,
        'dns': dns_features,
        'mqtt': mqtt_features,
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

with open('feature_analysis_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n✅ Analysis complete! Results saved to 'feature_analysis_results.json'")
