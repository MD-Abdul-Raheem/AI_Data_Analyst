import React, { useState } from 'react';
import Papa from 'papaparse';
import * as XLSX from 'xlsx';
import { Upload, FileSpreadsheet, BarChart3, Brain, Code, Database, TrendingUp, Download, Loader2, CheckCircle2, AlertCircle, Copy, Check } from 'lucide-react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { BarChart, Bar, LineChart, Line, ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import * as math from 'mathjs';

const GEMINI_API_KEY = 'AIzaSyDj7q6p1Y4Yz4MI6COBdvGCS7CV0D-vFoE';
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';

function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState([]);
  const [columns, setColumns] = useState([]);
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);
  const [statistics, setStatistics] = useState(null);
  const [copiedCode, setCopiedCode] = useState(null);

  const analysisOptions = [
    { id: 'stats', label: 'Basic Statistics', icon: BarChart3 },
    { id: 'advanced', label: 'Advanced Statistics & Hypothesis Testing', icon: TrendingUp },
    { id: 'ml', label: 'Machine Learning Recommendations', icon: Brain },
    { id: 'viz', label: 'Data Visualization Strategy', icon: BarChart3 },
    { id: 'python', label: 'Python Code Generation', icon: Code },
    { id: 'sql', label: 'SQL Queries', icon: Database },
    { id: 'excel', label: 'Excel Formulas', icon: FileSpreadsheet },
    { id: 'insights', label: 'Business Insights', icon: TrendingUp },
    { id: 'quality', label: 'Data Quality Report', icon: CheckCircle2 },
  ];

  const [selectedOptions, setSelectedOptions] = useState(analysisOptions.map(o => o.id));

  const handleFileUpload = (e) => {
    const uploadedFile = e.target.files?.[0];
    if (!uploadedFile) return;

    setFile(uploadedFile);
    setError(null);
    setAnalysis(null);

    const fileExtension = uploadedFile.name.split('.').pop().toLowerCase();

    if (fileExtension === 'csv') {
      Papa.parse(uploadedFile, {
        header: true,
        skipEmptyLines: true,
        complete: (results) => {
          setData(results.data);
          setColumns(results.meta.fields || []);
          calculateStatistics(results.data, results.meta.fields || []);
        },
        error: (error) => setError('Error parsing CSV: ' + error.message)
      });
    } else if (['xlsx', 'xls'].includes(fileExtension)) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const workbook = XLSX.read(e.target.result, { type: 'binary' });
          const sheetName = workbook.SheetNames[0];
          const worksheet = workbook.Sheets[sheetName];
          const jsonData = XLSX.utils.sheet_to_json(worksheet);
          setData(jsonData);
          const cols = jsonData.length > 0 ? Object.keys(jsonData[0]) : [];
          setColumns(cols);
          calculateStatistics(jsonData, cols);
        } catch (err) {
          setError('Error parsing Excel: ' + err.message);
        }
      };
      reader.readAsBinaryString(uploadedFile);
    } else {
      setError('Unsupported file format. Please upload CSV or Excel files.');
    }
  };

  const calculateStatistics = (dataset, cols) => {
    const numericCols = cols.filter(col => {
      const values = dataset.map(row => row[col]).filter(v => v !== null && v !== undefined && v !== '');
      return values.length > 0 && !isNaN(Number(values[0]));
    });

    const stats = {};
    numericCols.forEach(col => {
      const values = dataset.map(row => Number(row[col])).filter(v => !isNaN(v));
      if (values.length > 0) {
        stats[col] = {
          mean: math.mean(values),
          median: math.median(values),
          std: math.std(values),
          min: math.min(values),
          max: math.max(values),
          count: values.length
        };
      }
    });

    setStatistics(stats);
  };

  const analyzeData = async () => {
    if (!data.length) {
      setError('No data to analyze');
      return;
    }

    setLoading(true);
    setError(null);
    setProgress(10);

    const preview = data.slice(0, 5);
    
    const prompt = `You are a SENIOR DATA ANALYST with expertise in Excel, Python, R, SQL, Statistics, Machine Learning, and Data Visualization. You have mastered all skills from the professional Data Analyst Roadmap.

I have uploaded a dataset with ${data.length} rows and ${columns.length} columns.

COLUMNS: ${columns.join(', ')}

DATA PREVIEW (first 5 rows):
${JSON.stringify(preview, null, 2)}

Perform a COMPREHENSIVE PROFESSIONAL DATA ANALYSIS covering ALL aspects:

═══════════════════════════════════════════════════════════════════
1. DATA QUALITY ASSESSMENT & CLEANUP RECOMMENDATIONS
═══════════════════════════════════════════════════════════════════
- Analyze data types for each column
- Identify missing values (count and percentage)
- Detect duplicates
- Find outliers using statistical methods (IQR, Z-score)
- Data transformation needs
- Provide Python/Pandas code for cleanup:
  * Handling missing data (imputation strategies)
  * Removing duplicates
  * Outlier treatment
  * Data type conversions

═══════════════════════════════════════════════════════════════════
2. EXCEL ANALYSIS & FORMULAS
═══════════════════════════════════════════════════════════════════
Suggest Excel formulas for common operations:
- IF statements for business logic
- VLOOKUP/HLOOKUP for data matching
- AVERAGE, SUM, COUNT, MIN/MAX calculations
- Date functions (DATEDIF, DATE, MONTH, YEAR)
- Text functions (CONCAT, TRIM, UPPER, LOWER)
- Pivot table structure recommendations
- Chart types for each analysis need

═══════════════════════════════════════════════════════════════════
3. COMPREHENSIVE STATISTICAL ANALYSIS
═══════════════════════════════════════════════════════════════════

A) DESCRIPTIVE STATISTICS (for ALL numeric columns):
   - Mean, Median, Mode (Central Tendency)
   - Range, Variance, Standard Deviation (Dispersion)
   - Skewness, Kurtosis (Distribution shape)
   - Quartiles (Q1, Q2, Q3)
   - Present in a clear table format

B) CORRELATION ANALYSIS:
   - Calculate correlation between numeric variables
   - Identify strong correlations (positive/negative)
   - Recommend scatter plots for visualization

C) DISTRIBUTION ANALYSIS:
   - Analyze distribution of key variables
   - Identify normal vs skewed distributions
   - Recommend transformations if needed

D) HYPOTHESIS TESTING:
   - Suggest 3-5 testable hypotheses from the data
   - Recommend appropriate statistical tests
   - Expected outcomes and interpretations

E) REGRESSION ANALYSIS:
   - Identify potential dependent variables
   - Suggest independent variables
   - Linear/Logistic regression recommendations
   - Predictive modeling opportunities

═══════════════════════════════════════════════════════════════════
4. MACHINE LEARNING RECOMMENDATIONS
═══════════════════════════════════════════════════════════════════

Based on the data structure, recommend:

A) SUPERVISED LEARNING (if applicable):
   Classification Problems:
   - Logistic Regression: [when to use]
   - Decision Trees: [when to use]
   - K-Nearest Neighbors (KNN): [when to use]
   - Naive Bayes: [when to use]
   
   Regression Problems:
   - Linear Regression: [when to use]
   - Polynomial Regression: [when to use]

B) UNSUPERVISED LEARNING:
   - K-Means Clustering for segmentation
   - Number of clusters to test
   - Features to use for clustering

C) FEATURE ENGINEERING:
   - Important features identified
   - Feature transformations needed
   - Categorical encoding strategies

D) MODEL EVALUATION STRATEGY:
   - Train/Test split ratio (80/20 or 70/30)
   - Evaluation metrics to use
   - Cross-validation approach

E) PROVIDE PYTHON CODE:
   Complete scikit-learn implementation with:
   - Data preprocessing
   - Model training
   - Evaluation
   - Predictions

═══════════════════════════════════════════════════════════════════
5. DATA VISUALIZATION STRATEGY
═══════════════════════════════════════════════════════════════════

Recommend 8-10 SPECIFIC visualizations:

For each visualization specify:
- Chart Type (Bar, Line, Scatter, Histogram, Heatmap, Pie, Funnel, Box Plot)
- X-axis and Y-axis variables
- What insight it reveals
- Tool recommendation (Tableau/Power BI/Python)
- Color schemes and styling tips

Examples:
1. Bar Chart: [Column A] vs [Column B] - Shows comparison of categories
2. Line Chart: [Date] vs [Sales] - Shows trend over time
3. Scatter Plot: [Column X] vs [Column Y] - Shows correlation
4. Histogram: [Column Z] - Shows distribution
5. Heatmap: Correlation matrix of all numeric columns
... continue for 8-10 visualizations

═══════════════════════════════════════════════════════════════════
6. PYTHON CODE GENERATION (Complete & Executable)
═══════════════════════════════════════════════════════════════════

Provide complete Python scripts for:

A) DATA CLEANING SCRIPT:
\`\`\`python
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('your_file.csv')

# [Complete cleanup code with comments]
\`\`\`

B) STATISTICAL ANALYSIS SCRIPT:
\`\`\`python
# Calculate all descriptive statistics
# Correlation analysis
# Distribution analysis
\`\`\`

C) VISUALIZATION SCRIPT:
\`\`\`python
import matplotlib.pyplot as plt
import seaborn as sns

# [Complete visualization code for top 5 charts]
\`\`\`

D) MACHINE LEARNING SCRIPT:
\`\`\`python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# [Complete ML pipeline]
\`\`\`

═══════════════════════════════════════════════════════════════════
7. SQL ANALYSIS QUERIES
═══════════════════════════════════════════════════════════════════

Generate SQL queries for common analysis tasks:
\`\`\`sql
-- Query 1: Basic aggregations
SELECT column_name, COUNT(*), AVG(value)
FROM table_name
GROUP BY column_name;

-- Query 2: Top performers
-- Query 3: Trend analysis
-- Query 4: Complex joins (if multiple tables implied)
-- Query 5: Window functions for rankings
\`\`\`

═══════════════════════════════════════════════════════════════════
8. BUSINESS INSIGHTS & RECOMMENDATIONS
═══════════════════════════════════════════════════════════════════

Provide 8-10 actionable business recommendations:
1. [Specific insight with data backing]
2. [Trend identified and what it means]
3. [Opportunity for optimization]
4. [Risk or concern to address]
5. [Customer segment insights]
6. [Revenue/profit optimization strategy]
7. [Operational efficiency improvements]
8. [Predictive insights for planning]
9. [Benchmarking against industry standards]
10. [KPI tracking recommendations]

═══════════════════════════════════════════════════════════════════
9. ADVANCED TOPICS (if applicable)
═══════════════════════════════════════════════════════════════════

- Big Data considerations (if dataset is large)
- Deep Learning opportunities (Neural Networks for complex patterns)
- Time Series Forecasting (if temporal data exists)
- Natural Language Processing (if text data exists)
- A/B Testing frameworks
- Customer Lifetime Value predictions

═══════════════════════════════════════════════════════════════════
10. PROJECT PORTFOLIO RECOMMENDATIONS
═══════════════════════════════════════════════════════════════════

Suggest how to present this analysis:
- Dashboard layout for Tableau/Power BI
- Jupyter Notebook structure
- Executive summary format
- Technical documentation outline
- Presentation storytelling flow

═══════════════════════════════════════════════════════════════════
FORMAT YOUR RESPONSE
═══════════════════════════════════════════════════════════════════

Use clear markdown headers:
# SECTION TITLE
## Subsection
### Details

Include:
- Tables for statistics
- Code blocks with syntax highlighting
- Bullet points for lists
- Bold for emphasis
- Numbers and percentages for precision

Make it comprehensive, professional, and immediately actionable. This should be a complete analysis that a senior data analyst would deliver to stakeholders.`;

    try {
      setProgress(30);
      const response = await fetch(`${GEMINI_API_URL}?key=${GEMINI_API_KEY}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: {
            temperature: 0.7,
            maxOutputTokens: 8000,
          }
        })
      });

      setProgress(70);

      if (!response.ok) {
        const errorData = await response.json();
        console.error('API Error:', errorData);
        throw new Error(`API Error: ${response.status} - ${JSON.stringify(errorData)}`);
      }

      const result = await response.json();
      console.log('API Response:', result);
      setProgress(90);
      
      const analysisText = result.candidates?.[0]?.content?.parts?.[0]?.text || 'No analysis generated';
      console.log('Analysis Text Length:', analysisText.length);
      setAnalysis(analysisText);
      setProgress(100);
      setActiveTab('overview');
    } catch (err) {
      console.error('Analysis Error:', err);
      setError('Analysis failed: ' + err.message);
    } finally {
      setLoading(false);
      setTimeout(() => setProgress(0), 1000);
    }
  };

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedCode(id);
    setTimeout(() => setCopiedCode(null), 2000);
  };

  const extractCodeBlocks = (text) => {
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    const blocks = [];
    let match;
    while ((match = codeBlockRegex.exec(text)) !== null) {
      blocks.push({
        language: match[1] || 'text',
        code: match[2].trim()
      });
    }
    return blocks;
  };

  const parseAnalysisSections = (text) => {
    if (!text) return {};
    
    const sections = {
      overview: '',
      quality: '',
      excel: '',
      statistics: '',
      ml: '',
      visualization: '',
      python: '',
      sql: '',
      insights: '',
      advanced: '',
      portfolio: ''
    };

    const lines = text.split('\n');
    let currentSection = 'overview';
    
    lines.forEach(line => {
      if (line.includes('DATA QUALITY') || line.includes('CLEANUP')) currentSection = 'quality';
      else if (line.includes('EXCEL')) currentSection = 'excel';
      else if (line.includes('STATISTICAL ANALYSIS')) currentSection = 'statistics';
      else if (line.includes('MACHINE LEARNING')) currentSection = 'ml';
      else if (line.includes('VISUALIZATION STRATEGY')) currentSection = 'visualization';
      else if (line.includes('PYTHON CODE')) currentSection = 'python';
      else if (line.includes('SQL')) currentSection = 'sql';
      else if (line.includes('BUSINESS INSIGHTS')) currentSection = 'insights';
      else if (line.includes('ADVANCED TOPICS')) currentSection = 'advanced';
      else if (line.includes('PORTFOLIO')) currentSection = 'portfolio';
      
      sections[currentSection] += line + '\n';
    });

    return sections;
  };

  const sections = analysis ? parseAnalysisSections(analysis) : {};
  const codeBlocks = analysis ? extractCodeBlocks(analysis) : [];

  const tabs = [
    { id: 'overview', label: 'Overview', icon: BarChart3 },
    { id: 'quality', label: 'Data Quality', icon: CheckCircle2 },
    { id: 'statistics', label: 'Statistics', icon: TrendingUp },
    { id: 'ml', label: 'Machine Learning', icon: Brain },
    { id: 'visualization', label: 'Visualizations', icon: BarChart3 },
    { id: 'code', label: 'Code', icon: Code },
    { id: 'sql', label: 'SQL', icon: Database },
    { id: 'excel', label: 'Excel', icon: FileSpreadsheet },
    { id: 'insights', label: 'Insights', icon: TrendingUp },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-white mb-4 flex items-center justify-center gap-3">
            <Brain className="w-12 h-12 text-purple-400" />
            Advanced AI Data Analyst
          </h1>
          <p className="text-xl text-purple-200">Professional-Grade Data Analysis Platform</p>
          <p className="text-sm text-purple-300 mt-2">Excel • Python • SQL • Statistics • Machine Learning • Visualization</p>
        </div>

        {/* Upload Section */}
        {!data.length && (
          <div className="max-w-2xl mx-auto">
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-purple-500/30">
              <div className="text-center mb-6">
                <Upload className="w-16 h-16 text-purple-400 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-white mb-2">Upload Your Dataset</h2>
                <p className="text-purple-200">Supports CSV, Excel (.xlsx, .xls)</p>
              </div>
              
              <label className="block">
                <div className="border-2 border-dashed border-purple-400 rounded-xl p-12 text-center cursor-pointer hover:border-purple-300 hover:bg-white/5 transition">
                  <FileSpreadsheet className="w-12 h-12 text-purple-400 mx-auto mb-4" />
                  <p className="text-white font-semibold mb-2">Click to upload or drag and drop</p>
                  <p className="text-purple-300 text-sm">Maximum file size: 100MB</p>
                  <input
                    type="file"
                    accept=".csv,.xlsx,.xls"
                    onChange={handleFileUpload}
                    className="hidden"
                  />
                </div>
              </label>

              {error && (
                <div className="mt-4 p-4 bg-red-500/20 border border-red-500 rounded-lg flex items-center gap-2 text-red-200">
                  <AlertCircle className="w-5 h-5" />
                  {error}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Data Preview & Analysis */}
        {data.length > 0 && (
          <div className="space-y-6">
            {/* Data Info Card */}
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-purple-500/30">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-xl font-bold text-white mb-2">{file?.name}</h3>
                  <p className="text-purple-200">
                    {data.length.toLocaleString()} rows × {columns.length} columns
                  </p>
                </div>
                <button
                  onClick={() => {
                    setFile(null);
                    setData([]);
                    setColumns([]);
                    setAnalysis(null);
                    setError(null);
                  }}
                  className="px-4 py-2 bg-red-500/20 text-red-200 rounded-lg hover:bg-red-500/30 transition"
                >
                  Clear Data
                </button>
              </div>

              {/* Data Preview Table */}
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-purple-500/30">
                      {columns.slice(0, 8).map(col => (
                        <th key={col} className="text-left p-2 text-purple-200 font-semibold">
                          {col}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {data.slice(0, 5).map((row, idx) => (
                      <tr key={idx} className="border-b border-purple-500/10">
                        {columns.slice(0, 8).map(col => (
                          <td key={col} className="p-2 text-white">
                            {String(row[col] || '').slice(0, 50)}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Quick Statistics */}
            {statistics && Object.keys(statistics).length > 0 && (
              <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-purple-500/30">
                <h3 className="text-xl font-bold text-white mb-4">Quick Statistics</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {Object.entries(statistics).slice(0, 6).map(([col, stats]) => (
                    <div key={col} className="bg-white/5 rounded-lg p-4">
                      <h4 className="text-purple-300 font-semibold mb-2">{col}</h4>
                      <div className="space-y-1 text-sm">
                        <div className="flex justify-between text-white">
                          <span>Mean:</span>
                          <span className="font-mono">{stats.mean.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between text-white">
                          <span>Median:</span>
                          <span className="font-mono">{stats.median.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between text-white">
                          <span>Std Dev:</span>
                          <span className="font-mono">{stats.std.toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between text-purple-200">
                          <span>Range:</span>
                          <span className="font-mono">{stats.min.toFixed(1)} - {stats.max.toFixed(1)}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Analyze Button */}
            {!analysis && (
              <div className="text-center">
                <button
                  onClick={analyzeData}
                  disabled={loading}
                  className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl font-bold text-lg hover:from-purple-700 hover:to-pink-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-3 mx-auto"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-6 h-6 animate-spin" />
                      Analyzing... {progress}%
                    </>
                  ) : (
                    <>
                      <Brain className="w-6 h-6" />
                      Start Comprehensive Analysis
                    </>
                  )}
                </button>
                {loading && (
                  <div className="mt-4 max-w-md mx-auto">
                    <div className="bg-white/10 rounded-full h-2 overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-purple-500 to-pink-500 h-full transition-all duration-500"
                        style={{ width: `${progress}%` }}
                      />
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Analysis Results */}
            {analysis && (
              <div className="bg-white/10 backdrop-blur-lg rounded-xl border border-purple-500/30 overflow-hidden">
                <div className="bg-green-500/20 border-b border-green-500/30 p-4 flex items-center gap-3">
                  <CheckCircle2 className="w-6 h-6 text-green-400" />
                  <div>
                    <h3 className="text-white font-bold">Analysis Complete!</h3>
                    <p className="text-green-200 text-sm">Comprehensive report generated with {codeBlocks.length} code blocks</p>
                  </div>
                </div>
                {/* Tabs */}
                <div className="flex overflow-x-auto scrollbar-hide border-b border-purple-500/30">
                  {tabs.map(tab => {
                    const Icon = tab.icon;
                    return (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`flex items-center gap-2 px-6 py-4 font-semibold whitespace-nowrap transition ${
                          activeTab === tab.id
                            ? 'bg-purple-600 text-white'
                            : 'text-purple-200 hover:bg-white/5'
                        }`}
                      >
                        <Icon className="w-5 h-5" />
                        {tab.label}
                      </button>
                    );
                  })}
                </div>

                {/* Tab Content */}
                <div className="p-6 max-h-[600px] overflow-y-auto">
                  {activeTab === 'code' && (
                    <div className="space-y-6">
                      <h3 className="text-2xl font-bold text-white mb-4">Generated Code</h3>
                      {codeBlocks.map((block, idx) => (
                        <div key={idx} className="relative">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-purple-300 font-semibold uppercase text-sm">
                              {block.language}
                            </span>
                            <button
                              onClick={() => copyToClipboard(block.code, `code-${idx}`)}
                              className="flex items-center gap-2 px-3 py-1 bg-white/10 hover:bg-white/20 rounded text-white text-sm transition"
                            >
                              {copiedCode === `code-${idx}` ? (
                                <>
                                  <Check className="w-4 h-4" />
                                  Copied!
                                </>
                              ) : (
                                <>
                                  <Copy className="w-4 h-4" />
                                  Copy
                                </>
                              )}
                            </button>
                          </div>
                          <SyntaxHighlighter
                            language={block.language}
                            style={vscDarkPlus}
                            customStyle={{
                              borderRadius: '0.5rem',
                              fontSize: '0.875rem',
                              maxHeight: '400px'
                            }}
                          >
                            {block.code}
                          </SyntaxHighlighter>
                        </div>
                      ))}
                    </div>
                  )}

                  {activeTab !== 'code' && (
                    <div className="prose prose-invert max-w-none">
                      <div className="text-white" style={{ whiteSpace: 'pre-wrap', lineHeight: '1.8' }}>
                        {sections[activeTab] || analysis}
                      </div>
                    </div>
                  )}
                </div>

                {/* Download Options */}
                <div className="border-t border-purple-500/30 p-4 flex gap-3 flex-wrap">
                  <button className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition">
                    <Download className="w-4 h-4" />
                    Download Report (PDF)
                  </button>
                  <button className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition">
                    <Download className="w-4 h-4" />
                    Download Notebook (.ipynb)
                  </button>
                  <button className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition">
                    <Download className="w-4 h-4" />
                    Download Python Script
                  </button>
                  <button
                    onClick={() => copyToClipboard(analysis, 'full-analysis')}
                    className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition"
                  >
                    {copiedCode === 'full-analysis' ? (
                      <>
                        <Check className="w-4 h-4" />
                        Copied!
                      </>
                    ) : (
                      <>
                        <Copy className="w-4 h-4" />
                        Copy Full Analysis
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
