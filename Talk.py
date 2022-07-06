#видео: https://live.skillbox.ru/webinars/code/znakomimsya-s-python-i-arkhitekturoi-umnogo-chat-bota200622/
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

#форматируем очищаем текст 
def filter_text(text):
    text = text.lower()# приводим текст к нижнему регистру
    pattern = r'[^\w\s]'# Регулярное выражение "Всё что не слово и не пробел"
    # \w\s -(слово или пробел) w(слово) s(пробел)
    # ^ - отрицание
    # [...]- символьная группа
    text = re.sub(pattern, "", text)# заменяем в тексте "Всё что не слово и не пробел" на "" 
    return text

#форматируем текст 
def is_match(text1, text2):
    text1 = filter_text(text1)# текст пользователя
    text2 = filter_text(text2)# ответ бота
    
#проверяем чтобы текст не был пустым
    if len(text1) == 0 or len(text2) == 0:
        return False
    
#смотрим содержатся ли слова (фразы) из базы в вводимом тексте
    if text1.find(text2) != -1:
        return True
#смотрим содержатся ли слова (фразы) из вводимого текста в базе
    if text2.find(text1) != -1:
        return True
    
#работа с опечатками, смотрим насколько вводимые слова отличаются от исходных
    distance = nltk.edit_distance(text1, text2)
    length = (len(text1) + len(text2))/2
    score = distance / length

    return score < 0.1# если разница меньше 10% то слова равны

#создаём список вопросов и ответов - интенты
BOT_CONFIG = {
    "intents": {
        "Hello": {
            "examples": ["Привет", "Здарова", "Оу", "Приветос", "Хеллоу"],
            "responses": ["Здравствуй, человек", "Привет", "Ооо, привет"] #интент
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

#классификация текстов. Ищем в базе подходящий интент на вводимую фразу
def printAnswer(text, examples, responses):
    for example in examples: 
        if is_match(text, example):
            print(random.choice(responses))
            break


config_file = open(
    "C:\\Users\\dfg\Desktop\\Python\\Skillbox_data_sience\\New\\big_bot_config.json", "r")

BIG_CONFIG = json.load(config_file)#загружаем интенты в BIG_CONFIG
BIG_CONFIG.keys()
len(BIG_CONFIG["intents"])
X = []#вводимая фраза
y = []#ответная фраза (интент)

#находим нужный интент по фразе
for name, intent in BIG_CONFIG["intents"].items():# пробегаемся по каждому интенту
    for example in intent["examples"]:#пробегаемся по examples
        X.append(example)# ответы из интентов
        y.append(name)# name-название интента
    for example in intent["responses"]:#пробегаемся по responses
        X.append(example)
        y.append(name)
        
# векторизация перевод текста в набор чисел
vectorizer = CountVectorizer()#создаём векторайзер
vectorizer.fit(X)# обучаем векторайзер
model = RandomForestClassifier()#Создаём модель
vecX = vectorizer.transform(X)#Преобразуем тексты в вектора
model.fit(vecX, y)#Обучаем модель

#функция которая будет работать с моделью
def get_intent_ml(text):
    vec_text = vectorizer.transform([text])#векторизуем текст
    intent = model.predict(vec_text)[0]#предсказывает ответный интент, берём первый элемент[0]
    return intent

#ищем интент в файле 
def get_intent(text):
    for name, intent in BIG_CONFIG["intents"].items():
        for example in intent["examples"]:
            if is_match(text, example):
                return name

    return None

print("Можно пообщаться !")

def speak(phrase):
    phrase = filter_text(phrase)
    intent = get_intent(phrase)#ищем интент
    if not intent:# если намерение не найдено
        intent = get_intent_ml(phrase)# пробуем подключить модель
    if intent:# если нашелся интент выводим его из BIG_CONFIG
        responses = BIG_CONFIG["intents"][intent]["responses"]
        return random.choice(responses)
    failure = BIG_CONFIG["failure_phrases"]
    return choice(responses)

#фразы для выхода
#msg = ""
#exit_pharases = ["Выйти", "Выключись", "Пока", "пока", "давай", "Давай"]
#while not msg in exit_pharases:#пока нет фразы для выхода
#    msg = input()
#    print("[BOT]" + speak(msg))
        


