import spacy

nlp = spacy.load('en_core_web_sm')

sentence = "Hi Janani, how are you"

doc = nlp(sentence)

for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label)

