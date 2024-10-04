import requests
import random
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from bs4 import BeautifulSoup  # For HTML parsing

# Load the GPT-2 medium model and tokenizer
model_name = "gpt2-medium"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Function to fetch Wikipedia content
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
    search_result = response.json()["query"]["search"][0]
    page_id = search_result["pageid"]

    content_url = f"https://en.wikipedia.org/w/api.php?action=parse&pageid={page_id}&format=json&prop=text"
    content_response = requests.get(content_url)
    raw_content = content_response.json()["parse"]["text"]["*"]
    
    # Clean the HTML content
    soup = BeautifulSoup(raw_content, 'html.parser')
    return soup.get_text()

# Function to generate a question based on the content
def generate_question(content):
    sentences = content.split('. ')
    key_sentences = [sentence for sentence in sentences if len(sentence) > 30]
    
    if not key_sentences:
        return "No suitable content to generate a question."

    selected_sentence = random.choice(key_sentences)
    prompt = f"Generate a question about this topic: {selected_sentence}"

    # Encode the prompt
    input_ids = tokenizer.encode(prompt, return_tensors='pt')

    # Generate output
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=len(input_ids[0]) + 50,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            early_stopping=True
        )

    # Decode the generated text
    generated_question = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_question

def main():
    topic = input("Enter a topic for the quiz: ")
    content = fetch_wikipedia_content(topic)
    question = generate_question(content)

    print("Generated Question:", question)

if __name__ == "__main__":
    main()
