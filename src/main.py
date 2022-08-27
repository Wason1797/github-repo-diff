import asyncio

import httpx
from prettytable import PrettyTable

from .comparator import build_file_tree, compare_file_trees, make_row
from .downloader import configure_dirs, download_repo, unzip_repo


async def main(left_author: str, rihgt_author: str, repo: str, path: str) -> None:

    async with httpx.AsyncClient() as client:

        left_repo, right_repo = await asyncio.gather(*(
            download_repo(client, left_author, repo, './dist'),
            download_repo(client, rihgt_author, repo, './dist'),
        ))

    left_repo_dir, right_repo_dir = unzip_repo(left_repo), unzip_repo(right_repo)
    left_file_tree, right_file_tree = build_file_tree(left_repo_dir), build_file_tree(right_repo_dir)
    result = await compare_file_trees(left_file_tree, left_repo_dir, right_file_tree, right_repo_dir)

    rejected = {'__init__.py', '.gitignore', 'settings.json', 'requirements.txt', '.gitmodules'}

    table = PrettyTable((left_author, rihgt_author, 'Equal Lines', 'Percentage'))

    filtered_result = {file: data for file, data in result.items() if not set(file.split('/')).intersection(rejected)}

    table.add_rows(make_row(file, data, repo) for file, data in filtered_result.items())

    print(table)
    average_similarity = sum(data['percent'] for data in filtered_result.values())/len(filtered_result)
    print(f'=> Average Similarity = {average_similarity:.2f}%')


if __name__ == '__main__':
    configure_dirs()
    asyncio.run(main('MarcoAguirre', 'AlanysRojas', 'python-pizza-planet', './dist'))
