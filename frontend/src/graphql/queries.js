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

// Add artificial delay for development
export const delayedGetArticles = async () => {
  await new Promise(resolve => setTimeout(resolve, 2000));
  return GET_ARTICLES;
};