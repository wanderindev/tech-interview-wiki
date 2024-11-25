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
- Character Limit For Related Articles: 3000 characters

Existing Articles in our database:
{existing_articles}

Research Document:
{research_document}

Requirements:
1. Write the article in Markdown format
2. Base the content on the provided research document
3. Keep the content technical and precise
4. Include code examples where relevant
5. Focus on interview preparation
6. Use a professional but engaging tone
7. Include interview-specific tips
8. Stay within the word limit
9. Include a compelling excerpt (plain text) that summarizes the key points

For related articles:
- CAREFULLY review the existing articles list provided above
- If you suggest an article that's very similar to an existing one (similar title, same category, or overlapping tags), use the existing article's ID
- Avoid suggesting articles that would duplicate existing content
- Each suggestion should be clearly distinct from existing articles
- Include a brief excerpt for each suggested article

Structure your response in this exact order:
1. First, provide the article excerpt:
EXCERPT_START
[Your 80-word max excerpt here]
EXCERPT_END

2. Then, provide the full article content
[Your complete article content in markdown]

3. Finally, provide the related articles:
RELATED_ARTICLES_START
{{
    "articles": [
        {{
            "title": "Example Title",
            "taxonomy": "Example Taxonomy",
            "category": "Example Category",
            "level": "basic",
            "tags": ["tag1", "tag2"],
            "excerpt": "A brief maximum 80-word description of this related article that captures its key points and encourages readers to click through."
        }},
        ... 4 more articles ...
    ],
    "existing_articles_map": {{
        "0": "ID of existing article if suggestion 1 matches an existing article",
        "1": "ID of existing article if suggestion 2 matches an existing article"
    }}
}}
RELATED_ARTICLES_END

Begin your response now with the article excerpt:"""
