import requests
import random
from bs4 import BeautifulSoup

def fetch_wikipedia_content(query):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "utf8": 1,
        "srlimit": 1
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error fetching data from Wikipedia.")
        return ""
    
    search_result = response.json().get("query", {}).get("search", [])
    if not search_result:
        print("No results found.")
        return ""
    
    page_id = search_result[0]["pageid"]
    
    content_url = f"https://en.wikipedia.org/w/api.php?action=parse&pageid={page_id}&format=json&prop=text"
    content_response = requests.get(content_url)
    if content_response.status_code != 200:
        print("Error fetching page content.")
        return ""

    html_content = content_response.json()["parse"]["text"]["*"]
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

def generate_question(content):
    sentences = content.split('. ')
    key_sentences = [s for s in sentences if len(s) > 30]

    if not key_sentences:
        return "No suitable content found for question generation."
    
    selected_sentence = random.choice(key_sentences)
    words = selected_sentence.split()
    
    # Choose a random word to remove
    if len(words) > 2:
        answer = random.choice(words)
        question = selected_sentence.replace(answer, "_____")
        return question, answer
    else:
        return "Not enough words to create a question."

def main():
    topic = input("Enter a topic for the quiz: ")
    content = fetch_wikipedia_content(topic)
    if content:
        question, answer = generate_question(content)
        print("\nGenerated Quiz Question:")
        print(f"- {question}")
        print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
