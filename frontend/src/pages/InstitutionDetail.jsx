import { useParams, Link } from 'react-router-dom';
import { api } from '../lib/api';
import { useFetch } from '../lib/useFetch';
import { LoadingSkeleton, ErrorMessage, EmptyState } from '../components/Status';
import { AuthorCard } from '../components/Cards';
import { PaperCard } from '../components/Cards';

export default function InstitutionDetail() {
  const { id } = useParams();
  const { data: inst, loading, error } = useFetch(() => api.getInstitution(id), [id]);

  if (loading) return <LoadingSkeleton rows={4} type="table" />;
  if (error) return <ErrorMessage message={error} />;
  if (!inst) return <EmptyState message="Institution not found" />;

  return (
    <div className="space-y-6">
      <div>
        <Link to="/institutions" className="text-sm text-primary-600 hover:text-primary-700 mb-2 inline-block">
          &larr; All Institutions
        </Link>
        <h1 className="text-2xl font-bold text-gray-900 mb-1">{inst.name}</h1>
        <div className="flex items-center gap-3 text-sm text-gray-500">
          <span>{inst.country}</span>
          {inst.ranking > 0 && <span className="badge-purple">Rank #{inst.ranking}</span>}
        </div>
      </div>

      {inst.collaborating_institutions?.length > 0 && (
        <div className="card p-6">
          <h2 className="section-title mb-3">Collaborating Institutions</h2>
          <div className="flex flex-wrap gap-2">
            {[...new Set(inst.collaborating_institutions)].map((name) => (
              <span key={name} className="badge-green">{name}</span>
            ))}
          </div>
        </div>
      )}

      {inst.authors?.length > 0 && (
        <div>
          <h2 className="section-title mb-4">Authors ({inst.authors.length})</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {inst.authors.map((a) => (
              <AuthorCard key={a.id} author={{ ...a, institution: inst.name }} />
            ))}
          </div>
        </div>
      )}

      {inst.papers?.length > 0 && (
        <div>
          <h2 className="section-title mb-4">Papers ({inst.papers.length})</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {inst.papers.map((p) => (
              <PaperCard key={p.id} paper={p} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
