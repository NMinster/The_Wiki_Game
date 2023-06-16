import os
import requests
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import openai
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def extract_topics(common_links):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(common_links)

    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    return filtered_sentence

@lru_cache(maxsize=10000)
def get_links(page):
    # Get the response from the API for a specific page
    response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': page,
            'prop': 'links',
            'pllimit': 'max',
        }
    ).json()

    # Parse the pages from the response
    pages = list(response['query']['pages'].values())
    if len(pages) == 0:
        return []

    # Parse the links from the first page in the response
    links = pages[0].get('links', [])
    return [link['title'] for link in links]


def get_common_links(start, target):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": f"Give me a list of only words which may connect {start} with {target}. Do not print anything other than this list."
        }
    ]

    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    common_links = chat.choices[0].message.content

    return common_links  # The response may need to be processed to extract meaningful links or keywords.


def get_score(link, topics):
    score = 0
    for topic in topics:
        if topic in link:
            score += 1
    return score

def wikirace(start, target):
    common_links = get_common_links(start, target)  # The model provides topics, not actual links.

    topics = extract_topics(common_links)  # You'll need to implement this.

    queue = []
    # The queue now contains entries arranged by score (priority), path, visited set
    heapq.heappush(queue, (-1, [start], {start}))  # Note that heapq is a min-heap, so we negate the score

    while queue:
        score, path, visited = heapq.heappop(queue)
        page = path[-1]

        if page == target:
            return path

        links = get_links(page)
        scored_links = [(get_score(link, topics), link) for link in links]
        sorted_links = sorted(scored_links, key=lambda x: x[0], reverse=True)  # Prioritize links with higher scores

        for link_score, link in sorted_links:
            if link not in visited:
                # Add to the priority queue with cumulative score
                new_visited = visited.copy()
                new_visited.add(link)
                heapq.heappush(queue, (score - link_score, path + [link], new_visited))  # Negate score for min-heap

    return None


print(wikirace('Python (programming language)', 'Elvis Presley'))
