from typing import Union, Dict, List

from flask import request, abort, send_file
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, UnfollowEvent, TemplateSendMessage, ButtonsTemplate
from linebot.models.events import Event
from linebot.webhook import WebhookPayload

from flask_line import app, line_bot_api, parser
from fsm import LinebotMachine
from models import UserState, UserStock

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
                if UserState.get_user_state(userid=event.source.user_id) != None:
                    user_machines[event.source.user_id].state = UserState.get_user_state(    # type: ignore
                        userid=event.source.user_id
                    )   # yapf: disable
                print('A LinebotMachine is created for User {}'.format(event.source.user_id))

            response = user_machines[event.source.user_id].advance(event)
            UserState.set_user_state(userid=event.source.user_id, state=user_machines[event.source.user_id].state)
            print('User {} → {}'.format(event.source.user_id, user_machines[event.source.user_id].state))

            if response == False:
                message: str = '很抱歉不太理解您的意思，但我依然會當個忠實的聽眾唷'
                line_bot_api.reply_message(reply_token=event.reply_token, messages=TextSendMessage(text=message))

        elif isinstance(event, FollowEvent):
            if event.source.user_id not in user_machines:
                user_machines[event.source.user_id] = LinebotMachine()
                UserState.set_user_state(userid=event.source.user_id, state=user_machines[event.source.user_id].state)
                print('A LinebotMachine is created for User {}'.format(event.source.user_id))
            template_message: TemplateSendMessage = TemplateSendMessage(
                alt_text='股市追蹤 - 主選單',
                template=ButtonsTemplate(
                    title='股市追蹤小幫手',
                    text='歡迎使用股市追蹤小幫手！這是本頻道的主選單，請從這邊開始盡情享受服務吧',
                    actions=user_machines[event.source.user_id].create_main_menu()
                )
            )
            line_bot_api.reply_message(reply_token=event.reply_token, messages=template_message)

        elif isinstance(event, UnfollowEvent):
            user_machines.pop(event.source.user_id, None)
            UserState.delete_user(userid=event.source.user_id)
            UserStock.delete_user(userid=event.source.user_id)
            print('User {} has been deleted from my database.'.format(event.source.user_id))

    return 'OK'


@app.route('/show-fsm-graph', methods=['GET'])
def show_fsm_graph():
    dump_path: str = LinebotMachine.create_fsm_graph()
    return send_file(dump_path, mimetype='image/png')
