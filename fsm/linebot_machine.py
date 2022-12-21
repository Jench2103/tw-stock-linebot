from typing import Union, Union, Set, Dict, List

from transitions import Machine
from linebot.models import MessageEvent, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction

from .states import STATES, INIT_STATE
from .transistions import TRANSITIONS

from flask_line import line_bot_api
from models import StockInfo


class LinebotMachine(Machine):
    def __init__(
        self,
        states: List[str] = STATES,
        initial: str = INIT_STATE,
        transitions: List[Dict[str, str]] = TRANSITIONS,
        auto_transitions: bool = False
    ) -> None:
        super().__init__(
            model=Machine.self_literal,
            states=states,
            initial=initial,
            transitions=transitions,
            auto_transitions=auto_transitions
        )
        self.stock_set: Set[str] = set()

    def is_going_to_init(self, event: MessageEvent) -> bool:
        if self.state == 'stock_mgr':
            return event.message.text == '離開'
        return False

    def is_going_to_stock_mgr(self, event: MessageEvent) -> bool:
        if self.state == 'init':
            return event.message.text == '管理我的股票'
        elif self.state == 'add_stock_operation' or self.state == 'delete_stock_operation':
            return event.message.text == '結束'
        print('execute: is_going_to_stock_mgr()')
        return False

    def on_enter_stock_mgr(self, event: MessageEvent) -> None:
        template_message: TemplateSendMessage = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='股票管理',
                text='請選擇一項功能',
                actions=[
                    MessageTemplateAction(label='新增股票', text='新增股票'),
                    MessageTemplateAction(label='刪除股票', text='刪除股票'),
                    MessageTemplateAction(label='查看已儲存清單', text='查看已儲存清單'),
                    MessageTemplateAction(label='離開', text='離開')
                ]
            )
        )
        line_bot_api.reply_message(reply_token=event.reply_token, messages=template_message)

    def is_going_to_add_stock(self, event: MessageEvent) -> bool:
        return event.message.text == '新增股票'

    def on_enter_add_stock(self, event: MessageEvent) -> None:
        text_message: TextSendMessage = TextSendMessage(text='請輸入股票代號（ex. 新增台積電請輸入「2330」）')
        line_bot_api.reply_message(reply_token=event.reply_token, messages=text_message)

    def is_going_to_add_stock_operation(self, event: MessageEvent) -> bool:
        if self.state == 'add_stock':
            return True
        elif self.state == 'add_stock_operation':
            return event.message.text != '結束'
        return False

    def on_enter_add_stock_operation(self, event: MessageEvent) -> None:
        stock_id: str = event.message.text
        stock_info: Union[StockInfo, None] = StockInfo.query.filter_by(_stock_id=stock_id).first()
        if stock_info != None:
            self.stock_set.add(stock_id)
            text_message: str = '{} 新增成功！歡迎繼續輸入ID新增股票，或輸入「結束」返回股票管理選單，謝謝'.format(stock_info.short_name)
        else:
            text_message: str = '查無該股票代號，請確認後重新輸入ID，或輸入「結束」返回股票管理選單，謝謝'
        line_bot_api.reply_message(reply_token=event.reply_token, messages=TextSendMessage(text=text_message))

    def is_going_to_delete_stock(self, event: MessageEvent) -> bool:
        return event.message.text == '刪除股票'

    def on_enter_delete_stock(self, event: MessageEvent) -> None:
        text_message: TextSendMessage = TextSendMessage(text='請輸入股票代號（ex. 刪除台積電請輸入「2330」）')
        line_bot_api.reply_message(reply_token=event.reply_token, messages=text_message)

    def is_going_to_delete_stock_operation(self, event: MessageEvent) -> bool:
        if self.state == 'delete_stock':
            return True
        elif self.state == 'delete_stock_operation':
            return event.message.text != '結束'
        return False

    def on_enter_delete_stock_operation(self, event: MessageEvent) -> None:
        stock_id: str = event.message.text

        if stock_id in self.stock_set:
            stock_info: StockInfo = StockInfo.query.filter_by(_stock_id=stock_id).first()
            self.stock_set.remove(stock_id)
            text_message: str = '{} 刪除成功！歡迎繼續輸入ID刪除股票，或輸入「結束」返回股票管理選單，謝謝'.format(stock_info.short_name)
        else:
            text_message: str = '該檔股票未被儲存、或查無該股票代號，請確認後重新輸入，或輸入「結束」返回股票管理選單，謝謝'
        line_bot_api.reply_message(reply_token=event.reply_token, messages=TextSendMessage(text=text_message))
