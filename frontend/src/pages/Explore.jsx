import { useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../lib/api';
import { useFetch } from '../lib/useFetch';
import { LoadingSkeleton, ErrorMessage, EmptyState } from '../components/Status';

export default function Explore() {
  const [tab, setTab] = useState('path');

  return (
    <div className="space-y-6">
      <div>
        <h1 className="page-title mb-2">Explore the Network</h1>
        <p className="text-gray-500 text-sm">
          Multi-hop traversals and graph-native queries that a relational database would struggle with.
        </p>
      </div>

      <div className="flex gap-2 border-b border-gray-200 pb-2">
        {[
          { id: 'path', label: 'Collaboration Path' },
          { id: 'influence', label: 'Influence Network' },
          { id: 'interdisciplinary', label: 'Interdisciplinary' },
        ].map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              tab === t.id ? 'bg-primary-600 text-white' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {tab === 'path' && <CollaborationPathFinder />}
      {tab === 'influence' && <InfluenceNetworkExplorer />}
      {tab === 'interdisciplinary' && <InterdisciplinaryView />}
    </div>
  );
}

function CollaborationPathFinder() {
  const { data: authors, loading: authorsLoading } = useFetch(() => api.getAuthors(50));
  const [fromId, setFromId] = useState('');
  const [toId, setToId] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const findPath = async () => {
    if (!fromId || !toId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.findCollaborationPath(fromId, toId);
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="card p-6">
        <h2 className="section-title mb-2">Find Collaboration Path</h2>
        <p className="text-xs text-gray-500 mb-4">
          Multi-hop traversal: find the shortest path connecting two researchers through co-authorship and direct collaborations.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 items-end">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">From Author</label>
            <select value={fromId} onChange={(e) => setFromId(e.target.value)} className="input">
              <option value="">Select author...</option>
              {authors?.map((a) => (
                <option key={a.id} value={a.id}>{a.name}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">To Author</label>
            <select value={toId} onChange={(e) => setToId(e.target.value)} className="input">
              <option value="">Select author...</option>
              {authors?.map((a) => (
                <option key={a.id} value={a.id}>{a.name}</option>
              ))}
            </select>
          </div>
          <button onClick={findPath} disabled={!fromId || !toId || loading} className="btn-primary">
            {loading ? 'Finding...' : 'Find Path'}
          </button>
        </div>
      </div>

      {error && <ErrorMessage message={error} />}

      {result && (
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="section-title">Path Found</h3>
            <span className="badge-amber">Length: {result.path_length} hops</span>
          </div>

          {result.path_length === 0 ? (
            <p className="text-sm text-gray-500">No path found between these authors.</p>
          ) : (
            <div className="flex flex-wrap items-center gap-2">
              {result.path_nodes?.map((node, i) => (
                <div key={i} className="flex items-center gap-2">
                  {i > 0 && (
                    <div className="flex items-center gap-1 text-xs text-gray-400">
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                      <span className="text-[10px]">{result.path_relationships?.[i - 1]}</span>
                    </div>
                  )}
                  <div className={`px-3 py-2 rounded-lg text-sm font-medium border ${
                    node.type === 'Author'
                      ? 'bg-primary-50 border-primary-200 text-primary-800'
                      : 'bg-green-50 border-green-200 text-green-800'
                  }`}>
                    {node.name}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function InfluenceNetworkExplorer() {
  const { data: papers, loading: papersLoading } = useFetch(() => api.getPapers(50));
  const [paperId, setPaperId] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const findInfluence = async () => {
    if (!paperId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.getInfluenceNetwork(paperId);
      setResults(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="card p-6">
        <h2 className="section-title mb-2">Influence Network</h2>
        <p className="text-xs text-gray-500 mb-4">
          Awkward in relational: find all papers that influenced a given paper through multi-hop citation chains.
          This requires recursive traversal that relational databases handle poorly.
        </p>

        <div className="flex gap-4 items-end">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-1">Select Paper</label>
            <select value={paperId} onChange={(e) => setPaperId(e.target.value)} className="input">
              <option value="">Select paper...</option>
              {papers?.map((p) => (
                <option key={p.id} value={p.id}>{p.title} ({p.year})</option>
              ))}
            </select>
          </div>
          <button onClick={findInfluence} disabled={!paperId || loading} className="btn-primary">
            {loading ? 'Searching...' : 'Find Influences'}
          </button>
        </div>
      </div>

      {error && <ErrorMessage message={error} />}

      {results && (
        <div className="space-y-3">
          {results.length === 0 ? (
            <EmptyState message="No influence network found for this paper" />
          ) : (
            results.map((r) => (
              <Link key={r.id} to={`/papers/${r.id}`} className="card p-4 block hover:border-primary-300">
                <div className="flex items-start justify-between">
                  <div className="min-w-0">
                    <h3 className="text-sm font-semibold text-gray-900">{r.title}</h3>
                    <p className="text-xs text-gray-500 mt-1">
                      {r.authors?.join(', ')} &middot; {r.year}
                    </p>
                    <div className="flex flex-wrap gap-1 mt-2">
                      {r.topics?.map((t) => (
                        <span key={t} className="text-[10px] bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded">{t}</span>
                      ))}
                    </div>
                  </div>
                  <span className="badge-amber shrink-0 ml-2">depth: {r.influence_depth}</span>
                </div>
              </Link>
            ))
          )}
        </div>
      )}
    </div>
  );
}

function InterdisciplinaryView() {
  const { data: authors, loading, error } = useFetch(() => api.getInterdisciplinary());

  return (
    <div className="space-y-4">
      <div className="card p-6">
        <h2 className="section-title mb-2">Interdisciplinary Researchers</h2>
        <p className="text-xs text-gray-500">
          Authors whose papers span multiple research topics — a natural graph query finding
          nodes with diverse relationship types.
        </p>
      </div>

      {loading && <LoadingSkeleton rows={4} type="table" />}
      {error && <ErrorMessage message={error} />}
      {!loading && !error && authors?.length === 0 && (
        <EmptyState message="No interdisciplinary researchers found" />
      )}
      {!loading && !error && authors?.length > 0 && (
        <div className="space-y-3">
          {authors.map((a) => (
            <Link key={a.id} to={`/authors/${a.id}`} className="card p-5 block hover:border-primary-300">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-500 to-primary-300 flex items-center justify-center text-white text-sm font-semibold">
                    {a.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-gray-900">{a.name}</h3>
                    <p className="text-xs text-gray-500">{a.paper_count} papers &middot; {a.topic_count} topics</p>
                  </div>
                </div>
                <span className="badge-purple">h: {a.h_index}</span>
              </div>
              <div className="flex flex-wrap gap-1 mt-3 ml-13">
                {a.topics?.map((t) => (
                  <span key={t} className="text-[10px] bg-primary-50 text-primary-700 px-2 py-0.5 rounded-full">{t}</span>
                ))}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
