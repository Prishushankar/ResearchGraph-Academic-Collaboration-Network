import { api } from '../lib/api';
import { useFetch } from '../lib/useFetch';
import { LoadingSkeleton, ErrorMessage } from '../components/Status';
import { TopicBadge } from '../components/Cards';

export default function Topics() {
  const { data: topics, loading, error } = useFetch(() => api.getTopics(50));

  return (
    <div className="space-y-6">
      <div>
        <h1 className="page-title mb-2">Research Topics</h1>
        <p className="text-gray-500 text-sm">
          Areas of research and the number of papers in each.
        </p>
      </div>

      {loading && <LoadingSkeleton rows={6} />}
      {error && <ErrorMessage message={error} />}
      {!loading && !error && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {topics?.map((t) => (
            <div key={t.id} className="card p-5">
              <div className="flex items-start justify-between mb-2">
                <h3 className="text-sm font-semibold text-gray-900">{t.name}</h3>
                <span className="text-2xl font-bold text-primary-600">{t.paper_count}</span>
              </div>
              <TopicBadge topic={t} />
              <p className="text-xs text-gray-500 mt-2">
                {t.paper_count === 1 ? '1 paper' : `${t.paper_count} papers`}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
