import telebot
import json
import random

from telebot import types

bot = telebot.TeleBot('8040954547:AAHzO-szTBX9Er4nVoSY0FfllSySByJi3LU')
# @SuperSphinx_bot

with open('scenario.json', 'r', encoding='utf-8') as file:
    scenario = json.load(file)

user_states = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_states[message.chat.id] = {"current_node": "start", "score": 0}  # Устанавливаем начальное состояние
    send_node(message.chat.id, "start")


def send_node(chat_id, node_key):
    node = scenario[node_key]
    user_states[chat_id]["current_node"] = node_key

    bot.send_message(chat_id, node["text"])

    if node.get("media"):
        with open(node["media"], "rb") as media_file:
            bot.send_photo(chat_id, media_file)

    if node.get("options"):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for option_key, option in node["options"].items():
            markup.add(option_key + ". " + option["text"])
        bot.send_message(chat_id, "Выбери:", reply_markup=markup)
    else:
        bot.send_message(chat_id, "Игра окончена. Напиши /start, чтобы начать заново.",
                         reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id

    if chat_id not in user_states:
        bot.send_message(chat_id, "Напиши /start, чтобы начать.")
        return

    state = user_states[chat_id]
    current_node = state["current_node"]

    if current_node not in scenario or not scenario[current_node].get("options"):
        bot.send_message(chat_id, "Игра окончена. Напиши /start, чтобы начать заново.")
        return

    user_choice = message.text.split(".")[0].strip()
    if user_choice in scenario[current_node]["options"]:
        next_node = scenario[current_node]["options"][user_choice]["next"]
        send_node(chat_id, next_node)
    else:
        bot.send_message(chat_id, "Пожалуйста, выбери правильный вариант ответа.")


bot.polling()
