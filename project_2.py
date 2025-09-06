import telebot
token = ('8444389234:AAFRPlz74LySLomLc7-qLGp9v272mtaUhVI') 
bot = telebot.TeleBot(token)

text_input=''       # изначально создаем глобальные переменные 
                    # для текстов и ключа, чтобы потом можно было 
key=''              # внутри функций их вызывать и изменять так же глобально 

alphabet = ['(', '%', 'h', 'W', 'ч', "'", '}', ']', 'U', #
            '9', 'C', 'К', 'М', '+', 'ы', 'd', '!', 'У', # символы ~ _ * ` быть не должны в алфавите,
            'w', '>', 'а', 'П', 'R', 'щ','\n', '&', 'F', # потому что это знаки форматирования в телеграме
            'О', 's', 'I', 'Т', 'н', 'Ф', '4', ' ', 'A', # 
            'l', ',', 'у', 'e', 'й', 'з', '.', 'д', 'А', # 
            'P', ':', 'q', 'j', 'ю', 'р', '?', 'Й', 'r', #
            'Г', '^', 'H', 'с', '7', 'z', '2', '$', 'D', #
            'Э', 'Ц', '<', '0', 'Ь', 'T', 'O', '/', 'a', #
            'в', 'п', '5', 'V', 'З', '3', 'E', 'б', 'Ъ', #
            'v', 'ц', 'Н', 'Х', '@', 'S', 'Z', 'э', 'ь', #
           '\\', 'm', '[', 'k', '6', 'N', 'С', 'G', '-', #
            'ё', 'x', 'В', '1', 'o', 'ж', 't', 'ш', 'J', #
            'B', '|', '=', 'к', 'е', 'g', 'i', 'Е', 'Ы', #
            'Л', 'Р', 'L', 'K', 'Ю', 'Щ', 'Ш', '{', 'Д', #
            ')', 'х', 'Y', ';', 'p', '#', 'т', 'И', 'Я', #
            'л', 'ф', 'b', 'Q', 'и', 'f', '"', 'X', '8', #
            'Ё', 'Ч', 'Б', 'о', 'y', 'ъ', 'u', 'c', 'м', #
            'я', 'M', 'Ж', 'n', 'г',                 #
            #'`','*','~','_',                            #
            ]

def format_text(text,abc=alphabet):
    """
    проверяет строку на запрещенные символы и оставляет только те, что есть в алфавите
    """
    if not text:
        return None
    valid_text=''
    for letter in text:
        if letter in abc:
            valid_text+=letter
    return valid_text
def is_valid(k,abc=alphabet):
    """
    Проверяет ключ на наличие запрещенных символов. Если такие есть - возвращает первый из них
    """
    for letter in k:
        if letter not in abc:
            return letter
    return False

def chipher(text,key,mode='encrypt'):
    """
    шифрует сообщение text по заданному ключу key
    mode принимает значения encrypt и decrypt - расшифровка и зашифровка соответственно
    """                                                            #
    if mode == 'encrypt':                                          #  
        koef=1                                                     #
    elif mode == 'decrypt':                                        #
        koef=-1                                                    #  koef это просто 1 или -1 в зависимости от того, какой режим
    ready_text = ''                                                #  выбрал пользователь. Если пользователь выбрал режим ЗАшифровки, то
    text_indexes = []                                              #  koef положительный и, соответственно, индексы ключа будут прибавляться
    key_indexes = []                                               #  к индексам текста. А если koef == -1, то индексы будут наоборот отниматься
    for letter in text:                                            #  (т.е. будет расшифровка текста)
        text_indexes.append(alphabet.index(letter))                #
    for letter in key:                                             #
        key_indexes.append(alphabet.index(letter))                 #                              #
    for i in range(len(text_indexes)):                             #
        text_indexes[i]+=(key_indexes[i%len(key_indexes)]+1)*koef    # <---- вот здесь этот koef только и работает
        text_indexes[i]%=len(alphabet)                             #
        ready_text+=alphabet[text_indexes[i]]                      #
        if (i+1)%len(key_indexes) == 0:                        
            for j in range(len(key_indexes)):                  
                key_indexes[j]*=2                              
                key_indexes[j]%=len(alphabet)                  
    return ready_text                                          


