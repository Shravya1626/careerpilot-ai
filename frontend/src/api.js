const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

async function request(path, payload, { loading, errorHandler } = {}) {
  if (loading) loading(true);
  try {
    const response = await fetch(`${API_URL}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.detail || 'Request failed');
    }

    const data = await response.json();
    return data;
  } catch (err) {
    if (errorHandler) errorHandler(err.message || 'Unexpected error');
    throw err;
  } finally {
    if (loading) loading(false);
  }
}

export async function analyzeProfile(profile, { loading, errorHandler } = {}) {
  return request('/api/analyze', profile, { loading, errorHandler });
}

export async function searchOpportunities(profile, category, { loading, errorHandler } = {}) {
  return request('/api/opportunities', { profile, category }, { loading, errorHandler });
}

export async function generateProjects(profile, analysis, { loading, errorHandler } = {}) {
  return request('/api/projects', { profile, analysis }, { loading, errorHandler });
}

export async function generateRoadmap(profile, analysis, { loading, errorHandler } = {}) {
  return request('/api/roadmap', { profile, analysis }, { loading, errorHandler });
}
