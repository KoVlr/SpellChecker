# SpellChecker
Исправление опечаток и ошибок в словах, набранных пользователем.

Для запуска программы исправления опечаток нужно запустить файл SpellChecker.py. В этом файле вызывается функция из файла SpellChecker.cpp.  
Для работы программы нужны файлы substitution.csv и voctrie.csv, которые являются результатом обучения модели. Обучение происходит при выполнении файла ModelTraining.py.  
Входными данными для обучения модели являются файл dataset.txt с большим количеством сгенерированного пользователями текста, а также файл vocwords.txt, в котором содержится набор словарных слов.
