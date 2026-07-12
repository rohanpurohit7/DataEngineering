#!/usr/bin/env python3
import csv, sys
reader=csv.DictReader(sys.stdin)
for row in reader:
    print(f"{row['event_type']}\t1")
