import telebot
import re
import io

token = ('8444389234:AAFRPlz74LySLomLc7-qLGp9v272mtaUhVI')

bot = telebot.TeleBot(token)

encrypted_text=''   # global mainīgie
mrakobesije = {}    #šī vārdnīca ir vajadzīga, lai dažādi lietotāji varētu lietot robotu vienlaikus(lai katram lietotājam būtu atsevišķi mainīgie)

console_texts={ #Vārdnīca ar visām robota atbildēm dažādās valodās
    '/LV': {
        'Start':'Sveiki! Šis robots var šifrēt vai atšifrēt jūsu ziņojumu. Izmēģiniet to, ievadot komandu /encrypt vai /decrypt!',
        'Encode':'Ir izvēlēta šifrēšana. Tagad atsūtiet man tekstu, kas man jāšifrē.',
        'Decode':'Ir izvēlēta atšifrēšana. Tagad atsūtiet man tekstu, kas man jāatšifrē.',
        'Key_encrypt':'Es redzu jūsu tekstu! Tagad atsūtiet man atslēgu, ko izmantošu šifrēšanai.',
        'Key_decrypt':'Es redzu jūsu tekstu! Tagad atsūtiet man atslēgu, ko izmantošu atšifrēšanai.',
        'Encoded_text':'Lieliski! Lūk, jūsu šifrētais teksts:',
        'Decoded_text':'Lieliski! Lūk, jūsu atfrētais teksts:',
        'Error':'Kļūda! Ievadiet lūdzu tekstu vēlreiz. Nelieto šādus simbolus: ',
        'Error_type':'Kļūda! Nepazīstams ziņojuma tips. Lūdzu, sūtiet tikai teksta ziņojumus vai .txt failus.',
        'Error_lang':'Kļūda! Nepazīstama valoda! Izvelēties, lūdzu, vienu no piedavātam valodam!',
        'Language_change':'Valoda ir veiksmīgi atjaunota!',
        'Forbidden_symbols':'No teksta tika izdzēsti aizliegtie simboli: '
    },
    '/ENG': {
        'Start':'Hi! This bot can encrypt or decrypt your message. Try it by entering the /encrypt or /decrypt command!',
        'Encode':'Encryption selected. Now send me your text that I need to encrypt.',
        'Decode':'Decryption selected. Now send me your text that I need to decrypt.',
        'Key_encrypt':'I see your text! Now send me the key I will use to encrypt it.',
        'Key_decrypt':'I see your text! Now send me the key I will use to decrypt it.',
        'Encoded_text':'Excellent! Here is s your encrypted text:',
        'Decoded_text':'Excellent! Here is s your decrypted text:',
        'Error':'Error! Type your text one more time. Do not use prohibited symbols: ',
        'Error_type': 'Error! Unknown message type. Please send here only text messages or .txt files',
        'Error_lang': 'Error! Unknown language. Please choose one of provided languages',
        'Language_change':'Language has successfully changed!',
        'Forbidden_symbols':'Some forbidden symbols were deleted from your text: '
    },
    '/RU': {
        'Start':'Привет! Этот бот может зашифровать или расшифровать твое сообщение. Попробуй, введя команду /encrypt или /decrypt !',
        'Encode':'Выбрана зашифровка. Скинь теперь свой текст, который я должен зашифровать.',
        'Decode':'Выбрана расшифровка. Скинь теперь свой текст, который я должен расшифровать.',
        'Key_encrypt':'Вижу твой текст! Скинь теперь ключ, по которому я буду его шифровать.',
        'Key_decrypt':'Вижу твой текст! Скинь теперь ключ, по которому я буду его расшифровывать.',
        'Encoded_text':'Отлично! Вот твой зашифрованный текст:',
        'Decoded_text':'Отлично! Вот твой расшифрованный текст:',
        'Error':'Ошибка! Введите текст еще раз. Пожалуйста, не используйте запрещенные символы: ',
        'Error_type':'Ошибка! Неизвестный тип сообщения. Пожалуйста, присылайте только текстовые сообщения или файл формата .txt!',
        'Error_lang':'Ошибка! Неизвестный язык. Пожалуйста, выберите один из предложенных языков.',
        'Language_change':'Язык успешно был изменён!',
        'Forbidden_symbols': 'Некоторые запрещённые символы были удалены из текста: '
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
            'В', '1', 'o', 'ж', 't', 'ш', 'J', 'B', 'ž',
            '=', 'к', 'е', 'g', 'i', 'Е', 'Ы', 'Л', 'Р', 
            'L', 'K', 'Ю', 'Щ', 'Ш', '{', 'Д', ')', 'х', 
            'Y', ';', 'p', '#', 'т', 'И', 'Я', 'л', 'ф', 
            'b', 'Q', 'и', 'f', '"', 'X', '8', 'Ё', 'Ч', 
            'Б', 'о', 'y', 'ъ', 'u', 'c', 'м', 'я', 'M', 
            'Ж', 'n', 'г', 'ē', 'ļ', 'Ģ', 'Š',
            'ā', 'ņ', 'ū', 'Ī', 'Ļ', 'Č'
            ]

def encode(text,key, mode):
    """
    atgriež šifrēto un atšifrēto tekstu 
    text - teksts, kurš tiek apstrādāts
    key - atslēga šifrēšanai vai atšifrēšanai 
    mode - darba režīms("encrypt" vai "decrypt")
    """
    if mode == "encrypt":
        a = 1
    elif mode == "decrypt":
        a = -1
    else:
        return "Error 404"                                         
    ready_text = ''                                                
    text_indexes = []                                              
    key_indexes = []                                               
    for letter in text:                                            
        text_indexes.append(alphabet.index(letter))                
    for letter in key:                                             
        key_indexes.append(alphabet.index(letter))                                                            
    for i in range(len(text_indexes)):                             
        text_indexes[i]+=key_indexes[i%len(key_indexes)]*a         
        ready_text+=alphabet[text_indexes[i]%len(alphabet)]
    return ready_text                                              

def validate(text):
    """
    pārbauda vai teksts satur simbolus, kurus nav vārdnīcā, atgriež True/False
    """
    rejected_symbols = ''
    for letter in text:
        if letter not in alphabet and letter not in rejected_symbols:
            rejected_symbols+=letter
    return rejected_symbols

@bot.message_handler(commands=['start','menu'])
def language_choice(message): #Cita valodu izvēle
     global language
     if not message.text:
         bot.send_message(message.chat.id,console_texts[language]['Error_type'])
         bot.register_next_step_handler(message,language_choice)
         return
     bot.send_message(message.chat.id,  #encrypt un decrypt - tas ir teksta šifrēšana un atšifrēšana
                      'Choose the language: /LV ; /ENG ; /RU '
                      )
     bot.register_next_step_handler(message,start)

def start(message): #robota inicializācija
    global language
    if message.text not in ['/LV','/ENG','/RU']:
        language_choice(message)
        return
    mrakobesije[message.chat.id] = {
        'lang': message.text
    }
    
    language=message.text
    bot.send_message(message.chat.id, console_texts[mrakobesije[message.chat.id]['lang']]['Start'])


@bot.message_handler(commands=['lv','eng','ru']) #Dodam lietotājam iespēju izmainīt valodu jebkurā brīdī, izņemot laiku, kad strādā citas funkcija(/encrypt, /decrypt)
def change_language(message):
    global language
    mrakobesije[message.chat.id] = {
        'lang': message.text.upper()
    }
    
    language=message.text
    bot.send_message(message.chat.id, console_texts[mrakobesije[message.chat.id]['lang']]['Language_change'])


def esc(text): #Šī funkcija ir atbildīga par gatava teksta ekranēšanu, kas nozīmē noteikto simbolu izvadi ar "\"
    symbols=r'([_*\[\]()~`>#+\-=|{}.!])\\'
    replaced_symbols=''
    for letter in text:
        if letter in symbols and letter not in replaced_symbols:
            text=text.replace(letter,f'\\{letter}')
            replaced_symbols+=letter
    return re.sub(r'([_*[]()~`>#+-=|{}.!])', r'\\\1', text)
#
#
# Šis bloks par teksta šifrēšanu
#
#
@bot.message_handler(commands=['encrypt', 'decrypt'])
def mode_choice(message): #Lietotājs izvēlas režīmu(decrypt vai encrypt)
    if message.chat.id not in mrakobesije.keys():
        mrakobesije[message.chat.id] = {
        'lang': "/LV"
        }
    if not message.text:
         bot.send_message(message.chat.id,console_texts[mrakobesije[message.chat.id]['lang']]['Error_type'])
         bot.register_next_step_handler(message,mode_choice)
         return
    if message.text == '/encrypt':
        bot.register_next_step_handler(message,ask_for_text)
        bot.send_message(message.chat.id, console_texts[mrakobesije[message.chat.id]['lang']]["Encode"])

    elif message.text == '/decrypt':
        bot.register_next_step_handler(message,ask_for_text2)
        bot.send_message(message.chat.id, console_texts[mrakobesije[message.chat.id]['lang']]["Decode"])


def ask_for_text(message): #Programma prasa lietotāju uzrakstīt savu tekstu, kuru viņš gribētu pārveidot(šifrēšana)°
    mrakobesije[message.chat.id]['is_file'] = False
    mrakobesije[message.chat.id]['file_name'] = ''
    if message.document:
        if not message.document.file_name.lower().endswith('.txt'):  # ja fails nav txt formata 
            bot.send_message(message.chat.id,console_texts[mrakobesije[message.chat.id]['lang']]['Error_type'])
            bot.register_next_step_handler(message,ask_for_text)
            return
        else:
            mrakobesije[message.chat.id]['file_name']=message.document.file_name
        file = bot.get_file(message.document.file_id) # ieraksta saņemto failu mainīgajā
        file_bytes = bot.download_file(file.file_path) # pārveido failu baitos
        for enc in ('utf-8', 'utf-16', 'windows-1251', 'iso-8859-1'):
            try:
                text = file_bytes.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        #text=file_bytes.decode('utf-8') # bytes -> string
        mrakobesije[message.chat.id]['is_file'] = True   # lai noteiktu beigās, kada atbilde no bota ir vajadzīga(str or file)
        mrakobesije[message.chat.id]['encrypted_text']=text
    elif not message.text:
         bot.send_message(message.chat.id,console_texts[mrakobesije[message.chat.id]['lang']]['Error_type'])
         bot.register_next_step_handler(message,ask_for_text)
         return
    else:
        mrakobesije[message.chat.id]['is_file'] = False
        mrakobesije[message.chat.id]['encrypted_text'] = message.text
    forbidden_symbols=validate(mrakobesije[message.chat.id]['encrypted_text'])
    if forbidden_symbols:
        bot.send_message(message.chat.id,f"{console_texts[mrakobesije[message.chat.id]['lang']]['Forbidden_symbols']}{forbidden_symbols}")
        for symb in forbidden_symbols:
            mrakobesije[message.chat.id]['encrypted_text'] = mrakobesije[message.chat.id]['encrypted_text'].replace(symb, '')
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, console_texts[mrakobesije[message.chat.id]['lang']]['Key_encrypt'])
    bot.register_next_step_handler(message,ask_for_key)



