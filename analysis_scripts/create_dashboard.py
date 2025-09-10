import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
import json

# Load dataset
print("Loading Edge-IIoTset dataset...")
df = pd.read_csv("Edge-IIoTset dataset/Selected dataset for ML and DL/ML-EdgeIIoT-dataset.csv")
print(f"Dataset loaded: {len(df):,} records, {len(df.columns)} features")

# Generate executive summary
executive_summary = {
    "dataset_name": "Edge-IIoTset Cybersecurity Dataset",
    "total_records": len(df),
    "total_features": len(df.columns),
    "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
    "attack_types": len(df['Attack_type'].unique()),
    "normal_percentage": round((df['Attack_label'] == 0).sum() / len(df) * 100, 2),
    "attack_percentage": round((df['Attack_label'] == 1).sum() / len(df) * 100, 2),
    "data_quality": {
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "completeness": round((1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100, 2)
    }
}

# Create attack distribution chart
attack_counts = df['Attack_type'].value_counts()
attack_dist_fig = px.pie(
    values=attack_counts.values,
    names=attack_counts.index,
    title="Attack Type Distribution",
    color_discrete_sequence=px.colors.qualitative.Set3
)
attack_dist_fig.update_traces(textposition='inside', textinfo='percent+label')
attack_dist_fig.update_layout(title_font_size=20, font_size=12, height=500)

# Create class balance chart
label_counts = df['Attack_label'].value_counts()
labels = ['Normal Traffic', 'Attack Traffic']
colors = ['#2E8B57', '#DC143C']

class_balance_fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=label_counts.values,
    marker_colors=colors
)])
class_balance_fig.update_layout(
    title="Dataset Class Distribution",
    title_font_size=20,
    height=400
)

# Create attack categories chart
attack_categories = {
    'DDoS Attacks': ['DDoS_UDP', 'DDoS_ICMP', 'DDoS_TCP', 'DDoS_HTTP'],
    'Web Attacks': ['XSS', 'SQL_injection', 'Password', 'Uploading'],
    'Network Attacks': ['MITM', 'Port_Scanning', 'Fingerprinting'],
    'Malware': ['Ransomware', 'Backdoor'],
    'Reconnaissance': ['Vulnerability_scanner']
}

category_counts = {}
for category, attacks in attack_categories.items():
    count = sum(df[df['Attack_type'].isin(attacks)].shape[0])
    category_counts[category] = count

attack_categories_fig = px.bar(
    x=list(category_counts.keys()),
    y=list(category_counts.values()),
    title="Attack Categories Distribution",
    color=list(category_counts.values()),
    color_continuous_scale='Viridis'
)
attack_categories_fig.update_layout(
    title_font_size=20,
    xaxis_title="Attack Categories",
    yaxis_title="Number of Records",
    height=500
)

# Create data quality chart
quality_metrics = {
    'Complete Records': len(df) - df.isnull().sum().sum(),
    'Missing Values': df.isnull().sum().sum(),
    'Duplicate Records': df.duplicated().sum(),
    'Unique Records': len(df) - df.duplicated().sum()
}

data_quality_fig = px.bar(
    x=list(quality_metrics.keys()),
    y=list(quality_metrics.values()),
    title="Data Quality Metrics",
    color=list(quality_metrics.values()),
    color_continuous_scale='Blues'
)
data_quality_fig.update_layout(
    title_font_size=20,
    xaxis_title="Quality Metrics",
    yaxis_title="Count",
    height=400
)

