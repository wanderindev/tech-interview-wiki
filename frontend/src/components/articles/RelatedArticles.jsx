import {Link} from 'react-router-dom';

export default function RelatedArticles({articles}) {
  return (
    <div className="space-y-6">
      {articles.map(article => (
        <div key={article.id} className="border-l-4 border-gray-200 pl-4">
          <Link
            to={`/articles/${article.slug}`}
            className="text-lg font-semibold hover:text-blue-600"
          >
            {article.title}
          </Link>
          <p className="text-gray-600 mt-2">{article.excerpt}</p>
          <div className="flex flex-wrap gap-2 mt-2">
            <span className="text-sm text-gray-500">
              {article.taxonomy} • {article.category}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}