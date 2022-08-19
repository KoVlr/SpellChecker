#Подсчёт слов
def wordCounter(dataset_filename):
    wordFreq = dict()
    N = 0 #Общее количество слов
    with open(dataset_filename, "r") as rfile:
        for line in rfile:
            lineAlpha = ""
            for char in line:
                lineAlpha += char if char.isalpha() else " "
            words = lineAlpha.split()
            for word in words:
                N += 1
                wordFreq[word] = wordFreq[word] + 1 if word in wordFreq else 1
    for key in wordFreq:
        wordFreq[key] = wordFreq[key] / N
    return wordFreq


from jellyfish import damerau_levenshtein_distance

#Выделение слов с опечатками
def SelectionTypos(wordFreq, vocwords):
    #wordFreq - словарь, в котором перечислены слова и частоты их использования
    #vocwords - список слов, которые точно не являются опечатками
    rwords = set(wordFreq.keys()) #оставшиеся слова, среди которых будут искться эталонные
    maybeTypos = list() #список слов, среди которых могут быть опечатки
    for word in wordFreq:
        if word not in vocwords:
            maybeTypos += [word]
    typos = list()

    i = 0

    for maybeTypo in maybeTypos:

        i += 1

        isTypo = False
        for word in rwords:
            if damerau_levenshtein_distance(maybeTypo, word)==1 and wordFreq[word] > 10*wordFreq[maybeTypo]:
                isTypo = True
                typos += [(word, maybeTypo, wordFreq[maybeTypo])] #(правильное написание слова, слово с опечаткой, частота таких опечаток)
                break
        if isTypo:
            rwords.remove(maybeTypo)
    return typos

#подсчёт замен одних сочетаний букв на другие
def SubstitutionCount(typos):
    #typos - список кортежей формата: (правильное написание слова, слово с опечаткой, частота таких опечаток)
    def levenshtein_mapping(s1, s2): #функция построения отображения букв между двумя словами
        d = {}
        lenstr1 = len(s1)
        lenstr2 = len(s2)
        for i in range(-1,lenstr1+1):
            d[(i,-1)] = i+1
        for j in range(-1,lenstr2+1):
            d[(-1,j)] = j+1
    
        for i in range(lenstr1):
            for j in range(lenstr2):
                if s1[i] == s2[j]:
                    cost = 0
                else:
                    cost = 1
                d[(i,j)] = min(
                            d[(i-1,j)] + 1, # deletion
                            d[(i,j-1)] + 1, # insertion
                            d[(i-1,j-1)] + cost, # substitution
                            )

        #нахождение отображения букв s1 на s2 в соответствии с редакционным предписанием
        maps1 = list()
        maps2 = list()
        i = lenstr1 - 1
        j = lenstr2 - 1
        while i != -1 and j != -1:
            if i == -1:
                maps1.insert(0, "")
                maps2.insert(0, s2[j])
                j -= 1
                continue
            if j == -1:
                maps1.insert(0, s1[i])
                maps2.insert(0, "")
                i -= 1
                continue

            m = min(d[(i-1,j-1)], d[(i-1,j)], d[(i, j-1)])
            if m == d[(i-1,j-1)]:
                maps1.insert(0, s1[i])
                maps2.insert(0, s2[j])
                i -= 1
                j -=1
            elif m == d[(i-1,j)]:
                maps1.insert(0, s1[i])
                maps2.insert(0, "")
                i -= 1
            else:
                maps1.insert(0, "")
                maps2.insert(0, s2[j])
                j -= 1

        return maps1, maps2
        
    substitutions = dict() #словарь, в котором будут частоты замен сочетаний букв x на y,
    #где x - буквы которые имел ввиду пользователь, y - буквы, которые он ошибочно написал
    #будут рассматриваться сочетания букв длиной не более 2
    letters = dict() #словарь для подсчёта количества встреченных сочетаний букв x
    for typo in typos:
        maps1, maps2 = levenshtein_mapping(typo[0], typo[1])
        #подсчёт односимвольных соответствий
        for i in range(len(maps1)):
            x = maps1[i]
            y = maps2[i]

            if x in letters:
                letters[x] += typo[2]
            else:
                letters[x] = typo[2]
            
            if f"{x}>{y}" in substitutions:
                substitutions[f"{x}>{y}"] += typo[2]
            else:
                substitutions[f"{x}>{y}"] = typo[2]
        
        #подсчёт двусимвольных соответствий
        for i in range(len(maps1)-1):
            x = maps1[i]+maps1[i+1]
            y = maps2[i]+maps2[i+1]
                
            if x in letters:
                letters[x] += typo[2]
            else:
                letters[x] = typo[2]
            
            if f"{x}>{y}" in substitutions:
                substitutions[f"{x}>{y}"] += typo[2]
            else:
                substitutions[f"{x}>{y}"] = typo[2]
    for key in substitutions:
        substitutions[key] /= letters[key.split('>')[0]]
    return substitutions

from Trie import StrTrie

#Создание списка слов, расположенных в порядке обхода в глубину префиксного дерева
def CreateVoctrie(vocabulary):
    trie = StrTrie()
    for word in vocabulary:
        trie.add(word)
    voctrie = list()
    for node in trie:
        if str(node) in vocabulary:
            voctrie += [(
                        str(node), #слово
                        len(str(node.parent)) if node.parent is not None else 0, #длина предыдущего слова
                        vocabulary[str(node)] #частота использования слова
                        )]
    return voctrie



wordFreq = wordCounter("dataset.txt")
with open("vocwords.txt", "r") as rfile:
    vocwords = [line[:-1] for line in rfile.readlines()]
typos = SelectionTypos(wordFreq, vocwords)
substitutions = SubstitutionCount(typos)
vocabulary = dict()
for word in vocwords:
    if word in wordFreq:
        vocabulary[word] = wordFreq[word]
voctrie = CreateVoctrie(vocabulary)
with open("substitutions.csv", "w") as wfile:
    for key in substitutions:
        wfile.write(f"{key};{substitutions[key]}\n")
with open("voctrie.csv", "w") as wfile:
    for line in voctrie:
        wfile.write(f"{line[0]};{line[1]};{line[2]}\n")