import requests

# Your FastAPI API base URL
BASE_URL = "http://localhost:8000"  # URL where your FastAPI server is running (use localhost for development)

# Function to get input from the user
def get_input(prompt):
    return input(prompt)

# Text generation (generate)
def generate_text():
    text = get_input("Enter a text for generation: ")
    headers = {"Authorization": f"Bearer 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"}  # Place your API key here
    payload = {"text": text}
    response = requests.post(f"{BASE_URL}/generate/", headers=headers, json=payload)
    if response.status_code == 200:
        print("Generated text:", response.json()["generated_text"])
    else:
        print("An error occurred:", response.status_code, response.text)

# Text summarization (summarize)
def summarize_text():
    text = get_input("Enter a text to summarize: ")
    headers = {"Authorization": f"Bearer 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"}  # Place your API key here
    payload = {"text": text}
    response = requests.post(f"{BASE_URL}/summarize/", headers=headers, json=payload)
    if response.status_code == 200:
        print("Summary:", response.json()["summary"])
    else:
        print("An error occurred:", response.status_code, response.text)

# Question answering (question-answer)
def question_answer():
    question = get_input("Enter your question: ")
    context = get_input("Enter the context text: ")
    headers = {"Authorization": f"Bearer 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"}  # Place your API key here
    payload = {"question": question, "context": context}
    response = requests.post(f"{BASE_URL}/qa/", headers=headers, json=payload)
    if response.status_code == 200:
        print("Answer:", response.json()["answer"])
    else:
        print("An error occurred:", response.status_code, response.text)

# Sentiment analysis (sentiment)
def sentiment_analysis():
    text = get_input("Enter a text for sentiment analysis: ")
    headers = {"Authorization": f"Bearer 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"}  # Place your API key here
    payload = {"text": text}
    response = requests.post(f"{BASE_URL}/sentiment/", headers=headers, json=payload)
    if response.status_code == 200:
        print("Sentiment:", response.json())
    else:
        print("An error occurred:", response.status_code, response.text)

# Function to show the menu to the user
def main_menu():
    while True:
        print("\nAPI Testing Interface")
        print("1. Text Generation")
        print("2. Text Summarization")
        print("3. Question Answering")
        print("4. Sentiment Analysis")
        print("5. Exit")

        choice = get_input("Enter your choice (1-5): ")

        if choice == "1":
            generate_text()
        elif choice == "2":
            summarize_text()
        elif choice == "3":
            question_answer()
        elif choice == "4":
            sentiment_analysis()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main_menu()
