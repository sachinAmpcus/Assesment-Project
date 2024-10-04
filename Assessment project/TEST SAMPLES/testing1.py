import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load your dataset
dataset_path = r'C:\Users\ishaan.mishra\Documents\Assessment project\questions_with_dataset.csv'  # Replace with your dataset path
data = pd.read_csv(dataset_path)

# Ensure the dataset contains the correct columns
required_columns = ['Question Type', 'Technology', 'Difficulty', 'Question ']
for column_name in required_columns:
    if column_name not in data.columns:
        raise ValueError(f"Column '{column_name}' not found in the dataset.")

# Load the model and tokenizer
model_name = "gpt2"  # Change this to your preferred model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Function to generate questions
def generate_questions(language, topics, question_type, model, num_questions=1):
    # Create a clear and structured prompt
    prompt = (f"Generate {num_questions} clear and concise {question_type} questions "
              f"for the programming language {language} focusing on the following topics: {', '.join(topics)}.\n"
              "Format each question clearly, such as:\n"
              "1. What is a linked list? Write a function to implement it.\n"
              "2. Explain the difference between an array and an ArrayList.\n"
              "Please output only the questions, without any additional information or context.")

    # Encode the prompt
    input_ids = tokenizer.encode(prompt, return_tensors='pt')

    # Generate text with sampling
    output = model.generate(
        input_ids,
        max_length=150,
        num_return_sequences=num_questions,
        do_sample=True,
        no_repeat_ngram_size=2,
        temperature=0.7,
        top_k=50,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id,
        attention_mask=input_ids.new_ones(input_ids.shape)
    )

    # Decode the generated text
    questions = []
    for i in range(output.shape[0]):
        question = tokenizer.decode(output[i], skip_special_tokens=True).strip()
        # Filter for valid questions
        if question and "?" in question:
            questions.append(question)

    return questions

def main():
    # User input for parameters
    language = input("Enter the programming language (e.g., Java, Python): ")
    topics = input("Enter topics (comma-separated): ").split(',')
    question_type = input("Enter the type of question (e.g., coding, conceptual): ")

    # Generate questions
    questions = generate_questions(language.strip(), [topic.strip() for topic in topics], question_type.strip(), model, num_questions=1)
    
    # Print the generated questions
    for idx, question in enumerate(questions, start=1):
        print(f"Generated Interview Question {idx}: {question}")

if __name__ == "__main__":
    main()
