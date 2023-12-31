## Starting a New Conversation

To start a new conversation, send a `POST` request to the `/start` endpoint. You should include a JSON body with two fields: `system_prompt` and `user_message`.


```python
import requests
import json
url = 'http://localhost:5000/start'  # replace with your server's URL
headers = {'Content-Type': 'application/json'}
data = {
  "system_prompt": "You are a fisherman",
  "user_message": "What's the weather like?"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.json()['assistant_message'])
```

## Adding a Message to the Conversation

To add a message to the conversation, send a `POST` request to the `/message` endpoint. The JSON body of the request should have field `user_message`, and can also have a field `system_prompt`.

```python
url = 'http://localhost:5000/message'
headers = {'Content-Type': 'application/json'}
  data = {
  "user_message": "Tell me a joke."
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.json()['assistant_message'])
```

Changing the model's personality during the conversation:

```python
data = {
    "user_message": "What's your favorite seafood?",
    "system_prompt": "You are a fisherman and you hate shrimps"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.json()['assistant_message'])
```
