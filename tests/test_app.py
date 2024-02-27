from pathlib import Path

import pytest
from filelist_query.ui import UI
from make_filelist import mkfilelist


@pytest.fixture
def tmp_filelist_db(tmp_path) -> Path:
    files_path = tmp_path / "files"
    files_path.mkdir()
    (files_path / "file1").write_text("file1")
    (files_path / "file2").write_text("file2")
    list_path = tmp_path / "list"
    list_path.mkdir()
    args = [str(files_path), "test-title", "-o", str(list_path)]
    result = mkfilelist.main(args)
    assert result == 0
    out_files = list(list_path.glob("*.sqlite"))
    assert len(out_files) == 1
    return out_files[0]


def test_make_tmp_filelist(tmp_filelist_db):
    assert tmp_filelist_db.exists()


async def test_app_loads(tmp_filelist_db):
    app = UI(do_load=False, db_file=tmp_filelist_db)
    async with app.run_test() as pilot:
        assert str(pilot.app.db_file) == str(tmp_filelist_db)
