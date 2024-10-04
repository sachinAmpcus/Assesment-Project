import pandas as pd
import openai

# Set your OpenAI API key
openai.api_key = 'YOsk-proj-QEg_eqfmXZwDVHF8hIU8wkPc2d7YK8D3A3bxq5P-efWiKV0xkgw-VnDJV2A3QZSfA-bCGjnls9T3BlbkFJFV5B2a_56QbSKVMK5-S__oZjMoA0RX6vl76gEKqM_E_tXnsFyeTLVmpVYBGII1EJ9Nqg5gZWEA'  # Replace with your actual API key

def load_csv_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

def generate_question(row):
    prompt = (
        f"Generate a multiple-choice question based on the following parameters:\n"
        f"Question Type: {row['Question Type']}\n"
        f"Technology: {row['Technology']}\n"
        f"Difficulty: {row['Difficulty']}\n"
        f"Base Question: {row['Question']}\n"
        f"Provide 4 options and indicate the correct answer."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )

    return response['choices'][0]['message']['content']

def main():
    file_path = input("Enter the path to your CSV file: ")
    df = load_csv_data(file_path)

    if df is not None:
        df.columns = df.columns.str.strip()  # Trim whitespace from column names
        print("Columns in the DataFrame:", df.columns.tolist())  # Print the column names
        for index, row in df.iterrows():
            question = generate_question(row)
            print(f"\nGenerated Question {index + 1}:")
            print(question)

if __name__ == "__main__":
    main()
