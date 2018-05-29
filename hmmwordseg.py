import collections
import math


states = ['B', 'M', 'E', 'S']
init, trans, gen = [None] * 3
def fit(seqs):
    cinit = collections.defaultdict(lambda : 1)
    ctrans, cgen = [collections.defaultdict(lambda : collections.defaultdict(lambda : 1)) for _ in range(2)]
    for seq in seqs:
        observe = ''.join(seq)
        state = ''
        for term in seq:
            state += ('S' if len(term) == 1 else 'B' + 'M' * (len(term) - 2) + 'E')
        assert len(observe) == len(state)
        cinit[state[0]] += 1;
        for i in range(1, len(state)):
            ctrans[state[i - 1]][state[i]] += 1
        for i in range(len(state)):
            cgen[state[i]][observe[i]] += 1
    cnt = sum([cinit[k] for k in states])
    global init, trans, gen
    init, trans, gen = {}, {}, {}
    for state in states:
        init[state] = math.log(cinit[state] * 1.0 / cnt)
        ct = sum([ctrans[state][_] for _ in states])
        cg = sum([v for k, v in cgen[state].items()])
        trans[state], gen[state] = {}, collections.defaultdict(lambda : math.log(1.0 / cg))
        for nxt in states:
            trans[state][nxt] = math.log(ctrans[state][nxt] * 1.0 / ct)
        for k, v in cgen[state].items():
            gen[state][k] = math.log(v * 1.0 / cg)

def predict(seq):
    global init, trans, gen
    n = len(seq)
    path, dp = [[{} for l in range(n)] for _ in range(2)]
    for j in states:
        dp[0][j] = init[j] + gen[j][seq[0]]
        path[0][j] = j
    for i in range(1, n):
        for j in states:
            dp[i][j], path[i][j] = max([(dp[i - 1][k] + trans[k][j] + gen[j][seq[i]], path[i - 1][k] + j) for k in states])
    _, ob = max([(dp[n - 1][k], path[n - 1][k]) for k in states])
    ret, now = [], ''
    for i in range(n):
        if ob[i] == 'S':
            if len(now) > 0:
                ret.append(now)
                now = ''
            ret.append(seq[i])
        if ob[i] == 'M':
            now += seq[i]
        if ob[i] == 'E':
            now += seq[i]
            ret.append(now)
            now = ''
        if ob[i] == 'B':
            if len(now) > 0:
                ret.append(now)
                now = ''
            now += seq[i]
    if len(now) > 0:
        ret.append(now)
    return ret



def read_data(filepath):
    my_sentence = []
    my_tag_data = []
    for line in open(filepath, encoding='UTF-8').readlines():
        for _ in line.split():
                if len(_.split(' ')[0]) <4 :
                    my_sentence.append(_.split(' ')[0])
                else:
                    my_tag_data.append(my_sentence) if my_sentence else None
                    my_sentence = []
    return my_tag_data

def train():
    seqs=read_data('CTBtrainingset.txt')
    fit(seqs)

def test():
    my_sentence = []
    print('程序正在执行，需要一点时间')
    for line in open('CTBtestingset.txt', encoding='UTF-8').readlines():
        a=predict(line)
        my_sentence.append(a) 
        b=str(a).replace('\'','')
        b=str(b).replace(',','')
        b=str(b).replace('[','')
        b=str(b).replace(']','')
        b=str(b).replace('\\','')
        b=str(b).replace('n','')
        with open('output.utf8',"a") as f:
            f.write(str(b)+'\n')
    print('预测结果已经输出到文件夹')
    '''
    b=str(my_sentence).replace('\'','')
    with open('output.txt',"w") as f:
        f.write(str(b)+ '\n')
    '''
    
        
      
if __name__ == '__main__':
    #seqs = [[_.split('/')[0] for _ in line.split()[1 : ]] for line in open('data/renmin98.txt', encoding='UTF-8').readlines()]
    train()
    test()
    
    
    
    
    
    
    
    '''
    import os
    os.listdir('E:/课程/NLP/LDC2013T21/ctb8.0/data/postagged')
   
   
    for info in os.listdir('E:/课程/NLP/LDC2013T21/ctb8.0/data/postagged'):
        domain = os.path.abspath('E:/课程/NLP/LDC2013T21/ctb8.0/data/postagged')
        info = os.path.join(domain,info)
        for line in open(info, encoding='UTF-8').readlines():
            for _ in line.split()[1 : ]:
                if len(_.split('_')[0]) <4 :
                    my_sentence.append(_.split('_')[0])
                else:
                    my_tag_data.append(my_sentence) if my_sentence else None
                    my_sentence = []
    seqs=my_tag_data
    
   
    for line in open('E:\\课程\\NLP\\CTB-wordseg\\CTB\\CTBtrainingset.txt', encoding='UTF-8').readlines():
        for _ in line.split():
                if len(_.split(' ')[0]) <4 :
                    my_sentence.append(_.split(' ')[0])
                else:
                    my_tag_data.append(my_sentence) if my_sentence else None
                    my_sentence = []
    '''
    #seqs=read_data('E:\\课程\\NLP\\CTB-wordseg\\CTB\\CTBtrainingset.txt')
    
    #test = seq
   # fit(seqs)
    

   # print(predict('尽管习近平在担任中共领导人期间的外交政策并不完全符合改革时期中华人民共和国的中央外交政策原则'))
    
 
