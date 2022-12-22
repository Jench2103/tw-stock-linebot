from typing import Union, Dict, List

from flask import request, abort
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction
from linebot.models.events import Event
from linebot.webhook import WebhookPayload

from flask_line import app, line_bot_api, parser
from fsm import LinebotMachine

user_machines: Dict[str, LinebotMachine] = dict()


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        events: Union[WebhookPayload, List[Event]] = parser.parse(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    if not isinstance(events, list):
        raise RuntimeError

    for event in events:
        if isinstance(event, MessageEvent) and \
                isinstance(event.message, TextMessage) and \
                isinstance(event.message.text, str):
            if event.source.user_id not in user_machines:
                user_machines[event.source.user_id] = LinebotMachine()
                print('A LinebotMachine is created for User {}'.format(event.source.user_id))

            response = user_machines[event.source.user_id].advance(event)
            print('User {} → {}'.format(event.source.user_id, user_machines[event.source.user_id].state))

            if response == False:
                message: str = '很抱歉不太理解您的意思，但我依然會當個忠實的聽眾唷'
                line_bot_api.reply_message(reply_token=event.reply_token, messages=TextSendMessage(text=message))

        elif isinstance(event, FollowEvent):
            if event.source.user_id not in user_machines:
                user_machines[event.source.user_id] = LinebotMachine()
                print('A LinebotMachine is created for User {}'.format(event.source.user_id))
            template_message: TemplateSendMessage = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='股市追蹤小幫手',
                    text='歡迎使用股市追蹤小幫手！請選擇一項功能',
                    actions=user_machines[event.source.user_id].create_main_menu()
                )
            )
            line_bot_api.reply_message(reply_token=event.reply_token, messages=template_message)

    return 'OK'
