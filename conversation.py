import torch
from transformers import AutoTokenizer, LlamaForCausalLM
import time

AUTH_TOKEN = ''

print(torch.cuda.is_available())
device = torch.device("cuda")

# Load the model and tokenizer with float16 precision
model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", use_auth_token="AUTH_TOKEN").to(torch.float16).to(device)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf", use_auth_token="AUTH_TOKEN")

conversation = []  # Initialize an empty conversation list

while True:
    with open('system_prompt.txt', 'r') as f:  # Open the file with the system prompt
        system_prompt = f.read().strip()  # Read the contents and remove any trailing newline characters

    with open('user_message.txt', 'r') as f:  # Open the file with the user message
        user_message = f.read().strip()  # Read the contents and remove any trailing newline characters

    if len(conversation) == 0:  # If it's the start of the conversation
        conversation.append({'role':'system', 'content': system_prompt})
        conversation.append({'role':'user', 'content': user_message})

    # Create prompt from conversation history
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

    print('****************************')
    print(prompt)
    print('****************************')

    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    input_ids = inputs["input_ids"]  # Extract 'input_ids' from the dictionary

    # Generate
    a = time.time()
    generate_ids = model.generate(input_ids, max_new_tokens=500)
    print(time.time()-a)
    output_text = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

    # Get assistant's latest message
    assistant_message = output_text.split('[/INST]')[-1].strip()
    conversation.append({'role':'assistant', 'content': assistant_message})

    print('==============================')
    print(output_text)
    print('==============================')

    user_input = input("Press Enter to continue or 'n' to start a new conversation...")  # Wait for user input before continuing
    if user_input.lower() == 'n':
        conversation = []  # Reset the conversation for a new one
    else:
        # Add next user message to conversation
        with open('user_message.txt', 'r') as f:
            user_message = f.read().strip()
        conversation.append({'role':'user', 'content': user_message})
