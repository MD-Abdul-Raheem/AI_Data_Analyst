import { useState } from 'react';
import { downloadNotebook } from '../services/api';

export default function Dashboard({ result }) {
  const [activeTab, setActiveTab] = useState('summary');

  const tabs = [
    { id: 'summary', label: '📋 Summary' },
    { id: 'insights', label: '💡 Insights' },
    { id: 'charts', label: '📊 Charts' },
    { id: 'python', label: '🐍 Python' },
    { id: 'sql', label: '🗄️ SQL' },
    { id: 'dax', label: '📈 DAX' }
  ];

  const handleDownload = () => {
    downloadNotebook(result.notebook);
  };

  return (
    <div style={styles.container}>
      <div style={styles.tabs}>
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{...styles.tab, ...(activeTab === tab.id ? styles.activeTab : {})}}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div style={styles.content}>
        {activeTab === 'summary' && <SummaryView result={result} />}
        {activeTab === 'insights' && <InsightsView insights={result.insights} />}
        {activeTab === 'charts' && <ChartsView charts={result.analysis.charts} />}
        {activeTab === 'python' && <CodeView code={result.python_code} language="python" />}
        {activeTab === 'sql' && <SQLView queries={result.sql_queries} />}
        {activeTab === 'dax' && <DAXView measures={result.dax_measures} />}
      </div>

      <button onClick={handleDownload} style={styles.downloadBtn}>
        📥 Download Notebook
      </button>
    </div>
  );
}

function SummaryView({ result }) {
  return (
    <div>
      <h2>Executive Summary</h2>
      <div style={styles.metrics}>
        <div style={styles.metric}>
          <h3>{result.profile.shape.rows.toLocaleString()}</h3>
          <p>Rows</p>
        </div>
        <div style={styles.metric}>
          <h3>{result.profile.shape.columns}</h3>
          <p>Columns</p>
        </div>
        <div style={styles.metric}>
          <h3>{result.profile.quality_score.toFixed(1)}%</h3>
          <p>Quality Score</p>
        </div>
      </div>
    </div>
  );
}

function InsightsView({ insights }) {
  return (
    <div>
      <h2>Key Insights</h2>
      {insights.map((insight, i) => (
        <div key={i} style={styles.insight}>✓ {insight}</div>
      ))}
    </div>
  );
}

function ChartsView({ charts }) {
  return (
    <div>
      <h2>Visualizations</h2>
      {charts.map((chart, i) => (
        <div key={i} style={styles.chart}>
          <h3>{chart.title}</h3>
          <img src={chart.image} alt={chart.title} style={{maxWidth: '100%'}} />
        </div>
      ))}
    </div>
  );
}

function CodeView({ code, language }) {
  return (
    <div>
      <h2>Generated Code</h2>
      <pre style={styles.code}>{code}</pre>
    </div>
  );
}

function SQLView({ queries }) {
  return (
    <div>
      <h2>SQL Queries</h2>
      {queries.map((q, i) => (
        <div key={i} style={styles.queryBox}>
          <h3>{q.name}</h3>
          <pre style={styles.code}>{q.sql}</pre>
        </div>
      ))}
    </div>
  );
}

function DAXView({ measures }) {
  return (
    <div>
      <h2>DAX Measures</h2>
      {measures.map((m, i) => (
        <div key={i} style={styles.measureBox}>
          <h4>{m.name}</h4>
          <code>{m.dax}</code>
        </div>
      ))}
    </div>
  );
}

const styles = {
  container: { padding: '20px' },
  tabs: { display: 'flex', gap: '10px', marginBottom: '20px', flexWrap: 'wrap' },
  tab: { padding: '12px 24px', border: 'none', background: '#e0f2fe', borderRadius: '8px', cursor: 'pointer', fontSize: '14px' },
  activeTab: { background: '#0ea5e9', color: 'white' },
  content: { background: 'white', padding: '30px', borderRadius: '12px', minHeight: '400px' },
  metrics: { display: 'flex', gap: '20px', justifyContent: 'center', marginTop: '20px' },
  metric: { padding: '20px', background: '#f0f9ff', borderRadius: '8px', textAlign: 'center', minWidth: '150px' },
  insight: { padding: '12px', background: '#f0f9ff', margin: '10px 0', borderRadius: '6px', borderLeft: '4px solid #0ea5e9' },
  chart: { marginBottom: '30px' },
  code: { background: '#1e293b', color: '#e2e8f0', padding: '20px', borderRadius: '8px', overflow: 'auto' },
  queryBox: { marginBottom: '20px' },
  measureBox: { padding: '12px', background: '#f0f9ff', margin: '10px 0', borderRadius: '6px' },
  downloadBtn: { marginTop: '20px', padding: '14px 28px', background: '#0ea5e9', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '16px' }
};
