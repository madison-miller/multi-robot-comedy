def contain_words(s,w):
    return (' ' + w + ' ') in (' ' + s + ' ')

sentence = "Hi Janani , how are you"
print(contain_words(sentence,'Janani'))
print(contain_words('Hi Janani , how are you','Jan'))
print(contain_words('Hi Janani , how are you','you'))



if sentence.find("jan"):
    print("Found it")

print(sentence.find("ow"))
