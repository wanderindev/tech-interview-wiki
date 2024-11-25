import {useQuery} from '@apollo/client';
import {GET_ARTICLES} from '../graphql/queries';
import ArticleCard from '../components/articles/ArticleCard';
import ArticleSkeleton from '../components/articles/ArticleSkeleton';

function HomePage() {
  const {loading, error, data} = useQuery(GET_ARTICLES);

  if (loading) {
    return (
      <div className="py-8 w-full">
        <div className="h-8 w-48 bg-gray-200 rounded animate-pulse mb-6"/>
        <div className="space-y-12 w-full">
          {[...Array(5)].map((_, index) => (
            <div key={index} className="w-full">
              <ArticleSkeleton/>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="py-8 w-full">
        <h1 className="text-3xl font-bold mb-6">Error loading articles</h1>
        <p className="text-red-600">{error.message}</p>
      </div>
    );
  }

  return (
    <div className="py-8 w-full">
      <h1 className="text-3xl font-bold mb-6">Latest Articles</h1>
      <div className="space-y-12 w-full">
        {data.allArticles.map(article => (
          <div key={article.id} className="w-full">
            <ArticleCard article={article}/>
          </div>
        ))}
      </div>
    </div>
  );
}

export default HomePage;