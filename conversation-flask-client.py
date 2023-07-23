import requests
import time
import os

BASE_URL = 'http://127.0.0.1:5000'

def load_message(file_name):
    with open(file_name, 'r') as f:
        return f.read().strip()

def start_conversation():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    system_prompt = load_message('system_prompt.txt')
    user_message = load_message('user_message.txt')

    # Start a new conversation
    res = requests.post(f'{BASE_URL}/start', json={"system_prompt": system_prompt, "user_message": user_message})
    if res.status_code != 200:
        print(f"Error starting conversation: {res.text}")
        return

    while True:
        # Add next user message to conversation
        user_message = load_message('user_message.txt')


        start_time = time.time()
        # Post the user's message and get the assistant's response
        res = requests.post(f'{BASE_URL}/message', json={"user_message": user_message})
        print(time.time()-start_time)
        if res.status_code != 200:
            print(f"Error getting response: {res.text}")
            break

        data = res.json()

        print('==============================')
        print(data['output_text'])
        print('==============================')

        user_input = input("Press Enter to continue or 'n' to start a new conversation...")  # Wait for user input before continuing
        if user_input.lower() == 'n':
            break

if __name__ == "__main__":
    start_conversation()
