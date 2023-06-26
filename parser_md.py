#! /bin/env python3

import os
import re
from pathlib import Path
from functools import reduce
import unidecode


def map_markdown(data: tuple[str, list[str], list[str]]) -> list[Path]:
    root_name, _, files = data
    dir_path = Path(root_name)

    markdown_files = [dir_path /
                      file for file in files if file.endswith('.md') > 0]

    return markdown_files


def filter_empty_lists(x: list[Path]) -> bool:
    return len(x) > 0


def concatenate_list(list_a: list, list_b: list) -> list:
    return list_a + list_b


def github_links_to_zola_links(markdown_content: str) -> str:
    links_to_markdown = re.findall(r"\[.*\](\(.*.md\))", markdown_content)
    all_anchors = re.findall(r"\[.*\](\(#.*\))", markdown_content)
    all_pngs = re.findall(r"\[.*\](\(.*.png\))", markdown_content)

    def github_link_to_zola(link: str) -> str:
        if link[0:2] == '(/':  # exemplo (/advanced/test.md)
            return f"(@/{link[2:]}"
        else:  # exemplo (advanced/test.md)
            return f"(@/{link[1:]}"

    def img_link_to_zola(link: str) -> str:
        repo_name = '/Tutorials'
        if link[0:2] == '(/':  # exemplo (/advanced/test.md)
            return f"({repo_name}/{link[2:]}"
        else:  # exemplo (advanced/test.md)
            return f"({repo_name}/{link[1:]}"

    for link in links_to_markdown:
        new_link = github_link_to_zola(link)
        print(f'current link:{link}\tnew_link:{new_link}')
        markdown_content = markdown_content.replace(link, new_link)

    for link in all_anchors:
        new_link = unidecode.unidecode(link).replace('---', '-')
        markdown_content = markdown_content.replace(link, new_link)

    for png_link in all_pngs:
        new_link = img_link_to_zola(png_link)
        print(f'current link:{png_link}\tnew_link:{new_link}')
        markdown_content = markdown_content.replace(png_link, new_link)

    return markdown_content


def update_markdown_content(markdown_file: Path):
    content = markdown_file.read_text()

    content = github_links_to_zola_links(content)

    if markdown_file.name == 'README.md':
        title = 'title = "index"\ninsert_anchor_links = "right"'
    else:
        title = re.findall("# (.*)", content)[0]
        title = f'title = "{title}"'

    content = f"+++\n{title}\n+++\n{content}"
    markdown_file.write_text(content)


def move_markdown_to_content_dir(markdown_file: Path, content_dir: Path):

    if markdown_file.name == 'README.md':
        markdown_file.rename(content_dir / '_index.md')
    else:
        path = str(markdown_file).replace('Tutorials', content_dir.name)
        new_markdown_path = Path(path)
        new_markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_file.rename(new_markdown_path)


def move_assets_to_static_dir(tutorials: Path) -> None:

    assets = tutorials / 'assets'
    static_path = Path('static') / assets.name
    if static_path.exists():
        os.system(f'rm -rf {static_path}')

    assets.rename(static_path)


def create_indexs(content: Path):
    titles = {
        'beginner': 'iniciante',
        'intermediate': 'intermediário',
        'advanced': 'avançado'
    }
    
    for dir_name, title in titles.items():
        sub_dir = content / dir_name
        index_file = sub_dir / '_index.md'

        index_content = f"+++\ntitle:{title}\n+++\n"
        index_file.write_text(index_content)


def main() -> None:

    content_dir = Path('content')
    tutorials_path = Path('Tutorials')
    walked_files = os.walk(tutorials_path)
    walked_markdown_files = map(map_markdown, walked_files)
    walked_markdown_files = filter(filter_empty_lists, walked_markdown_files)

    markdown_files = reduce(concatenate_list, walked_markdown_files)

    for markdown in markdown_files:
        update_markdown_content(markdown)
        move_markdown_to_content_dir(markdown, content_dir)

    move_assets_to_static_dir(tutorials_path)
    create_indexs(content_dir)


if __name__ == "__main__":
    main()
