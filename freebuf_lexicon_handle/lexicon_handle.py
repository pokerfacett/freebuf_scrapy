#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from urllib.parse import quote,unquote
lexicon = "test.txt"

lexicon_final = "lexicon_final.txt"

read_file = open(lexicon,'r')
write_file = open(lexicon_final,'a')

all_lines = read_file.readlines()
read_file.close()

s = set()

for i in all_lines:
    j = quote(i).replace('%20','')
    s.add(unquote(j))

for i in s:
    write_file.write(i)

write_file.close()