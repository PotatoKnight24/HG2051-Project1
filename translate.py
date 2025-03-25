import requests
import nltk
import json
import string

# To load generated english to bahasa mapping from json file into a dictionary, removing any punctuation and making everything lowercase.
def load_dict(file_path): 
    with open('word_mapping.json','r',encoding='utf-8') as f:
        raw_dict = json.load(f)
        cleaned_dict = {}
        for k,v in raw_dict.items():
            k.strip().lower().translate(rm_punctiuation_table)
            cleaned_dict[k] = v
        return cleaned_dict

# To create an inverse mapping of words from bahasa to english for translation in both directions.
def inverse_mapping(billingual_dict):
    return {v:k for k,v in billingual_dict.items()}

# 
lemmatizer = nltk.stem.WordNetLemmatizer()
def process_token(token):
    token = token.lower().strip()
    token.strip().lower().translate(rm_punctiuation_table)
    token = lemmatizer.lemmatize(token)
    return token

# Simple dictionary lookup using the mapping
def translate_sent(sent,billingual_dict):
    tokens = nltk.word_tokenize(sent)
    translated_tokens = []
    for token in tokens:
        processed = process_token(token)
        translated = billingual_dict.get(processed, token)
        translated_tokens.append(translated)
    return ' '.join(translated_tokens)

# Load in UDHR text in english
url_eng = 'https://research.ics.aalto.fi/cog/data/udhr/txt/eng.txt'
raw_eng = requests.get(url_eng).content # Download the bytes from the URL
data_eng = raw_eng.decode('utf-8')
sents_eng = nltk.sent_tokenize(data_eng)

# Load in UDHR text in bahasa
url_idn = 'https://research.ics.aalto.fi/cog/data/udhr/txt/inz.txt'
raw_idn = requests.get(url_idn).content # Download the bytes from the URL
data_idn = raw_idn.decode('utf-8')

# Main function
sents_idn = nltk.sent_tokenize(data_idn)
rm_punctiuation_table = str.maketrans('','',string.punctuation)
billigual_dict = load_dict('word_mapping.json')
inv_dict = inverse_mapping(billigual_dict)
res = []

for eng, idn in zip(sents_eng,sents_idn):
    eng_to_id = translate_sent(eng,billigual_dict)
    id_to_eng = translate_sent(idn, inv_dict)
    res.append([eng,idn,eng_to_id,id_to_eng])
    for entry in res[:5]:
        print("English:  \n", entry[0],'\n')
        print("Bahasa:   \n", entry[1],'\n')
        print("Eng -> Bahasa: \n", entry[2],'\n')
        print("Bahasa -> Eng: \n", entry[3],'\n')
        print("-" * 100)


