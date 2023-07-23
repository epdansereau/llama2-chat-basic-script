import requests
import time
import os

BASE_URL = 'http://127.0.0.1:5000'

def load_message(file_name):
    with open(file_name, 'r') as f:
        return f.read().strip()

def start_conversation():
    system_prompt = load_message('system_prompt.txt')
    user_message = load_message('user_message.txt')

    # Start a new conversation
    start_time = time.time()
    res = requests.post(f'{BASE_URL}/start', json={"system_prompt": system_prompt, "user_message": user_message})
    print(time.time()-start_time)
    if res.status_code != 200:
        raise f"Error starting conversation: {res.text}"
    data = res.json()       
    print('==============================')
    print(data['output_text'])
    print('==============================')

    while True:
        user_input = input("Press Enter to continue or 'n' to start a new conversation...")  # Wait for user input before continuing
        if user_input.lower() == 'n':
            break
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

if __name__ == "__main__":
    while True:
        start_conversation()
