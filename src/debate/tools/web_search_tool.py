import os
from crewai.tools import tool
import serpapi

@tool("Web Search Tool")
def web_search_tool(query: str) -> str:
    """Search the web for latest information, facts, news, and statistics."""
    normalized_query = query.lower().strip()
    try:
        serpapi_api_key = os.getenv("SERPAPI_API_KEY")
        if not serpapi_api_key:
            raise ValueError("SERPAPI_API_KEY environment variable is missing")

        client = serpapi.Client(api_key=serpapi_api_key)
        data = client.search({
            "engine": "google",
            "q": normalized_query,
            "num": 5,
        })

        results = data.get("organic_results", [])
        if not results:
            return "No relevant search results found."

        return "\n\n".join(
            f"Title: {r.get('title')}\nBody: {r.get('snippet')}\nURL: {r.get('link')}"
            for r in results
        )

    except ValueError as e:
        raise RuntimeError(f"Web search configuration error: {str(e)}") from e
    except Exception as e:
        return f"Web search temporarily unavailable: {str(e)}"

#---------------------------------------------DDG Implementaion----------------------------------
# from typing import Any
# from crewai.tools import tool
# from ddgs import DDGS

# @tool("Web Search Tool")
# def web_search_tool(query: str) -> str:
#     """Search the web for latest information, facts, news, and statistics."""
#     normalized_query = query.lower().strip()
#     try:
#         results = list[Any](DDGS().text(normalized_query, max_results=5))
#         if not results:
#             return "No relevant search results found."
        
#         return "\n\n".join(
#             f"Title: {r.get('title')}\nBody: {r.get('body')}\nURL: {r.get('href')}"
#             for r in results
#         )
#     except Exception as e:
#         return "Web search temporarily unavailable."

#-----------------------------------------------Caching logic below------------------------------
# from crewai.tools import BaseTool
# from ddgs import DDGS
# from typing import ClassVar

# import redis
# import hashlib
# import logging
# import time
# import subprocess
# import urllib.parse
# import re
# import html

# logger = logging.getLogger(__name__)

# class WebSearchTool(BaseTool):

#     name: str = "Web Search Tool"

#     description: str = (
#         "Search the web for latest information, "
#         "facts, news, and statistics"
#     )

#     # ------------------------------------------------
#     # CONFIG
#     # ------------------------------------------------
#     CACHE_TTL_SECONDS: ClassVar[int] = 3600

#     # ------------------------------------------------
#     # REDIS
#     # ------------------------------------------------
#     redis_client: ClassVar[redis.Redis] = redis.Redis(
#         host="localhost",
#         port=6379,
#         db=0,
#         decode_responses=True
#     )

#     # ------------------------------------------------
#     # MAIN ENTRY
#     # ------------------------------------------------
#     def _run(self, query: str) -> str:

#         try:
#             normalized_query = self._normalize_query(query)
#             cache_key = self._build_cache_key(normalized_query)

#             # ----------------------------------------
#             # CACHE CHECK
#             # ----------------------------------------
#             cached_result = self._get_cached_result(cache_key)
#             if cached_result:
#                 return cached_result
#             logger.info(f"Web search: {normalized_query}")

#             # ----------------------------------------
#             # REAL SEARCH
#             # ----------------------------------------
#             output = self._perform_search(normalized_query)

#             # ----------------------------------------
#             # CACHE SAVE
#             # ----------------------------------------
#             self._cache_result(cache_key,output)
#             return output

#         except Exception as e:
#             logger.exception("Web search failed")
#             return f"Web search failed: {str(e)}"

#     # ------------------------------------------------
#     # QUERY HELPERS
#     # ------------------------------------------------
#     @staticmethod
#     def _normalize_query(query: str) -> str:
#         return query.lower().strip()

#     @staticmethod
#     def _generate_query_hash(query: str) -> str:
#         return hashlib.md5(query.encode()).hexdigest()

#     def _build_cache_key(self, query: str) -> str:
#         query_hash = self._generate_query_hash(query)
#         return f"web_search:{query_hash}"

