import httpx
from tqdm import tqdm
import shutil
import aiofiles


async def download_repo(session: httpx.AsyncClient, author: str, repo: str, path: str) -> str:
    out_path = f'{path}/{author}_{repo}.zip'
    async with aiofiles.open(out_path, 'wb') as downloaded_file:

        'https://github.com/brendenlake/omniglot/raw/master/python/images_evaluation.zip'

        async with session as client:

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
