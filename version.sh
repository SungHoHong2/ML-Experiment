git config credential.helper store
git pull origin main
LOCATION="$(pwd)"
VERSION=3

if [ "$1" = "commit" ]
then
  git add .
  git commit -m "$2"
  git push origin main

elif [ "$1" = "Intro" ]
then
  cd Introduction
  python3 $2.py

else
  echo "no argument"
fi