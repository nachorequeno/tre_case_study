#!/bin/bash
# List of attacks: "avg" "min_avg" "max_avg" "const50" "const150" "rsa01_08" "rsa2_5" "swap" "normal"
for attack in "avg" "min_avg" "max_avg" "const50" "const150" "rsa01_08" "rsa2_5" "swap" "normal"
do
	python ./signals2prsignal.py $attack ./day_0_360_user_1143/$attack/*csv
done