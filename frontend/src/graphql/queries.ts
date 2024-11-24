import {gql} from '@apollo/client';
import {DocumentNode} from 'graphql';

export const GET_TAXONOMIES: DocumentNode = gql`
    query GetTaxonomies {
        allTaxonomies {
            taxonomy
            categories
            totalArticles
        }
    }
`;

export const GET_ARTICLES_BY_TAXONOMY: DocumentNode = gql`
    query GetArticlesByTaxonomy($taxonomy: String!) {
        articlesByTaxonomy(taxonomy: $taxonomy) {
            id
            title
            slug
            level
            category
            tags
        }
    }
`;