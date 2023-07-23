import torch
from transformers import AutoTokenizer, LlamaForCausalLM
import time

AUTH_TOKEN = ''

device = torch.device("cuda")

# Load the model and tokenizer with float16 precision
model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", use_auth_token=AUTH_TOKEN).to(torch.float16).to(device)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf", use_auth_token=AUTH_TOKEN)

conversation = []  # Initialize an empty conversation list

def load_message(file_name):
    with open(file_name, 'r') as f:
        return f.read().strip()

def generate_prompt(conversation, system_prompt):
    prompt = ''
    for turn in conversation:
        if turn['role'] == 'system':
            prompt += f'''<s>[INST] <<SYS>>
{system_prompt}
<</SYS>>

'''
        elif turn['role'] == 'user':
            prompt += f'{turn["content"]}  [/INST]'
        else:
            prompt += f''' {turn["content"]} </s>\\
<s>[INST] '''
    return prompt

def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    input_ids = inputs["input_ids"]  # Extract 'input_ids' from the dictionary

    # Generate
    a = time.time()
    generate_ids = model.generate(input_ids, max_new_tokens=500)
    print(time.time()-a)
    output_text = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

    # Get assistant's latest message
    assistant_message = output_text.split('[/INST]')[-1].strip()
    return output_text, assistant_message

def start_conversation():
    global conversation

    while True:
        system_prompt = load_message('system_prompt.txt')
        user_message = load_message('user_message.txt')

        if len(conversation) == 0:  # If it's the start of the conversation
            conversation.append({'role':'system', 'content': system_prompt})
            conversation.append({'role':'user', 'content': user_message})

        prompt = generate_prompt(conversation, system_prompt)

        print('****************************')
        print(prompt)
        print('****************************')

        output_text, assistant_message = generate_response(prompt)
        conversation.append({'role':'assistant', 'content': assistant_message})

        print('==============================')
        print(output_text)
        print('==============================')

        user_input = input("Press Enter to continue or 'n' to start a new conversation...")  # Wait for user input before continuing
        if user_input.lower() == 'n':
            conversation = []  # Reset the conversation for a new one
        else:
            # Add next user message to conversation
            user_message = load_message('user_message.txt')
            conversation.append({'role':'user', 'content': user_message})

if __name__ == "__main__":
    start_conversation()
