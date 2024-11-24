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

ARTICLE_GENERATION_PROMPT = """
You are writing a technical article for a programming interview preparation website.

Context:
- Title: {title}
- Target Audience: {level_description}
- Topic Area: {taxonomy}
- Category: {category}
- Tags: {tags}
- Word Limit: {word_limit} words

Existing Articles in our database:
{existing_articles}

Research Document:
{research_document}

Requirements:
1. Write the article in Markdown format
2. Keep the content technical and precise
3. Include code examples where relevant
4. Focus on interview preparation
5. Use a professional but engaging tone
6. Include interview-specific tips
7. Stay within the word limit

After the article, suggest 5 related articles we should create next. For each one provide:
- title: string
- taxonomy: string (same options as current article)
- category: string
- level: one of [basic, intermediate, advanced]
- tags: array of strings

Format the related articles as a JSON array.

If any of your suggestions match or are very similar to existing articles in our database, instead of creating new ones, reference the existing articles by their IDs.

Begin with the article content in Markdown:
"""
