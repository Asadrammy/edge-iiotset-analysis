import pandas as pd
import json
import os

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
    },
    "attack_distribution": df['Attack_type'].value_counts().to_dict(),
    "most_common_attack": df['Attack_type'].value_counts().index[0],
    "least_common_attack": df['Attack_type'].value_counts().index[-1],
    "class_imbalance_ratio": round((df['Attack_label'] == 1).sum() / (df['Attack_label'] == 0).sum(), 2)
}

# Create simple HTML dashboard
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edge-IIoTset Dataset Analysis Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            max-width: 1200px;
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
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
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
        .attack-list {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .attack-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #e74c3c;
        }}
        .attack-name {{
            font-weight: bold;
            color: #2c3e50;
        }}
        .attack-count {{
            color: #7f8c8d;
            font-size: 0.9em;
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
                <canvas id="attackChart" width="400" height="200"></canvas>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">⚖️ Class Balance Analysis</div>
                <canvas id="classChart" width="400" height="200"></canvas>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">🎯 Attack Types Breakdown</div>
                <div class="attack-list">
"""

# Add attack list
for attack, count in executive_summary['attack_distribution'].items():
    percentage = round((count / executive_summary['total_records']) * 100, 1)
    html_content += f"""
                    <div class="attack-item">
                        <div class="attack-name">{attack}</div>
                        <div class="attack-count">{count:,} records ({percentage}%)</div>
                    </div>
    """

html_content += f"""
                </div>
            </div>
        </div>
        
        <div class="insights">
            <h3>💡 Key Insights for Your Business</h3>
            <ul>
                <li><strong>Dataset Size:</strong> {executive_summary['total_records']:,} records provide robust training data for ML models</li>
                <li><strong>Attack Coverage:</strong> {executive_summary['attack_types']} different attack types ensure comprehensive security coverage</li>
                <li><strong>Data Quality:</strong> {executive_summary['data_quality']['completeness']}% completeness means minimal data preprocessing needed</li>
                <li><strong>Class Distribution:</strong> {executive_summary['attack_percentage']}% attack vs {executive_summary['normal_percentage']}% normal traffic</li>
                <li><strong>Most Common Attack:</strong> {executive_summary['most_common_attack']} requires immediate attention</li>
                <li><strong>Imbalance Ratio:</strong> {executive_summary['class_imbalance_ratio']}:1 ratio suggests need for balanced sampling</li>
                <li><strong>Memory Usage:</strong> {executive_summary['memory_usage_mb']} MB dataset size suitable for most ML frameworks</li>
                <li><strong>Missing Data:</strong> {executive_summary['data_quality']['missing_values']} missing values across entire dataset</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>📈 Generated by AI-Powered Dataset Analysis | Edge-IIoTset Cybersecurity Research</p>
            <p>🔗 <a href="https://github.com/Asadrammy" style="color: #3498db;">GitHub Repository</a> | 📧 Contact: +92 314 0479594</p>
        </div>
    </div>
    
    <script>
        // Attack Distribution Chart
        const attackCtx = document.getElementById('attackChart').getContext('2d');
        const attackData = {json.dumps(list(executive_summary['attack_distribution'].keys()))};
        const attackCounts = {json.dumps(list(executive_summary['attack_distribution'].values()))};
        
        new Chart(attackCtx, {{
            type: 'doughnut',
            data: {{
                labels: attackData,
                datasets: [{{
                    data: attackCounts,
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                        '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384',
                        '#36A2EB', '#FFCE56'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});
        
        // Class Balance Chart
        const classCtx = document.getElementById('classChart').getContext('2d');
        new Chart(classCtx, {{
            type: 'pie',
            data: {{
                labels: ['Normal Traffic', 'Attack Traffic'],
                datasets: [{{
                    data: [{executive_summary['normal_percentage']}, {executive_summary['attack_percentage']}],
                    backgroundColor: ['#2E8B57', '#DC143C']
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});
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
print(f"\n🔗 Dashboard URL: file:///{os.path.abspath('edge_iiotset_dashboard.html')}")
