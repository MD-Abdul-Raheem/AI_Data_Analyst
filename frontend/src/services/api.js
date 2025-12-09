import axios from 'axios';

const API_BASE = '/api';

export const uploadFile = async (file, onProgress) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await axios.post(`${API_BASE}/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (e) => onProgress?.(Math.round((e.loaded * 100) / e.total))
  });
  
  return response.data;
};

export const pollJobStatus = async (jobId, onUpdate) => {
  const poll = async () => {
    const response = await axios.get(`${API_BASE}/jobs/${jobId}`);
    const data = response.data;
    
    onUpdate(data);
    
    if (data.status === 'pending' || data.status === 'processing') {
      setTimeout(poll, 2000);
    }
  };
  
  poll();
};

export const downloadNotebook = async (notebook) => {
  const response = await axios.post(`${API_BASE}/download/notebook`, { notebook }, {
    responseType: 'blob'
  });
  
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', 'analysis.ipynb');
  document.body.appendChild(link);
  link.click();
  link.remove();
};
