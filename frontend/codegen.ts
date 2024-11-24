import type {Types} from '@graphql-codegen/cli';

const config: Types.Config = {
    schema: 'http://backend:5000/api/graphql',
    documents: ['src/**/*.tsx', 'src/**/*.ts'],
    generates: {
        './src/gql/': {
            preset: 'client',
            plugins: [
                'typescript',
                'typescript-operations',
                'typescript-react-apollo'
            ]
        }
    },
    ignoreNoDocuments: true
};

export default config;