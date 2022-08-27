import asyncio
from argparse import ArgumentParser
from typing import Optional

import httpx
import aiofiles
from github_repo_diff.comparator import (build_file_tree, compare_file_trees,
                                         make_row)
from github_repo_diff.downloader import (configure_dirs, download_repo,
                                         unzip_repo)
from prettytable import PrettyTable


def get_args() -> tuple:
    parser = ArgumentParser(description='Get a comparison percentage from two GitHub Forks')
    parser.add_argument("-la", "--left_author", help="GitHub author for the left fork", type=str, required=True)
    parser.add_argument("-ra", "--right_author", help="GitHub author for the right fork", type=str, required=True)
    parser.add_argument("-r", "--repo", help="Name of the GitHub repo", type=str, required=True)
    parser.add_argument("-d", "--dist", help="Download Directory", type=str, default='./repo_dist')
    parser.add_argument("-of", "--out_file", help="Output File", type=str)
    args = parser.parse_args()
    return args.left_author, args.right_author, args.repo, args.dist, args.out_file


async def main(left_author: str, rihgt_author: str, repo: str, path: str, out_file: Optional[str] = None) -> None:

    async with httpx.AsyncClient() as client:

        left_repo, right_repo = await asyncio.gather(*(
            download_repo(client, left_author, repo, path),
            download_repo(client, rihgt_author, repo, path),
        ))

    left_repo_dir, right_repo_dir = unzip_repo(left_repo), unzip_repo(right_repo)
    left_file_tree, right_file_tree = build_file_tree(left_repo_dir), build_file_tree(right_repo_dir)
    result = await compare_file_trees(left_file_tree, left_repo_dir, right_file_tree, right_repo_dir)

    rejected = {'__init__.py', '.gitignore', 'settings.json', 'requirements.txt', '.gitmodules'}

    table = PrettyTable((left_author, rihgt_author, 'Equal Lines', 'Percentage'))

    filtered_result = {file: data for file, data in result.items() if not set(file.split('/')).intersection(rejected)}

    table.add_rows(make_row(file, data, repo) for file, data in filtered_result.items())
    average_similarity = sum(data['percent'] for data in filtered_result.values())/len(filtered_result)
    similarity_label = f'=> Average Similarity = {average_similarity:.2f}%'
    if not out_file:
        print(table)
        print(similarity_label)
        return

    async with aiofiles.open(f'./{out_file}', 'w') as output:
        await output.write(f'{table}\n')
        await output.write(f'{similarity_label}\n')

    print(f'Results stored in {out_file}')


def entry_point() -> None:
    configure_dirs()
    asyncio.run(main(*get_args()))
