#!/usr/bin/bash
# Discription:
#	This program is to clean all the a.out file
#
# Virsion: 1.0
#	Cavon 2015/05/20		First Realease

for i in *
do
	rm ./$i/a.out
	git rm ./$i/a.out
done
rm log
