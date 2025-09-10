import pandas as pd
import json
import os

print("🚀 Creating Complete Edge-IIoTset Dataset Analysis Dashboard...")

# Load dataset
print("Loading dataset...")
df = pd.read_csv("Edge-IIoTset dataset/Selected dataset for ML and DL/ML-EdgeIIoT-dataset.csv")
print(f"✅ Dataset loaded: {len(df):,} records, {len(df.columns)} features")

# Generate comprehensive statistics
attack_dist = df['Attack_type'].value_counts()
label_dist = df['Attack_label'].value_counts()

# Calculate additional metrics
total_records = len(df)
total_features = len(df.columns)
memory_usage = round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
attack_types = len(df['Attack_type'].unique())
normal_percentage = round((df['Attack_label'] == 0).sum() / len(df) * 100, 2)
attack_percentage = round((df['Attack_label'] == 1).sum() / len(df) * 100, 2)
missing_values = int(df.isnull().sum().sum())
duplicate_rows = int(df.duplicated().sum())
completeness = round((1 - missing_values / (len(df) * len(df.columns))) * 100, 2)
imbalance_ratio = round((df['Attack_label'] == 1).sum() / (df['Attack_label'] == 0).sum(), 2)

# Convert to lists for JSON serialization
attack_names = list(attack_dist.index)
attack_counts = [int(x) for x in attack_dist.values]

