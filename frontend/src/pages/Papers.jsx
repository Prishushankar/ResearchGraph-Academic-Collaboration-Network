import { api } from '../lib/api';
import { useFetch } from '../lib/useFetch';
import { LoadingSkeleton, ErrorMessage, EmptyState } from '../components/Status';
import { PaperCard } from '../components/Cards';

export default function Papers() {
  const { data: papers, loading, error } = useFetch(() => api.getPapers(50));

  return (
    <div className="space-y-6">
      <div>
        <h1 className="page-title mb-2">Papers</h1>
        <p className="text-gray-500 text-sm">
          Browse the research papers in the network, sorted by recency and citation count.
        </p>
      </div>

      {loading && <LoadingSkeleton rows={6} />}
      {error && <ErrorMessage message={error} />}
      {!loading && !error && papers?.length === 0 && <EmptyState message="No papers found" />}
      {!loading && !error && papers?.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {papers.map((p) => (
            <PaperCard key={p.id} paper={p} />
          ))}
        </div>
      )}
    </div>
  );
}
