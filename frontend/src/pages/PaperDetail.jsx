import { useParams, Link } from 'react-router-dom';
import { api } from '../lib/api';
import { useFetch } from '../lib/useFetch';
import { LoadingSkeleton, ErrorMessage, EmptyState } from '../components/Status';
import { TopicBadge } from '../components/Cards';

export default function PaperDetail() {
  const { id } = useParams();
  const { data: paper, loading, error } = useFetch(() => api.getPaper(id), [id]);
  const { data: influence } = useFetch(() => api.getInfluenceNetwork(id), [id]);

  if (loading) return <LoadingSkeleton rows={4} type="table" />;
  if (error) return <ErrorMessage message={error} />;
  if (!paper) return <EmptyState message="Paper not found" />;

  return (
    <div className="space-y-6">
      <div>
        <Link to="/papers" className="text-sm text-primary-600 hover:text-primary-700 mb-2 inline-block">
          &larr; All Papers
        </Link>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">{paper.title}</h1>
        <div className="flex flex-wrap items-center gap-3 text-sm text-gray-500">
          <span className="badge-blue">{paper.year}</span>
          <span>{paper.citations_count} citations</span>
        </div>
      </div>

      {paper.abstract && (
        <div className="card p-6">
          <h2 className="section-title mb-2">Abstract</h2>
          <p className="text-sm text-gray-600 leading-relaxed">{paper.abstract}</p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card p-6">
          <h2 className="section-title mb-3">Authors</h2>
          {paper.authors?.length > 0 ? (
            <div className="space-y-2">
              {paper.authors.map((a) => (
                <Link key={a.id} to={`/authors/${a.id}`} className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-500 to-primary-300 flex items-center justify-center text-white text-xs font-semibold">
                    {a.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <span className="text-sm font-medium text-gray-900">{a.name}</span>
                </Link>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-500">No authors listed</p>
          )}
        </div>

        <div className="card p-6">
          <h2 className="section-title mb-3">Topics</h2>
          {paper.topics?.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {paper.topics.map((t) => (
                <TopicBadge key={t.id} topic={t} />
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-500">No topics tagged</p>
          )}
        </div>
      </div>

      {paper.cited_papers?.length > 0 && (
        <div className="card p-6">
          <h2 className="section-title mb-3">References (papers this cites)</h2>
          <div className="space-y-2">
            {paper.cited_papers.map((c) => (
              <Link key={c.id} to={`/papers/${c.id}`} className="block p-3 rounded-lg hover:bg-gray-50 border border-gray-100">
                <span className="text-sm font-medium text-gray-900">{c.title}</span>
              </Link>
            ))}
          </div>
        </div>
      )}

      {paper.citing_papers?.length > 0 && (
        <div className="card p-6">
          <h2 className="section-title mb-3">Cited By (papers that cite this)</h2>
          <div className="space-y-2">
            {paper.citing_papers.map((c) => (
              <Link key={c.id} to={`/papers/${c.id}`} className="block p-3 rounded-lg hover:bg-gray-50 border border-gray-100">
                <span className="text-sm font-medium text-gray-900">{c.title}</span>
              </Link>
            ))}
          </div>
        </div>
      )}

      {influence?.length > 0 && (
        <div className="card p-6">
          <h2 className="section-title mb-2">Influence Network</h2>
          <p className="text-xs text-gray-500 mb-4">
            Papers that indirectly influenced this work through citation chains (multi-hop traversal)
          </p>
          <div className="space-y-2">
            {influence.map((inf) => (
              <Link key={inf.id} to={`/papers/${inf.id}`} className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 border border-gray-100">
                <div className="min-w-0">
                  <span className="text-sm font-medium text-gray-900 block truncate">{inf.title}</span>
                  <div className="flex items-center gap-2 text-xs text-gray-500 mt-1">
                    <span>{inf.year}</span>
                    <span>&middot;</span>
                    <span>{inf.authors?.join(', ')}</span>
                  </div>
                </div>
                <span className="badge-amber ml-2 shrink-0">depth: {inf.influence_depth}</span>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
