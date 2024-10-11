import ChatCheeCheeT

def all_uniq_words(word_list):
    word_set = set()
    for word in word_list:
        if word == 'the':
            continue
        elif word in word_set:
            return False
        else:
            word_set.add(word)
    return True

for i in range(0,100):
    word_list = ChatCheeCheeT.generate('S')
    if all_uniq_words(word_list):
        print(' '.join(word_list))
