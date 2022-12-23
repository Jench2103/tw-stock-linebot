from typing import Union, Set, Dict, List

from transitions import Machine
from linebot.models import MessageEvent, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction

from .states import STATES, INIT_STATE
from .transistions import TRANSITIONS

from flask_line import line_bot_api
from models import StockInfo, UserStock
from stock_api import TWSE, FinMind


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

    def create_main_menu(self) -> List[MessageTemplateAction]:
        options: List[MessageTemplateAction] = [
            MessageTemplateAction(label='管理我收藏的股票', text='管理收藏股票'),
            MessageTemplateAction(label='股票名稱代號翻譯', text='股票名稱代號翻譯'),
            MessageTemplateAction(label='查詢收藏股票最新資訊', text='查詢收藏股票最新資訊'),
        ]
        return options

    def is_going_to_init(self, event: MessageEvent) -> bool:
        if self.state == 'stock_mgr' or self.state == 'list_stocks':
            return event.message.text == '離開'
        elif self.state == 'stock_lookup':
            return event.message.text == '取消'
        elif self.state == 'search_resp':
            return event.message.text == '退出'
        elif self.state in ['info_query', 'current_price', 'daily_price', 'latest_dividend']:
            return event.message.text == '離開'
        return False

    def on_enter_init(self, event: MessageEvent) -> None:
        template_message: TemplateSendMessage = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(title='股市追蹤小幫手', text='請選擇一項功能', actions=self.create_main_menu())
        )
        line_bot_api.reply_message(reply_token=event.reply_token, messages=template_message)

    # Stock Manager
    def create_stock_mgr_menu(self, menu_title: str, menu_text: str) -> TemplateSendMessage:
        template_message: TemplateSendMessage = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title=menu_title,
                text=menu_text,
                actions=[
                    MessageTemplateAction(label='新增股票', text='新增股票'),
                    MessageTemplateAction(label='刪除股票', text='刪除股票'),
                    MessageTemplateAction(label='查看已儲存清單', text='查看已儲存清單'),
                    MessageTemplateAction(label='離開', text='離開')
                ]
            )
        )
        return template_message

    def is_going_to_stock_mgr(self, event: MessageEvent) -> bool:
        if self.state == 'init':
            return event.message.text == '管理收藏股票'
        elif self.state == 'add_stock_operation' or self.state == 'delete_stock_operation':
            return event.message.text == '結束'
        print('execute: is_going_to_stock_mgr()')
        return False

    def on_enter_stock_mgr(self, event: MessageEvent) -> None:
        template_message: TemplateSendMessage = self.create_stock_mgr_menu(menu_title='股票管理', menu_text='請選擇一項功能')
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
            UserStock.create(userid=event.source.user_id, stock_id=stock_id)
            text_message: str = '{} 新增成功！歡迎繼續輸入股票代號以將其收藏，或輸入「結束」返回股票管理選單，謝謝'.format(stock_info.stock_name)
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

        if UserStock.delete(userid=event.source.user_id, stock_id=stock_id):
            stock_info: StockInfo = StockInfo.query.filter_by(_stock_id=stock_id).first()
            text_message: str = '{} 刪除成功！歡迎繼續輸入ID刪除股票，或輸入「結束」返回股票管理選單，謝謝'.format(stock_info.stock_name)
        else:
            text_message: str = '該檔股票未被儲存、或查無該股票代號，請確認後重新輸入，或輸入「結束」返回股票管理選單，謝謝'
        line_bot_api.reply_message(reply_token=event.reply_token, messages=TextSendMessage(text=text_message))

    def is_going_to_list_stocks(self, event: MessageEvent) -> bool:
        return event.message.text == '查看已儲存清單'

    def on_enter_list_stocks(self, event: MessageEvent) -> None:
        message_text: str = '您已儲存的股票包括：\n'
        stock_list: List[str] = UserStock.get_user_stock(userid=event.source.user_id)
        for index in range(len(stock_list)):
            message_text += '\n{idx}. {stock_id} {stock_name}'.format(
                idx=index + 1, stock_id=stock_list[index], stock_name=StockInfo.get_name(stock_list[index])
            )
        message_text += '\n\n請繼續利用「股票管理」功能選單進行操作，謝謝！'
        line_bot_api.reply_message(reply_token=event.reply_token, messages=TextSendMessage(text=message_text))

        template_message: TemplateSendMessage = self.create_stock_mgr_menu(menu_title='股票管理', menu_text='點選「離開」即可返回主選單')
        line_bot_api.push_message(to=event.source.user_id, messages=template_message)

    def is_going_to_stock_lookup(self, event: MessageEvent) -> bool:
        if self.state == 'init':
            return event.message.text == '股票名稱代號翻譯'
        return False

    def on_enter_stock_lookup(self, event: MessageEvent) -> None:
        message_text: str = '請輸入股票代號以查詢其名稱，或輸入簡稱查詢股票代號；如欲取消請輸入「取消」'
        line_bot_api.reply_message(reply_token=event.reply_token, messages=TextSendMessage(text=message_text))

    def is_going_to_search_resp(self, event: MessageEvent) -> bool:
        if self.state == 'stock_lookup':
            return event.message.text != '取消'
        elif self.state == 'search_resp':
            return event.message.text != '退出'

        return False

    def on_enter_search_resp(self, event: MessageEvent) -> None:
        token: str = event.message.text
        message_text: str = '如欲查詢下一筆資料請繼續輸入，或傳送「退出」回到主選單喔'

        result_name: Union[str, None] = StockInfo.get_name(token)
        result_id: Union[str, None] = StockInfo.get_id(token)

        if result_id != None:
            message_text = '{} 的代號是 {}，'.format(token, result_id) + message_text
        elif result_name != None:
            message_text = '代號 {} 的股票名稱是「{}」，'.format(token, result_name) + message_text
        else:
            message_text = '很抱歉查無資訊🥲\n' + message_text

        line_bot_api.reply_message(reply_token=event.reply_token, messages=TextSendMessage(text=message_text))

    # Info Query
    def create_info_query_menu(self, menu_title: str, menu_text: str) -> TemplateSendMessage:
        template_message: TemplateSendMessage = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title=menu_title,
                text=menu_text,
                actions=[
                    MessageTemplateAction(label='最新價格', text='最新價格'),
                    MessageTemplateAction(label='當日成交資訊', text='當日成交資訊'),
                    MessageTemplateAction(label='除權息資訊', text='除權息資訊'),
                    MessageTemplateAction(label='離開', text='離開')
                ]
            )
        )
        return template_message

    def is_going_to_info_query(self, event: MessageEvent) -> bool:
        return event.message.text == '查詢收藏股票最新資訊'

    def on_enter_info_query(self, event: MessageEvent) -> None:
        template_message: TemplateSendMessage = self.create_info_query_menu(
            menu_title='取得最新資訊', menu_text='收藏股票的最新狀態，從此一手掌握！'
        )
        line_bot_api.reply_message(reply_token=event.reply_token, messages=template_message)

    def is_going_to_current_price(self, event: MessageEvent) -> bool:
        return event.message.text == '最新價格'

    def on_enter_current_price(self, event: MessageEvent) -> None:
        message_text: str = '收藏股票的最新價格\n'
        stock_list: List[str] = UserStock.get_user_stock(userid=event.source.user_id)
        for idx in range(len(stock_list)):
            current_price: Union[float, None] = TWSE.ExchangeReport.get_current_price(stock_list[idx])
            if current_price != None:
                message_text += '\n{}. {} : {} 元'.format(idx + 1, stock_list[idx], str(current_price))
            else:
                message_text += '\n{}. {} : {}'.format(idx + 1, stock_list[idx], '查無價格資訊')
        line_bot_api.reply_message(reply_token=event.reply_token, messages=TextSendMessage(text=message_text))

        template_message: TemplateSendMessage = self.create_info_query_menu(menu_title='繼續查詢', menu_text='您還想知道哪些情報呢')
        line_bot_api.push_message(to=event.source.user_id, messages=template_message)

    def is_going_to_daily_price(self, event: MessageEvent) -> bool:
        return event.message.text == '當日成交資訊'

    def on_enter_daily_price(self, event: MessageEvent) -> None:
        message_text: str = '最近一個交易日的成交資訊：\n'
        stock_list: List[str] = UserStock.get_user_stock(userid=event.source.user_id)
        for idx in range(len(stock_list)):
            daily_price: Union[Dict[str, Union[str, int, float]], None] = FinMind.stock_daily_price(stock_list[idx])
            if daily_price != None:
                daily_msg: str = \
                    '在 {} 這天：\n'.format(daily_price['date']) + \
                    '   * 最高價：{} 元\n'.format(daily_price['max']) + \
                    '   * 最低價：{} 元\n'.format(daily_price['min']) + \
                    '   * 開盤價：{} 元\n'.format(daily_price['open']) + \
                    '   * 收盤價：{} 元\n'.format(daily_price['close'])
            else:
                daily_msg = '查無交易資訊'
            message_text += '\n{}. {} {}'.format(idx + 1, StockInfo.get_name(stock_list[idx]), daily_msg)

        line_bot_api.reply_message(reply_token=event.reply_token, messages=TextSendMessage(text=message_text))

        template_message: TemplateSendMessage = self.create_info_query_menu(menu_title='繼續查詢', menu_text='您還想知道哪些情報呢')
        line_bot_api.push_message(to=event.source.user_id, messages=template_message)

    def is_going_to_latest_dividend(self, event: MessageEvent) -> bool:
        return event.message.text == '除權息資訊'

    def on_enter_latest_dividend(self, event: MessageEvent) -> None:
        message_text: str = '最近一次除權息'
        stock_list: List[str] = UserStock.get_user_stock(userid=event.source.user_id)
        for idx in range(len(stock_list)):
            latest_dividend: Union[Dict[str, Union[str, float]], None] = FinMind.stock_dividend(stock_list[idx])
            if latest_dividend != None:
                dividend_msg: str = '最近一次在 {} 除息 {} 元及除權 {} 股，並在 {} 發放\n'.format(
                    latest_dividend['CashExDividendTradingDate'], str(latest_dividend['CashEarningsDistribution']),
                    str(latest_dividend['StockEarningsDistribution']), latest_dividend['CashDividendPaymentDate']
                )
            else:
                dividend_msg = '查無除權息資訊'
            message_text += '\n{}. {} : {}'.format(idx + 1, StockInfo.get_name(stock_list[idx]), dividend_msg)
        line_bot_api.reply_message(reply_token=event.reply_token, messages=TextSendMessage(text=message_text))

        template_message: TemplateSendMessage = self.create_info_query_menu(menu_title='繼續查詢', menu_text='您還想知道哪些情報呢')
        line_bot_api.push_message(to=event.source.user_id, messages=template_message)
