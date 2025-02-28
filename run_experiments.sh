#!/bin/bash
rm -f ./results.txt
# List of attacks: "avg" "min_avg" "max_avg" "fdi50" "fdi150" "rsa01_08" "rsa2_5" "swap" "normal"
for attack in "avg" "min_avg" "max_avg" "fdi50" "fdi150" "rsa01_08" "rsa2_5" "swap" "normal"
do
  # python ./experiments.py $attack ./day_0_360_user_1143/$attack/days_*
  python ./testing.py $attack ./day_0_360_user_1143/$attack/days_* 2>&1 | tee -a ./results.txt
done
