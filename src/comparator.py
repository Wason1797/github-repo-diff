import asyncio
import os
from difflib import unified_diff
from typing import List
from uuid import uuid4

import aiofiles


def build_file_tree(repo_path: str) -> dict:

    file_tree: dict = {}

    for root, _, files in os.walk(repo_path):
        agnostic_root = root.replace(repo_path, '.')
        file_tree[agnostic_root] = {os.path.join(agnostic_root, filename) for filename in files}

    return file_tree


def get_default_comparison() -> dict:
    return {
        'equal_lines': 0,
        'diff': [],
        'percent': 0,
        'source': 'both'
    }


async def get_lines_from_file(file_path: str) -> List[str]:
    async with aiofiles.open(file_path) as handler:
        return await handler.readlines()


async def compare_files(file_1: str, file_2: str) -> dict:
    result: dict = get_default_comparison()
    file_1_lines, file_2_lines = await asyncio.gather(*(get_lines_from_file(file_1), get_lines_from_file(file_2)))
    file_1_id,  file_2_id = str(uuid4()), str(uuid4())

    diff = list(unified_diff(file_1_lines, file_2_lines, file_1_id, file_2_id))

    if not diff:
        result['percent'] = 100
        result['equal_lines'] = len(file_1_lines)
        return result

    for line in diff:
        result['diff'].append(line)
        if file_1_id in line or file_2_id in line:
            continue
        if line.startswith('+') or line.startswith('-'):
            continue

        result['equal_lines'] += 1

    result['percent'] = (result['equal_lines'] / max(len(file_1_lines), len(file_2_lines))) * 100

    return result


async def compare_file_trees(left_tree: dict, left_root: str, right_tree: dict, right_root: str) -> dict:

    async def __compare_files(file: str, left_root: str, right_root: str) -> tuple:
        return file, await compare_files(file.replace('./', f'{left_root}/'), file.replace('./', f'{right_root}/'))

    comparison_result: dict = {}

    for path, files in left_tree.items():
        if path in right_tree:
            comparisons = await asyncio.gather(*tuple(__compare_files(file, left_root, right_root) for file in files.intersection(right_tree[path])))
            comparison_result.update(comparisons)

            for file in right_tree[path].symmetric_difference(files):
                comparison_result[file] = get_default_comparison()
                if file in files:
                    comparison_result[file]['source'] = 'left'
                else:
                    comparison_result[file]['source'] = 'right'
        else:
            for file in files:
                comparison_result[file] = get_default_comparison()
                comparison_result[file]['source'] = 'left'

    for path, files in right_tree.items():
        if path not in left_tree:
            for file in files:
                comparison_result[file] = get_default_comparison()
                comparison_result[file]['source'] = 'right'

    return comparison_result


def make_row(file: str, comparison: dict, repo_name: str) -> tuple:
    left_file = file.replace(f'{repo_name}-', '') if comparison['source'] in {'left', 'both'} else ''
    right_file = file.replace(f'{repo_name}-', '') if comparison['source'] in {'right', 'both'} else ''

    return (left_file, right_file, comparison['equal_lines'], f"{comparison['percent']:.2f}%")
