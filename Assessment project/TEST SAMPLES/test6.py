import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# Initialize the pipelines for summarization and question generation
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
question_generator = pipeline("text2text-generation", model="t5-small")

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

def summarize_text(text):
    # Truncate text if it's too long for the model
    if len(text) > 1024:  # Set a limit for summarization input
        text = text[:1024]
    
    # Summarize the text and ensure it's concise
    try:
        summarized = summarizer(text, max_length=150, min_length=30, do_sample=False)
        return summarized[0]['summary_text']
    except Exception as e:
        print(f"Error during summarization: {e}")
        return text

def generate_question(content):
    summarized_content = summarize_text(content)

    # Prepare the prompt for question generation
    prompt = f"Create a multiple-choice question based on this information: {summarized_content}."
    
    try:
        question = question_generator(prompt, max_length=150, num_return_sequences=1)[0]['generated_text']
        return question.strip()
    except Exception as e:
        print(f"Error generating question: {e}")
        return None

def main():
    topic = input("Enter a topic for the quiz: ")
    content = fetch_wikipedia_content(topic)
    if content:
        question = generate_question(content)
        if question:
            print("\nGenerated Quiz Question:")
            print(f"- {question}")
        else:
            print("No question was generated.")

if __name__ == "__main__":
    main()
