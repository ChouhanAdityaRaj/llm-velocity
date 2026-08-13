from pathlib import Path
from platformdirs import user_data_dir


class _Storage:
    def __init__(self, project_name: str, database_name: str, index_name: str):
        self.storage_dir = Path(user_data_dir(project_name))

        self.storage_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.database_path = self.storage_dir / f"{database_name}.db"
        self.index_path = self.storage_dir / f"{index_name}.index"