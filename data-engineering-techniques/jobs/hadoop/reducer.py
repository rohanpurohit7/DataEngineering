#!/usr/bin/env python3
import sys
current=None
total=0
for line in sys.stdin:
    key,value=line.rstrip().split("\t",1)
    if current is not None and key != current:
        print(f"{current}\t{total}")
        total=0
    current=key
    total += int(value)
if current is not None:
    print(f"{current}\t{total}")
