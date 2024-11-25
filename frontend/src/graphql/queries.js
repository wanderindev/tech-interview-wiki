import {gql} from '@apollo/client';

export const GET_ARTICLES = gql`
    query GetArticles {
        allArticles {
            id
            title
            slug
            excerpt
            taxonomy
            category
            tags
            wordCount
            isGenerated
        }
    }
`;

export const GET_ARTICLE = gql`
    query GetArticle($slug: String!) {
        articleBySlug(slug: $slug) {
            id
            title
            content
            taxonomy
            category
            tags
            wordCount
            isGenerated
            relatedArticles {
                id
                title
                slug
                excerpt
                taxonomy
                category
                tags
            }
        }
    }
`;