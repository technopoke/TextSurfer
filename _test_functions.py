

wordsets = {}
    wordsets['stops'] = PhraseCleaner()
    wordsets['joins'] = PhraseCleaner(join_word_list)
    wordsets['swaps'] = PhraseCleaner(swap_word_list)


test_text = gensim.utils.simple_preprocess(str(test_text), deacc=True)

swaped = wordsets['swaps'](test_text)
joined = wordsets['joins'](swaped)
stoped = wordsets['stops'](joined)
print(stoped)