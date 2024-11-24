import {ApolloClient, InMemoryCache, ApolloProvider} from '@apollo/client';
import {BrowserRouter} from 'react-router-dom';
import Layout from './components/layout/Layout';
import Routes from './Routes';

const client = new ApolloClient({
    uri: 'http://localhost:5000/api/graphql',
    cache: new InMemoryCache(),
});

function App() {
    return (
        <ApolloProvider client={client}>
            <BrowserRouter>
                <Layout>
                    <Routes/>
                </Layout>
            </BrowserRouter>
        </ApolloProvider>
    );
}

export default App;