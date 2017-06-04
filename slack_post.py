# utf-8
# python3.5.0

from slackclient import SlackClient
import os
import password_list

token = password_list.token
channel = password_list.channel

slack_token = token
sc = SlackClient(slack_token)

sc.api_call(
  "chat.postMessage",
  channel=channel,
  text="test :tada:"
)
