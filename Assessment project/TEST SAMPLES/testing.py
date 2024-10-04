import openai

# Set your OpenAI API key
openai.api_key = 'YOUR_API_KEY'  # Replace with your actual API key

def generate_questions(language, topics, question_type):
    if question_type.lower() == 'mcq':
        prompt = f"Generate Multiple Choice Questions for the programming language {language} covering the following topics: {', '.join(topics)}."
    elif question_type.lower() == 'coding':
        prompt = f"Generate coding problems for the programming language {language} covering the following topics: {', '.join(topics)}."
    else:  # Text-based questions
        prompt = f"Generate text-based interview questions for the programming language {language} covering the following topics: {', '.join(topics)}."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use a supported model
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        n=5,  # Number of questions to generate
        temperature=0.7,
    )
    
    questions = [choice['message']['content'] for choice in response['choices']]
    return questions

def main():
    print("Welcome to the Coding Interview Question Generator!")
    
    language = input("Enter the programming language (e.g., Python, C++, Ruby, Java, JavaScript): ")
    topics = input("Enter topics (comma-separated, e.g., Data Structures, Algorithms): ").split(',')
    topics = [topic.strip() for topic in topics]
    question_type = input("Enter question type (MCQ, Coding, Text): ")
    
    questions = generate_questions(language, topics, question_type)
    
    print("\nGenerated Interview Questions:")
    for question in questions:
        print(f"- {question}")

if __name__ == "__main__":
    main()
