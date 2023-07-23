from flask import Flask, request, jsonify
import llama_conversation 

app = Flask(__name__)

@app.route('/start', methods=['POST'])
def start():
    system_prompt = request.json['system_prompt']
    user_message = request.json['user_message']

    llama_conversation.conversation = []  # Reset the conversation for a new one
    llama_conversation.conversation.append({'role':'system', 'content': system_prompt})
    llama_conversation.conversation.append({'role':'user', 'content': user_message})

    prompt = llama_conversation.generate_prompt(llama_conversation.conversation, llama_conversation.conversation[0]['content'])

    output_text, assistant_message = llama_conversation.generate_response(prompt)
    llama_conversation.conversation.append({'role':'assistant', 'content': assistant_message})

    return jsonify({
        "assistant_message": assistant_message,
        "output_text": output_text,
        "conversation": llama_conversation.conversation
    }), 200

@app.route('/message', methods=['POST'])
def message():
    user_message = request.json['user_message']
    system_prompt = request.json.get('system_prompt')  # Get system_prompt if it exists, else None

    if not llama_conversation.conversation:
        return jsonify({"error": "Please start a conversation first by calling /start"}), 400

    # If a system prompt is provided
    if system_prompt:
        # Check if the first element in the conversation is a system prompt
        if llama_conversation.conversation[0]['role'] == 'system':
            # If so, update its content
            llama_conversation.conversation[0]['content'] = system_prompt
        else:
            # If not, add a new system prompt to the start of the conversation
            llama_conversation.conversation.insert(0, {'role': 'system', 'content': system_prompt})

    llama_conversation.conversation.append({'role':'user', 'content': user_message})

    # Generate the prompt using the first message in the conversation as the system prompt
    prompt = llama_conversation.generate_prompt(llama_conversation.conversation, llama_conversation.conversation[0]['content'])

    output_text, assistant_message = llama_conversation.generate_response(prompt)
    llama_conversation.conversation.append({'role':'assistant', 'content': assistant_message})

    return jsonify({
        "assistant_message": assistant_message,
        "output_text": output_text,
        "conversation": llama_conversation.conversation
    }), 200


if __name__ == "__main__":
    app.run(debug=False, port=5000)
