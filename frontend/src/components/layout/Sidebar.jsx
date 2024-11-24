import {useQuery} from '@apollo/client';
import {Link, useLocation} from 'react-router-dom';
import {GET_TAXONOMIES} from 'graphql/queries.js';

export default function Sidebar() {
  const {loading, error, data} = useQuery(GET_TAXONOMIES);
  const location = useLocation();

  if (loading) {
    return (
      <div className="h-[calc(100vh-4rem)] w-64 border-r border-gray-200 bg-white p-4 shadow-md">
        <div className="animate-pulse space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="space-y-2">
              <div className="h-4 w-2/3 rounded bg-gray-200"/>
              <div className="h-3 w-1/2 rounded bg-gray-100"/>
              <div className="h-3 w-1/2 rounded bg-gray-100"/>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="h-[calc(100vh-4rem)] w-64 border-r border-gray-200 bg-white p-4 shadow-md">
        <p className="text-sm text-red-600">Error loading navigation</p>
      </div>
    );
  }

  return (
    <aside className="h-[calc(100vh-4rem)] w-64 border-r border-gray-200 bg-white shadow-lg">
      <div className="h-full overflow-y-auto p-4 scrollbar-thin scrollbar-track-gray-100 scrollbar-thumb-gray-300">
        <nav className="space-y-6">
          {data.allTaxonomies.map((taxonomy) => (
            <div key={taxonomy.taxonomy} className="space-y-2">
              <div className="flex items-center justify-between">
                <h2 className="text-sm font-semibold text-gray-900">{taxonomy.taxonomy}</h2>
                <span className="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600">
                  {taxonomy.totalArticles}
                </span>
              </div>
              <ul className="space-y-1">
                {taxonomy.categories.map((category) => {
                  const isActive = location.pathname === `/categories/${encodeURIComponent(category)}`;
                  return (
                    <li key={category}>
                      <Link
                        to={`/categories/${encodeURIComponent(category)}`}
                        className={`block rounded-md px-2 py-1 text-sm transition-colors ${
                          isActive
                            ? 'bg-indigo-50 text-indigo-600'
                            : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                        }`}
                      >
                        {category}
                      </Link>
                    </li>
                  );
                })}
              </ul>
            </div>
          ))}
        </nav>
      </div>
    </aside>
  );
}