#     # ------------------------------------------------
#     # CACHE
#     # ------------------------------------------------
#     def _get_cached_result(self,cache_key: str):
#         cached_result = self.redis_client.get(cache_key)
#         if cached_result:
#             logger.info(f"Cache hit: {cache_key}")
#         return cached_result

#     def _cache_result(self,cache_key: str,value: str):
#         self.redis_client.setex(cache_key,self.CACHE_TTL_SECONDS,value)

#     # ------------------------------------------------
#     # SEARCH
#     # ------------------------------------------------
#     def _perform_search(self,query: str) -> str:
#         start = time.time()

#         # Try the DDGS library first
#         try:
#             results = DDGS().text(query,max_results=5)
#             output = self._format_results(results)
#             elapsed = round(time.time() - start,2)
#             logger.info(f"DDGS search completed in {elapsed}s")
#             return output
#         except Exception as e:
#             logger.warning(f"DDGS library failed ({e}), falling back to curl-based search")

#         # Fallback: use curl + DuckDuckGo Lite HTML
#         output = self._curl_fallback_search(query)
#         elapsed = round(time.time() - start,2)
#         logger.info(f"Curl fallback search completed in {elapsed}s")
#         return output

#     def _curl_fallback_search(self, query: str) -> str:
#         """Fallback search using curl to fetch DuckDuckGo Lite results."""
#         encoded_query = urllib.parse.quote_plus(query)
#         url = f"https://lite.duckduckgo.com/lite/?q={encoded_query}"

#         try:
#             result = subprocess.run(
#                 [
#                     "curl", "-s", "-L",
#                     "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
#                     url,
#                 ],
#                 capture_output=True,
#                 text=True,
#                 timeout=15,
#             )
#             if result.returncode != 0:
#                 return f"Curl search failed with return code {result.returncode}"

#             return self._parse_ddg_lite_html(result.stdout)
#         except subprocess.TimeoutExpired:
#             return "Web search timed out"
#         except Exception as e:
#             return f"Curl fallback search failed: {str(e)}"

#     @staticmethod
#     def _parse_ddg_lite_html(raw_html: str) -> str:
#         """Parse DuckDuckGo Lite HTML to extract search results."""
#         formatted_results = []

#         # DuckDuckGo Lite: <a rel="nofollow" href="..." class='result-link'>Title</a>
#         # Note: href appears BEFORE class in the HTML
#         link_pattern = re.compile(
#             r"""<a[^>]*href=['"]([^'"]*?)['"][^>]*class=['"]result-link['"][^>]*>(.*?)</a>""",
#             re.DOTALL
#         )
#         snippet_pattern = re.compile(
#             r"""<td\s+class=['"]result-snippet['"]>(.*?)</td>""",
#             re.DOTALL
#         )

#         links = link_pattern.findall(raw_html)
#         snippets = snippet_pattern.findall(raw_html)

#         for i, (href, title_html) in enumerate(links[:5]):
#             title = re.sub(r'<[^>]+>', '', title_html).strip()
#             title = html.unescape(title)

#             # Extract actual URL from DDG redirect: //duckduckgo.com/l/?uddg=<encoded_url>&...
#             href = html.unescape(href)
#             uddg_match = re.search(r'[?&]uddg=([^&]+)', href)
#             if uddg_match:
#                 href = urllib.parse.unquote(uddg_match.group(1))

#             body = ""
#             if i < len(snippets):
#                 body = re.sub(r'<[^>]+>', '', snippets[i]).strip()
#                 body = html.unescape(body)
#             formatted_results.append(
#                 f"""
#                 Title: {title}
#                 Body: {body}
#                 URL: {href}
#                 """
#             )

#         if not formatted_results:
#             return "No search results found."

#         return "\n\n".join(formatted_results)

#     @staticmethod
#     def _format_results(results) -> str:
#         formatted_results = []
#         for r in results:
#             formatted_results.append(
#                 f"""
#                 Title: {r.get('title')}
#                 Body: {r.get('body')}
#                 URL: {r.get('href')}
#                 """
#             )
#         return "\n\n".join(formatted_results)
