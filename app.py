import json
import flask
import requests
import settrade.openapi
import time
import sys
import linebot
import os

from flask import Flask, request, abort
from settrade.openapi import Investor

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, PostbackEvent, TextMessage, TextSendMessage, FlexSendMessage, QuickReply, QuickReplyButton, MessageAction, PostbackAction
)

#[STT-OPENAPI-AUTH]
#app_id = "MDQfX4OjSGxTPqa"
#app_secret = "BIhomc1bJN4XqCOyIW+OgVK9SqK4WwSJrhKqQjnGORA"
#app_code = "SANDBOX"
#broker_id = "SANDBOX"
app_id = os.environ['STT-OPENAPI-AUTH-APP-ID'] 
app_secret = os.environ['STT-OPENAPI-AUTH-APP-SECRET'] 
app_code = os.environ['STT-OPENAPI-AUTH-APP-CODE'] 
broker_id = os.environ['STT-OPENAPI-AUTH-BROKER-ID'] 
is_auto_queue = False
USER_BOT = os.environ['USER_BOT'] 
BOT_NAME = os.environ['BOT_NAME'] 
#settrade.openapi.Investor(app_id, app_secret, broker_id, app_code, is_auto_queue)

sandbox_balance = 0

app = Flask(__name__)

lineaccesstoken = 'Jq7k9B7z8B8XiAF1d3RM6ArQxNVxIZSR/5ar1kZM/i4JifJASL4pEcLVQgxv+6/fVODlumGnQg4d7Z9bbTnWNopm+qG4W1sQ4lak8UImYc8kC/LnARaoClL9bm1UMW5PrCW6xcUOs3abtcleo7i1PgdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(lineaccesstoken)
handler = WebhookHandler('314a6dc14b6f028ca89803ce048fa8c1')
investor = Investor(app_id= app_id ,app_secret = app_secret, app_code = app_code, broker_id = broker_id, is_auto_queue = is_auto_queue)
realtime = investor.RealtimeDataConnection()
equity = investor.Equity(account_no="lamphu-E") #For Original Teerasak
account_info = equity.get_account_info()
deri = investor.Derivatives(account_no="lamphu-D")
account_info_deri = deri.get_account_info()

time.sleep(0.25)

@app.route("/")
def hello_world():
    return BOT_NAME + "God Trader X48 It's Here !!"

account_info = equity.get_account_info()
print(account_info)
print('-------------------------------------')
print('-------------------------------------')
print('-------------------------------------')
print(account_info_deri)

@app.route('/webhook', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

print("Line Settrade API Start = My Account Name Is : >>",USER_BOT)
print("---------------------------------------------------------------------------------")
print("██   ██ ██   ██  █████   ██ ███████  ██  ██████  ██████  ██████  ██   ██ ██████ ") 
print(" ██ ██  ██   ██ ██   ██ ███ ██      ███ ██            ██      ██ ██   ██      ██") 
print("  ███   ███████  █████   ██ ███████  ██ ███████   █████   █████  ███████  █████ ") 
print(" ██ ██       ██ ██   ██  ██      ██  ██ ██    ██ ██           ██      ██ ██     ") 
print("██   ██      ██  █████   ██ ███████  ██  ██████  ███████ ██████       ██ ███████")     
print("---------------------------------------------------------------------------------")   

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    # user click rich menu
    if "My portfolio" in text:
        check_my_portfolio(event)
        
    # user send symbol to check the price before buy/sell
    else:
        sub = realtime.subscribe_price_info(
            event.message.text, on_message=price_info, args=(event,))
        sub.start()

def check_my_portfolio(event):
    portfolio = equity.get_portfolio()
    portfolio_datas = []

    # get data from each stock in portfolio
    for data in portfolio["data"]:
        # green color
        color_code = "#00df5b"
        if data["profit"] < 0:
            # red color, if the profit is minus
            color_code = "#ed1c24"

        content = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": data["symbol"],
                    "size": "xxl",
                    "weight": "bold",
                    "color": "#ffffff"
                },
                {
                    "type": "text",
                    "text": str(data["profit"]) + " (" + str(data["percent_profit"]) + "%)",
                    "size": "xl",
                    "weight": "bold",
                    "color": color_code
                },
                {
                    "type": "text",
                    "text": "Actual Vol " + str(data["actual_volume"]),
                    "size": "xs",
                    "color": "#bababa"
                },
                {
                    "type": "text",
                    "text": "Amount " + str(data["amount"]),
                    "size": "xs",
                    "color": "#bababa"
                },
                {
                    "type": "text",
                    "text": "Avg Price " + str(data["average_price"]),
                    "size": "xs",
                    "color": "#bababa"
                },
                {
                    "type": "text",
                    "text": "Market Price " + str(data["market_price"]),
                    "size": "xs",
                    "color": "#bababa"
                },
                {
                    "type": "text",
                    "text": "Market Value " + str(data["market_value"]),
                    "size": "xs",
                    "color": "#bababa"
                }
            ],
            "paddingTop": "5px"
        }
        portfolio_datas.append(content)

    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='My portfolio',
            contents={
                "type": "bubble",
                "size": "mega",
                "header": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [],
                    "backgroundColor": "#37e165",
                    "height": "10px"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": portfolio_datas,
                    "backgroundColor": "#0d0d0d"
                },
                "styles": {
                    "footer": {
                        "backgroundColor": "#0d0d0d"
                    }
                }
            }
        )
    )

