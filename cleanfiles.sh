#!/bin/sh

#go through all directories in data
LANGUAGE=en

BASE=./data/$LANGUAGE

for oldfile in $BASE/dirty/* ; do
    filename=${oldfile##*/}
    echo cleaning $filename

    newfile=$BASE/clean/$filename

    touch newfile
    ./wikifil.pl $oldfile > $newfile
done