def ask_for_key(message): #Programma prasa lietotāju uzrakstīt savu atslēgu, ar kuru viņš gribētu pārveidot savu tekstu(šifrēšana)
    if not message.text:
         bot.send_message(message.chat.id,console_texts[mrakobesije[message.chat.id]['lang']]['Error_type'])
         bot.register_next_step_handler(message,ask_for_key)
         return
    global key
    key=message.text
    mrakobesije[message.chat.id]['key'] = message.text
    if validate(mrakobesije[message.chat.id]['key']):
        bot.send_message(message.chat.id,f"{console_texts[mrakobesije[message.chat.id]['lang']]['Error']} {validate(mrakobesije[message.chat.id]['key'])}")
        bot.register_next_step_handler(message,ask_for_key)
        return
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    text = encode(mrakobesije[message.chat.id]['encrypted_text'],mrakobesije[message.chat.id]['key'],'encrypt')
    bot.send_message(message.chat.id, console_texts[mrakobesije[message.chat.id]['lang']]["Encoded_text"])
    if not mrakobesije[message.chat.id]['is_file']:
        bot.send_message(message.chat.id, 
                            f"||{esc(text)}||",
                            parse_mode = "MarkdownV2"
                            ) #šifrēta teksta izvade ar spoiler efektu
    else:
        bio = io.BytesIO()
        bio.write(text.encode('utf-8'))
        bio.name = f"encrypted_{mrakobesije[message.chat.id]['file_name']}"
        bio.seek(0)
        bot.send_document(message.chat.id,bio)


