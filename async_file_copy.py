import asyncio
import shutil
import argparse
import logging
from pathlib import Path

from utils import file_generator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(file_path: Path, output_folder: Path):
    try:
        ext_folder = output_folder / file_path.suffix.lstrip('.')
        ext_folder.mkdir(parents=True, exist_ok=True)
        
        dest_path = ext_folder / file_path.name
        
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, shutil.copy2, file_path, dest_path)
        logging.info(f'Copied: {file_path} -> {dest_path}')
    except Exception as e:
        logging.error(f'Error copying {file_path}: {e}')

async def read_folder(source_folder: Path, output_folder: Path):
    tasks = []
    for file_path in source_folder.rglob('*'):
        if file_path.is_file():
            tasks.append(copy_file(file_path, output_folder))
    
    if tasks:
        await asyncio.gather(*tasks)

async def main():
    parser = argparse.ArgumentParser(description='Асинхронне сортування файлів за розширенням.')
    parser.add_argument('source', type=str, help='Шлях до вихідної папки')
    parser.add_argument('output', type=str, help='Шлях до цільової папки')
    
    args = parser.parse_args()
    source_folder = Path(args.source)
    output_folder = Path(args.output)
    file_generator(source_folder)
    
    if not source_folder.exists() or not source_folder.is_dir():
        logging.error('Вихідна папка не існує або не є директорією.')
        return
    
    output_folder.mkdir(parents=True, exist_ok=True)
    
    await read_folder(source_folder, output_folder)
    
if __name__ == '__main__':
    asyncio.run(main())
