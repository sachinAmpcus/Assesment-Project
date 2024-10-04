import openai

# Set your OpenAI API key
openai.api_key = 'sk-GZ5AeDG6QXMjmAq8fTeLXZB9elfBO_9o-8gKW12dDfT3BlbkFJz-Krmf9410OnjXCUjSoDGoyKOplfkuED7AO98HVsYA'  # Replace with your actual API key

def generate_questions(role, topics):
    prompt = f"Generate coding interview questions for a {role} position covering the following topics: {', '.join(topics)}."
    
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
    
    role = input("Enter the role (e.g., Software Developer, Data Scientist): ")
    topics = input("Enter topics (comma-separated, e.g., Data Structures, Algorithms): ").split(',')
    topics = [topic.strip() for topic in topics]
    
    questions = generate_questions(role, topics)
    
    print("\nGenerated Interview Questions:")
    for question in questions:
        print(f"- {question}")

if __name__ == "__main__":
    main()
