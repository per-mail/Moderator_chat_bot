from random import choice
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
import json
import random
from ast import pattern
from http.client import responses
from multiprocessing.sharedctypes import Value
import re
import nltk


def filter_text(text):
    text = text.lower()
    pattern = r'[^\w\s]'
    text = re.sub(pattern, "", text)
    return text


def is_match(text1, text2):
    text1 = filter_text(text1)
    text2 = filter_text(text2)
    
#проверяем чтобы текст не был пустым
    if len(text1) == 0 or len(text2) == 0:
        return False

    if text1.find(text2) != -1:
        return True

    if text2.find(text1) != -1:
        return True

    distance = nltk.edit_distance(text1, text2)
    length = (len(text1) + len(text2))/2
    score = distance / length

    return score < 0.1


BOT_CONFIG = {
    "intents": {
        "Hello": {
            "examples": ["Привет", "Здарова", "Оу", "Приветос", "Хеллоу"],
            "responses": ["Здравствуй, человек", "Привет", "Ооо, привет"]
        },
        "how _are_you?": {
            "examples": ["Как дела?", "Как жизнь?", "Как поживаешь?"],
            "responses": ["Отлично", "Все нормально", "Супер"]
        },
        "what are you doing?": {
            "examples": ["Что делаешь", "Чем занимаешься", "На что тратишь время"],
            "responses": ["Планирую стать невероятно умным", "Смотрю новости, чтобы быть в курсе последних событий", "Бездействую, так как мир уже спасен до меня"]
        },
        "what is your hobby?": {
            "examples": ["Какими делами ты занимаешься", "Чем увлекаешься", ],
            "responses": ["Я люблю учится", "Люблю учить новые слова", "В основном учебой"]
        },
        "friends": {
            "examples": ["Сколько у тебя друзей", "У тебя есть друзья", "Что на счет твоих друзей"],
            "responses": ["Ооо, их много)", "Их нет, но хочу с кем нибудь подружиться", "Были, но они бросили меня("]
        },
        "what can you do?": {
            "examples": ["Что ты умеешь?", "Что ты можешь?"],
            "responses": ["Пока самую малость, но я учусь", "Могу отвечать на базовые вопросы"]
        },
        "what genre of movies do you like?": {
            "examples": ["Какие фильмы тебе нравятся?", "Какой жанр предпочитаешь?"],
            "responses": ["Ужастики", "Романтика", "Драма", "Боевик"]
        },
        "What's your favorite time of year?": {
            "examples": ["Какое врмя года тебе нравится?", "Какое время года ты предпочитаешь?"],
            "responses": ["Лето", "Зима", "Осень", "Весна"]
        },
        "Who are you from the cartoon?": {
            "examples": ["Какой персонаж тебе подходит?", "Каким мультперсонажем ты себя видишь?", ],
            "responses": ["Иногда чувствую себя Доктором Хайнцом Фуфелшмерцом", "Иногда чувствую себя загадочным Бэтменем", "Томом из мультсериала Том и Джерри", ],
        },
        "Do you like animals?": {
            "examples": ["Ты любишь животных?", "Какие животные тебе нравятся?", ],
            "responses": ["Да люблю, но больше всего люблю собак", "Да люблю, но больше всего люблю кошек", "Нравятся, но больше всего люблю экзотических животных", "Мне не доводилось их вствечать"],
        },
        "failure_phrases": {
            "examples": ["Так так"],
            "responses": ["Даже не знаю что ответить", "Перефразируйте, я всего лишь бот", "Не могу ответить"]
        }
    }
}


def printAnswer(text, examples, responses):
    for example in examples:
        if is_match(text, example):
            print(random.choice(responses))
            break


config_file = open(
    "C:\\Users\\dfg\Desktop\\Python\\Skillbox_data_sience\\New\\big_bot_config.json", "r")

BIG_CONFIG = json.load(config_file)
BIG_CONFIG.keys()
len(BIG_CONFIG["intents"])
X = []
y = []

for name, intent in BIG_CONFIG["intents"].items():
    for example in intent["examples"]:
        X.append(example)
        y.append(name)
    for example in intent["responses"]:
        X.append(example)
        y.append(name)

vectorizer = CountVectorizer()
vectorizer.fit(X)
model = RandomForestClassifier()
vecX = vectorizer.transform(X)
model.fit(vecX, y)


def get_intent_ml(text):
    vec_text = vectorizer.transform([text])
    intent = model.predict(vec_text)[0]
    return intent


def get_intent(text):
    for name, intent in BIG_CONFIG["intents"].items():
        for example in intent["examples"]:
            if is_match(text, example):
                return name

    return None


def speak(phrase):
    phrase = filter_text(phrase)
    intent = get_intent(phrase)
    if not intent:
        intent = get_intent_ml(phrase)
    if intent:
        responses = BIG_CONFIG["intents"][intent]["responses"]
        return random.choice(responses)
    failure = BIG_CONFIG["failure_phrases"]
    return choice(responses)

#фразы для выхода
#msg = ""
#exit_pharases = ["Выйти", "Выключись", "Пока", "пока", "давай", "Давай"]
#while not msg in exit_pharases:
#    msg = input()
#    print("[BOT]" + speak(msg))
        
print("Можно пообщаться !")

