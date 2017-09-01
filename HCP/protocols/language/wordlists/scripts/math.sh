#!/bin/bash

grep -n math maths3.txt > test.txt

#for i in $list_line
while read i
do
echo $i
idx=`expr index "$i" :`
line1=${i:0:idx-1}
num=$((line1 + 1))

idx2=`expr index "$i" .`
dif=$((idx2-1-idx))
fname=${i:idx:dif}
fname=${fname}.txt

line2=`sed -n ${num}p maths3.txt`

echo $line2 > $fname

done < test.txt