#
#
# Šis bloks par teksta atšifrēšanu
#
#
def ask_for_text2(message): #Programma prasa lietotāju uzrakstīt savu tekstu, kuru viņš gribētu pārveidot(atšifrēšana)
    mrakobesije[message.chat.id]['is_file'] = False
    mrakobesije[message.chat.id]['file_name'] = ''
    if message.document:
        if not message.document.file_name.lower().endswith('.txt'):  # ja fails nav txt formata 
            bot.send_message(message.chat.id,console_texts[mrakobesije[message.chat.id]['lang']]['Error_type'])
            bot.register_next_step_handler(message,ask_for_text2)
            return
        else:
            mrakobesije[message.chat.id]['file_name']=message.document.file_name
        file = bot.get_file(message.document.file_id) # ieraksta saņemto failu mainīgajā
        file_bytes = bot.download_file(file.file_path) # pārveido failu baitos
        text=file_bytes.decode('utf-8') # bytes -> string
        mrakobesije[message.chat.id]['is_file'] = True   # lai noteiktu beigās, kada atbilde no bota ir vajadzīga(str or file)
        mrakobesije[message.chat.id]['decrypted_text']=text
    elif not message.text:
         bot.send_message(message.chat.id,console_texts[mrakobesije[message.chat.id]['lang']]['Error_type'])
         bot.register_next_step_handler(message,ask_for_text2)
         return
    else:
        mrakobesije[message.chat.id]['is_file'] = False
        mrakobesije[message.chat.id]['decrypted_text'] = message.text
    forbidden_symbols=validate(mrakobesije[message.chat.id]['decrypted_text'])
    if forbidden_symbols:
        bot.send_message(message.chat.id,f"{console_texts[mrakobesije[message.chat.id]['lang']]['Forbidden_symbols']}{forbidden_symbols}")
        for symb in forbidden_symbols:
            mrakobesije[message.chat.id]['decrypted_text'] = mrakobesije[message.chat.id]['decrypted_text'].replace(symb, '')
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, console_texts[mrakobesije[message.chat.id]['lang']]["Key_decrypt"])
    bot.register_next_step_handler(message,ask_for_key2)


