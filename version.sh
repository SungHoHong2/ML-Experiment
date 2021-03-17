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
  cd ud120-projects/naive_bayes
  python3 nb_author_id.py

elif [ "$1" = "SVM" ]
then
  cd ud120-projects/svm
  python3 svm_author_id.py

else
  echo "no argument"
fi