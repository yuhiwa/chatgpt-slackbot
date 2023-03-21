from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import re
import os
import time
import pickle
import openai

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")
HISTORY_TIME = 60

app = App(token=SLACK_BOT_TOKEN)

@app.message("hello slackbot!")
def message_hello(message, say):
    say("hi")

def check_messages(identifier):
    file_path = os.path.dirname(os.path.abspath(__file__)) + "/" + identifier + ".cache"
    if not os.path.exists(file_path):
        return False
    file_mtime = os.path.getmtime(file_path)
    now = time.time()
    diff = now - file_mtime
    if diff < HISTORY_TIME:
        return True
    else:
        return False

def check_system_message():
    file_path = os.path.dirname(os.path.abspath(__file__)) + "/" + "system" + ".cache"
    if os.path.exists(file_path):
        return True
    else:
        return False

def set_system_message(system_message):
    pickle.dump(system_message, open(os.path.dirname(os.path.abspath(__file__)) + "/" + "system" + ".cache", "wb"))

def set_messages(identifier, messages):
    messages = [m for m in messages if not m['role'] == "system"]
    pickle.dump(messages, open(os.path.dirname(os.path.abspath(__file__)) + "/" + identifier + ".cache", "wb"))

def get_messages(identifier):
    try: messages = pickle.load(open(os.path.dirname(os.path.abspath(__file__)) + "/" + identifier + ".cache", "rb"))
    except (OSError, IOError) as e:
        print(e)
        print(type(e))
    return messages

@app.message(re.compile("get-chatgpt-system"))
def message_set_system(message, say, context):
    system_message = get_messages("system")
    say(system_message)

@app.message(re.compile("set-chatgpt-system (.*)"))
def message_set_system(message, say, context):
    user_input = context['matches'][0]
    set_system_message(user_input)
    say("AI behavior has been updated.")

@app.message(re.compile("unset-chatgpt-system"))
def message_unset_system(message, say, context):
    user_input = ""
    identifier = 'system'
    set_messages(identifier, user_input)
    say("AI behavior returned to normal.")

def completion(new_message_text, settings_text, past_messages):
    system = {"role": "system", "content": settings_text}
    past_messages.append(system)
    new_message = {"role": "user", "content": new_message_text}
    past_messages.append(new_message)

    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=past_messages
    )
    response_message = {"role": "assistant", "content": result.choices[0].message.content}
    past_messages.append(response_message)
    response_message_text = result.choices[0].message.content
    return response_message_text, past_messages

@app.event("app_mention")
def message_mention(body, say):
    event = body["event"]
    message = body["event"]["text"]
    user = body["event"]["user"]
    channel = body["event"]["channel"]
    identifier = user + channel
    user_input = re.sub('^\S+\s', '', message)

    messages = []
    system_message = ""
    if check_messages(identifier):
        messages = get_messages(identifier)

    if check_system_message():
        system_message = get_messages('system')

    response, messages = completion(user_input,system_message, messages)
    set_messages(identifier, messages)

    if event.get("thread_ts") is None:
        say(response)
    else:
        say(text=response, thread_ts=body["event"]["thread_ts"])

if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()

