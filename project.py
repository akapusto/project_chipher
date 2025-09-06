import telebot


token = ('8444389234:AAFRPlz74LySLomLc7-qLGp9v272mtaUhVI')


bot = telebot.TeleBot(token)


encrypted_text=''   # изначально создаем глобальные переменные
decrypted_text=''   # для текстов и ключа, чтобы потом можно было
key=''              # внутри функций их вызывать и изменять так же глобально




alphabet = ['а','А','б','Б','в','В','г','Г','д', #
            'Д','е','Е','ё','Ё','ж','Ж','з','З', #
            'и','И','й','Й','к','К','л','Л','м', #
            'М','н','Н','о','О','п','П','р','Р', #  алфавит нужно будет расширить(добавить все ascii символы и табуляции желательно тоже)
            'с','С','т','Т','у','У','ф','Ф','х', #  и возможно сделать более рандомный порядок чтобы шифр был менее предсказуемый
            'Х','ц','Ц','ч','Ч','ш','Ш','щ','Щ', #
            'ъ','Ъ','ы','Ы','ь','Ь','э','Э','ю', #
            'Ю','я','Я',' ']




def encode(text,key,mode='encrypt'):                                              #
    ready_text = ''                                                #  
    text_indexes = []                                              #
    key_indexes = []                                               #
    for letter in text:                                            #
        text_indexes.append(alphabet.index(letter))                #
    for letter in key:                                             #
        key_indexes.append(alphabet.index(letter))                 #
    for i in range(len(text_indexes)):                             #
        text_indexes[i]+=key_indexes[i%len(key_indexes)]           #
        ready_text+=alphabet[text_indexes[i]%len(alphabet)]        #
    return ready_text                                              #




@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,  # encrypt и decrypt это зашифровка и расшифровка соответственно
                     'Привет! Этот бот может зашифровать или расшифровать твое сообщение. Попробуй, введя команду /encrypt или /decrypt !'
                     )
#
#
# весь этот блок - только про зашифровку сообщения
#
#
@bot.message_handler(command=['encrypt'])
def encrypt(message):
   bot.register_next_step_handler(message,ask_for_text)
   bot.reply_to(message,'Выбрана зашифровка. Скинь теперь свой текст, который я должен зашифровать.')
   ...
@bot.message_handler(func=encrypt) #func=encrypt значит, что этот handler будет выполняться только тогда, когда будет вызвана функция encrypt
def ask_for_text(message):
    global encrypted_text
    encrypted_text = message.text
    bot.reply_to(message, 'Вижу твой текст! Скинь теперь ключ, по которому я буду его шифровать.')
    bot.register_next_step_handler(message,ask_for_key)


@bot.message_handler(message=True)
def ask_for_key(message):
    global key
    key=message.text
    bot.send_message(message.chat.id, 'Отлично! Вот твой зашифрованный текст:')
    bot.send_message(message.chat.id, encode(encrypted_text,key))
#
#
#
#
#






bot.polling(none_stop=True, interval=0) # это должно стоять в самом конце, это mainloop
