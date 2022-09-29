class Trie_elem:
    def __init__(self, data, child=None, next=None, parent = None):
        self.data = data
        self.child = child
        self.next = next
        self.parent = parent
    def __str__(self):
        return str(self.data)

class StrTrie:
    def __init__(self):
        self.root = None

    def __str__(self):
        s = ""
        L = [self.root]
        while L != []:
            newL = []
            for elem in L:
                s += "|"
                while elem is not None:
                    newL += [elem.child]
                    s += f"{elem} "
                    elem = elem.next
                else:
                    s += f"{elem} "
                s += "|   "
            s += "\n"
            L = list(newL)
        return s

    def __iter__(self):
        trie_elem = self.root
        while trie_elem is not None:
            yield trie_elem
            if trie_elem.child is not None:
                trie_elem = trie_elem.child
            elif trie_elem.next is not None:
                trie_elem = trie_elem.next
            else:
                trie_elem = trie_elem.parent
                while trie_elem is not None:
                    if trie_elem.next is not None:
                        trie_elem = trie_elem.next
                        break
                    else:
                        trie_elem = trie_elem.parent

    #поиск узла дерева
    def search(self, data: str):
        trie_elem = self.root
        while trie_elem is not None:
            if data == trie_elem.data:
                return trie_elem
            if data.find(trie_elem.data) == 0:
                trie_elem = trie_elem.child
            else:
                trie_elem = trie_elem.next
        return None

    #Добавление элемента в дерево
    def add(self, data: str):

        #функция нахождения наибольшего общего префикса двух строк
        def prefix(s1, s2):
            l = min(len(s1), len(s2))
            for i in range(l):
                if s1[i] != s2[i]:
                    return s1[:i]
            return s1[:l]

        #Если дерево пустое
        if self.root is None:
            self.root = Trie_elem(data)
            return

        trie_elem = self.root #текущий узел
        basestr = "" #переменная для хранения строки родительского узла
        while True:
            #если этот элемент уже есть в дереве
            if data == trie_elem.data:
                return

            #вычисление наибольшего общего префикса
            strpref = prefix(data, trie_elem.data)

            #если строка текущего узла это префикс добавляемого элемента, то нужно переходить к дочернему узлу
            if trie_elem.data == strpref:
                #если у текущего нет дочернего узла, то новый элемент добавляется на его место
                if trie_elem.child is None: 
                    trie_elem.child = Trie_elem(data, parent=trie_elem)
                    return

                #иначе переход к дочернему узлу
                basestr = str(trie_elem) #запомнить строку родительского узла
                trie_elem = trie_elem.child
                continue
            
            #если префикс совпадает с родительским узлом, то переход к следующему узлу
            elif strpref == basestr:
                #если следующего узла нет, то новый элемент добавляется на его место
                if trie_elem.next is None: 
                    trie_elem.next = Trie_elem(data, parent=trie_elem.parent)
                    return

                trie_elem = trie_elem.next
                continue

            #Иначе префикс больше чем строка в родительском узле, и значит над текущим узлом должен быть узел с префиксом
            else:
                new_elem = Trie_elem(trie_elem.data, child=trie_elem.child, parent=trie_elem)
                trie_elem.data = strpref
                trie_elem.child = new_elem

                #исправление атрибута parent для дочерних узлов элемента new_elem
                fix_elem = new_elem.child
                while fix_elem is not None:
                    fix_elem.parent = new_elem
                    fix_elem = fix_elem.next

                if data != strpref: #если добавляемая строка не совпадает с префиксом, то для неё создаётся новый узел
                    new_elem.next = Trie_elem(data, parent=trie_elem)