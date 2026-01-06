#!/usr/bin/env python3

# modificacion del codigo original para filtrado de caracteres unicos
# el codigo de reducer.py no requiere modificacion
import sys

# reading entire line from STDIN (standard input)
for line in sys.stdin:
    # to remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    words = line.split()
    
    # we are looping over the words array and printing the word
    # with the count of 1 to the STDOUT
    for word in words:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        if len(word) == 1 :
            print(f"{word}\t{1}")
