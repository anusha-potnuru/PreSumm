import json, re, glob
from os.path import join as pjoin
# from prepro.data_builder import greedy_selection

def clean(x):
    return re.sub(
        r"-lrb-|-rrb-|-lcb-|-rcb-|-lsb-|-rsb-|``|''",
        lambda m: REMAP.get(m.group()), x)

# similar to load_json in prepro/data_builder.py
def load_json1(p, lower): # for lega doc processing
    source = []
    tgt = []
    sents = json.load(open(p , encoding="utf-8" ))['sentences']
    # print('no of sents: ', len(sents))

    # write code such that sents are broken at $$$, and if 0 added to src, if 1 added to tgt
    tokens = []
    
    for s in sents:
        s_tokens = [t['word'] for t in s['tokens']]
        if (s_tokens[0]=='$' and s_tokens[1]=='$' and s_tokens[2]=='$'):
            source.append(tokens)
            if s_tokens[3]=='1':
                tgt.append(tokens)
            tokens = []
        else:
            tokens.extend(s_tokens)  

    source = [clean(' '.join(sent)).split() for sent in source]
    tgt = [clean(' '.join(sent)).split() for sent in tgt]
    return source, tgt


# similar to greedy_selection in prepro/data_builder.py
def total_selection(src, tgt): #return all sent ids of src that are tgt
    sent_labels = []
    i=0
    for sent in tgt:
        while i<len(src) and sent!=src[i]:
            i+=1
        if i==len(src):
            break
        sent_labels.append(i)
    return sent_labels



def get_sent_analysis():
    src_len = []
    summ_len = []
    for file in glob.glob(pjoin('../legal_data/data_preprocessed/', '*.json')):
        a,b = load_json1(file, True)
        src_len.append(len(a))
        summ_len.append(len(b))

    for file in glob.glob(pjoin('../legal_data/test_preprocessed/', '*.json')):
        a,b = load_json1(file, True)
        src_len.append(len(a))
        summ_len.append(len(b))


    print('Length of dataset: ', len(src_len))
    print('Average src len: ', sum(src_len)/len(src_len))
    print('Average summary len: ', sum(summ_len)/len(summ_len))
    print('Maximum src len: ', max(src_len))
    print('Maximum summary len: ', max(summ_len))



get_sent_analysis()


'''
wrong len of tgt and len of labels: just three docs - not bad
../legal_data/data_preprocessed/5880.txt.json
../legal_data/data_preprocessed/5519.txt.json
../legal_data/data_preprocessed/5195.txt.json
'''
# in each doc's json
# for file in glob.glob(pjoin('../legal_data/data_preprocessed/', '*.json')):
#     a,b = load_json1(file, True)
#     # print(a, '\n\n', b)
#     # print(len(a), len(b))
#     # sent_labels = total_selection(a,b)
#     sent_labels = total_selection(a[:100],b)
#     print(sent_labels)
#     # print(sent_labels, sum(sent_labels))
#     # if(len(b)!=sum(sent_labels)):
#     #     print(file)



# # corpus json
# files = glob.glob(pjoin('../legal_data/data_json/', '*.json'))
# print(files)

# for file in files:
#     d = json.load(open(file)) #  list of dict - src, tgt
#     print(len(d))
#     print(d[0].keys())