def price_info(result, subscriber, event):
    high_price = result['data']['high']
    last_price = result['data']['last']
    low_price = result['data']['low']
    volume = result['data']['total_volume']
    symbol = event.message.text

    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text=symbol,
            contents={
                "type": "bubble",
                "size": "mega",
                "header": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [],
                    "backgroundColor": "#37e165",
                    "height": "10px"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": symbol,
                            "size": "xl",
                            "weight": "bold",
                            "color": "#a6a6a6"
                        },
                        {
                            "type": "text",
                            "text": str(last_price),
                            "size": "3xl",
                            "weight": "bold",
                            "color": "#ebebeb"
                        },
                        {
                            "type": "text",
                            "text": "High " + str(high_price),
                            "size": "xs",
                            "color": "#bababa"
                        },
                        {
                            "type": "text",
                            "text": "Low " + str(low_price),
                            "size": "xs",
                            "color": "#bababa"
                        },
                        {
                            "type": "text",
                            "text": "Volume " + str(volume),
                            "size": "xs",
                            "color": "#bababa"
                        },
                        {
                            "type": "separator",
                            "margin": "xl",
                            "color": "#bdbdbd"
                        }
                    ],
                    "paddingTop": "23px",
                    "backgroundColor": "#0d0d0d"
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "BUY",
                                            "size": "sm",
                                            "color": "#ffffff",
                                            "align": "center",
                                            "gravity": "center",
                                            "weight": "bold"
                                        }
                                    ],
                                    "height": "40px",
                                    "borderWidth": "medium",
                                    "borderColor": "#2edc39",
                                    "cornerRadius": "4px",
                                    "action": {
                                        "type": "postback",
                                        "label": "buy",
                                        "data": "symbol=" + symbol + "&side=buy&price=" + str(last_price)
                                    }
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "SELL",
                                            "size": "sm",
                                            "color": "#ffffff",
                                            "align": "center",
                                            "gravity": "center",
                                            "weight": "bold"
                                        }
                                    ],
                                    "height": "40px",
                                    "borderWidth": "medium",
                                    "borderColor": "#dc2e39",
                                    "cornerRadius": "4px",
                                    "action": {
                                        "type": "postback",
                                        "label": "sell",
                                        "data": "symbol=" + symbol + "&side=sell&price=" + str(last_price)
                                    }
                                }
                            ],
                            "spacing": "md"
                        }
                    ],
                    "paddingAll": "13px"
                },
                "styles": {
                    "footer": {
                        "backgroundColor": "#0d0d0d"
                    }
                }
            }
        )
    )
    # stop this subscription
    subscriber.stop()
        
@handler.add(PostbackEvent)
def handle_postback(event):
    postback_data = event.postback.data
    values = get_value_from_postback(postback_data)
    symbol = values[0]
    side = values[1]
    price = values[2]

    # case user confirm to buy/sell stock
    if "confirm=true" in postback_data:
        volume = values[3]
        place_order = equity.place_order(
            symbol=symbol,
            price=price,
            volume=volume,
            side=side,
            pin="your-pin")

    # case user click buy/sell after check the price
    elif "vol" not in postback_data:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Select the volume that you want to ' + side + ' ' + symbol + ' at price ' + price,
                            quick_reply=QuickReply(items=[
                                QuickReplyButton(action=PostbackAction(
                                    label='+100',
                                    display_text='+100',
                                    data=postback_data + '&vol=100'
                                )),
                                QuickReplyButton(action=PostbackAction(
                                    label='+300',
                                    display_text='+300',
                                    data=postback_data + '&vol=300'
                                )),
                                QuickReplyButton(action=PostbackAction(
                                    label='+500',
                                    display_text='+500',
                                    data=postback_data + '&vol=500'
                                )),
                                QuickReplyButton(action=PostbackAction(
                                    label='+700',
                                    display_text='+700',
                                    data=postback_data + '&vol=700'
                                )),
                                QuickReplyButton(action=PostbackAction(
                                    label='+1000',
                                    display_text='+1000',
                                    data=postback_data + '&vol=1000'
                                ))
                            ])))
    
    # case user already choose volume how much they want to buy/sell
    else:
        volume = values[3]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Confirm to ' + side + ' ' + symbol + ' at price ' + price + ' with volume ' + volume,
                            quick_reply=QuickReply(items=[
                                QuickReplyButton(action=PostbackAction(
                                    label='Confirm',
                                    display_text='Confirm to ' +
                                    side + ' ' + symbol + ' at price ' +
                                    price + ' with volume ' + volume,
                                    data=postback_data + '&confirm=true'
                                )),
                                QuickReplyButton(action=MessageAction(
                                    label='Cancel',
                                    text='Cancel'
                                ))
                            ])))

def get_value_from_postback(data):
    datas = data.split("&")
    values = []
    for word in datas:
        tmp_value = word.split("=")
        values.append(tmp_value[1])

    return values

if __name__ == '__main__':
    app.run()
