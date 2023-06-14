The_Wiki_Game

This Python program implements a version of the Wikippedia Game aka a "wikirace". In a wikirace, the goal is to navigate from one Wikipedia page to another, exclusively using the links on each page. This script aims to find a path from a starting Wikipedia page to a target Wikipedia page. 

E.g. Start on the wiki page for Ford Motor Company, your goal is to reach Lady Gaga. Using only internal links a solution is the following, Ford Motor Company-> Ford Field -> Madonna -> Lady Gaga.

This is acomplished programatically by the following outline:

get_links(): This function sends a request to the Wikipedia API to get all the links on a given Wikipedia page. It then returns a list of titles of these linked pages. This function is decorated with lru_cache to avoid repeated network calls for the same page.

get_common_links(): This function uses OpenAI's ChatCompletion API to chat with GPT-3.5-turbo model. It feeds in a system and user message to the model, where the user message is asking about common connections between the start and target pages. The returned model-generated message content is searched for common links between the pages.

get_score(): This function returns the number of times topics appear in a given link.

wikirace(): This function implements the core logic of the wikirace. It starts with the start page and uses breadth-first search to traverse the pages linked from the current page. It prioritizes the links that have higher scores determined by get_score(), meaning those having more common links or topics with the target. The search stops when it reaches the target page.

Execution: The script calls wikirace() with 'Python (programming language)' and 'Elvis Presley' as example arguments and prints the path from the start page to the target page.

