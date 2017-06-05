import json
import time
import urllib
import requests
import dborder
import dbmenu
from datetime import datetime


db1 = dborder.DBOrder()
db2 = dbmenu.DBMenu()

TOKEN = "394797326:AAENj4pBxD86utZ4okjd_23Iy3_uQ8KeTOo"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


order = []


def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        menu_items = db2.get_items()
        if text == "/menu":
            message = "\n".join(menu_items)
            send_message(message, chat)
        elif text == "/order":
            keyboard = build_menu_keyboard(menu_items)
            send_message("Что вы пьете сегодня?", chat, keyboard)
        elif text == "/cancel":
            db1.delete_item(text)
            send_message("Надеемся увидится снова!", chat)

        elif text == "/start":
            send_message(
                "Good MO! Мы рады, что ты зашел к нам! Если хочешь посмотерть меню, отправь /menu. "
                "Если уже знаешь, что хочешь заказать, отправь /order. "
                "Для отмены отправь /cancel.",
                chat)
        elif text.startswith("/"):
            continue
        else:
            if text in menu_items:
                message = 'Ваш заказ: ' + text
                date = datetime.now()
                order.append(text)
                order.append(date)
                send_message(message, chat)
                send_message("Введите свое имя и время, в которое заберете свой заказ. ФОРМАТ ЗАПИСИ: Мария 10:30", chat)
            else:
                try:
                    order.append(text)
                    body = str(order[0])
                    person = str(order[2])
                    created = str(order[1])
                    tables_id = 1
                    db1.add_item(tables_id, body, person, created,)
                    send_message("Спасибо за заказ! Мы очень вас ждем!", chat)
                    order.clear()
                except:
                    send_message("Некорректно введены данные, повторите ввод", chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def build_menu_keyboard(menu_items):
    menu_keyboard = [[item] for item in menu_items]
    reply_markup = {"keyboard": menu_keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def main():
    # db1.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
