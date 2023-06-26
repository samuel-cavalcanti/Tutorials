
git checkout gh-pages

git submodule update --init --recursive

pip install -r requirements.txt

git clone https://github.com/samuel-cavalcanti/Tutorials.git

./parser_md.py

rm -rf Tutorials

rm -rf docs

zola build

git add docs content

echo "updating docs"

git commit -m "updated docs"

git push --set-upstream origin gh-pages
