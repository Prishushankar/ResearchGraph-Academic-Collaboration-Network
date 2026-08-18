import { api } from '../lib/api';
import { useFetch } from '../lib/useFetch';
import { LoadingSkeleton, ErrorMessage } from '../components/Status';
import { Link } from 'react-router-dom';

function StatCard({ label, value, color = 'primary', link }) {
  const colors = {
    primary: 'from-primary-500 to-primary-400',
    green: 'from-green-500 to-green-400',
    purple: 'from-purple-500 to-purple-400',
    amber: 'from-amber-500 to-amber-400',
    red: 'from-red-500 to-red-400',
    cyan: 'from-cyan-500 to-cyan-400',
  };
  const content = (
    <div className="card p-5 group">
      <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${colors[color]} flex items-center justify-center mb-3`}>
        <span className="text-white text-lg font-bold">{typeof value === 'number' ? value.toLocaleString() : value}</span>
      </div>
      <p className="text-sm font-medium text-gray-600">{label}</p>
    </div>
  );
  return link ? <Link to={link} className="block hover:ring-2 hover:ring-primary-200 rounded-xl transition-all">{content}</Link> : content;
}

export default function Dashboard() {
  const { data: stats, loading, error, } = useFetch(() => api.getStats());
  const { data: papers } = useFetch(() => api.getPapers(5));
  const { data: authors } = useFetch(() => api.getAuthors(5));

  if (loading) return <LoadingSkeleton type="stat" />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="page-title mb-2">Academic Research Network</h1>
        <p className="text-gray-500">
          Explore connections between researchers, papers, institutions, and topics
          across the global academic landscape.
        </p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <StatCard label="Papers" value={stats?.papers} color="primary" link="/papers" />
        <StatCard label="Authors" value={stats?.authors} color="green" link="/authors" />
        <StatCard label="Institutions" value={stats?.institutions} color="purple" link="/institutions" />
        <StatCard label="Topics" value={stats?.topics} color="amber" link="/topics" />
        <StatCard label="Citations" value={stats?.citations} color="red" />
        <StatCard label="Authorships" value={stats?.authorships} color="cyan" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="section-title">Recent Papers</h2>
            <Link to="/papers" className="text-sm text-primary-600 hover:text-primary-700 font-medium">
              View all
            </Link>
          </div>
          <div className="space-y-3">
            {papers?.map((p) => (
              <Link key={p.id} to={`/papers/${p.id}`} className="card p-4 block hover:border-primary-300">
                <h3 className="text-sm font-semibold text-gray-900 mb-1 line-clamp-1">{p.title}</h3>
                <div className="flex items-center gap-3 text-xs text-gray-500">
                  <span>{p.year}</span>
                  <span>{p.citations_count} citations</span>
                </div>
              </Link>
            ))}
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="section-title">Top Authors</h2>
            <Link to="/authors" className="text-sm text-primary-600 hover:text-primary-700 font-medium">
              View all
            </Link>
          </div>
          <div className="space-y-3">
            {authors?.map((a) => (
              <Link key={a.id} to={`/authors/${a.id}`} className="card p-4 block hover:border-primary-300">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-full bg-gradient-to-br from-primary-500 to-primary-300 flex items-center justify-center text-white font-semibold text-xs shrink-0">
                    {a.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div className="min-w-0">
                    <h3 className="text-sm font-semibold text-gray-900 truncate">{a.name}</h3>
                    <p className="text-xs text-gray-500 truncate">{a.institution}</p>
                  </div>
                  <span className="badge-green ml-auto shrink-0">h: {a.h_index}</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>

      <div className="card p-6 bg-gradient-to-r from-primary-50 to-blue-50 border-primary-200">
        <h2 className="section-title mb-2">Explore the Network</h2>
        <p className="text-sm text-gray-600 mb-4">
          Discover collaboration paths between researchers, trace citation chains,
          and find interdisciplinary connections across the academic landscape.
        </p>
        <div className="flex flex-wrap gap-3">
          <Link to="/explore" className="btn-primary">
            Open Explorer
          </Link>
          <Link to="/topics" className="btn-secondary">
            Browse Topics
          </Link>
        </div>
      </div>
    </div>
  );
}
