from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the model and tokenizer
model_name = 'ZhangCheng/T5-Base-Fine-Tuned-for-Question-Generation'
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def generate_question(context):
    # Prepend a prefix to indicate the task
    input_text = f"generate question: {context}"
    
    # Tokenize the input
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    
    # Generate questions
    output_ids = model.generate(input_ids, max_length=50, num_return_sequences=1)
    
    # Decode the generated question
    question = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return question

if __name__ == "__main__":
    context = "Python"
    generated_question = generate_question(context)
    print(f"Generated Question: {generated_question}")
