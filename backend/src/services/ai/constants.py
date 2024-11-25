from typing import Dict

RESEARCH_WORD_LIMITS: Dict[str, int] = {
    "basic": 400,
    "intermediate": 800,
    "advanced": 1200,
}

ARTICLE_WORD_LIMITS: Dict[str, int] = {
    "basic": 250,
    "intermediate": 500,
    "advanced": 750,
}

LEVEL_DESCRIPTIONS: Dict[str, str] = {
    "basic": "junior developers or those new to this topic",
    "intermediate": "developers with 2-4 years of experience",
    "advanced": "senior developers with 5+ years of experience",
}

RESEARCH_PROMPT_TEMPLATE = """
You are helping prepare a research document for a technical interview preparation article.

Context:
- Title: {title}
- Target Audience: {level_description}
- Topic Area: {taxonomy}
- Category: {category}
- Related Topics: {tags}
- Excerpt: {excerpt}

Guidelines:
1. Research depth should match a {level} level article
2. Focus on key technical concepts and interview relevance
3. Include practical examples and common interview questions
4. Maximum length: {word_limit} words
5. Structure the research to cover:
   - Core concepts
   - Technical details
   - Common misconceptions
   - Interview question patterns
   - Best practices

The research will be used to write an article that helps developers prepare for technical interviews. Keep the focus technical and practical.

Please provide comprehensive research that will allow us to write an informative article.
"""

ARTICLE_GENERATION_PROMPT = """You are writing a technical article for a programming interview preparation website.

Context:
- Title: {title}
- Target Audience: {level_description}
- Topic Area: {taxonomy}
- Category: {category}
- Tags: {tags}
- Word Limit For Article: {word_limit} words
- Word Limit For Excerpt: 80 words
- Character Limit For Related Articles: 4000 characters

Existing Articles in our database:
{existing_articles}

Research Document:
{research_document}

Requirements:
For the article
1. Write the article in Markdown format
2. Base the content on the provided research document
3. Keep the content technical and precise
4. Include code examples where relevant
5. Focus on interview preparation
6. Use a professional but engaging tone
7. Include interview-specific tips
8. Stay within the word limit for the article

For excerpt
1. Provide a brief excerpt of the article with a maximum of 80 words

For related articles:
1. Suggest 5 related articles based on the content.  These suggestions should contain the following metadata: title, taxonomy, category, level, tags, and excerpt.
2. The word limit for the related article excerpt is 50 words.  The total character limit for all related articles is 4000 characters.
2. CAREFULLY review the existing articles list provided above
3. If you suggest an article that's very similar to an existing one (similar title, same category, or overlapping tags), use the existing article's ID
4. Avoid suggesting articles that would duplicate existing content
5. Each suggestion should be clearly distinct from existing articles

Format your response exactly as follows:
1. Start with EXCERPT_START, then your excerpt (max 80 words), then EXCERPT_END
2. Next line should be your article content in markdown (no additional headers or comments)
3. End with the related articles section between RELATED_ARTICLES_START and RELATED_ARTICLES_END

Example:
EXCERPT_START
Your excerpt here...
EXCERPT_END

# Article Title
Article content...

RELATED_ARTICLES_START
{{
    "articles": [
        {{
            "title": "Example Title",
            "taxonomy": "Example Taxonomy",
            "category": "Example Category",
            "level": "basic",
            "tags": ["tag1", "tag2"],
            "excerpt": "A brief (maximum 50-word) description of this related article that captures its key points and encourages readers to click through."
        }},
        ... 4 more articles ...
    ],
    "existing_articles_map": {{
        "0": "ID of existing article if suggestion 1 matches an existing article",
        "1": "ID of existing article if suggestion 2 matches an existing article"
    }}
}}
RELATED_ARTICLES_END

Begin your response now:"""
