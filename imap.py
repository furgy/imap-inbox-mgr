import email
import imaplib
import pprint
import os
import json
from slack import WebClient
from slack.errors import SlackApiError
import html2markdown

client = WebClient(token=os.environ['SLACK_API_TOKEN'])

imap_host = 'mail.fourmoons.net'
imap_user = 'ta1@fourmoons.net'
imap_pass = 'GAP_skod3clel8wrot'

mail = imaplib.IMAP4_SSL(imap_host)
mail.login(imap_user,imap_pass)

mail.select("inbox")

result, data = mail.uid('search', None, "ALL")

inbox_item_list = data[0].split()

for item in inbox_item_list:
    result2, email_data = mail.uid('fetch', item, '(RFC822)')
    raw_email = email_data[0][1].decode("utf-8")
    email_message = email.message_from_string(raw_email)
    to_ = email_message['To']
    from_ = email_message['From']
    subject_ = email_message['Subject']
    body_ = ""
    counter = 1
    for part in email_message.walk():
        if part.get_content_maintype() == "multipart":
            continue
        content_type = part.get_content_type()
        if 'text' in content_type:
            body_ = part.get_payload(decode=True)
        # if 'html' in content_type:
        #     body_ = html2markdown.convert(part.get_payload(decode=True))

    pl = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                        				"text": '{}'.format(subject_)
                }
            },
            {
                "type": "section",
                "block_id": "section567",
             			"text": {
                                    "type": "mrkdwn",
                        				"text": "{}".format(body_)
                                },
                "accessory": {
                                    "type": "image",
                        				"image_url": "https://is5-ssl.mzstatic.com/image/thumb/Purple3/v4/d3/72/5c/d3725c8f-c642-5d69-1904-aa36e4297885/source/256x256bb.jpg",
                        				"alt_text": "Haunted hotel image"
                                }
            },
            {
                "type": "section",
                "block_id": "section789",
             			"fields": [
                                    {
                                        "type": "mrkdwn",
                                        "text": "*Average Rating*\n1.0"
                                    }
                                ]
            }
	]

    pl

    try:
        response = client.chat_postMessage(
           channel='#pythontesting',
           blocks=pl)
        # assert response["message"]["text"] == subject_
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")
