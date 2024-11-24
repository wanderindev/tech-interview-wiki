import {gql} from '@apollo/client';

export const GET_TAXONOMIES = gql`
    query GetTaxonomies {
        allTaxonomies {
            categories
            taxonomy
            totalArticles
        }
    }
`;

export const GET_ARTICLES_BY_TAXONOMY = gql`
    query GetArticlesByTaxonomy($taxonomy: String!) {
        articlesByTaxonomy(taxonomy: $taxonomy) {
            category
            content
            id
            isGenerated
            level
            slug
            tags
            taxonomy
            title
            updatedAt
            wordCount
        }
    }
`;