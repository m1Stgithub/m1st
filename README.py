from time import sleep
import telebot
from telebot import types
import configure
import sqlite3
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


mas=[]
status = ['creator', 'administrator', 'member']

hidemark=types.ReplyKeyboardRemove(selective=False)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
bot = telebot.TeleBot(configure.config['token'])
CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#START
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я kngibot, созданный учеником "Хакаской национальной гимназии-интернат". Перед тем, как начать работать пройди верефекацию (Введи /ver)')
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Верификация
@bot.message_handler(commands=['ver'])
def verification(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton('Учитель🎓')
    item2=types.KeyboardButton('Учeник🔍')
    item3=types.KeyboardButton('В/Кл.Рук📖')
    markup.add(item1, item2, item3)
    mesgt=bot.send_message(message.chat.id, 'Кто вы, {0.first_name}?'.format(message.from_user), reply_markup = markup)
    bot.register_next_step_handler(mesgt,bot_message)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.message_handler(content_types=CONTENT_TYPES)
def bot_message(message): 
    if message.chat.type == "private":
        connect=sqlite3.connect('users.db')
        cursor=connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS teacher_id(
                idt NUMERIC,
                name NUMERIC
            ) """)
        connect.commit()
        cursor.execute("""CREATE TABLE IF NOT EXISTS student_id(
                ids INTEGER,
                name NUMERIC
            ) """)
        connect.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS ot_zadan(
                id_teach INTEGER,
                txt NUMERIC,
                doc NUMERIC,
                photo NUMERIC,
                voice NUMERIC,
                id_st INTEGER
            )""")
        connect.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS info(
                data NUMERIC,
                inf1 NUMERIC,
                inf2 NUMERIC,
                inf3 NUMERIC,
                inf4 NUMERIC
            )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS zadan(
                data NUMERIC,
                txt NUMERIC,
                doc NUMERIC,
                photo NUMERIC,
                voice NUMERIC
            ) """)
        connect.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS Mentor(
                name_v TEXT,
                idv INTEGER
            )""")

        con=sqlite3.connect('classes.db')
        cur=con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS class_id(
            name TEXT,
            idz INTEGER
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS chat_id(
                id INTEGER
            )""")

        people_id=message.chat.id
        cursor.execute(f"SELECT ids FROM student_id WHERE ids={people_id}")
        data1=cursor.fetchone()
    
        cursor.execute(f"SELECT idt FROM teacher_id WHERE idt={people_id}")
        data2=cursor.fetchone()

        cursor.execute(f"SELECT idv FROM Mentor WHERE idv = {people_id}")
        data3=cursor.fetchone()

        if message.text == 'Учeник🔍':
            mesage_st=bot.send_message(message.chat.id, text = 'Напишите свое ФИО полностью')
            bot.register_next_step_handler(mesage_st, name_st)

        if message.text == "В/Кл.Рук📖":
            mesage_v=bot.send_message(message.chat.id, text = 'Напишите свое ФИО полностью')
            bot.register_next_step_handler(mesage_v, name_v)

        if message.text == 'Учитель🎓':
            mesage_th=bot.send_message(message.chat.id, text = 'Напишите свое ФИО полностью')
            bot.register_next_step_handler(mesage_th, name_th)

        if message.text == 'Ещё зaдать📋':
            mesg31=bot.send_message(message.chat.id, text='Напишите задание классу📜, {0.first_name}.'.format(message.from_user))
            bot.register_next_step_handler(mesg31, Pereslat1)
        if message.text == 'Ещё зaдать🔑':
            mesg31=bot.send_message(message.chat.id, text='Напишите задание классу📜, {0.first_name}.'.format(message.from_user))
            bot.register_next_step_handler(mesg31, Pereslat2)
        if message.text == 'Ещё задать☑':
            mesg31=bot.send_message(message.chat.id, text='Напишите задание классу📜, {0.first_name}.'.format(message.from_user))
            bot.register_next_step_handler(mesg31, Pereslat)

        if message.text == 'Устоновить таймер⏲':
            send_notification2(message)


def additional(message):
    if message.text == '⬅ Назад':
        markup1=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_th1=types.KeyboardButton('Задать задание классу📜')
        item_th2=types.KeyboardButton('Проверить задание🔎')
        markup1.add(item_th1, item_th2)
        m=bot.send_message(message.chat.id, text='⬅ Назад', reply_markup=markup1)
        bot.register_next_step_handler(m, answert_th1)
    if message.text == 'Ещё зaдать📋':
        mesg31=bot.send_message(message.chat.id, text='Напишите задание классу📜, {0.first_name}.'.format(message.from_user))
        bot.register_next_step_handler(mesg31, Pereslat1)
    if message.text == 'Ещё зaдать🔑':
        mesg31=bot.send_message(message.chat.id, text='Напишите задание классу📜, {0.first_name}.'.format(message.from_user))
        bot.register_next_step_handler(mesg31, Pereslat2)
    if message.text == 'Ещё задать☑':
        mesg31=bot.send_message(message.chat.id, text='Напишите задание классу📜, {0.first_name}.'.format(message.from_user))
        bot.register_next_step_handler(mesg31, Pereslat)
#teacher
def name_th(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    people_id=message.chat.id
    cursor.execute(f"SELECT ids FROM student_id WHERE ids={people_id}")
    data1=cursor.fetchone()
    markup1=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_th1=types.KeyboardButton('Задать задание классу📜')
    item_th2=types.KeyboardButton('Проверить задание🔎')
    markup1.add(item_th1, item_th2)
    name_t=message.text
    cursor.execute(f"DELETE FROM teacher_id WHERE idt = {people_id} OR name = '{name_t}' ")
    connect.commit()
    if data1 is None:
        #add values in fields
        t_id=message.chat.id
        cursor.execute("INSERT INTO teacher_id (idt, name) VALUES(?, ?);", (t_id, name_t,))
        connect.commit()
        msgt=bot.send_message(message.chat.id, 'Выберите функцию, {0.first_name}.'.format(message.from_user), reply_markup = markup1)
        bot.register_next_step_handler(msgt, answert_th1)
    else:
        bot.send_message(message.chat.id, 'Вы уже выбрали Учeник🔍.Если вы хотите пройти верификацию занаво, то введите /adminver')

def answert_th1(message):
    if message.text == 'Задать задание классу📜':
        markup2=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
        item__th1=types.KeyboardButton('Классная работа📗')
        item__th2=types.KeyboardButton('Проверочная работа📕')
        markup2.add(item__th1, item__th2)
        msgt1=bot.send_message(message.chat.id,'Выберите функцию, {0.first_name}.'.format(message.from_user), reply_markup=markup2)
        bot.register_next_step_handler(msgt1, answert_th2)

    if message.text == 'Проверить задание🔎':
        con=sqlite3.connect('classes.db')
        cur=con.cursor()
        markproverk=types.ReplyKeyboardMarkup(resize_keyboard=True)
        cur.execute("SELECT name, idz FROM class_id")
        rows_p=cur.fetchall()
        buttons=[]
        for i in rows_p:
            buttons.append(i[0])
        markproverk.add(*buttons)
        msgvibor_16=bot.send_message(message.chat.id, 'Выберите класс, {0.first_name}.'.format(message.from_user), reply_markup=markproverk)
        bot.register_next_step_handler(msgvibor_16, vibor_1_16)            

def answert_th2(message):
    if message.text == 'Классная работа📗':
        markup1_1=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
        ith1=types.KeyboardButton('Просто выполнить задание📘')
        ith2=types.KeyboardButton('Задание надо отправить⏲')
        back=types.KeyboardButton('⬅ Назад')
        markup1_1.add(ith1, ith2, back)
        kl=bot.send_message(message.chat.id,'Выберите функцию, {0.first_name}.'.format(message.from_user), reply_markup=markup1_1)
        bot.register_next_step_handler(kl, answert_th3)
    
    if message.text == 'Проверочная работа📕': 
        vibor2(message)

def answert_th3(message):
    if message.text == 'Просто выполнить задание📘':
        vibor(message)

    if message.text == 'Задание надо отправить⏲':
        vibor1(message)

    if message.text == '⬅ Назад':
        additional(message)


#function(vibor for teacher)
def vibor(message):
    con=sqlite3.connect('classes.db')
    cur=con.cursor()
    markvibor=types.ReplyKeyboardMarkup(resize_keyboard=True)
    cur.execute("SELECT name, idz FROM class_id")
    rows=cur.fetchall()
    buttons=[]
    for i in rows:
        buttons.append(i[0])
    markvibor.add(*buttons)
    msgvibor=bot.send_message(message.chat.id, 'Выберите класс,{0.first_name}.'.format(message.from_user), reply_markup=markvibor)
    bot.register_next_step_handler(msgvibor, vibor_1)

def vibor_1(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    con=sqlite3.connect('classes.db')
    cur=con.cursor()
    mark=types.ReplyKeyboardMarkup(resize_keyboard=True)
    stop=types.KeyboardButton('Ещё зaдать🔑')
    back=types.KeyboardButton('⬅ Назад')
    mark.add(stop, back)
    cur.execute("SELECT name, idz FROM class_id")
    rows=cur.fetchall()
    for i in rows:
        if message.text == i[0]:
            chat_id = [int(i[1])]
            cursor.execute("INSERT INTO chat_id  VALUES(?);", chat_id)
            connect.commit()
    msgvibor_1=bot.send_message(message.chat.id, 'Напишите задание классу📜, {0.first_name}.'.format(message.from_user), reply_markup=mark)
    bot.register_next_step_handler(msgvibor_1, Pereslat2)    

def vibor1(message):
    con=sqlite3.connect('classes.db')
    cur=con.cursor()
    markvibor1=types.ReplyKeyboardMarkup(resize_keyboard=True)
    cur.execute("SELECT name, idz FROM class_id")
    rows=cur.fetchall()
    buttons=[]
    for i in rows:
        buttons.append(i[0])
    markvibor1.add(*buttons)
    msgvibor1=bot.send_message(message.chat.id, 'Выберите класс,{0.first_name}.'.format(message.from_user), reply_markup=markvibor1)
    bot.register_next_step_handler(msgvibor1, vibor1_1)

def vibor1_1(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    con=sqlite3.connect('classes.db')
    cur=con.cursor()
    mark=types.ReplyKeyboardMarkup(resize_keyboard=True)
    stop=types.KeyboardButton('Ещё зaдать📋')
    timer=types.KeyboardButton('Устоновить таймер⏲')
    back=types.KeyboardButton('⬅ Назад')
    mark.add(stop, timer, back)
    cur.execute("SELECT name, idz FROM class_id")
    rows=cur.fetchall()
    for i in rows:
        if message.text == i[0]:
            chat_id = [int(i[1])]
            cursor.execute("INSERT INTO chat_id  VALUES(?);", chat_id)
            connect.commit()
    msgvibor1_1=bot.send_message(message.chat.id, 'Напишите задание классу📜, {0.first_name}.'.format(message.from_user), reply_markup=mark)
    bot.register_next_step_handler(msgvibor1_1, Pereslat1)


def vibor2(message):
    con=sqlite3.connect('classes.db')
    cur=con.cursor()
    markvibor2=types.ReplyKeyboardMarkup(resize_keyboard=True)
    cur.execute("SELECT name, idz FROM class_id")
    rows=cur.fetchall()
    buttons=[]
    for i in rows:
        buttons.append(i[0])
    markvibor2.add(*buttons)  
    msgvibor2=bot.send_message(message.chat.id, text='Выберите класс, {0.first_name}.'.format(message.from_user), reply_markup=markvibor2)
    bot.register_next_step_handler(msgvibor2, vibor2_1) 

def vibor2_1(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    con=sqlite3.connect('classes.db')
    cur=con.cursor()
    mark=types.ReplyKeyboardMarkup(resize_keyboard=True)
    stop=types.KeyboardButton('Ещё задать☑')
    back=types.KeyboardButton('⬅ Назад')
    mark.add(stop, back) 
    cur.execute("SELECT name, idz FROM class_id")
    rows=cur.fetchall()
    for i in rows:
        if message.text == i[0]:
            chat_id = [int(i[1])]
            cursor.execute("INSERT INTO chat_id  VALUES(?);", chat_id)
            connect.commit()
    msgvibor2_1=bot.send_message(message.chat.id, 'Напишите задание классу📜, {0.first_name}.'.format(message.from_user), reply_markup=mark)
    bot.register_next_step_handler(msgvibor2_1, Pereslat)

def vibor_1_16(message):
    markup1=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_th1=types.KeyboardButton('Задать задание классу📜')
    item_th2=types.KeyboardButton('Проверить задание🔎')
    markup1.add(item_th1, item_th2)
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    cursor.execute("SELECT txt, doc, photo, voice, id_st FROM ot_zadan")
    zadaniya=cursor.fetchall()
    cursor.execute("SELECT ids, name FROM student_id")
    name_st=cursor.fetchall()
    mas3=[]  
    mas=[]   
    bot.send_message(message.chat.id, 'Задание отправили:') 
    for zad in zadaniya:
        for n in name_st:
            name=n
            if zad[-1]==name[0]:
                if name[1] not in mas:
                    bot.send_message(message.chat.id, text=name[1])
                    mas.append(name[1])
                else:
                    
                    if zad[0]!=0:
                        mas3.append(zad[0])
                        bot.send_message(message.chat.id, text =mas3[-1])
                    if zad[0]==0 and zad[1]!=0:
                        mas3.append(zad[1])
                        bot.send_document(message.chat.id, document=mas3[-1])
                    if zad[0]==0 and zad[1]==0 and zad[2]!=0:
                        mas3.append(zad[2])
                        bot.send_photo(message.chat.id, photo=mas3[-1])
                    if zad[0]==0 and zad[1]==0 and zad[2]==0 and zad[3]!=0:
                        mas3.append(zad[3])    
                        bot.send_voice(message.chat.id, voice=mas3[-1])
    mas3.clear()
    mas.clear()
    msgt=bot.send_message(message.chat.id, 'Выберите функцию, {0.first_name}.'.format(message.from_user), reply_markup = markup1)
    bot.register_next_step_handler(msgt, answert_th1)


#student
def name_st(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    people_id=message.chat.id
    cursor.execute(f"SELECT idt FROM teacher_id WHERE idt={people_id}")
    data2=cursor.fetchone()
    cursor.execute(f"SELECT idv FROM Mentor WHERE idv = {people_id}")
    data3=cursor.fetchone()
    murkup_st = types.ReplyKeyboardMarkup(resize_keyboard=True)
    st_class=types.KeyboardButton('Домашняя работа📕')
    st2_class=types.KeyboardButton('Отправить задание⏲')
    st1_class1=types.KeyboardButton('Задания сейчас📟')
    murkup_st.add(st_class, st1_class1, st2_class)
    name_s=message.text
    cursor.execute(f"DELETE FROM student_id WHERE ids = {people_id} OR name = '{name_s}' ")
    connect.commit()
    if (data2 or data3) is None:
        #add values in fields
        st_id=message.chat.id
        cursor.execute("INSERT INTO student_id (name, ids) VALUES(?, ?);", (name_s, st_id,))
        connect.commit()
        msgs=bot.send_message(message.chat.id, 'Выберите функцию, {0.first_name}.'.format(message.from_user), reply_markup = murkup_st)
        bot.register_next_step_handler(msgs, answert_st1)
    else:
        bot.send_message(message.chat.id, 'Вы уже выбрали Учитель🎓 или В/Кл.Рук📖.Если вы хотите пройти верификацию занаво, то введите /adminver') 
def menu_st(message):
    murkup_st = types.ReplyKeyboardMarkup(resize_keyboard=True)
    st_class=types.KeyboardButton('Домашняя работа📕')
    st2_class=types.KeyboardButton('Отправить задание⏲')
    st1_class1=types.KeyboardButton('Задания сейчас📟')
    murkup_st.add(st_class, st1_class1, st2_class)
    msgs=bot.send_message(message.chat.id, 'Выберите функцию, {0.first_name}.'.format(message.from_user), reply_markup = murkup_st)
    bot.register_next_step_handler(msgs, answert_st1)

def answert_st1(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor() 
    if message.text == 'Задания сейчас📟':
        vibor_st(message)

    if message.text == 'Отправить задание⏲':
        markzad_st=types.ReplyKeyboardMarkup(resize_keyboard=True)
        cursor.execute("SELECT name FROM teacher_id")
        teachers=cursor.fetchall()
        buttons=[]
        for th in teachers:
            buttons.append(th[0])
        markzad_st.add(*buttons)            
        msgzad_st=bot.send_message(message.chat.id, text='Выбирите своего Учителя🎓, {0.first_name}.'.format(message.from_user), reply_markup=markzad_st)
        bot.register_next_step_handler(msgzad_st, otpravka) 
    if message.text == 'Домашняя работа📕': 
        cursor.execute("SELECT data FROM zadan")
        zadan=cursor.fetchall()
        bot.send_message(message.chat.id, 'Ожидайте...', reply_markup=hidemark)
        for z in zadan:
            sleep(1.5)
            bot.send_message(message.chat.id, text=z)
        dz=bot.send_message(message.chat.id, 'Выбирите дату отправления домашнего задания📘 (Выпишите её)', reply_markup=hidemark)
        bot.register_next_step_handler(dz, homework)

def homework(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    cursor.execute("SELECT data, txt, photo, voice, doc FROM zadan")
    homeworks=cursor.fetchall()
    mas2=[]
    murkup_st1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    st_class1=types.KeyboardButton('Домашняя работа📕')
    st2_class1=types.KeyboardButton('Отправить задание⏲')
    st1_class2=types.KeyboardButton('Задания сейчас📟')
    murkup_st1.add(st_class1, st1_class2, st2_class1)
    for i in homeworks:
        if str(message.text) == i[0]:
            if i[1]!=0:
                mas2.append(i[1])
                bot.send_message(message.chat.id, text = mas2[-1])
            if i[1]==0 and i[2]!=0:
                mas2.append(i[2])
                bot.send_photo(message.chat.id, photo=mas2[-1])
            if i[1]==0 and i[2]==0 and i[3]!=0:
                mas2.append(i[3])
                bot.send_voice(message.chat.id, voice=mas2[-1])
            if i[1]==0 and i[2]==0 and i[3]==0 and i[4]!=0:
                mas2.append(i[4])    
                bot.send_document(message.chat.id, document=mas2[-1])
        mas2.clear()
    menu_st(message)
#function 
def otpravka(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    cursor.execute("SELECT name, idt FROM teacher_id")
    ot=cursor.fetchall()
    for j in ot:
        if message.text == j[0]:
            teach=[int(j[1])]
            cursor.execute("INSERT INTO ot_zadan (id_teach) VALUES(?);", teach)
            connect.commit()                      
            otp=bot.send_message(message.chat.id, 'Напишите задание🔎, {0.first_name}.'.format(message.from_user))
            bot.register_next_step_handler(otp, pereslat_th) 
#function vibor for student
def vibor_st(message):
    con=sqlite3.connect('classes.db')
    cur=con.cursor()
    markvibor_st=types.ReplyKeyboardMarkup(resize_keyboard=True)
    cur.execute("SELECT name, idz FROM class_id")
    rows=cur.fetchall()
    buttons=[]
    for i in rows:
        buttons.append(i[0])
    markvibor_st.add(*buttons)
    msgvibor_st=bot.send_message(message.chat.id, text='Выберите класс, {0.first_name}.'.format(message.from_user), reply_markup=markvibor_st)
    bot.register_next_step_handler(msgvibor_st, vibor_st_2) 

def vibor_st_2(message):
    con=sqlite3.connect('classes.db')
    cur=con.cursor()
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    cur.execute("SELECT name, idz FROM class_id")
    rows=cur.fetchall()
    for i in rows:
        if message.text == i[0]:
            chat_id = [int(i[1])]
            cursor.execute("INSERT INTO chat_id  VALUES(?);", chat_id)
            connect.commit()
    vibor_st_3(message)
def vibor_st_3(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    cursor.execute("SELECT id FROM chat_id")
    chats=cursor.fetchall()
    chat_id=chats[-1]
    classroom=chat_id[0]
    user_status = str(bot.get_chat_member(chat_id=classroom, user_id=message.from_user.id).status)    
    if user_status in status:
        mas1=[]
        cursor.execute("SELECT txt, photo, voice, doc  FROM zadan")
        rows=cursor.fetchall()
        for i in rows:
            k=i
        if k[0]!=0:
            mas1.append(k[0])
            bot.send_message(message.chat.id, text = mas1[-1])
        if k[0]==0 and k[1]!=0:
            mas1.append(k[1])
            bot.send_photo(message.chat.id, photo=mas1[-1])
        if k[0]==0 and k[1]==0 and k[2]!=0:
            mas1.append(k[2])
            bot.send_voice(message.chat.id, voice=mas1[-1])
        if k[0]==0 and k[1]==0 and k[2]==0 and k[3]!=0:
            mas1.append(k[3])    
            bot.send_document(message.chat.id, document=mas1[-1])             
        mas1.clear()
    else: 
        bot.send_message(message.chat.id, 'Вы не состоите в группе с ботом')
    menu_st(message)
#mentor
def name_v(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    murkup_class = types.ReplyKeyboardMarkup(resize_keyboard=True)
    i_class=types.KeyboardButton('Создать класс🎩')
    i_class1=types.KeyboardButton('Информация📒')
    murkup_class.add(i_class, i_class1)
    people_id=message.chat.id
    cursor.execute(f"SELECT ids FROM student_id WHERE ids={people_id}")
    data1=cursor.fetchone()
    name_v=message.text
    cursor.execute(f"DELETE FROM Mentor WHERE idv = {people_id} OR name_v = '{name_v}' ")
    connect.commit()
    if data1 is None:
        #add values in fields
        v_id=message.chat.id
        cursor.execute("INSERT INTO Mentor (name_v, idv) VALUES(?, ?);", (name_v, v_id,))
        connect.commit()
        msgv=bot.send_message(message.chat.id, 'Выберите функцию, {0.first_name}.'.format(message.from_user), reply_markup = murkup_class)
        bot.register_next_step_handler(msgv, answert_v1)
    else:
        bot.send_message(message.chat.id, 'Вы уже выбрали Учeник🔍.Если вы хотите пройти верификацию занаво, то введите /adminver')

def answert_v1(message):
    if message.text == 'Информация📒':
        vibor_v(message)
    if message.text == 'Создать класс🎩':
        msgnamecreated=bot.send_message(message.chat.id, 'Напишите название чата класса , {0.first_name}.'.format(message.from_user))
        bot.register_next_step_handler(msgnamecreated, crname_class)

def crname_class(message):
    con=sqlite3.connect('classes.db')
    cur=con.cursor()
    name_class=message.text
    mas.append(name_class)
    idmsg=bot.send_message(message.chat.id, 'Напишите id группы класса (Воспользуетесь ботом @username_to_id_bot), {0.first_name}.'.format(message.from_user))
    bot.register_next_step_handler(idmsg, crid_class)

def crid_class(message):
    con=sqlite3.connect('classes.db')
    cur=con.cursor()
    id_class=int(message.text)
    cur.execute(f"SELECT idz FROM class_id WHERE idz = {id_class}")
    data5=cur.fetchone()
    if data5 is None:
        cur.execute("INSERT INTO class_id (name, idz) VALUES (?, ?);", (mas[0], id_class,))
        con.commit()
        bot.send_message(message.chat.id, 'Класс успешно создан, {0.first_name}.'.format(message.from_user))
    else:
        bot.send_message(message.chat.id, 'Класс с такими данными уже существет, {0.first_name}. (Если произвошла ошибка введите /admin)'.format(message.from_user))
    mas.clear()

def vibor_v(message):
    con=sqlite3.connect('classes.db')
    cur=con.cursor()
    markvibor_v=types.ReplyKeyboardMarkup(resize_keyboard=True)
    cur.execute("SELECT name, idz FROM class_id")
    rows=cur.fetchall()
    buttons=[]
    for i in rows:
        buttons.append(i[0])
    markvibor_v.add(*buttons)
    msgvibor_v=bot.send_message(message.chat.id, text='Выберите класс, {0.first_name}.'.format(message.from_user), reply_markup=markvibor_v)
    bot.register_next_step_handler(msgvibor_v, vibor_v_1) 

def vibor_v_1(message):
    murkup_class = types.ReplyKeyboardMarkup(resize_keyboard=True)
    i_class=types.KeyboardButton('Создать класс🎩')
    i_class1=types.KeyboardButton('Информация📒')
    murkup_class.add(i_class, i_class1)
    con=sqlite3.connect('classes.db')
    cur=con.cursor()
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    cur.execute("SELECT name, idz FROM class_id")
    rows=cur.fetchall()
    for i in rows:
        if message.text == i[0]:
            chat_id = [int(i[1])]
            cursor.execute("INSERT INTO chat_id  VALUES(?);", chat_id)
            connect.commit()
    msgvibor_v_1=bot.send_message(message.chat.id, 'Напишите информацию классу📜, {0.first_name}.'.format(message.from_user), reply_markup=murkup_class)
    bot.register_next_step_handler(msgvibor_v_1, Pereslat_info)



def send_notification(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    bot.send_message(message.chat.id, "45 минут идут")
    cursor.execute("SELECT id FROM chat_id")
    chats=cursor.fetchall()
    chat_id=chats[-1]
    classroom=chat_id[0]
    time_s = 10
    for t in range(time_s, 0, -1):
        sleep(1)
    bot.send_message(message.chat.id, "Время истекло")
    bot.send_message(chat_id=classroom, text="Время истекло")
    ad=bot.send_message(message.chat.id,'Выберите функцию, {0.first_name}.'.format(message.from_user)) 
    bot.register_next_step_handler(ad, additional)
def send_notification2(message):
    tim = bot.send_message(message.chat.id, "Укажите таймер в секундах")
    bot.register_next_step_handler(tim, timer)



def timer(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    cursor.execute("SELECT id FROM chat_id")
    chats=cursor.fetchall()
    chat_id=chats[-1]
    classroom=chat_id[0]
    time_s = int(message.text)
    eq=bot.send_message(chat_id=classroom, text=f"Ваш таймер {time_s} секунд")
    bot.send_message(message.chat.id, "Время идёт")
    for i in range(time_s, 0, -1):
        sleep(1)
    bot.send_message(message.chat.id, "Время истекло")
    bot.send_message(chat_id=classroom, text="Время истекло")
    ad=bot.send_message(message.chat.id,'Выберите функцию, {0.first_name}.'.format(message.from_user)) 
    bot.register_next_step_handler(ad, additional)

def Pereslat_info(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    import datetime
    dt_now = str(datetime.datetime.now())
    cursor.execute("SELECT id FROM chat_id")
    chats=cursor.fetchall()
    chat_id=chats[-1]
    classroom=chat_id[0]
    if message.text is None:
        text1=0
    else:
        text1=str(message.text)
        bot.send_message(chat_id=classroom, text=text1, reply_markup=hidemark)
    if message.document is None:
        doc=0
    else:
        doc=message.document.file_id
        bot.send_document(chat_id=classroom, document=doc,reply_markup=hidemark)
    if message.voice is None:
        voice1=0
    else:
        voice1=message.voice.file_id
        bot.send_voice(chat_id=classroom, voice=voice1,reply_markup=hidemark)
    if message.photo is None: 
        photo=0
    else:
        photo=message.photo[-1].file_id
        bot.send_photo(chat_id=classroom, photo=photo,reply_markup=hidemark)
    cursor.execute("INSERT INTO info (data, inf1, inf2, inf3, inf4) VALUES(?, ?, ?, ?, ?);", (dt_now, text1, doc, photo, voice1,))
    connect.commit()


def Pereslat2(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    import datetime
    cursor.execute("SELECT id FROM chat_id")
    chats=cursor.fetchall()
    chat_id=chats[-1]
    classroom=chat_id[0]
    dt_now = str(datetime.datetime.now())
    if message.text is None:
        text1=0
    else:
        text1=message.text
        bot.send_message(chat_id=classroom, text=text1, reply_markup=hidemark)
    if message.document is None:
        doc=0
    else:
        doc=message.document.file_id
        bot.send_document(chat_id=classroom, document=doc,reply_markup=hidemark)
    if message.voice is None:
        voice1=0
    else:
        voice1=message.voice.file_id
        bot.send_voice(chat_id=classroom, voice=voice1,reply_markup=hidemark)
    if message.photo is None: 
        photo=0
    else:
        photo=message.photo[-1].file_id
        bot.send_photo(chat_id=classroom, photo=photo,reply_markup=hidemark)
    cursor.execute("INSERT INTO zadan (data, txt, doc, photo, voice) VALUES(?, ?, ?, ?, ?);", (dt_now, text1, doc, photo, voice1,))
    connect.commit()
    ad=bot.send_message(message.chat.id,'Выберите функцию, {0.first_name}.'.format(message.from_user)) 
    bot.register_next_step_handler(ad, additional)

def Pereslat1(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    import datetime
    dt_now = str(datetime.datetime.now())
    cursor.execute("SELECT id FROM chat_id")
    chats=cursor.fetchall()
    chat_id=chats[-1]
    classroom=chat_id[0]
    if message.text is None:
        text1=0
    else:
        text1=str(message.text)
        bot.send_message(chat_id=classroom, text=text1, reply_markup=hidemark)
    if message.document is None:
        doc=0
    else:
        doc=message.document.file_id
        bot.send_document(chat_id=classroom, document=doc,reply_markup=hidemark)
    if message.voice is None:
        voice1=0
    else:
        voice1=message.voice.file_id
        bot.send_voice(chat_id=classroom, voice=voice1,reply_markup=hidemark)
    if message.photo is None: 
        photo=0
    else:
        photo=message.photo[-1].file_id
        bot.send_photo(chat_id=classroom, photo=photo,reply_markup=hidemark)
    cursor.execute("INSERT INTO zadan (data, txt, doc, photo, voice) VALUES(?, ?, ?, ?, ?);", (dt_now, text1, doc, photo, voice1,))
    connect.commit()


def Pereslat(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    import datetime
    cursor.execute("SELECT id FROM chat_id")
    chats=cursor.fetchall()
    chat_id=chats[-1]
    classroom=chat_id[0]
    dt_now = str(datetime.datetime.now())
    if message.text is None:
        text1=0
    else:
        text1=str(message.text)
        bot.send_message(chat_id=classroom, text=text1, reply_markup=hidemark)
    if message.document is None:
        doc=0
    else:
        doc=message.document.file_id
        bot.send_document(chat_id=classroom, document=doc,reply_markup=hidemark)
    if message.voice is None:
        voice1=0
    else:
        voice1=message.voice.file_id
        bot.send_voice(chat_id=classroom, voice=voice1,reply_markup=hidemark)
    if message.photo is None: 
        photo=0
    else:
        photo=message.photo[-1].file_id
        bot.send_photo(chat_id=classroom, photo=photo,reply_markup=hidemark)
    cursor.execute("INSERT INTO zadan (data, txt, doc, photo, voice) VALUES(?, ?, ?, ?, ?);", (dt_now, text1, doc, photo, voice1,))
    connect.commit()
    send_notification(message)
def pereslat_th(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    cursor.execute("SELECT id_teach FROM ot_zadan")
    chats_th=cursor.fetchall()
    chat_id=chats_th[-1]
    chat=chat_id[0]
    if message.text is None:
        text1=0
    else:
        text1=str(message.text)
    if message.document is None:
        doc=0
    else:
        doc=message.document.file_id
    if message.voice is None:
        voice1=0
    else:
        voice1=message.voice.file_id
    if message.photo is None: 
        photo=0
    else:
        photo=message.photo[-1].file_id
    cursor.execute("INSERT INTO ot_zadan (txt, doc, photo, voice, id_st) VALUES(?, ?, ?, ?, ?);", (text1, doc, photo, voice1, message.chat.id,))
    connect.commit()
    bot.send_message(message.chat.id, 'Задание было отпрвлено')
    menu_st(message)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------            
bot.polling(none_stop=True, interval=0)