@bot.message_handler(commands=['start'],content_types=['text','document']) 
def start(message):
    bot.send_message(message.chat.id,
                     'Привет! Этот бот может зашифровать или расшифровать твое сообщение. Попробуй, введя команду /encrypt или /decrypt !' 
                     )
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,'Список доступных команд:\n/start - запустить бота\n/help - вызвать это меню\n/encrypt - зашифровать сообщение\n/decrypt - расшифровать сообщение')    
#
#
# начало блока с зашифровкой
#
#
@bot.message_handler(commands=['encrypt']) 
def encrypt(message):
   bot.reply_to(message,'Выбрана зашифровка. Скинь теперь свой текст, который я должен зашифровать.')
   bot.register_next_step_handler(message,ask_for_text_to_encrypt) #register_next_step_handler - принимает новое сообщение от пользователя 
def ask_for_text_to_encrypt(message):                              #и указывает функцию, которая должна обработать его                    
    global text_input
    text_input=format_text(message.text)
    bot.reply_to(message, 'Вижу твой текст! Скинь теперь ключ, по которому я буду его шифровать.')
    bot.register_next_step_handler(message,ask_for_key_to_encrypt)
    print(text_input)
def ask_for_key_to_encrypt(message):
    global key
    key=message.text
    if is_valid(key):
        bot.reply_to(message,f'Твой ключ содержит недопустимый символ - {is_valid(key)}. Пожалуйста, выбери другой пароль!')
        bot.register_next_step_handler(message,ask_for_key_to_encrypt)
    else:
        #key=key.replace('\n','').replace('\t','').replace(' ','')   
        bot.send_message(message.chat.id, 'Отлично! Вот твой зашифрованный текст:')
        bot.send_message(message.chat.id, chipher(text_input,key))
        bot.send_message(message.chat.id,'Чтобы зашифровать что-то ещё, напиши /encrypt \nЕсли же ты хочешь что-то расшифровать, напиши /decrypt')
#
#
# конец блока с зашифровкой
#
#


#
#
# начало блока с зашифровкой
#
#
@bot.message_handler(commands=['decrypt'])
def decrypt(message):
    bot.reply_to(message,'Выбрана расшифровка. Скинь теперь свой текст, который я должен расшифровать.')
    bot.register_next_step_handler(message,ask_for_text_to_decrypt)   #register_next_step_handler - принимает новое сообщение от пользователя                    
def ask_for_text_to_decrypt(message):                                 #и указывает функцию, которая должна обработать его
    global text_input
    text_input=format_text(message.text)
    bot.reply_to(message, 'Вижу твой текст! Скинь теперь ключ, по которому я буду его расшифровывать.')
    bot.register_next_step_handler(message,ask_for_key_to_decrypt)
def ask_for_key_to_decrypt(message):
    global key
    key=message.text
    if is_valid(key):
        bot.reply_to(message,f'Твой ключ содержит недопустимый символ - {is_valid(key)}. Пожалуйста, выбери другой пароль!')
        bot.register_next_step_handler(message,ask_for_key_to_decrypt)
    else:
        bot.send_message(message.chat.id, 'Отлично! Вот твой расшифрованный текст:')
        bot.send_message(message.chat.id, chipher(text_input,key,mode='decrypt'))
        bot.send_message(message.chat.id,'Чтобы зашифровать что-то ещё, напиши /encrypt \nЕсли же ты хочешь что-то расшифровать, напиши /decrypt')
#
#
# конец блока с расшифровкой
#
#
@bot.message_handler()
def info(message):
    if message.from_user.is_bot:
        return
    bot.reply_to(message,f'Прости, я тебя не понимаю. Я понимаю только команды из списка /help :( {len(message.text)}')

bot.polling(none_stop=True, interval=0) # это должно стоять в самом конце, это mainloop
