/* eslint-disable */
import { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';
import { gql } from '@apollo/client';
import * as Apollo from '@apollo/client';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
export type MakeEmpty<T extends { [key: string]: unknown }, K extends keyof T> = { [_ in K]?: never };
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
const defaultOptions = {} as const;
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string; }
  String: { input: string; output: string; }
  Boolean: { input: boolean; output: boolean; }
  Int: { input: number; output: number; }
  Float: { input: number; output: number; }
};

export type ArticleType = {
  __typename?: 'ArticleType';
  category: Scalars['String']['output'];
  content?: Maybe<Scalars['String']['output']>;
  id: Scalars['Int']['output'];
  isGenerated: Scalars['Boolean']['output'];
  level: Scalars['String']['output'];
  slug: Scalars['String']['output'];
  tags: Array<Scalars['String']['output']>;
  taxonomy: Scalars['String']['output'];
  title: Scalars['String']['output'];
  updatedAt?: Maybe<Scalars['String']['output']>;
};

export type CategoryStats = {
  __typename?: 'CategoryStats';
  category: Scalars['String']['output'];
  levels: Array<Scalars['String']['output']>;
  taxonomy: Scalars['String']['output'];
  totalArticles: Scalars['Int']['output'];
};

export enum Level {
  Advanced = 'ADVANCED',
  Basic = 'BASIC',
  Intermediate = 'INTERMEDIATE'
}

export type Query = {
  __typename?: 'Query';
  /** Get all articles */
  allArticles: Array<ArticleType>;
  /** Get statistics about all categories */
  allCategories: Array<CategoryStats>;
  /** Get statistics about all taxonomies */
  allTaxonomies: Array<TaxonomyStats>;
  /** Get an article by its slug */
  articleBySlug?: Maybe<ArticleType>;
  /** Get articles by category and optional taxonomy */
  articlesByCategory: Array<ArticleType>;
  /** Get articles by difficulty level */
  articlesByLevel: Array<ArticleType>;
  /** Get articles by taxonomy */
  articlesByTaxonomy: Array<ArticleType>;
};


export type QueryArticleBySlugArgs = {
  slug: Scalars['String']['input'];
};


export type QueryArticlesByCategoryArgs = {
  category: Scalars['String']['input'];
  taxonomy?: InputMaybe<Scalars['String']['input']>;
};


export type QueryArticlesByLevelArgs = {
  level: Level;
};


export type QueryArticlesByTaxonomyArgs = {
  taxonomy: Scalars['String']['input'];
};

export type TaxonomyStats = {
  __typename?: 'TaxonomyStats';
  categories: Array<Scalars['String']['output']>;
  taxonomy: Scalars['String']['output'];
  totalArticles: Scalars['Int']['output'];
};

export type GetTaxonomiesQueryVariables = Exact<{ [key: string]: never; }>;


export type GetTaxonomiesQuery = { __typename?: 'Query', allTaxonomies: Array<{ __typename?: 'TaxonomyStats', taxonomy: string, categories: Array<string>, totalArticles: number }> };

export type GetArticlesByTaxonomyQueryVariables = Exact<{
  taxonomy: Scalars['String']['input'];
}>;


export type GetArticlesByTaxonomyQuery = { __typename?: 'Query', articlesByTaxonomy: Array<{ __typename?: 'ArticleType', id: number, title: string, slug: string, level: string, category: string, tags: Array<string> }> };


export const GetTaxonomiesDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"GetTaxonomies"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"allTaxonomies"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"taxonomy"}},{"kind":"Field","name":{"kind":"Name","value":"categories"}},{"kind":"Field","name":{"kind":"Name","value":"totalArticles"}}]}}]}}]} as unknown as DocumentNode<GetTaxonomiesQuery, GetTaxonomiesQueryVariables>;
export const GetArticlesByTaxonomyDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"GetArticlesByTaxonomy"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"taxonomy"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"articlesByTaxonomy"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"taxonomy"},"value":{"kind":"Variable","name":{"kind":"Name","value":"taxonomy"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"title"}},{"kind":"Field","name":{"kind":"Name","value":"slug"}},{"kind":"Field","name":{"kind":"Name","value":"level"}},{"kind":"Field","name":{"kind":"Name","value":"category"}},{"kind":"Field","name":{"kind":"Name","value":"tags"}}]}}]}}]} as unknown as DocumentNode<GetArticlesByTaxonomyQuery, GetArticlesByTaxonomyQueryVariables>;
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string; }
  String: { input: string; output: string; }
  Boolean: { input: boolean; output: boolean; }
  Int: { input: number; output: number; }
  Float: { input: number; output: number; }
};

export type ArticleType = {
  __typename?: 'ArticleType';
  category: Scalars['String']['output'];
  content?: Maybe<Scalars['String']['output']>;
  id: Scalars['Int']['output'];
  isGenerated: Scalars['Boolean']['output'];
  level: Scalars['String']['output'];
  slug: Scalars['String']['output'];
  tags: Array<Scalars['String']['output']>;
  taxonomy: Scalars['String']['output'];
  title: Scalars['String']['output'];
  updatedAt?: Maybe<Scalars['String']['output']>;
};

export type CategoryStats = {
  __typename?: 'CategoryStats';
  category: Scalars['String']['output'];
  levels: Array<Scalars['String']['output']>;
  taxonomy: Scalars['String']['output'];
  totalArticles: Scalars['Int']['output'];
};

export enum Level {
  Advanced = 'ADVANCED',
  Basic = 'BASIC',
  Intermediate = 'INTERMEDIATE'
}

