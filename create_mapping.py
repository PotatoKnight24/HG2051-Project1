
import json
import asyncio
from googletrans import Translator

# Downloaded a list of 10000 most common english words found on github https://github.com/first20hours/google-10000-english
english_words = []
with open("google-10000-english-no-swears.txt", 'r') as file:
    for word in file:
        english_words.append(word.lower())

# Used googletrans library's translator to translate each individual word from the 10000 english words wordlist
async def create_word_mapping(word_list, src_lang='en', dest_lang='id'):
    translator = Translator()
    mapping = {}
    for word in word_list:
        try:
            # Await the asynchronous translation call
            translation = await translator.translate(word, src=src_lang, dest=dest_lang)
            mapping[word] = translation.text
            print(f"Translated '{word}' -> '{translation.text}'")
        except Exception as e:
            print(f"Error translating '{word}': {e}")
    return mapping


    
# Run the asynchronous mapping function.
word_mapping = asyncio.run(create_word_mapping(english_words, src_lang='en', dest_lang='id'))

# Save the mapping to a JSON file.
with open("word_mapping.json", "w", encoding="utf-8") as outfile:
    json.dump(word_mapping, outfile, indent=4, ensure_ascii=False)

print("Word mapping saved to 'word_mapping.json'")

# Clean the mapping

# Load the JSON file
with open('word_mapping.json', 'r', encoding='utf-8') as infile:
    data = json.load(infile)

# Remove newline characters from keys and values
cleaned_data = {key.replace('\n', '').strip(): value.replace('\n', '').strip() 
                for key, value in data.items()}

# Write the cleaned JSON to a new file
with open('word_mapping.json', 'w', encoding='utf-8') as outfile:
    json.dump(cleaned_data, outfile, ensure_ascii=False, indent=2)

