import { useState } from 'react';
import { uploadFile, pollJobStatus } from '../services/api';

export default function UploadZone({ onAnalysisComplete }) {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('');

  const handleFileSelect = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    setStatus('Uploading...');

    try {
      const { job_id } = await uploadFile(file, setProgress);
      setStatus('Processing...');
      
      pollJobStatus(job_id, (data) => {
        if (data.status === 'completed') {
          setStatus('Complete!');
          setUploading(false);
          onAnalysisComplete(data.result);
        } else if (data.status === 'failed') {
          setStatus(`Error: ${data.error}`);
          setUploading(false);
        } else {
          setStatus(`Processing... (${data.status})`);
        }
      });
    } catch (error) {
      setStatus(`Error: ${error.message}`);
      setUploading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.uploadBox}>
        <h2>📊 Upload Your Dataset</h2>
        <p>Supports CSV, Excel, JSON files</p>
        
        <input
          type="file"
          accept=".csv,.xlsx,.xls,.json"
          onChange={handleFileSelect}
          disabled={uploading}
          style={styles.input}
        />
        
        {uploading && (
          <div style={styles.progress}>
            <div style={{...styles.progressBar, width: `${progress}%`}} />
            <p>{status}</p>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: { padding: '40px', textAlign: 'center' },
  uploadBox: { maxWidth: '600px', margin: '0 auto', padding: '40px', border: '2px dashed #0ea5e9', borderRadius: '12px', background: 'white' },
  input: { padding: '12px', fontSize: '16px', cursor: 'pointer' },
  progress: { marginTop: '20px' },
  progressBar: { height: '8px', background: '#0ea5e9', borderRadius: '4px', transition: 'width 0.3s' }
};
