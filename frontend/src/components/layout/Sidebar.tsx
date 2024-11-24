import {useQuery} from '@apollo/client';
import {Link} from 'react-router-dom';
import {GET_TAXONOMIES} from '../../graphql/queries';

interface Taxonomy {
    taxonomy: string;
    categories: string[];
    totalArticles: number;
}

export default function Sidebar() {
    const {loading, error, data} = useQuery(GET_TAXONOMIES);

    if (loading) return <div className="w-64 bg-white p-4">Loading...</div>;
    if (error) return <div className="w-64 bg-white p-4">Error loading taxonomies</div>;

    return (
        <div className="w-64 bg-white p-4 shadow-md">
            <nav>
                {data.allTaxonomies.map((taxonomy: Taxonomy) => (
                    <div key={taxonomy.taxonomy} className="mb-4">
                        <h2 className="mb-2 font-semibold text-gray-900">{taxonomy.taxonomy}</h2>
                        <ul className="space-y-1">
                            {taxonomy.categories.map((category) => (
                                <li key={category}>
                                    <Link
                                        to={`/categories/${encodeURIComponent(category)}`}
                                        className="block rounded-md px-2 py-1 text-sm text-gray-600 hover:bg-gray-100"
                                    >
                                        {category}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}
            </nav>
        </div>
    );
}