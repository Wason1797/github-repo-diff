import os
import shutil

import aiofiles
import aiofiles.os
import httpx
from tqdm import tqdm


def configure_dirs() -> None:
    os.makedirs('./dist', exist_ok=True)


async def download_repo(client: httpx.AsyncClient, author: str, repo: str, path: str) -> str:
    out_path = f'{path}/{author}_{repo}.zip'

    if await aiofiles.os.path.exists(out_path):
        print(f' {out_path} exists skipping download ')
        return out_path

    async with aiofiles.open(out_path, 'wb') as downloaded_file:

        async with client.stream('GET', f'https://github.com/{author}/{repo}/archive/main.zip', follow_redirects=True) as response:

            with tqdm(total=None, unit_scale=True, unit_divisor=1024, unit='B') as progress_bar:
                downloaded_bytes = response.num_bytes_downloaded

                async for chunk in response.aiter_raw():
                    await downloaded_file.write(chunk)

                    progress_bar.update(response.num_bytes_downloaded - downloaded_bytes)
                    downloaded_bytes = response.num_bytes_downloaded

    return out_path


def unzip_repo(repo_file: str) -> str:
    repo_path = repo_file.removesuffix('.zip')
    shutil.unpack_archive(repo_file, repo_path)
    return repo_path
