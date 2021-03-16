git config credential.helper store
git pull origin main
LOCATION="$(pwd)"
VERSION=3

if [ "$1" = "commit" ]
then
  git add .
  git commit -m "$2"
  git push origin main

elif [ "$1" = "Naive" ]
then
  python3 ud120-projects/naive_bayes/nb_author_id.py

else
  echo "no argument"
fi