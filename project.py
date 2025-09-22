import telebot
import re


token = ('8444389234:AAFRPlz74LySLomLc7-qLGp9v272mtaUhVI')


bot = telebot.TeleBot(token)


encrypted_text=''   # изначально создаем глобальные переменные
decrypted_text=''   # для текстов и ключа, чтобы потом можно было
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
            'я', 'M', 'Ж', 'n', 'г',                     #
            #'`','*','~','_',                            #
            ]   




def encode(text,key, mode):
    if mode == "encrypt":
        a = 1
    elif mode == "decrypt":
        a = -1
    else:
        return "Error 404"                                         # decode function
    ready_text = ''                                                #  
    text_indexes = []                                              #
    key_indexes = []                                               #
    for letter in text:                                            #
        text_indexes.append(alphabet.index(letter))                #
    for letter in key:                                             #
        key_indexes.append(alphabet.index(letter))                 #
    for i in range(len(text_indexes)):                             #
        text_indexes[i]+=key_indexes[i%len(key_indexes)]*a         #
        ready_text+=alphabet[text_indexes[i]%len(alphabet)]        #
    return ready_text                                              #

    
def esc(text): 
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)
#
#
# весь этот блок - только про зашифровку сообщения
#
#
@bot.message_handler(commands=['encrypt', 'decrypt','start'])
def mode_choice(message):
    if message.text == '/encrypt':
        bot.register_next_step_handler(message,ask_for_text)
        bot.send_message(message.chat.id,'Выбрана зашифровка. Скинь теперь свой текст, который я должен зашифровать.')
        
    elif message.text == '/decrypt':
        bot.register_next_step_handler(message,ask_for_text2)
        bot.send_message(message.chat.id,'Выбрана расшифровка. Скинь теперь свой текст, который я должен расшифровать.')
    elif message.text == '/start':
        bot.send_message(message.chat.id,  # encrypt и decrypt это зашифровка и расшифровка соответственно
                     'Привет! Этот бот может зашифровать или расшифровать твое сообщение. Попробуй, введя команду /encrypt или /decrypt !'
                     )
        

def ask_for_text(message):
    global encrypted_text
    encrypted_text = message.text
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, 'Вижу твой текст! Скинь теперь ключ, по которому я буду его шифровать.')
    bot.register_next_step_handler(message,ask_for_key)

    

def ask_for_key(message):
    global key
    key=message.text
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, 'Отлично! Вот твой зашифрованный текст:')
    text = encode(encrypted_text,key,'encrypt')
    bot.send_message(message.chat.id, f"||{ esc(text) }||", parse_mode = "MarkdownV2")
#
#
#
#
#


#
#
# весь этот блок - только про расшифровку сообщения
#
#
def ask_for_text2(message):
    global decrypted_text
    decrypted_text = message.text
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, 'Вижу твой текст! Скинь теперь ключ, по которому я буду его расшифровывать.')
    bot.register_next_step_handler(message,ask_for_key2)


def ask_for_key2(message):
    global key
    key=message.text
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, 'Отлично! Вот твой расшифрованный текст:')
    text = encode(decrypted_text,key,'decrypt')
    bot.send_message(message.chat.id, f"||{ esc(text) }||", parse_mode = "MarkdownV2")
#
#
#
#
#


bot.polling(none_stop=True, interval=0) # это должно стоять в самом конце, это mainloop
