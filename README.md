# Tech Interview Wiki

A technical interview preparation platform leveraging AI to generate interconnected technical articles. The system uses
a two-phase content generation approach with OpenAI and Anthropic for optimal content quality.

## Technology Stack

### Frontend

- React with Vite
- GraphQL (Apollo Client)
- Tailwind CSS
- react-markdown & react-syntax-highlighter
- Client-side caching and state management

### Backend

- Flask with blueprints architecture
- PostgreSQL (SQLAlchemy ORM)
- Redis for caching
- Strawberry for GraphQL
- OpenAI & Anthropic APIs

## Architecture

### Database Design

- Self-referencing Article model for content relationships
- Efficient indexing for taxonomy/category queries
- Word count and relevance score tracking
- Relationship mapping for article connections

### Content Generation Pipeline

1. **Research Phase (OpenAI)**
    - Low temperature for factual accuracy
    - Structured research document generation
    - Taxonomy-aware content organization

2. **Content Generation (Anthropic)**
    - Higher creative freedom for engaging content
    - Markdown formatting with code examples
    - Related article suggestions
    - Auto-excerpt generation

### GraphQL Implementation

- Strawberry-based schema definition
- Efficient nested queries for related articles
- Automatic type generation
- Query optimization for N+1 problems

## Core Features

### Article Discovery

- Homepage displays articles by relevance score
- Taxonomy/category/tag-based navigation
- Dynamic content generation on first access
- Progress tracking for generation status

### Content Display

- Markdown rendering with syntax highlighting
- Code block copy functionality
- Related articles suggestions
- Loading state management

### Dynamic Generation

- Background content generation
- Progress feedback
- Caching of research results
- Error recovery mechanisms

## CLI Commands

```bash
# Populate database with initial articles
flask populate-db [--force]

# Update article word counts
flask update-word-counts

# Recalculate article relevance scores
flask update-relevance-scores
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- OpenAI & Anthropic API keys

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/tech-interview-wiki.git
cd tech-interview-wiki

# Backend setup
cp backend/.env.example backend/.env
# Edit .env with your API keys

# Start services
docker-compose up --build

# Run migrations
docker-compose exec backend flask db upgrade

# Populate initial content
docker-compose exec backend flask populate-db
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

Environment variables:

```
VITE_API_URL=http://localhost:5173
```

## Future Improvements

### Backend

- API failure recovery mechanisms
- Rate limiting implementation
- Response caching optimization
- Parallel content generation
- Enhanced error logging

### Frontend

- Full-text search
- Advanced filtering
- Personalized learning paths
- Interactive interview simulations
- Client-side search indexing

### Performance

- Infinite scrolling
- Image optimization
- Enhanced caching strategies
- Response compression

## License

MIT License