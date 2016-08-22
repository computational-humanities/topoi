##!/bin/bash

for ((i = 1 ; i < 10; i++ ))
do
scp root@176.9.17.176:/var/repositories/MAPD/ReposMAPD/MAPD000${i}/*_*.jpg . 
mv *.jpg MAPD000${i}.jpg
scp -r MAPD000${i}.jpg ..
rm *.jpg
done

for ((i = 10 ; i < 100; i++ ))
do
scp root@176.9.17.176:/var/repositories/MAPD/ReposMAPD/MAPD00${i}/*_*.jpg . 
mv *.jpg MAPD00${i}.jpg
scp -r MAPD00${i}.jpg ..
rm *.jpg
done

for ((i = 100 ; i < 733; i++ ))
do
scp root@176.9.17.176:/var/repositories/MAPD/ReposMAPD/MAPD0${i}/*_*.jpg . 
mv *.jpg MAPD0${i}.jpg
scp -r MAPD0${i}.jpg ..
rm *.jpg
done
