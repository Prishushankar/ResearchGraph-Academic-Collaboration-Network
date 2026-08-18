import { api } from '../lib/api';
import { useFetch } from '../lib/useFetch';
import { LoadingSkeleton, ErrorMessage } from '../components/Status';
import { InstitutionCard } from '../components/Cards';

export default function Institutions() {
  const { data: institutions, loading, error } = useFetch(() => api.getInstitutions(50));

  return (
    <div className="space-y-6">
      <div>
        <h1 className="page-title mb-2">Institutions</h1>
        <p className="text-gray-500 text-sm">
          Academic institutions and their research output.
        </p>
      </div>

      {loading && <LoadingSkeleton rows={6} />}
      {error && <ErrorMessage message={error} />}
      {!loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {institutions?.map((i) => (
            <InstitutionCard key={i.id} institution={i} />
          ))}
        </div>
      )}
    </div>
  );
}
