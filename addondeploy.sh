#!/usr/bin/env bash

cdr="$PWD"
addons_folder="/home/la0rg/Documents/Anki/addons/"
echo "Cleaning addon folder"
cd "$addons_folder"
rm Genum.py Genum.pyc
rm -r GenumCore/
echo "Cleaning if finished"
cd "$cdr"

echo "Copying new version of Genum"
ls
cp Genum.py "$addons_folder"
cp -r GenumCore/ "$addons_folder"
echo "Genum deploy is finished"