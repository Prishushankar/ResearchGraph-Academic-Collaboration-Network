import { useParams, Link } from 'react-router-dom';
import { api } from '../lib/api';
import { useFetch } from '../lib/useFetch';
import { LoadingSkeleton, ErrorMessage, EmptyState } from '../components/Status';
import { TopicBadge, PaperCard } from '../components/Cards';

export default function AuthorDetail() {
  const { id } = useParams();
  const { data: author, loading, error } = useFetch(() => api.getAuthor(id), [id]);
  const { data: recommendations } = useFetch(() => api.getRecommendations(id), [id]);

  if (loading) return <LoadingSkeleton rows={4} type="table" />;
  if (error) return <ErrorMessage message={error} />;
  if (!author) return <EmptyState message="Author not found" />;

  return (
    <div className="space-y-6">
      <div>
        <Link to="/authors" className="text-sm text-primary-600 hover:text-primary-700 mb-2 inline-block">
          &larr; All Authors
        </Link>
        <div className="flex items-center gap-4 mb-2">
          <div className="w-14 h-14 rounded-full bg-gradient-to-br from-primary-500 to-primary-300 flex items-center justify-center text-white text-xl font-bold">
            {author.name.split(' ').map(n => n[0]).join('')}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{author.name}</h1>
            <div className="flex items-center gap-3 text-sm text-gray-500">
              {author.institution_name && <span>{author.institution_name}</span>}
              {author.institution_country && <span>&middot; {author.institution_country}</span>}
              <span className="badge-green">h-index: {author.h_index}</span>
            </div>
          </div>
        </div>
      </div>

      {author.topics?.length > 0 && (
        <div className="card p-6">
          <h2 className="section-title mb-3">Research Topics</h2>
          <div className="flex flex-wrap gap-2">
            {author.topics.map((t) => (
              <span key={t} className="badge-blue">{t}</span>
            ))}
          </div>
        </div>
      )}

      {author.papers?.length > 0 && (
        <div>
          <h2 className="section-title mb-4">Papers ({author.papers.length})</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {author.papers.map((p) => (
              <PaperCard key={p.id} paper={p} />
            ))}
          </div>
        </div>
      )}

      {recommendations?.length > 0 && (
        <div className="card p-6">
          <h2 className="section-title mb-2">Recommended Collaborators</h2>
          <p className="text-xs text-gray-500 mb-4">
            Researchers with overlapping interests but no direct collaboration yet
          </p>
          <div className="space-y-2">
            {recommendations.map((r) => (
              <Link key={r.id} to={`/authors/${r.id}`} className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 border border-gray-100">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-green-500 to-green-300 flex items-center justify-center text-white text-xs font-semibold">
                    {r.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div>
                    <span className="text-sm font-medium text-gray-900">{r.name}</span>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {r.shared_topics?.map((t) => (
                        <span key={t} className="text-[10px] bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded">{t}</span>
                      ))}
                    </div>
                  </div>
                </div>
                <span className="badge-purple">h: {r.h_index}</span>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