# Create HTML dashboard
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edge-IIoTset Dataset Analysis Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            text-align: center;
            border-left: 4px solid #3498db;
        }}
        .card h3 {{
            margin: 0 0 10px 0;
            color: #2c3e50;
            font-size: 1.1em;
        }}
        .card .value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #3498db;
            margin: 10px 0;
        }}
        .card .label {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .charts-section {{
            padding: 30px;
        }}
        .chart-container {{
            margin: 30px 0;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }}
        .chart-title {{
            font-size: 1.5em;
            color: #2c3e50;
            margin-bottom: 20px;
            text-align: center;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 10px;
        }}
        .insights {{
            background: #e8f5e8;
            padding: 25px;
            margin: 20px 0;
            border-radius: 10px;
            border-left: 4px solid #27ae60;
        }}
        .insights h3 {{
            color: #27ae60;
            margin-top: 0;
        }}
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Edge-IIoTset Dataset Analysis</h1>
            <p>Comprehensive Statistical Dashboard for IoT Cybersecurity Research</p>
        </div>
        
        <div class="summary-cards">
            <div class="card">
                <h3>Total Records</h3>
                <div class="value">{executive_summary['total_records']:,}</div>
                <div class="label">Data Points</div>
            </div>
            <div class="card">
                <h3>Features</h3>
                <div class="value">{executive_summary['total_features']}</div>
                <div class="label">Attributes</div>
            </div>
            <div class="card">
                <h3>Attack Types</h3>
                <div class="value">{executive_summary['attack_types']}</div>
                <div class="label">Categories</div>
            </div>
            <div class="card">
                <h3>Data Quality</h3>
                <div class="value">{executive_summary['data_quality']['completeness']}%</div>
                <div class="label">Complete</div>
            </div>
            <div class="card">
                <h3>Normal Traffic</h3>
                <div class="value">{executive_summary['normal_percentage']}%</div>
                <div class="label">of Dataset</div>
            </div>
            <div class="card">
                <h3>Attack Traffic</h3>
                <div class="value">{executive_summary['attack_percentage']}%</div>
                <div class="label">of Dataset</div>
            </div>
        </div>
        
        <div class="charts-section">
            <div class="chart-container">
                <div class="chart-title">📊 Attack Type Distribution</div>
                <div id="attack-distribution"></div>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">⚖️ Class Balance Analysis</div>
                <div id="class-balance"></div>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">🎯 Attack Categories Breakdown</div>
                <div id="attack-categories"></div>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">✅ Data Quality Metrics</div>
                <div id="data-quality"></div>
            </div>
        </div>
        
        <div class="insights">
            <h3>💡 Key Insights for Your Business</h3>
            <ul>
                <li><strong>Dataset Size:</strong> {executive_summary['total_records']:,} records provide robust training data for ML models</li>
                <li><strong>Attack Coverage:</strong> {executive_summary['attack_types']} different attack types ensure comprehensive security coverage</li>
                <li><strong>Data Quality:</strong> {executive_summary['data_quality']['completeness']}% completeness means minimal data preprocessing needed</li>
                <li><strong>Class Distribution:</strong> {executive_summary['attack_percentage']}% attack vs {executive_summary['normal_percentage']}% normal traffic</li>
                <li><strong>Most Common Attack:</strong> {attack_counts.index[0]} requires immediate attention</li>
                <li><strong>Imbalance Ratio:</strong> {round((df['Attack_label'] == 1).sum() / (df['Attack_label'] == 0).sum(), 2)}:1 ratio suggests need for balanced sampling</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>📈 Generated by AI-Powered Dataset Analysis | Edge-IIoTset Cybersecurity Research</p>
            <p>🔗 <a href="https://github.com/Asadrammy" style="color: #3498db;">GitHub Repository</a> | 📧 Contact: +92 314 0479594</p>
        </div>
    </div>
    
    <script>
        // Attack Distribution Chart
        {attack_dist_fig.to_html(include_plotlyjs=False, div_id="attack-distribution")}
        
        // Class Balance Chart
        {class_balance_fig.to_html(include_plotlyjs=False, div_id="class-balance")}
        
        // Attack Categories Chart
        {attack_categories_fig.to_html(include_plotlyjs=False, div_id="attack-categories")}
        
        // Data Quality Chart
        {data_quality_fig.to_html(include_plotlyjs=False, div_id="data-quality")}
    </script>
</body>
</html>
"""

# Save dashboard
with open("edge_iiotset_dashboard.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Dashboard created: edge_iiotset_dashboard.html")

# Save JSON report
with open("dataset_report.json", "w", encoding="utf-8") as f:
    json.dump(executive_summary, f, indent=2)

print("✅ Report generated: dataset_report.json")
print("\n📊 Dashboard Features:")
print("  - Interactive visualizations")
print("  - Executive summary")
print("  - Statistical analysis")
print("  - Data quality metrics")
print("  - Business insights")
