from googletrans import Translator
translator = Translator()

def str_range_to_eng(text):
    count = len(text) % 1500
    add_count = 1500 - count + 1
    trans = ''
    for i in range(1500,len(text)+add_count,1500):
        trans += translator.translate(text[i-1500:i], dest='en', to_lang='en').text
    return trans

def str_range_to_th(text):
    count = len(text) % 1500
    add_count = 1500 - count + 1
    trans = ''
    for i in range(1500,len(text)+add_count,1500):
        trans += translator.translate(text[i-1500:i], dest='th', to_lang='th').text
    return trans