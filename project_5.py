import telebot
import re
#from telegram import escape_markdown


token = ('8444389234:AAFRPlz74LySLomLc7-qLGp9v272mtaUhVI')


bot = telebot.TeleBot(token)


encrypted_text=''   # изначально создаем глобальные переменные
decrypted_text=''   # для текстов и ключа, чтобы потом можно было
key=''              # внутри функций их вызывать и изменять так же глобально
language = '/LV'

console_texts={
    '/LV': {
        'Start':'Sveiki! Šis robots var šifrēt vai atšifrēt jūsu ziņojumu. Izmēģiniet to, ievadot komandu /encrypt vai /decrypt!',
        'Encode':'Ir izvēlēta šifrēšana. Tagad atsūtiet man tekstu, kas man jāšifrē.',
        'Decode':'Ir izvēlēta atšifrēšana. Tagad atsūtiet man tekstu, kas man jāatšifrē.',
        'Key_encrypt':'Es redzu jūsu tekstu! Tagad atsūtiet man atslēgu, ko izmantošu šifrēšanai.',
        'Key_decrypt':'Es redzu jūsu tekstu! Tagad atsūtiet man atslēgu, ko izmantošu atšifrēšanai.',
        'Encoded_text':'Lieliski! Lūk, jūsu šifrētais teksts:',
        'Decoded_text':'Lieliski! Lūk, jūsu atfrētais teksts:',
        'Error':'Kļūda! Ievadiet lūdzu tekstu vēlreiz. Nelieto šādus simbolus: '
    },
    '/ENG': {
        'Start':'Hi! This bot can encrypt or decrypt your message. Try it by entering the /encrypt or /decrypt command!',
        'Encode':'Encryption selected. Now send me your text that I need to encrypt.',
        'Decode':'Decryption selected. Now send me your text that I need to decrypt.',
        'Key_encrypt':'I see your text! Now send me the key I will use to encrypt it.',
        'Key_decrypt':'I see your text! Now send me the key I will use to decrypt it.',
        'Encoded_text':'Excellent! Here is s your encrypted text:',
        'Decoded_text':'Excellent! Here is s your decrypted text:',
        'Error':'Error! Type your text one more time. Do not use prohibited symbols: '
    },
    '/RU': {
        'Start':'Привет! Этот бот может зашифровать или расшифровать твое сообщение. Попробуй, введя команду /encrypt или /decrypt !',
        'Encode':'Выбрана зашифровка. Скинь теперь свой текст, который я должен зашифровать.',
        'Decode':'Выбрана расшифровка. Скинь теперь свой текст, который я должен расшифровать.',
        'Key_encrypt':'Вижу твой текст! Скинь теперь ключ, по которому я буду его шифровать.',
        'Key_decrypt':'Вижу твой текст! Скинь теперь ключ, по которому я буду его расшифровывать.',
        'Encoded_text':'Отлично! Вот твой зашифрованный текст:',
        'Decoded_text':'Отлично! Вот твой расшифрованный текст:',
        'Error':'Ошибка! Введите текст еще раз. Пожалуйста, не используйте запрещенные символы: '
    }
}


alphabet = ['(', '%', 'h', 'W', 'ч', "'", '}', ']', 'U', 
            'Ā', 'ģ', '9', 'C', 'К', 'Ž', 'М', '+', 'ы', 
            'd', '!', 'Ū', 'У', 'w', '>', 'а', 'П', 'R', 
            'щ','\n', '&', 'F', 'Ņ', 'О', 's', 'I', 'Т', 
            'н', 'Ф', '4', ' ', 'A', 'l', ',', 'у', 'e', 
            'й', 'з', '.', 'д', 'А', 'P', 'č', ':', 'q', 
            'j', 'ю', 'р', '?', 'Й', 'r', 'Г', '^', 'H', 
            'с', '7', 'z', '2', '$', 'D', 'Э', 'Ц', '<', 
            'ī', '0', 'Ь', 'T', 'O', '/', 'a', 'в', 'п', 
            '5', 'V', 'З', '3', 'E', 'б', 'Ъ', 'v', 'ц', 
            'Н', 'Х', '@', 'S', 'Z', 'э', 'ь', 'm', 'š',
            '[', 'k', '6', 'N', 'С', 'G', '-', 'ё', 'x', 
            'В', '1', 'o', 'ж', 't', 'ш', 'J', 'B', '|', 
            '=', 'к', 'е', 'g', 'i', 'Е', 'Ы', 'Л', 'Р', 
            'L', 'K', 'Ю', 'Щ', 'Ш', '{', 'Д', ')', 'х', 
            'Y', ';', 'p', '#', 'т', 'И', 'Я', 'л', 'ф', 
            'b', 'Q', 'и', 'f', '"', 'X', '8', 'Ё', 'Ч', 
            'Б', 'о', 'y', 'ъ', 'u', 'c', 'м', 'я', 'M', 
            'Ж', 'n', 'г', 'ē', 'ļ', 'Ģ', 'Š', ''
            'ā', 'ņ', 'ū', 'Ī', 'Ļ', 'Č', 
            'ž']

            #'`','*','~','_',   