def ask_for_key2(message):#Programma prasa lietotāju uzrakstīt savu atslēgu, ar kuru viņš gribētu pārveidot savu tekstu(atšifrēšana)
    if not message.text:
         bot.send_message(message.chat.id,console_texts[mrakobesije[message.chat.id]['lang']]['Error_type'])
         bot.register_next_step_handler(message,ask_for_key2)
         return
    global key
    key=message.text
    mrakobesije[message.chat.id]['key'] = message.text
    if validate(mrakobesije[message.chat.id]['key']):
        bot.send_message(message.chat.id,f"{console_texts[mrakobesije[message.chat.id]['lang']]['Error']} {validate(mrakobesije[message.chat.id]['key'])}")
        bot.register_next_step_handler(message,ask_for_key2)
        return
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    text = encode(mrakobesije[message.chat.id]['decrypted_text'],mrakobesije[message.chat.id]['key'],'decrypt')
    bot.send_message(message.chat.id, console_texts[mrakobesije[message.chat.id]['lang']]["Decoded_text"])
    if not mrakobesije[message.chat.id]['is_file']:
        bot.send_message(message.chat.id, 
                            f"||{esc(text)}||",
                            parse_mode = "MarkdownV2"
                            ) #šifrēta teksta izvade ar spoiler efektu
    else:
        bio = io.BytesIO()
        bio.write(text.encode('utf-8'))
        bio.name = f"decrypted_{mrakobesije[message.chat.id]['file_name']}"
        bio.seek(0)
        bot.send_document(message.chat.id,bio)


bot.polling(none_stop=True, interval=0) # tas ir vienkārši vajadzīgs, lai bots strādātu(mainloop)
