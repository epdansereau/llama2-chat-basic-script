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

    return jsonify({"status": "ok"}), 200

@app.route('/message', methods=['POST'])
def message():
    user_message = request.json['user_message']

    if not llama_conversation.conversation:
        return jsonify({"error": "Please start a conversation first by calling /start"}), 400

    llama_conversation.conversation.append({'role':'user', 'content': user_message})
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