def encode(text,key, mode):
    """
    возвращает зашифрованный или расшифрованный текст
    text - обрабатываемый текст
    key - ключ шифрования
    mode - режим работы, предполагается "encrypt" и "decrypt"
    """
    if mode == "encrypt":
        a = 1
    elif mode == "decrypt":
        a = -1
    else:
        return "Error 404"                                         # decode function
    ready_text = ''                                                #  
    text_indexes = []                                              #
    key_indexes = [] 
    #print(f"""{mode}\n"{text}"\nkey: *** {key} ***""")                                              #
    for letter in text:                                            #
        text_indexes.append(alphabet.index(letter))                #
    for letter in key:                                             #
        key_indexes.append(alphabet.index(letter))                 #
    #print(f"")
    for i in range(len(text_indexes)):                             #
        text_indexes[i]+=key_indexes[i%len(key_indexes)]*a         #
        ready_text+=alphabet[text_indexes[i]%len(alphabet)]        #
    #print(f"\n{bytes(ready_text, "utf-8")}\n{[bin(ord(c)) for c in ready_text]}")
    return ready_text                                              #

def validate(text):
    """
    проверяет текст на наличие символов отсутствующих в словаре, возвращает True/False
    """
    rejected_symbols = ''
    for letter in text:
        if letter not in alphabet and letter not in rejected_symbols:
            rejected_symbols+=letter
    return rejected_symbols
@bot.message_handler(commands=['start','menu'])
def language_choice(message):
     bot.send_message(message.chat.id,  # encrypt и decrypt это зашифровка и расшифровка соответственно
                      'Choose the language: /LV ; /ENG ; /RU '
                      )
     bot.register_next_step_handler(message,start)
def start(message):
    global language
    language=message.text
    bot.send_message(message.chat.id, console_texts[language]['Start'])


def esc(text): 
    symbols='([_*\[\]()~`>#+\-=|{}.!])\\'
    replaced_symbols=''
    for letter in text:
        if letter in symbols and letter not in replaced_symbols:
            text=text.replace(letter,f'\\{letter}')
            replaced_symbols+=letter
    #return text
    return re.sub(r'([_*[]()~`>#+-=|{}.!])', r'\\\1', text)
#
#
# весь этот блок - только про зашифровку сообщения
#
#
@bot.message_handler(commands=['encrypt', 'decrypt',])
def mode_choice(message):
    if message.text == '/encrypt':
        bot.register_next_step_handler(message,ask_for_text)
        bot.send_message(message.chat.id, console_texts[language]["Encode"])

    elif message.text == '/decrypt':
        bot.register_next_step_handler(message,ask_for_text2)
        bot.send_message(message.chat.id, console_texts[language]["Decode"])


def ask_for_text(message):
    global encrypted_text
    encrypted_text = message.text
    if validate(encrypted_text):
        bot.send_message(message.chat.id,f'{console_texts[language]["Error"]} {validate(encrypted_text)}')
        bot.register_next_step_handler(message,ask_for_text)
        return
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, console_texts[language]["Key_encrypt"])
    bot.register_next_step_handler(message,ask_for_key)



def ask_for_key(message):
    global key
    key=message.text
    if validate(key):
        bot.send_message(message.chat.id,f'{console_texts[language]["Error"]} {validate(key)}')
        bot.register_next_step_handler(message,ask_for_key)
        return
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, console_texts[language]["Encoded_text"])
    text = encode(encrypted_text,key,'encrypt')
    bot.send_message(message.chat.id, 
                     f"||{esc(text)}||",
                     parse_mode = "MarkdownV2"
                     )
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
    if validate(decrypted_text):
        bot.send_message(message.chat.id,f'{console_texts[language]["Error"]} {validate(decrypted_text)}')
        bot.register_next_step_handler(message,ask_for_text2)
        return
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, console_texts[language]["Key_decrypt"])
    bot.register_next_step_handler(message,ask_for_key2)


def ask_for_key2(message):
    global key
    key=message.text
    if validate(key):
        bot.send_message(message.chat.id,f'{console_texts[language]["Error"]} {validate(key)}')
        bot.register_next_step_handler(message,ask_for_key2)
        return
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, console_texts[language]["Decoded_text"])
    text = encode(decrypted_text,key,'decrypt')
    bot.send_message(message.chat.id, 
                     f"||{esc(text)}||",  # || ||
                     parse_mode = "MarkdownV2"
                     )
#
#
#
#
#


bot.polling(none_stop=True, interval=0) # это должно стоять в самом конце, это mainloop
