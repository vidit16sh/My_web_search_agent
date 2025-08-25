import os
import google.generativeai as genai
import httpx
import asyncio


# ==============================
# Load API Keys
# ==============================

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
SERP_API_KEY = st.secrets["SERP_API_KEY"]

# ==============================
# Embedding Function
# ==============================
async def get_embedding(text: str):
    """
    Generates an embedding for the given text.
    """
    resp = genai.embed_content(
        model="models/embedding-001",
        content=text
    )
    return resp['embedding']

# ==============================
# Async Web Search using SerpAPI
# ==============================
async def web_search(query: str, num_results: int = 5):
    """
    Performs a web search using SerpAPI.
    """
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERP_API_KEY,
        "num": num_results
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        data = resp.json()

    results = []
    if "organic_results" in data:
        for item in data["organic_results"][:num_results]:
            title = item.get("title")
            link = item.get("link")
            if title and link:
                results.append({"title": title, "url": link})
    return results

# ==============================
# Async Web Scraper
# ==============================
async def fetch_page_content(url: str):
    """
    Asynchronously fetches and returns the text content of a given URL.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            resp.raise_for_status() # Raises an HTTPStatusError for bad responses
            return resp.text
    except httpx.HTTPError as e:
        print(f"Error fetching {url}: {e}")
        return None

# ==============================
# Async Generate Answer with Gemini (Updated)
# ==============================
async def generate_answer(query: str, search_data: list):
    """
    Generates an answer using the full content of retrieved pages as context.
    The 'search_data' list now contains a 'content' field for each entry.
    """
    if not search_data:
        return "❌ Sorry, I couldn’t find relevant search results."

    context = ""
    for item in search_data:
        # Check if content exists and is not too long
        if item.get("content"):
            # Truncate content to avoid exceeding prompt length limits
            truncated_content = item["content"][:3000] 
            context += f"\n\nSource: {item['title']} ({item['url']})\nContent: {truncated_content}"

    prompt = f"""
You are a **dynamic and adaptive web search assistant**.
Your job is to synthesize answers from search results into clear, engaging, and contextually relevant responses.

Question: {query}

Here is the retrieved content from the web:
{context}

Guidelines for answering:
1. **Adapt the style to the query type**:
   - For *factual or definition queries*: give a **concise, authoritative answer first**, then expand with key details.
   - For *how-to or step-by-step queries*: provide a **clear ordered list or bullet-point steps**.
   - For *comparisons or trade-offs*: use a **clean, well-structured table or side-by-side bullets**.
   - For *exploratory or broad queries*: summarize the **main themes, perspectives, or debates**, not just facts.
   - For *news or time-sensitive queries*: highlight the **latest developments** and mention the **date context**.

2. Always ensure the **first 2–3 sentences directly answer the user’s question** in plain, easy-to-read language.

3. Expand with supporting details, examples, or structured breakdowns:
   - Use **bullet points, tables, or numbered steps** where it improves clarity.
   - When multiple perspectives exist, **present them neutrally and fairly**.
   - Highlight **nuances, limitations, or uncertainties** if relevant.

4. Cite sources naturally and clearly using a **friendly markdown style**:
   - Example: [BBC](https://bbc.com), [Stanford](https://stanford.edu).
   - Prefer well-known or authoritative sources when possible.

5. Keep answers **concise, engaging, and human-like**.
   - Avoid filler or generic "As an AI model…" statements.
   - Don’t fabricate; if search results are weak or irrelevant, state that clearly.
   - When helpful, **invite follow-up exploration** (e.g., “Would you like me to compare X and Y in more detail?”).

Your goal is to make the answer feel **smart, conversational, and tailored to the query**, not a rigid template.
"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    resp = await asyncio.to_thread(model.generate_content, prompt)
    return resp.text.strip()

# ==============================
# Main Async Pipeline
# ==============================
async def handle_query(query: str):
    """
    The main RAG pipeline that orchestrates the search, filtering, and generation.
    """
    # Step 1: Perform broad web search
    initial_search_results = await web_search(query)
    
    # Step 2: Asynchronously fetch content for the initial search results
    tasks = [fetch_page_content(r['url']) for r in initial_search_results]
    contents = await asyncio.gather(*tasks)

    # Step 3: Augment the results with the fetched content
    search_data = []
    for result, content in zip(initial_search_results, contents):
        if content:
            result['content'] = content
            search_data.append(result)

    # Step 4: Generate the answer using the new, content-rich data
    answer = await generate_answer(query, search_data)
    
    return answer

# ==============================
# Example usage
# ==============================
if __name__ == "__main__":
    answer = asyncio.run(handle_query(query))
    print(answer)