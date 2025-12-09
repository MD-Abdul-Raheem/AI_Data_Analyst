import { useState } from 'react';
import UploadZone from './components/UploadZone';
import Dashboard from './components/Dashboard';

export default function App() {
  const [result, setResult] = useState(null);

  return (
    <div style={styles.app}>
      <header style={styles.header}>
        <h1>🤖 AI Data Analyst</h1>
        <p>Professional Data Analysis Platform</p>
      </header>

      {!result ? (
        <UploadZone onAnalysisComplete={setResult} />
      ) : (
        <>
          <Dashboard result={result} />
          <button onClick={() => setResult(null)} style={styles.resetBtn}>
            ← Upload New File
          </button>
        </>
      )}
    </div>
  );
}

const styles = {
  app: { minHeight: '100vh', background: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #bae6fd 100%)' },
  header: { textAlign: 'center', padding: '40px 20px', background: 'white', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' },
  resetBtn: { margin: '20px', padding: '12px 24px', background: '#64748b', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer' }
};
