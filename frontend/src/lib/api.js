const API_BASE = '/api';

async function fetchJSON(url, options = {}) {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

export const api = {
  getStats: () => fetchJSON('/stats'),
  getPapers: (limit = 50) => fetchJSON(`/papers?limit=${limit}`),
  getPaper: (id) => fetchJSON(`/papers/${encodeURIComponent(id)}`),
  getAuthors: (limit = 50) => fetchJSON(`/authors?limit=${limit}`),
  getAuthor: (id) => fetchJSON(`/authors/${encodeURIComponent(id)}`),
  getInstitutions: (limit = 50) => fetchJSON(`/institutions?limit=${limit}`),
  getInstitution: (id) => fetchJSON(`/institutions/${encodeURIComponent(id)}`),
  getTopics: (limit = 50) => fetchJSON(`/topics?limit=${limit}`),
  findCollaborationPath: (from, to) =>
    fetchJSON(`/collaboration-path?from_id=${encodeURIComponent(from)}&to_id=${encodeURIComponent(to)}`),
  getCitationChain: (id, depth = 3) =>
    fetchJSON(`/citation-chain/${encodeURIComponent(id)}?depth=${depth}`),
  getInfluenceNetwork: (id) => fetchJSON(`/influence-network/${encodeURIComponent(id)}`),
  getRecommendations: (id) => fetchJSON(`/recommendations/${encodeURIComponent(id)}`),
  getInterdisciplinary: () => fetchJSON('/interdisciplinary'),
  search: (q) => fetchJSON(`/search?q=${encodeURIComponent(q)}`),
  healthCheck: () => fetchJSON('/health'),
};
