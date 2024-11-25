import {useParams} from 'react-router-dom';
import {useQuery} from '@apollo/client';
import ReactMarkdown from 'react-markdown';
import {GET_ARTICLE} from '../graphql/queries';
import RelatedArticles from '../components/articles/RelatedArticles';
import CodeBlock from '../components/articles/CodeBlock';

function ArticlePage() {
  const {slug} = useParams();
  const {loading, error, data} = useQuery(GET_ARTICLE, {
    variables: {slug}
  });

  if (loading) {
    return (
      <div className="py-8 animate-pulse">
        <div className="h-8 bg-gray-200 w-3/4 mb-4 rounded"/>
        <div className="space-y-4">
          <div className="h-4 bg-gray-100 w-full rounded"/>
          <div className="h-4 bg-gray-100 w-5/6 rounded"/>
          <div className="h-4 bg-gray-100 w-4/6 rounded"/>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="py-8">
        <div className="bg-red-50 border-l-4 border-red-500 p-4">
          <p className="text-red-700">Error loading article: {error.message}</p>
        </div>
      </div>
    );
  }

  // Make sure we have data and article before trying to render
  if (!data || !data.articleBySlug) {
    return (
      <div className="py-8">
        <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4">
          <p className="text-yellow-700">Article not found</p>
        </div>
      </div>
    );
  }

  const article = data.articleBySlug;

  return (
    <div className="py-8">
      <article className="prose max-w-none">
        {/* Metadata */}
        <div className="flex flex-wrap gap-2 mb-8 not-prose">
          <span className="px-2 py-1 bg-purple-100 rounded-full text-sm">
            {article.taxonomy}
          </span>
          <span className="px-2 py-1 bg-blue-100 rounded-full text-sm">
            {article.category}
          </span>
          {article.tags.map(tag => (
            <span
              key={tag}
              className="px-2 py-1 bg-green-100 rounded-full text-sm"
            >
              {tag}
            </span>
          ))}
          <span className="px-2 py-1 bg-gray-100 rounded-full text-sm">
            {article.wordCount} words
          </span>
        </div>

        {/* Article content */}
        <ReactMarkdown
          components={{
            code: CodeBlock,
            h1: ({node, ...props}) => {
              if (node.position?.start.line === 1) return null;
              return <h1 {...props} />;
            }
          }}
        >
          {article.content}
        </ReactMarkdown>
      </article>

      {/* Related articles section */}
      {article.relatedArticles && article.relatedArticles.length > 0 && (
        <div className="mt-12">
          <h2 className="text-2xl font-bold mb-6">Related Articles</h2>
          <RelatedArticles articles={article.relatedArticles}/>
        </div>
      )}
    </div>
  );
}

export default ArticlePage;