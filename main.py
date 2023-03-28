import jieba
import math
import re
from collections import Counter

corpus=[]
with open('data.txt', "r", encoding="ANSI") as file:
    text = [line.strip("\n").replace("\u3000", "").replace("\t", "") for line in file][3:]
    corpus += text

with open('cn_stopwords.txt',"r", encoding="ANSI") as file:
    words= [line.strip() for line in file.readlines()]


sub= u'[a-zA-Z0-9’!"#$%&\'()*+,-./:：;「<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
for j in range(len(corpus)):
    corpus[j] = re.sub(sub, "", corpus[j])


new_corpus = []
character_count = 0
for text in corpus:
    new_words = []
    split_words = list(jieba.cut(text))
    for word in split_words:
        if word not in words:
            new_words.append(word)
    character_count += len(''.join(map(str, new_words)))
    new_corpus.append(''.join(map(str, new_words)))

# with open("data-pre.txt", "w", encoding="utf-8") as f:
#     for line in corpus:
#         if len(line) > 1:
#             f.write(line)
#             print(line, file=f)
#
# with open("data-pre.txt", "r", encoding="utf-8") as f:
#     corpus = [eve.strip("\n") for eve in f]

# token = []
# for para in corpus:
#     token += jieba.lcut(para)
# token_num = len(token)
# ct = Counter(token)
# vocab1 = ct.most_common()
# entropy_1gram = sum([-(eve[1]/token_num)*math.log((eve[1]/token_num),2) for eve in vocab1])
#
# print("词库总词数：", token_num, " ", "不同词的个数：", len(vocab1))
# print("出现频率前10的1-gram词语：", vocab1[:10])
# print("entropy_1gram:", entropy_1gram)

def combine2gram(cutword_list):
    if len(cutword_list) == 1:
        return []
    res = []
    for i in range(len(cutword_list)-1):
        res.append(cutword_list[i] + "s"+ cutword_list[i+1])
    return res


token_2gram = []
for para in new_corpus:
    cutword_list = jieba.lcut(para)
    token_2gram += combine2gram(cutword_list)
# 2-gram的频率统计
token_2gram_num = len(token_2gram)
ct2 = Counter(token_2gram)
vocab2 = ct2.most_common()
# print(vocab2[:20])
# 2-gram相同句首的频率统计
same_1st_word = [eve.split("s")[0] for eve in token_2gram]
assert token_2gram_num == len(same_1st_word)
ct_1st = Counter(same_1st_word)
vocab_1st = dict(ct_1st.most_common())
vocab1=ct_1st.most_common()
entropy_2gram = 0
for eve in vocab2:
    p_xy = eve[1]/token_2gram_num
    first_word = eve[0].split("s")[0]
    # p_y = eve[1]/vocab_1st[first_word]
    entropy_2gram += -p_xy*math.log(eve[1]/vocab_1st[first_word], 2)
print("词库总词数：", token_2gram_num, " ", "不同词的个数：", len(vocab1))
print("出现频率前10的2-gram词语：", vocab1[:10])
print("entropy_2gram:", entropy_2gram)
