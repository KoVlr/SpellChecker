import ctypes

with open("substitutions.csv", "r") as rfile:
    substitutions = {}
    for line in rfile.readlines():
        line = line.split(';')
        substitutions[line[0]] = float(line[1])

with open("voctrie.csv", "r") as rfile:
    voctrie = [[line.split(';')[0], int(line.split(';')[1]), float(line.split(';')[2])] for line in rfile.readlines()]

class Voctrie(ctypes.Structure):
    _fields_ = [("word", ctypes.POINTER(ctypes.c_char_p)),
                ("prelen", ctypes.POINTER(ctypes.c_int)),
                ("p", ctypes.POINTER(ctypes.c_double)),
                ("N", ctypes.c_int)]

class Substitutions(ctypes.Structure):
    _fields_ = [("spell", ctypes.POINTER(ctypes.c_char_p)),
                ("p", ctypes.POINTER(ctypes.c_double)),
                ("N", ctypes.c_int)]

ctypes.cdll.LoadLibrary("D:\Programms\mingw64\\bin\libstdc++-6.dll")
cfunc = ctypes.CDLL("./libsch.dll")
cfunc.SpellCheck.restype = ctypes.c_char_p
cfunc.SpellCheck.argtypes = [ctypes.c_char_p, ctypes.POINTER(Voctrie), ctypes.POINTER(Substitutions)]

vt = Voctrie()
vt.N = len(voctrie)
vt.word = (ctypes.c_char_p * vt.N)()
vt.prelen = (ctypes.c_int * vt.N)()
vt.p = (ctypes.c_double * vt.N)()

sb = Substitutions()
sb.N = len(substitutions)
sb.spell = (ctypes.c_char_p * sb.N)()
sb.p = (ctypes.c_double * sb.N)()

i = 0
for line in voctrie:
    vt.word[i] = line[0].encode("utf-8")
    vt.prelen[i] = line[1]
    vt.p[i] = line[2]
    i += 1

i = 0
for key in substitutions:
    sb.spell[i] = key.encode("utf-8")
    sb.p[i] = ctypes.c_double(substitutions[key])
    i += 1

vocabulary = set()
for line in voctrie:
    vocabulary.add(line[0])

print("-", end=" ")
inputStr = input()
while inputStr != "exit":
    output = ""
    i = 0
    while i < len(inputStr):
        if(inputStr[i].isalpha()):
            j = i + 1
            while True:
                if j < len(inputStr):
                    if inputStr[j].isalpha():
                        j += 1
                        continue
                if inputStr[i:j] in vocabulary:
                    output += inputStr[i:j]
                else:
                    output += cfunc.SpellCheck(inputStr[i:j].encode("utf-8"), ctypes.byref(vt), ctypes.byref(sb)).decode("utf-8")
                i = j
                break
        else:
            output += inputStr[i]
            i += 1
    print("Возможно, вы имели ввиду:", output)
    print("-", end=" ")
    inputStr = input()