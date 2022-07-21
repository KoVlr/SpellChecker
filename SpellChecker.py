def SpellCheck(typo, voctrie, substitutions):
    d = {}
    i0 = -1
    def typo_probability(vocword, typoword, substitutions):
        nonlocal d
        nonlocal i0
        len_vocword = len(vocword)
        len_typoword = len(typoword)
        for i in range(i0, len_vocword):
            for j in range(-1, len_typoword):
                x = vocword[:i+1]
                y = typoword[:j+1]
                maxvalue = substitutions[(x,y)] if (x,y) in substitutions else 0
                for n in range(max(i-2, -1), i+1):
                    for m in range(max(j-2, -1), j+1):
                        if n != i or m != j:
                            x = vocword[n+1:i+1]
                            y = typoword[m+1:j+1]
                            value = d[(n,m)] * substitutions[(x,y)] if (x,y) in substitutions else 0
                            if value > maxvalue:
                                maxvalue = value
                d[(i,j)] = maxvalue
        return d[(len_vocword-1, len_typoword-1)]
    
    maxp = 0
    for line in voctrie:
        i0 = line[1]
        p = typo_probability(line[0], typo, substitutions) * line[2]
        if p > maxp:
            maxp = p
            output = line[0]
    return output

with open("substitutions.txt", "r") as rfile:
    substitutions = {}
    for line in rfile.readlines():
        line = line.split()
        line[0] = "" if line[0] == "_" else line[0]
        line[1] = "" if line[1] == "_" else line[1]
        substitutions[(line[0], line[1])] = float(line[2])

with open("voctrie.txt", "r") as rfile:
    voctrie = [[line.split()[0], int(line.split()[1]), float(line.split()[2])] for line in rfile.readlines()]

print(len(substitutions))

print("Введите слово")
typo = input()
while typo != "exit":
    output = SpellCheck(typo, voctrie, substitutions)
    print("Возможно, вы имели ввиду:", output)
    print("Введите слово")
    typo = input()