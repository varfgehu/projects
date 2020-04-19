from cs50 import get_string

chars = set("""abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ""")

text = get_string("Text: ")
number_of_word = len(text.split())
#print("number of words: " + str(number_of_word))
number_of_sentences = text.count('.') + text.count('!') + text.count('?')
#print("number of sentences: " + str(number_of_sentences))
number_of_letters = sum(c in chars for c in text)
#print("number of chars: " + str(number_of_letters))

cl_index = (0.0588 * number_of_letters / number_of_word * 100) - (0.296 * number_of_sentences / number_of_word * 100) - 15.8

if(cl_index >= 16):
    print("Grade 16+")
elif(cl_index < 1):
    print("Before Grade 1")
else:
    print("Grade " + str(round(cl_index)))