from datetime import datetime
import ctypes

with open("substitutions.txt", "r") as rfile:
    substitutions = {}
    for line in rfile.readlines():
        line = line.split()
        substitutions[line[0]] = float(line[1])

with open("voctrie.txt", "r") as rfile:
    voctrie = [[line.split()[0], int(line.split()[1]), float(line.split()[2])] for line in rfile.readlines()]

class Voctrie(ctypes.Structure):
    _fields_ = [("word", ctypes.POINTER(ctypes.c_char_p)),
                ("prelen", ctypes.POINTER(ctypes.c_int)),
                ("p", ctypes.POINTER(ctypes.c_double)),
                ("N", ctypes.c_int)]

class Substitutions(ctypes.Structure):
    _fields_ = [("spell", ctypes.POINTER(ctypes.c_char_p)),
                ("p", ctypes.POINTER(ctypes.c_double)),
                ("N", ctypes.c_int)]

ctypes.cdll.LoadLibrary("C:\WINDOWS\system32\MSVCRT.dll")
ctypes.cdll.LoadLibrary("C:\WINDOWS\system32\kernel32.dll")
ctypes.cdll.LoadLibrary("D:\Programms\mingw64\\bin\libgcc_s_sjlj-1.dll")
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
    vt.word[i] = line[0].encode("ASCII")
    vt.prelen[i] = line[1]
    vt.p[i] = line[2]
    i += 1

i = 0
for key in substitutions:
    sb.spell[i] = key.encode("ASCII")
    sb.p[i] = ctypes.c_double(substitutions[key])
    i += 1

print("Введите слово")
typo = input()
while typo != "exit":
    start_time = datetime.now()
    output = cfunc.SpellCheck(typo.encode("ASCII"), ctypes.byref(vt), ctypes.byref(sb)).decode("ASCII")
    print(datetime.now() - start_time)
    print("Возможно, вы имели ввиду:", output)
    print("Введите слово")
    typo = input()