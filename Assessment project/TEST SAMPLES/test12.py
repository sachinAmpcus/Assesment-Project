from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# Load the model and tokenizer
trained_model_path = 'ZhangCheng/T5-Base-Fine-Tuned-for-Question-Generation'
tokenizer = T5Tokenizer.from_pretrained(trained_model_path)
model = T5ForConditionalGeneration.from_pretrained(trained_model_path)

def generate_question(text):
    # Prepare the input text for the model
    input_text = f"generate question: {text}"
    input_ids = tokenizer.encode(input_text, return_tensors='pt')

    # Generate question with modified parameters
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=100,  # Allow longer questions
            num_beams=5,     # Increase beam search
            early_stopping=True,
            temperature=0.9, # Control randomness
            top_k=50         # Control diversity
        )

    # Decode and return the generated question
    question = tokenizer.decode(output[0], skip_special_tokens=True)
    return question

def main():
    # Get input from the user
    topic = input("Enter a topic for the quiz: ")
    # Generate a question based on the input topic
    question = generate_question(topic)
    print("Generated Question:", question)

if __name__ == "__main__":
    main()
