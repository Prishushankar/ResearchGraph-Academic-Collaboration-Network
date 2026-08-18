import { Link } from 'react-router-dom';

export function PaperCard({ paper }) {
  return (
    <Link to={`/papers/${paper.id}`} className="card p-5 block hover:border-primary-300">
      <div className="flex items-start justify-between mb-2">
        <h3 className="text-sm font-semibold text-gray-900 line-clamp-2 leading-snug">
          {paper.title}
        </h3>
        <span className="badge-blue ml-2 shrink-0">{paper.year}</span>
      </div>
      <div className="flex items-center gap-3 text-xs text-gray-500">
        <span className="flex items-center gap-1">
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
          </svg>
          {paper.citations_count} citations
        </span>
      </div>
    </Link>
  );
}

export function AuthorCard({ author }) {
  return (
    <Link to={`/authors/${author.id}`} className="card p-5 block hover:border-primary-300">
      <div className="flex items-center gap-3 mb-2">
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-500 to-primary-300 flex items-center justify-center text-white font-semibold text-sm">
          {author.name.split(' ').map(n => n[0]).join('')}
        </div>
        <div>
          <h3 className="text-sm font-semibold text-gray-900">{author.name}</h3>
          {author.institution && (
            <p className="text-xs text-gray-500">{author.institution}</p>
          )}
        </div>
      </div>
      <div className="flex items-center gap-2 mt-2">
        <span className="badge-green">h-index: {author.h_index}</span>
      </div>
    </Link>
  );
}

export function InstitutionCard({ institution }) {
  return (
    <Link to={`/institutions/${institution.id}`} className="card p-5 block hover:border-primary-300">
      <h3 className="text-sm font-semibold text-gray-900 mb-1">{institution.name}</h3>
      <p className="text-xs text-gray-500 mb-3">{institution.country}</p>
      <div className="flex items-center gap-3 text-xs text-gray-500">
        <span>{institution.author_count} authors</span>
        <span>{institution.paper_count} papers</span>
      </div>
    </Link>
  );
}

export function TopicBadge({ topic, showCount = false }) {
  const colors = {
    'Computer Science': 'badge-blue',
    'Biology': 'badge-green',
    'Neuroscience': 'badge-purple',
    'Environmental Science': 'badge-green',
    'Physics': 'badge-amber',
    'Engineering': 'badge-blue',
    'Philosophy': 'badge-purple',
    'Medicine': 'badge-green',
    'Mathematics': 'badge-amber',
  };
  return (
    <span className={colors[topic.category] || 'badge-blue'}>
      {topic.name}
      {showCount && topic.paper_count !== undefined && ` (${topic.paper_count})`}
    </span>
  );
}
