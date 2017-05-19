#/bin/bash
for i in {1..10}; do python3 GameManager_3.py |tail -n 1 |tee output.txt; done