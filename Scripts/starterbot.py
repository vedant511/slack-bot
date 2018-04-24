import os
import time
import re
from slackclient import SlackClient


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND_1 = "Well, okay. Can I get 5 tickets for first day first show of Deadpool 2?"
EXAMPLE_COMMAND_2 = "AMC at Mill Ave"
EXAMPLE_COMMAND_3 = "Ummm...I guess 7 pm then"
EXAMPLE_COMMAND_4 = "Yes!! We have our poster presentation in the morning that day. After that we all will be free for the evening!"
EXAMPLE_COMMAND_5 = "No. Thanks bro!"

EXAMPLE_COMMAND_6 = "Who is the STUD of our group!"
EXAMPLE_COMMAND_7 = "Who is our savior!"

MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                # return
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    # print matches.group(1), matches.group(2)
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean :( All I can do for now is book movie tickets :D"
    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND_1):
        response = "Sure, what theatre would be best for you guys?"

    if command.startswith(EXAMPLE_COMMAND_2):
        response = "Lemme check bruh! Oops..first day first show is full, what other time will work?"

    if command.startswith(EXAMPLE_COMMAND_3):
        response = "Okay. BTW, are you sure you all will be free that day? Not all of you have just 1 course :o"

    if command.startswith(EXAMPLE_COMMAND_4):
        response = "Give me a second.......Done and Dusted. Anything else I can do for you bud?"

    if command.startswith(EXAMPLE_COMMAND_5):
        response = "Cool! See you later, need to knock out some jerks ;)"

    if command.startswith(EXAMPLE_COMMAND_6):
        response = "Mingfei :o"

    if command.startswith(EXAMPLE_COMMAND_7):
        response = "Mingfei! Mingfei!! Mingfei!!!"

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
