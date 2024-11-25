import {useState, useEffect} from 'react';
import {useParams} from 'react-router-dom';
import {useQuery} from '@apollo/client';
import ReactMarkdown from 'react-markdown';
import {GET_ARTICLE} from '../graphql/queries';
import RelatedArticles from '../components/articles/RelatedArticles';
import CodeBlock from '../components/articles/CodeBlock';

const LOADING_MESSAGES = [
  "Teaching GPT-4 how to write better code...",
  "Consulting Stack Overflow for the millionth time...",
  "Converting coffee into code explanations...",
  "Debugging the AI's debugging skills...",
  "Asking senior developers for their secret sauce...",
  "Mining Bitcoin to pay for API calls... (just kidding)",
  "Translating tech jargon into human speak...",
  "Convincing the algorithm to be more creative...",
  "Gathering wisdom from ancient programming scrolls...",
  "Bribing the cache for faster responses..."
];

function ArticlePage() {
  const [loadingMessage, setLoadingMessage] = useState(LOADING_MESSAGES[0]);
  const {slug} = useParams();
  const {loading, error, data, refetch} = useQuery(GET_ARTICLE, {
    variables: {slug},
    pollInterval: 10000,
  });

  useEffect(() => {
    if (data?.articleBySlug?.isGenerated) {
      refetch();
    } else {
      const interval = setInterval(() => {
        setLoadingMessage(LOADING_MESSAGES[Math.floor(Math.random() * LOADING_MESSAGES.length)]);
      }, 10000);
      return () => clearInterval(interval);
    }
  }, [data?.articleBySlug?.isGenerated, refetch]);

  if (loading || !data?.articleBySlug?.isGenerated) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[calc(100vh-200px)]">
        <div className="animate-spin w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mb-4"/>
        <p className="text-lg text-center animate-pulse">{loadingMessage}</p>
      </div>
    );
  }

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