export type Query = {
  __typename?: 'Query';
  /** Get all articles */
  allArticles: Array<ArticleType>;
  /** Get statistics about all categories */
  allCategories: Array<CategoryStats>;
  /** Get statistics about all taxonomies */
  allTaxonomies: Array<TaxonomyStats>;
  /** Get an article by its slug */
  articleBySlug?: Maybe<ArticleType>;
  /** Get articles by category and optional taxonomy */
  articlesByCategory: Array<ArticleType>;
  /** Get articles by difficulty level */
  articlesByLevel: Array<ArticleType>;
  /** Get articles by taxonomy */
  articlesByTaxonomy: Array<ArticleType>;
};


export type QueryArticleBySlugArgs = {
  slug: Scalars['String']['input'];
};


export type QueryArticlesByCategoryArgs = {
  category: Scalars['String']['input'];
  taxonomy?: InputMaybe<Scalars['String']['input']>;
};


export type QueryArticlesByLevelArgs = {
  level: Level;
};


export type QueryArticlesByTaxonomyArgs = {
  taxonomy: Scalars['String']['input'];
};

export type TaxonomyStats = {
  __typename?: 'TaxonomyStats';
  categories: Array<Scalars['String']['output']>;
  taxonomy: Scalars['String']['output'];
  totalArticles: Scalars['Int']['output'];
};

export type GetTaxonomiesQueryVariables = Exact<{ [key: string]: never; }>;


export type GetTaxonomiesQuery = { __typename?: 'Query', allTaxonomies: Array<{ __typename?: 'TaxonomyStats', taxonomy: string, categories: Array<string>, totalArticles: number }> };

export type GetArticlesByTaxonomyQueryVariables = Exact<{
  taxonomy: Scalars['String']['input'];
}>;


export type GetArticlesByTaxonomyQuery = { __typename?: 'Query', articlesByTaxonomy: Array<{ __typename?: 'ArticleType', id: number, title: string, slug: string, level: string, category: string, tags: Array<string> }> };


export const GetTaxonomiesDocument = gql`
    query GetTaxonomies {
  allTaxonomies {
    taxonomy
    categories
    totalArticles
  }
}
    `;

/**
 * __useGetTaxonomiesQuery__
 *
 * To run a query within a React component, call `useGetTaxonomiesQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetTaxonomiesQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetTaxonomiesQuery({
 *   variables: {
 *   },
 * });
 */
export function useGetTaxonomiesQuery(baseOptions?: Apollo.QueryHookOptions<GetTaxonomiesQuery, GetTaxonomiesQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetTaxonomiesQuery, GetTaxonomiesQueryVariables>(GetTaxonomiesDocument, options);
      }
export function useGetTaxonomiesLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetTaxonomiesQuery, GetTaxonomiesQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetTaxonomiesQuery, GetTaxonomiesQueryVariables>(GetTaxonomiesDocument, options);
        }
export function useGetTaxonomiesSuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetTaxonomiesQuery, GetTaxonomiesQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetTaxonomiesQuery, GetTaxonomiesQueryVariables>(GetTaxonomiesDocument, options);
        }
export type GetTaxonomiesQueryHookResult = ReturnType<typeof useGetTaxonomiesQuery>;
export type GetTaxonomiesLazyQueryHookResult = ReturnType<typeof useGetTaxonomiesLazyQuery>;
export type GetTaxonomiesSuspenseQueryHookResult = ReturnType<typeof useGetTaxonomiesSuspenseQuery>;
export type GetTaxonomiesQueryResult = Apollo.QueryResult<GetTaxonomiesQuery, GetTaxonomiesQueryVariables>;
export const GetArticlesByTaxonomyDocument = gql`
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

/**
 * __useGetArticlesByTaxonomyQuery__
 *
 * To run a query within a React component, call `useGetArticlesByTaxonomyQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetArticlesByTaxonomyQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useGetArticlesByTaxonomyQuery({
 *   variables: {
 *      taxonomy: // value for 'taxonomy'
 *   },
 * });
 */
export function useGetArticlesByTaxonomyQuery(baseOptions: Apollo.QueryHookOptions<GetArticlesByTaxonomyQuery, GetArticlesByTaxonomyQueryVariables> & ({ variables: GetArticlesByTaxonomyQueryVariables; skip?: boolean; } | { skip: boolean; }) ) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<GetArticlesByTaxonomyQuery, GetArticlesByTaxonomyQueryVariables>(GetArticlesByTaxonomyDocument, options);
      }
export function useGetArticlesByTaxonomyLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<GetArticlesByTaxonomyQuery, GetArticlesByTaxonomyQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<GetArticlesByTaxonomyQuery, GetArticlesByTaxonomyQueryVariables>(GetArticlesByTaxonomyDocument, options);
        }
export function useGetArticlesByTaxonomySuspenseQuery(baseOptions?: Apollo.SkipToken | Apollo.SuspenseQueryHookOptions<GetArticlesByTaxonomyQuery, GetArticlesByTaxonomyQueryVariables>) {
          const options = baseOptions === Apollo.skipToken ? baseOptions : {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<GetArticlesByTaxonomyQuery, GetArticlesByTaxonomyQueryVariables>(GetArticlesByTaxonomyDocument, options);
        }
export type GetArticlesByTaxonomyQueryHookResult = ReturnType<typeof useGetArticlesByTaxonomyQuery>;
export type GetArticlesByTaxonomyLazyQueryHookResult = ReturnType<typeof useGetArticlesByTaxonomyLazyQuery>;
export type GetArticlesByTaxonomySuspenseQueryHookResult = ReturnType<typeof useGetArticlesByTaxonomySuspenseQuery>;
export type GetArticlesByTaxonomyQueryResult = Apollo.QueryResult<GetArticlesByTaxonomyQuery, GetArticlesByTaxonomyQueryVariables>;