#!/usr/bin/env python3

# modificacion del codigo original para ex filtrado de prepocisiones
# el codigo de reducer.py no requiere modificacion
import sys

preposiciones = set(("a ante bajo cabe con contra de desde durante en entre hacia hasta mediante para por según sin so sobre tras versus vía").split())
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
        if word.lower() not in preposiciones :
            print(f"{word}\t{1}")
