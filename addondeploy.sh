#!/usr/bin/env bash

cdr="$PWD"
addons_folder="${HOME}/Documents/Anki/addons/"
genum_core_folder="${addons_folder}GenumCore/"
echo "Cleaning addon folder"
cd "$addons_folder"
rm Genum.py Genum.pyc
rm -rf GenumCore/
echo "Cleaning is finished"
cd "$cdr"

echo "Copying new version of Genum"
ls
cp Genum.py "$addons_folder"
mkdir "$genum_core_folder"
cp LICENSE.md "$genum_core_folder"
cp README.md "$genum_core_folder"
cp -r GenumCore/ "$addons_folder"
echo "Genum deploy is finished"