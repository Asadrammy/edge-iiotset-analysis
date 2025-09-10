import pandas as pd
import json
import os

print("🚀 Creating Edge-IIoTset Dataset Analysis Dashboard...")

# Load dataset
print("Loading dataset...")
df = pd.read_csv("Edge-IIoTset dataset/Selected dataset for ML and DL/ML-EdgeIIoT-dataset.csv")
print(f"✅ Dataset loaded: {len(df):,} records, {len(df.columns)} features")

# Generate statistics
attack_dist = df['Attack_type'].value_counts()
label_dist = df['Attack_label'].value_counts()

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
    "attack_distribution": attack_dist.to_dict(),
    "most_common_attack": attack_dist.index[0],
    "least_common_attack": attack_dist.index[-1],
    "class_imbalance_ratio": round((df['Attack_label'] == 1).sum() / (df['Attack_label'] == 0).sum(), 2)
}

# Create HTML dashboard
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edge-IIoTset Dataset Analysis Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
            margin-top: 20px;
            margin-bottom: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        .header p {{
            font-size: 1.3em;
            opacity: 0.9;
        }}
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}
        .card {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            text-align: center;
            border-left: 5px solid #3498db;
            transition: transform 0.3s ease;
        }}
        .card:hover {{
            transform: translateY(-5px);
        }}
        .card h3 {{
            color: #2c3e50;
            font-size: 1.1em;
            margin-bottom: 15px;
        }}
        .card .value {{
            font-size: 3em;
            font-weight: bold;
            color: #3498db;
            margin: 15px 0;
        }}
        .card .label {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .charts-section {{
            padding: 40px;
        }}
        .chart-container {{
            margin: 40px 0;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }}
        .chart-title {{
            font-size: 1.8em;
            color: #2c3e50;
            margin-bottom: 25px;
            text-align: center;
            border-bottom: 3px solid #ecf0f1;
            padding-bottom: 15px;
        }}
        .chart-wrapper {{
            position: relative;
            height: 400px;
            margin: 20px 0;
        }}
        .insights {{
            background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
            padding: 40px;
            margin: 30px;
            border-radius: 15px;
            border-left: 5px solid #27ae60;
        }}
        .insights h3 {{
            color: #27ae60;
            font-size: 1.5em;
            margin-bottom: 20px;
        }}
        .insights ul {{
            list-style: none;
            padding: 0;
        }}
        .insights li {{
            padding: 10px 0;
            border-bottom: 1px solid #d5dbdb;
        }}
        .insights li:last-child {{
            border-bottom: none;
        }}
        .attack-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 25px;
        }}
        .attack-item {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #e74c3c;
            transition: transform 0.2s ease;
        }}
        .attack-item:hover {{
            transform: translateX(5px);
        }}
        .attack-name {{
            font-weight: bold;
            color: #2c3e50;
            font-size: 1.1em;
        }}
        .attack-count {{
            color: #7f8c8d;
            margin-top: 5px;
        }}
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .footer a {{
            color: #3498db;
            text-decoration: none;
        }}
        .footer a:hover {{
            text-decoration: underline;
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
                <h3>📊 Total Records</h3>
                <div class="value">{executive_summary['total_records']:,}</div>
                <div class="label">Data Points</div>
            </div>
            <div class="card">
                <h3>🔧 Features</h3>
                <div class="value">{executive_summary['total_features']}</div>
                <div class="label">Attributes</div>
            </div>
            <div class="card">
                <h3>⚔️ Attack Types</h3>
                <div class="value">{executive_summary['attack_types']}</div>
                <div class="label">Categories</div>
            </div>
            <div class="card">
                <h3>✅ Data Quality</h3>
                <div class="value">{executive_summary['data_quality']['completeness']}%</div>
                <div class="label">Complete</div>
            </div>
            <div class="card">
                <h3>🟢 Normal Traffic</h3>
                <div class="value">{executive_summary['normal_percentage']}%</div>
                <div class="label">of Dataset</div>
            </div>
            <div class="card">
                <h3>🔴 Attack Traffic</h3>
                <div class="value">{executive_summary['attack_percentage']}%</div>
                <div class="label">of Dataset</div>
            </div>
        </div>
        
        <div class="charts-section">
            <div class="chart-container">
                <div class="chart-title">📊 Attack Type Distribution</div>
                <div class="chart-wrapper">
                    <canvas id="attackChart"></canvas>
                </div>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">⚖️ Class Balance Analysis</div>
                <div class="chart-wrapper">
                    <canvas id="classChart"></canvas>
                </div>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">🎯 Detailed Attack Breakdown</div>
                <div class="attack-grid">
"""

# Add attack items
for attack, count in attack_dist.items():
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
            <h3>💡 Key Business Insights & Recommendations</h3>
            <ul>
                <li><strong>📈 Dataset Scale:</strong> {executive_summary['total_records']:,} records provide robust training data for enterprise ML models</li>
                <li><strong>🛡️ Security Coverage:</strong> {executive_summary['attack_types']} attack types ensure comprehensive IoT security coverage</li>
                <li><strong>✨ Data Quality:</strong> {executive_summary['data_quality']['completeness']}% completeness means minimal preprocessing overhead</li>
                <li><strong>⚖️ Class Distribution:</strong> {executive_summary['attack_percentage']}% attack vs {executive_summary['normal_percentage']}% normal traffic</li>
                <li><strong>🎯 Priority Attack:</strong> {executive_summary['most_common_attack']} requires immediate security attention</li>
                <li><strong>📊 Imbalance Ratio:</strong> {executive_summary['class_imbalance_ratio']}:1 ratio suggests balanced sampling strategies</li>
                <li><strong>💾 Memory Efficient:</strong> {executive_summary['memory_usage_mb']} MB dataset size suitable for most ML frameworks</li>
                <li><strong>🔍 Data Integrity:</strong> Only {executive_summary['data_quality']['missing_values']} missing values across entire dataset</li>
                <li><strong>🚀 Ready for Production:</strong> Dataset is research-ready with minimal preprocessing required</li>
                <li><strong>🎓 Academic Standard:</strong> Created by Dr. Mohamed Amine Ferrag for peer-reviewed research</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>📈 Generated by AI-Powered Dataset Analysis | Edge-IIoTset Cybersecurity Research</p>
            <p>🔗 <a href="https://github.com/Asadrammy">GitHub Repository</a> | 📧 Contact: +92 314 0479594</p>
            <p>📊 Analysis Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
    
    <script>
        // Attack Distribution Chart
        const attackCtx = document.getElementById('attackChart').getContext('2d');
        const attackData = {json.dumps(list(attack_dist.keys()))};
        const attackCounts = {json.dumps(list(attack_dist.values()))};
        
        new Chart(attackCtx, {{
            type: 'doughnut',
            data: {{
                labels: attackData,
                datasets: [{{
                    data: attackCounts,
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                        '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384',
                        '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 20,
                            usePointStyle: true
                        }}
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return context.label + ': ' + context.parsed.toLocaleString() + ' (' + percentage + '%)';
                            }}
                        }}
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
                    backgroundColor: ['#2E8B57', '#DC143C'],
                    borderWidth: 3,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 20,
                            usePointStyle: true,
                            font: {{
                                size: 14
                            }}
                        }}
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return context.label + ': ' + context.parsed + '%';
                            }}
                        }}
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
print("  - Interactive visualizations with Chart.js")
print("  - Executive summary with key metrics")
print("  - Statistical analysis and insights")
print("  - Data quality assessment")
print("  - Business recommendations")
print("  - Responsive design for all devices")

print(f"\n🔗 Dashboard URL: file:///{os.path.abspath('edge_iiotset_dashboard.html')}")
print("\n🚀 Ready for GitHub deployment!")
