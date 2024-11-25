import {Link} from 'react-router-dom';

export default function ArticleCard({article}) {
  return (
    <div className="w-full p-6 bg-[#fcfcfc] shadow-[0px_7px_12px_-10px_rgba(0,0,0,0.2)] rounded-lg">
      <Link
        to={`/articles/${article.slug}`}
        className="inline-block text-xl font-semibold mb-3 hover:text-blue-600"
      >
        {article.title}
      </Link>
      <p className="text-gray-600 mb-4">
        {article.excerpt}
      </p>
      <div className="flex flex-wrap gap-2 items-center text-sm">
        <span className="px-2 py-1 bg-purple-100 rounded-full">
          {article.taxonomy}
        </span>
        <span className="px-2 py-1 bg-blue-100 rounded-full">
          {article.category}
        </span>
        {article.tags.map(tag => (
          <span
            key={tag}
            className="px-2 py-1 bg-green-100 rounded-full"
          >
            {tag}
          </span>
        ))}
        <span className="text-gray-500">
          Article length: {article.wordCount} words
        </span>
        {!article.isGenerated && (
          <span className="text-yellow-600 bg-yellow-100 px-2 py-1 rounded-full">
            Generation in progress
          </span>
        )}
      </div>
    </div>
  );
}