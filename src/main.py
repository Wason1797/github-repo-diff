import httpx
import asyncio

from .downloader import download_repo, unzip_repo


async def main() -> None:
    repos = await asyncio.gather(*(
        download_repo(httpx.AsyncClient(), 'AlanysRojas', 'python-pizza-planet', '.'),
        download_repo(httpx.AsyncClient(), 'MarcoAguirre', 'python-pizza-planet', '.'),
    ))

    for repo in repos:
        print(repo)
        unzip_repo(repo)


if __name__ == '__main__':
    asyncio.run(main())