# Create comprehensive HTML dashboard
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
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
            overflow: hidden;
            margin-top: 20px;
            margin-bottom: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 50px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 3.5em;
            margin-bottom: 15px;
            font-weight: 300;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .header p {{
            font-size: 1.4em;
            opacity: 0.9;
        }}
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            padding: 50px;
            background: #f8f9fa;
        }}
        .card {{
            background: white;
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
            border-left: 6px solid #3498db;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        .card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #3498db, #2ecc71);
        }}
        .card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        }}
        .card h3 {{
            color: #2c3e50;
            font-size: 1.2em;
            margin-bottom: 20px;
            font-weight: 600;
        }}
        .card .value {{
            font-size: 3.5em;
            font-weight: bold;
            color: #3498db;
            margin: 20px 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }}
        .card .label {{
            color: #7f8c8d;
            font-size: 1em;
            font-weight: 500;
        }}
        .charts-section {{
            padding: 50px;
        }}
        .chart-container {{
            margin: 50px 0;
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .chart-title {{
            font-size: 2em;
            color: #2c3e50;
            margin-bottom: 30px;
            text-align: center;
            border-bottom: 4px solid #ecf0f1;
            padding-bottom: 20px;
            font-weight: 600;
        }}
        .chart-wrapper {{
            position: relative;
            height: 500px;
            margin: 30px 0;
        }}
        .insights {{
            background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
            padding: 50px;
            margin: 40px;
            border-radius: 20px;
            border-left: 6px solid #27ae60;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .insights h3 {{
            color: #27ae60;
            font-size: 1.8em;
            margin-bottom: 25px;
            font-weight: 600;
        }}
        .insights ul {{
            list-style: none;
            padding: 0;
        }}
        .insights li {{
            padding: 15px 0;
            border-bottom: 1px solid #d5dbdb;
            font-size: 1.1em;
            line-height: 1.6;
        }}
        .insights li:last-child {{
            border-bottom: none;
        }}
        .attack-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }}
        .attack-item {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid #e74c3c;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }}
        .attack-item:hover {{
            transform: translateX(8px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }}
        .attack-name {{
            font-weight: bold;
            color: #2c3e50;
            font-size: 1.2em;
            margin-bottom: 8px;
        }}
        .attack-count {{
            color: #7f8c8d;
            font-size: 1em;
        }}
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .footer a {{
            color: #3498db;
            text-decoration: none;
            font-weight: 600;
        }}
        .footer a:hover {{
            text-decoration: underline;
        }}
        .stats-highlight {{
            background: linear-gradient(135deg, #3498db, #2ecc71);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
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
                <div class="value stats-highlight">{total_records:,}</div>
                <div class="label">Data Points</div>
            </div>
            <div class="card">
                <h3>🔧 Features</h3>
                <div class="value stats-highlight">{total_features}</div>
                <div class="label">Attributes</div>
            </div>
            <div class="card">
                <h3>⚔️ Attack Types</h3>
                <div class="value stats-highlight">{attack_types}</div>
                <div class="label">Categories</div>
            </div>
            <div class="card">
                <h3>✅ Data Quality</h3>
                <div class="value stats-highlight">{completeness}%</div>
                <div class="label">Complete</div>
            </div>
            <div class="card">
                <h3>🟢 Normal Traffic</h3>
                <div class="value stats-highlight">{normal_percentage}%</div>
                <div class="label">of Dataset</div>
            </div>
            <div class="card">
                <h3>🔴 Attack Traffic</h3>
                <div class="value stats-highlight">{attack_percentage}%</div>
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
    percentage = round((count / total_records) * 100, 1)
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
                <li><strong>📈 Dataset Scale:</strong> {total_records:,} records provide robust training data for enterprise ML models</li>
                <li><strong>🛡️ Security Coverage:</strong> {attack_types} attack types ensure comprehensive IoT security coverage</li>
                <li><strong>✨ Data Quality:</strong> {completeness}% completeness means minimal preprocessing overhead</li>
                <li><strong>⚖️ Class Distribution:</strong> {attack_percentage}% attack vs {normal_percentage}% normal traffic</li>
                <li><strong>🎯 Priority Attack:</strong> {attack_dist.index[0]} requires immediate security attention</li>
                <li><strong>📊 Imbalance Ratio:</strong> {imbalance_ratio}:1 ratio suggests balanced sampling strategies</li>
                <li><strong>💾 Memory Efficient:</strong> {memory_usage} MB dataset size suitable for most ML frameworks</li>
                <li><strong>🔍 Data Integrity:</strong> Only {missing_values} missing values across entire dataset</li>
                <li><strong>🚀 Ready for Production:</strong> Dataset is research-ready with minimal preprocessing required</li>
                <li><strong>🎓 Academic Standard:</strong> Created by Dr. Mohamed Amine Ferrag for peer-reviewed research</li>
                <li><strong>🔄 Duplicate Handling:</strong> {duplicate_rows} duplicate records need cleaning for optimal performance</li>
                <li><strong>📱 IoT Focus:</strong> Specifically designed for Industrial Internet of Things security</li>
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
        const attackData = {json.dumps(attack_names)};
        const attackCounts = {json.dumps(attack_counts)};
        
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
                    borderWidth: 3,
                    borderColor: '#fff',
                    hoverBorderWidth: 5
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 25,
                            usePointStyle: true,
                            font: {{
                                size: 14,
                                weight: 'bold'
                            }}
                        }}
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return context.label + ': ' + context.parsed.toLocaleString() + ' (' + percentage + '%)';
                            }}
                        }},
                        titleFont: {{
                            size: 16,
                            weight: 'bold'
                        }},
                        bodyFont: {{
                            size: 14
                        }}
                    }}
                }},
                animation: {{
                    animateRotate: true,
                    duration: 2000
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
                    data: [{normal_percentage}, {attack_percentage}],
                    backgroundColor: ['#2E8B57', '#DC143C'],
                    borderWidth: 4,
                    borderColor: '#fff',
                    hoverBorderWidth: 6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 25,
                            usePointStyle: true,
                            font: {{
                                size: 16,
                                weight: 'bold'
                            }}
                        }}
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return context.label + ': ' + context.parsed + '%';
                            }}
                        }},
                        titleFont: {{
                            size: 16,
                            weight: 'bold'
                        }},
                        bodyFont: {{
                            size: 14
                        }}
                    }}
                }},
                animation: {{
                    animateRotate: true,
                    duration: 2000
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

# Create comprehensive JSON report
comprehensive_report = {
    "dataset_info": {
        "name": "Edge-IIoTset Cybersecurity Dataset",
        "creator": "Dr. Mohamed Amine Ferrag et al.",
        "purpose": "IoT/IIoT Intrusion Detection Research",
        "total_records": total_records,
        "total_features": total_features,
        "memory_usage_mb": memory_usage
    },
    "data_quality": {
        "completeness_percentage": completeness,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "data_integrity_score": round(completeness - (duplicate_rows / total_records * 100), 2)
    },
    "attack_analysis": {
        "total_attack_types": attack_types,
        "attack_distribution": attack_dist.to_dict(),
        "most_common_attack": attack_dist.index[0],
        "least_common_attack": attack_dist.index[-1],
        "attack_percentage": attack_percentage,
        "normal_percentage": normal_percentage,
        "class_imbalance_ratio": imbalance_ratio
    },
    "business_insights": {
        "dataset_readiness": "Production Ready",
        "preprocessing_needed": "Minimal",
        "recommended_use_cases": [
            "Intrusion Detection Systems",
            "Anomaly Detection",
            "Federated Learning",
            "Network Security Research",
            "IoT Behavior Analysis"
        ],
        "technical_recommendations": [
            "Handle class imbalance with SMOTE or class weights",
            "Remove duplicate records for optimal performance",
            "Use stratified sampling for train/test splits",
            "Consider feature selection from 63 features",
            "Implement proper validation strategies"
        ]
    },
    "statistical_summary": {
        "mean_records_per_attack": round(total_records / attack_types),
        "data_density": round(total_records / memory_usage, 2),
        "feature_to_record_ratio": round(total_features / total_records * 1000, 4),
        "attack_coverage_score": round(attack_types / 15 * 100, 2)
    }
}

# Save JSON report
with open("dataset_report.json", "w", encoding="utf-8") as f:
    json.dump(comprehensive_report, f, indent=2)

print("✅ Comprehensive report generated: dataset_report.json")

print("\n📊 Dashboard Features:")
print("  - Interactive visualizations with Chart.js")
print("  - Executive summary with key metrics")
print("  - Statistical analysis and insights")
print("  - Data quality assessment")
print("  - Business recommendations")
print("  - Responsive design for all devices")
print("  - Professional styling and animations")

print(f"\n🔗 Dashboard URL: file:///{os.path.abspath('edge_iiotset_dashboard.html')}")
print("\n🚀 Ready for GitHub deployment!")
print("\n📋 Next Steps:")
print("  1. Upload files to GitHub repository")
print("  2. Enable GitHub Pages for live hosting")
print("  3. Share dashboard link with client")
print("  4. Provide analysis summary")
