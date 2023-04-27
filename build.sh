
git checkout gh-pages

pip install -r requirements.txt

git clone https://github.com/samuel-cavalcanti/Tutorials.git

./parser_md.py

rm -rf Tutorials

zola build -o docs

