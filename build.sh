
git checkout gh-pages

git submodule update

pip install -r requirements.txt

git clone https://github.com/samuel-cavalcanti/Tutorials.git

./parser_md.py

rm -rf Tutorials

rm -rf docs

zola build -o docs

git add docs

echo "updating docs"

git commit -m "updated docs"

git push --set-upstream origin gh-pages