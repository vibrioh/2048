#!/usr/bin/env bash

# The first line is "she-bang" -- specifying the program to interpret this script.
# In the above case, we set "bash" (Bourne-Again Shell) to be the interpreter.
# Note: Some people might be using zsh or ksh,
#       but the following script uses bash-specific syntax and might not work in other shell

set -eu
# e: exit this script immediately if return code of each command is non-zero
# u: exit this script immediately if a referenced variable is undefined

ALPHABETA_FLAG=${2:-n}  # default is n
PYTHON3_FLAG=${3:-none} # default is Python2
LOG_DIR_NAME=logs

if [ "${ALPHABETA_FLAG}" == "" ]; then
  echo "usage: ./run_2048.sh <# of games> <y or n for alpha-beta> <3 if Python3>"
  echo "   ex: ./run_2048.sh 10 y"
  echo "   ex: ./run_2048.sh  5 y 3"
fi

echo "run 2048 $1 times. Stop by Ctrl + C (or sending SIGINT to this bash process)"

if [ "${PYTHON3_FLAG}" == "3" ]; then
  PYTHON_BINARY=python3
  GM=GameManager_3.py
else
  PYTHON_BINARY=python
  GM=GameManager.py
fi

mkdir -p ${LOG_DIR_NAME} # -p: create the directory if not existed

for i in `seq 1 $1`; do
  echo -n "Game ${i} start  "                     # -n : no newline
  I_PADDED=$(printf "%03d" ${i})
  ${PYTHON_BINARY} ${GM} ${ALPHABETA_FLAG} > ${LOG_DIR_NAME}/${I_PADDED}.log 2>&1
   tail -1 ${LOG_DIR_NAME}/${I_PADDED}.log
done

# show the last lines of all games
tail -1 ${LOG_DIR_NAME}/*.log
# -1 : just one line
# * matches any filenames