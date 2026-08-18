import { api } from '../lib/api';
import { useFetch } from '../lib/useFetch';
import { LoadingSkeleton, ErrorMessage } from '../components/Status';
import { AuthorCard } from '../components/Cards';

export default function Authors() {
  const { data: authors, loading, error } = useFetch(() => api.getAuthors(50));

  return (
    <div className="space-y-6">
      <div>
        <h1 className="page-title mb-2">Authors</h1>
        <p className="text-gray-500 text-sm">
          Researchers in the network, sorted by h-index.
        </p>
      </div>

      {loading && <LoadingSkeleton rows={6} />}
      {error && <ErrorMessage message={error} />}
      {!loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {authors?.map((a) => (
            <AuthorCard key={a.id} author={a} />
          ))}
        </div>
      )}
    </div>
  );
}
