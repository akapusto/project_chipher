import telebot
import re
#from telegram import escape_markdown


token = ('8444389234:AAFRPlz74LySLomLc7-qLGp9v272mtaUhVI')


bot = telebot.TeleBot(token)


encrypted_text=''   # изначально создаем глобальные переменные
decrypted_text=''   # для текстов и ключа, чтобы потом можно было
key=''              # внутри функций их вызывать и изменять так же глобально
language = 0

console_texts = {
     "Start": ['Sveiki! Šis robots var šifrēt vai atšifrēt jūsu ziņojumu. Izmēģiniet to, ievadot komandu /encrypt vai /decrypt!','Hi! This bot can encrypt or decrypt your message. Try it by entering the /encrypt or /decrypt command!','Привет! Этот бот может зашифровать или расшифровать твое сообщение. Попробуй, введя команду /encrypt или /decrypt !'],
     "Encode": ['Ir izvēlēta šifrēšana. Tagad atsūtiet man tekstu, kas man jāšifrē.','Encryption selected. Now send me your text that I need to encrypt.','Выбрана зашифровка. Скинь теперь свой текст, который я должен зашифровать.'],
     "Decode":['Ir izvēlēta atšifrēšana. Tagad atsūtiet man tekstu, kas man jāatšifrē.','Decryption selected. Now send me your text that I need to decrypt.','Выбрана расшифровка. Скинь теперь свой текст, который я должен расшифровать.'],
     "Key_encrypt":['Es redzu jūsu tekstu! Tagad atsūtiet man atslēgu, ko izmantošu tā šifrēšanai.','I see your text! Now send me the key I will use to encrypt it.','Вижу твой текст! Скинь теперь ключ, по которому я буду его шифровать.'],
     "Key_decrypt":['Es redzu jūsu tekstu! Tagad atsūtiet man atslēgu, ko izmantošu tā atšifrēšanai.','I see your text! Now send me the key I will use to decrypt it.','Вижу твой текст! Скинь теперь ключ, по которому я буду его расшифровывать.'],
     "Encoded_text":['Lieliski! Lūk, jūsu šifrētais teksts:','Excellent! Here is s your encrypted text:','Отлично! Вот твой зашифрованный текст:'],
     "Decoded_text":['Lieliski! Lūk, jūsu atfrētais teksts:','Excellent! Here is s your decrypted text:','Отлично! Вот твой расшифрованный текст:']

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
            'Н', 'Х', '@', 'S', 'Z', 'э', 'ь', '\\', 'm', 
            '[', 'k', '6', 'N', 'С', 'G', '-', 'ё', 'x', 
            'В', '1', 'o', 'ж', 't', 'ш', 'J', 'B', '|', 
            '=', 'к', 'е', 'g', 'i', 'Е', 'Ы', 'Л', 'Р', 
            'L', 'K', 'Ю', 'Щ', 'Ш', '{', 'Д', ')', 'х', 
            'Y', ';', 'p', '#', 'т', 'И', 'Я', 'л', 'ф', 
            'b', 'Q', 'и', 'f', '"', 'X', '8', 'Ё', 'Ч', 
            'Б', 'о', 'y', 'ъ', 'u', 'c', 'м', 'я', 'M', 
            'Ж', 'n', 'г', 'ē', 'ļ', 'Ģ', 'Š', 
            'ā', 'ņ', 'ū', 'Ī', 'Ļ', 'Č', 'š', 
            'ž']

            #'`','*','~','_',   


def encode(text,key, mode):
    if mode == "encrypt":
        a = 1
    elif mode == "decrypt":
        a = -1
    else:
        return "Error 404"                                              # decode function
    ready_text = ''                                                #  
    text_indexes = []                                              #
    key_indexes = []                                               #
    for letter in text:                                            #
        text_indexes.append(alphabet.index(letter))                #
    for letter in key:                                             #
        key_indexes.append(alphabet.index(letter))                 #
    for i in range(len(text_indexes)):                             #
        text_indexes[i]+=key_indexes[i%len(key_indexes)]*a           #
        ready_text+=alphabet[text_indexes[i]%len(alphabet)]        #
    return ready_text                                           #




@bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(message.chat.id,  # encrypt и decrypt это зашифровка и расшифровка соответственно
#                      'Привет! Этот бот может зашифровать или расшифровать твое сообщение. Попробуй, введя команду /encrypt или /decrypt !'
#
#                       )
def language_choice(message):
     bot.send_message(message.chat.id,  # encrypt и decrypt это зашифровка и расшифровка соответственно
                      'Choose the language: /LV ; /ENG ; /RU '
                      )
     
@bot.message_handler(commands=['LV','ENG','RU']) 
def start(message):
    global language
    if message.text == '/LV':
        language = 0
        bot.send_message(message.chat.id,  # encrypt и decrypt это зашифровка и расшифровка соответственно
                  console_texts["Start"][language])
    elif message.text == '/ENG':
        language = 1
        bot.send_message(message.chat.id,  # encrypt и decrypt это зашифровка и расшифровка соответственно
                  console_texts["Start"][language])
    elif message.text == '/RU':
        language = 2
        bot.send_message(message.chat.id,  # encrypt и decrypt это зашифровка и расшифровка соответственно
                  console_texts["Start"][language])

    
def esc(text): 
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)
#
#
# весь этот блок - только про зашифровку сообщения
#
#
@bot.message_handler(commands=['encrypt', 'decrypt'])
def mode_choice(message):
    if message.text == '/encrypt':
        bot.register_next_step_handler(message,ask_for_text)
        bot.send_message(message.chat.id, console_texts["Encode"][language])
        
    elif message.text == '/decrypt':
        bot.register_next_step_handler(message,ask_for_text2)
        bot.send_message(message.chat.id, console_texts["Decode"][language])
        

def ask_for_text(message):
    global encrypted_text
    encrypted_text = message.text
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, console_texts["Key_encrypt"][language])
    bot.register_next_step_handler(message,ask_for_key)

    

def ask_for_key(message):
    global key
    key=message.text
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, console_texts["Encoded_text"][language])
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
    bot.send_message(message.chat.id, console_texts["Key_decrypt"][language])
    bot.register_next_step_handler(message,ask_for_key2)


def ask_for_key2(message):
    global key
    key=message.text
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, console_texts["Decoded_text"][language])
    text = encode(decrypted_text,key,'decrypt')
    bot.send_message(message.chat.id, f"||{ esc(text) }||", parse_mode = "MarkdownV2")
#
#
#
#
#


bot.polling(none_stop=True, interval=0) # это должно стоять в самом конце, это mainloop
