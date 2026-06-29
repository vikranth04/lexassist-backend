from typing import Dict, Any


class FileRepository:
    def __init__(self):
        self._files: Dict[str, Dict[str, Any]] = {}

    def save_file_metadata(self, file_id: str, metadata: Dict[str, Any]):
        self._files[file_id] = metadata

    def get_file_metadata(self, file_id: str) -> Dict[str, Any]:
        return self._files.get(file_id, {})

    def list_files(self) -> Dict[str, Dict[str, Any]]:
        return self._files
