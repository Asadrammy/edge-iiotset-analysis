#!/usr/bin/env python3
"""
Interactive Statistical Dashboard for Edge-IIoTset Dataset
Client Analysis Tool
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
from flask import Flask, render_template, jsonify
import json
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class DatasetAnalyzer:
    def __init__(self, dataset_path):
        """Initialize the analyzer with dataset path"""
        self.dataset_path = dataset_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load the dataset"""
        print("Loading Edge-IIoTset dataset...")
        self.df = pd.read_csv(self.dataset_path)
        print(f"Dataset loaded: {len(self.df):,} records, {len(self.df.columns)} features")
    
    def generate_executive_summary(self):
        """Generate executive summary for client"""
        summary = {
            "dataset_name": "Edge-IIoTset Cybersecurity Dataset",
            "total_records": len(self.df),
            "total_features": len(self.df.columns),
            "memory_usage_mb": round(self.df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
            "attack_types": len(self.df['Attack_type'].unique()),
            "normal_percentage": round((self.df['Attack_label'] == 0).sum() / len(self.df) * 100, 2),
            "attack_percentage": round((self.df['Attack_label'] == 1).sum() / len(self.df) * 100, 2),
            "data_quality": {
                "missing_values": int(self.df.isnull().sum().sum()),
                "duplicate_rows": int(self.df.duplicated().sum()),
                "completeness": round((1 - self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100, 2)
            }
        }
        return summary
    
    def create_attack_distribution_chart(self):
        """Create attack type distribution chart"""
        attack_counts = self.df['Attack_type'].value_counts()
        
        fig = px.pie(
            values=attack_counts.values,
            names=attack_counts.index,
            title="Attack Type Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            title_font_size=20,
            font_size=12,
            height=500
        )
        return fig
    
    def create_class_balance_chart(self):
        """Create class balance visualization"""
        label_counts = self.df['Attack_label'].value_counts()
        labels = ['Normal Traffic', 'Attack Traffic']
        colors = ['#2E8B57', '#DC143C']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=label_counts.values,
            marker_colors=colors
        )])
        fig.update_layout(
            title="Dataset Class Distribution",
            title_font_size=20,
            height=400
        )
        return fig
    
    def create_attack_categories_chart(self):
        """Create attack categories breakdown"""
        attack_categories = {
            'DDoS Attacks': ['DDoS_UDP', 'DDoS_ICMP', 'DDoS_TCP', 'DDoS_HTTP'],
            'Web Attacks': ['XSS', 'SQL_injection', 'Password', 'Uploading'],
            'Network Attacks': ['MITM', 'Port_Scanning', 'Fingerprinting'],
            'Malware': ['Ransomware', 'Backdoor'],
            'Reconnaissance': ['Vulnerability_scanner']
        }
        
        category_counts = {}
        for category, attacks in attack_categories.items():
            count = sum(self.df[self.df['Attack_type'].isin(attacks)].shape[0])
            category_counts[category] = count
        
        fig = px.bar(
            x=list(category_counts.keys()),
            y=list(category_counts.values()),
            title="Attack Categories Distribution",
            color=list(category_counts.values()),
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            title_font_size=20,
            xaxis_title="Attack Categories",
            yaxis_title="Number of Records",
            height=500
        )
        return fig
    
    def create_feature_analysis(self):
        """Create feature analysis visualization"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        # Remove target columns
        feature_cols = [col for col in numeric_cols if col not in ['Attack_label']]
        
        # Sample data for correlation matrix (too large otherwise)
        sample_df = self.df[feature_cols].sample(n=min(10000, len(self.df)))
        corr_matrix = sample_df.corr()
        
        fig = px.imshow(
            corr_matrix,
            title="Feature Correlation Matrix (Sample)",
            color_continuous_scale='RdBu',
            aspect="auto"
        )
        fig.update_layout(height=600)
        return fig
    
    def create_data_quality_chart(self):
        """Create data quality visualization"""
        quality_metrics = {
            'Complete Records': len(self.df) - self.df.isnull().sum().sum(),
            'Missing Values': self.df.isnull().sum().sum(),
            'Duplicate Records': self.df.duplicated().sum(),
            'Unique Records': len(self.df) - self.df.duplicated().sum()
        }
        
        fig = px.bar(
            x=list(quality_metrics.keys()),
            y=list(quality_metrics.values()),
            title="Data Quality Metrics",
            color=list(quality_metrics.values()),
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            title_font_size=20,
            xaxis_title="Quality Metrics",
            yaxis_title="Count",
            height=400
        )
        return fig
    
    def generate_statistical_report(self):
        """Generate comprehensive statistical report"""
        report = {
            "executive_summary": self.generate_executive_summary(),
            "attack_distribution": self.df['Attack_type'].value_counts().to_dict(),
            "class_distribution": self.df['Attack_label'].value_counts().to_dict(),
            "feature_analysis": {
                "total_features": len(self.df.columns),
                "numeric_features": len(self.df.select_dtypes(include=[np.number]).columns),
                "categorical_features": len(self.df.select_dtypes(include=['object']).columns)
            },
            "data_insights": {
                "most_common_attack": self.df['Attack_type'].value_counts().index[0],
                "least_common_attack": self.df['Attack_type'].value_counts().index[-1],
                "class_imbalance_ratio": round(
                    (self.df['Attack_label'] == 1).sum() / (self.df['Attack_label'] == 0).sum(), 2
                )
            }
        }
        return report
    
    def create_dashboard_html(self):
        """Create complete HTML dashboard"""
        # Generate all charts
        attack_dist_fig = self.create_attack_distribution_chart()
        class_balance_fig = self.create_class_balance_chart()
        attack_categories_fig = self.create_attack_categories_chart()
        feature_analysis_fig = self.create_feature_analysis()
        data_quality_fig = self.create_data_quality_chart()
        
        # Generate report
        report = self.generate_statistical_report()
        
        # Convert figures to HTML divs
        attack_dist_div = attack_dist_fig.to_html(include_plotlyjs=False, div_id="attack-distribution")
        class_balance_div = class_balance_fig.to_html(include_plotlyjs=False, div_id="class-balance")
        attack_categories_div = attack_categories_fig.to_html(include_plotlyjs=False, div_id="attack-categories")
        feature_analysis_div = feature_analysis_fig.to_html(include_plotlyjs=False, div_id="feature-analysis")
        data_quality_div = data_quality_fig.to_html(include_plotlyjs=False, div_id="data-quality")
        
        # Create HTML template
        html_template = f"""
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
                        <div class="value">{report['executive_summary']['total_records']:,}</div>
                        <div class="label">Data Points</div>
                    </div>
                    <div class="card">
                        <h3>Features</h3>
                        <div class="value">{report['executive_summary']['total_features']}</div>
                        <div class="label">Attributes</div>
                    </div>
                    <div class="card">
                        <h3>Attack Types</h3>
                        <div class="value">{report['executive_summary']['attack_types']}</div>
                        <div class="label">Categories</div>
                    </div>
                    <div class="card">
                        <h3>Data Quality</h3>
                        <div class="value">{report['executive_summary']['data_quality']['completeness']}%</div>
                        <div class="label">Complete</div>
                    </div>
                    <div class="card">
                        <h3>Normal Traffic</h3>
                        <div class="value">{report['executive_summary']['normal_percentage']}%</div>
                        <div class="label">of Dataset</div>
                    </div>
                    <div class="card">
                        <h3>Attack Traffic</h3>
                        <div class="value">{report['executive_summary']['attack_percentage']}%</div>
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
                        <div class="chart-title">🔍 Feature Correlation Matrix</div>
                        <div id="feature-analysis"></div>
                    </div>
                    
                    <div class="chart-container">
                        <div class="chart-title">✅ Data Quality Metrics</div>
                        <div id="data-quality"></div>
                    </div>
                </div>
                
                <div class="insights">
                    <h3>💡 Key Insights for Your Business</h3>
                    <ul>
                        <li><strong>Dataset Size:</strong> {report['executive_summary']['total_records']:,} records provide robust training data for ML models</li>
                        <li><strong>Attack Coverage:</strong> {report['executive_summary']['attack_types']} different attack types ensure comprehensive security coverage</li>
                        <li><strong>Data Quality:</strong> {report['executive_summary']['data_quality']['completeness']}% completeness means minimal data preprocessing needed</li>
                        <li><strong>Class Distribution:</strong> {report['executive_summary']['attack_percentage']}% attack vs {report['executive_summary']['normal_percentage']}% normal traffic</li>
                        <li><strong>Most Common Attack:</strong> {report['data_insights']['most_common_attack']} requires immediate attention</li>
                        <li><strong>Imbalance Ratio:</strong> {report['data_insights']['class_imbalance_ratio']}:1 ratio suggests need for balanced sampling</li>
                    </ul>
                </div>
                
                <div class="footer">
                    <p>📈 Generated by AI-Powered Dataset Analysis | Edge-IIoTset Cybersecurity Research</p>
                    <p>🔗 <a href="https://github.com/Asadrammy" style="color: #3498db;">GitHub Repository</a> | 📧 Contact: +92 314 0479594</p>
                </div>
            </div>
            
            <script>
                // Attack Distribution Chart
                {attack_dist_div}
                
                // Class Balance Chart
                {class_balance_div}
                
                // Attack Categories Chart
                {attack_categories_div}
                
                // Feature Analysis Chart
                {feature_analysis_div}
                
                // Data Quality Chart
                {data_quality_div}
            </script>
        </body>
        </html>
        """
        
        return html_template

def main():
    """Main function to generate dashboard"""
    print("🚀 Creating Interactive Dashboard for Edge-IIoTset Dataset...")
    
    # Initialize analyzer
    analyzer = DatasetAnalyzer("Edge-IIoTset dataset/Selected dataset for ML and DL/ML-EdgeIIoT-dataset.csv")
    
    # Generate dashboard HTML
    dashboard_html = analyzer.create_dashboard_html()
    
    # Save dashboard
    with open("edge_iiotset_dashboard.html", "w", encoding="utf-8") as f:
        f.write(dashboard_html)
    
    print("✅ Dashboard created: edge_iiotset_dashboard.html")
    
    # Generate JSON report for API
    report = analyzer.generate_statistical_report()
    with open("dataset_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    
    print("✅ Report generated: dataset_report.json")
    print("\n📊 Dashboard Features:")
    print("  - Interactive visualizations")
    print("  - Executive summary")
    print("  - Statistical analysis")
    print("  - Data quality metrics")
    print("  - Business insights")
    
    return analyzer

if __name__ == "__main__":
    analyzer = main()
