import os
from pathlib import Path

import dotenv


def get_db_file() -> Path:
    dotenv.load_dotenv()
    file_name = os.environ.get("FILELIST_QUERY_DEFAULT_FILE")
    if file_name:
        p = Path(file_name)
        if p.exists():
            return p
        raise FileNotFoundError(f"File not found: {file_name}")
    dir_name = os.environ.get("FILELIST_QUERY_DIR_LATEST")
    if dir_name:
        p = Path(dir_name).expanduser().resolve()
        if p.exists():
            files = list(p.glob("*.sqlite"))
            files.sort(key=lambda x: x.stat().st_mtime)
            if files:
                return files[-1]
            raise FileNotFoundError(f"No sqlite files in {dir_name}")
        raise FileNotFoundError(f"Directory not found: {dir_name}")
    return None
