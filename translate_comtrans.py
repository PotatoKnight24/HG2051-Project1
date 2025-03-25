from nltk import tokenize, Alignment, AlignedSent
from nltk.translate import IBMModel1,IBMModel2,IBMModel3
import requests


def load_aligned_UDHR(source,target):
    aligned_sents =[]
    for source_line, target_line in zip(source, target):
        # source_line = source_line.strip().lower()
        # target_line = target_line.strip().lower()
        if target_line and source_line:
            source_tokens = tokenize.word_tokenize(source_line)
            target_tokens = tokenize.word_tokenize(target_line)
            aligned_sent = AlignedSent(source_tokens,target_tokens)
            aligned_sents.append(aligned_sent)
    return aligned_sents

def translate_sent(sent,model):
    tokens = tokenize.word_tokenize(sent.lower())
    translated_tokens = []
    for token in tokens:
        if token in model.translation_table:
            # print(type(model.translation_table.get(token)))
            # exit()
            distribution = model.translation_table.get(token)
            filtered_distribution = {tgt: prob for tgt,prob in distribution.items() if prob is not None}
            best_target = max(filtered_distribution, key = filtered_distribution.get)
            translated_tokens.append(best_target)
        else:
            translated_tokens.append(f"[{token}]")
        translated_tokens = [i for i in translated_tokens if i is not None]
    return " ".join(translated_tokens) 
# Load in UDHR text in english
# translation_table = model2.translation_table
url_eng = 'https://research.ics.aalto.fi/cog/data/udhr/txt/eng.txt'
raw_eng = requests.get(url_eng).content # Download the bytes from the URL
data_eng = tokenize.sent_tokenize(raw_eng.decode('utf-8')) # Tokenise the raw string as sentences

# Load in UDHR text in bahasa
url_idn = 'https://research.ics.aalto.fi/cog/data/udhr/txt/inz.txt'
raw_idn = requests.get(url_idn).content # Download the bytes from the URL
data_idn = tokenize.sent_tokenize(raw_idn.decode('utf-8')) # Tokenise the raw string as sentences

aligned_UDHR_eng_idn = load_aligned_UDHR(data_eng,data_idn)
print(aligned_UDHR_eng_idn[0])

# model1 = IBMModel1(aligned_UDHR_eng_idn,10)
model2 = IBMModel2(aligned_UDHR_eng_idn,20)
# model3 = IBMModel3(aligned_UDHR_eng_idn,10)


print(translate_sent("All human beings are born free and equal in dignity and rights.",model2))
