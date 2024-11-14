import argparse
import asyncio
import logging

from aiopath import AsyncPath
from aioshutil import copy

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


def create_destination_subdir_path(
    source_file: AsyncPath, destination_dir: AsyncPath
) -> AsyncPath:
    extension = source_file.suffix[1:].lower().strip(".")
    return destination_dir / extension


async def copy_file(source_file: AsyncPath, destination_dir: AsyncPath):
    try:
        await destination_dir.mkdir(parents=True, exist_ok=True)
        await copy(source_file, destination_dir)

        logging.info(f"File {source_file} was copied to {destination_dir}")
    except Exception as error:
        logging.error(
            f"Error occurred during coping {source_file} to {destination_dir}: {error}"
        )


async def sort_files_by_extension(source_dir: AsyncPath, destination_dir: AsyncPath):
    tasks = []
    async for source_file in source_dir.glob("**/*"):
        if await source_file.is_file():
            tasks.append(
                copy_file(
                    source_file,
                    create_destination_subdir_path(source_file, destination_dir),
                )
            )
    await asyncio.gather(*tasks)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", help="Source directory.")
    parser.add_argument("destination_dir", help="Destination directory.")
    args = parser.parse_args()
    return args.source_dir, args.destination_dir


def main():
    source_dir, destination_dir = parse_arguments()
    asyncio.run(
        sort_files_by_extension(AsyncPath(source_dir), AsyncPath(destination_dir))
    )


if __name__ == "__main__":
    main()
