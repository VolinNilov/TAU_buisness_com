from distutils.command.config import config
from os import stat
import telebot
import pickle
from Config import *

bot = telebot.TeleBot(token)

def PrintUserData (message):
    msg = message.text # Текст сообщения, написаного пользователем
    user_id = message.from_user.id # Id пользователя в Телеграм
    f_name = message.from_user.first_name # Имя пользователя
    l_name = message.from_user.last_name # Фамилия пользователя
    username = message.from_user.username # Никнейм пользвателя
    
    print ("Пользователь " + username + " (" + f_name + " " + l_name + ") id: " + str (user_id) + " отправил сообщение: " + msg)

def Send (message, text): # Отправка сообщений. Использование: Send (message, ТЕКСТ)
    bot.send_message(message.from_user.id, text)

def SavePosts (posts):
    with open(data_file_name, 'wb') as f:
        return pickle.dump(posts, f)

def AddPost (text):
    if text == "":
        return not_added_exists
    try:
        posts = GetAllPosts ()
        if text in posts:
            return not_added_exists

        posts.append (text)
        SavePosts (posts)
        return successfull_added
    except:
        return not_added

def DeletePost (keyword): # Удалить статью
    posts = GetAllPosts ()
    deletedPost = nothing_find

    for post in posts:
        if keyword in post:
            print ("Статья Найдена: " + post)
            posts.remove (post)
            deletedPost = "Статья удалена:\n" + post
            break
            
    SavePosts (posts)
    return deletedPost

def LoadPost (keyword): # Загрузка статьи по ключевому слову
    posts = GetAllPosts ()
    currentPost = nothing_find

    for post in posts:
        if keyword in post:
            currentPost = post
            break
    return "Найдена статья:\n" + post

def GetAllPosts (): # Загрузить все посты
    p = []

    try:
        with open(data_file_name, 'rb') as f:
            p = pickle.load(f)
    except:
        print ("[Ошибка загрузки данных]")

    return p
    
@bot.message_handler(commands=[add_post_command]) # Команда добавить статью
def add_post(message):
    PrintUserData (message)

    if not str (message.from_user.id) in admin_list:
        return

    opt = message.text.replace ("/" + add_post_command + " ", "")
    if len (opt) > 0:
        Send (message, AddPost (opt))

@bot.message_handler(commands=[delete_post_command]) # Команда удалить статью
def delete_post(message):
    PrintUserData (message)

    if str (not message.from_user.id) in admin_list:
        return

    opt = message.text.replace ("/" + delete_post_command + " ", "")
    if len (opt) > 0:
        Send (message, DeletePost (opt))

@bot.message_handler(commands=[show_all_posts_command]) # Команда показать все статьи
def show_all_posts(message):
    PrintUserData (message)

    posts = GetAllPosts ()
    txt = "Найдено статей: " + str (len (posts)) + "\n"
    for post in posts:
        txt += post + "\n\n"
    Send (message, txt)

@bot.message_handler(commands=['start'])
def start_message(message):
	Send (message, hello_message)

@bot.message_handler(content_types=['text']) # Обработка обычных сообщений
def get_text_messages(message):
    msg = message.text # Текст сообщения, написаного пользователем
    user_id = message.from_user.id # Id пользователя в Телеграм
    f_name = message.from_user.first_name # Имя пользователя
    l_name = message.from_user.last_name # Фамилия пользователя
    username = message.from_user.username # Никнейм пользвателя
    
    print ("Пользователь " + username + " (" + f_name + " " + l_name + ") id: " + str (user_id) + " отправил сообщение: " + msg)

    post = LoadPost (msg)
    Send (message, post)

bot.polling(none_stop=True, interval=0)