from typing import Dict, Any


class MetadataManager:
    """
    Cleans and flattens metadata dictionaries since ChromaDB demands primitive attributes
    (str, int, float, bool) and rejects nested structures.
    """
    def sanitize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Flattens dictionary values and converts objects to primitive structures."""
        flat_metadata = {}
        for key, val in metadata.items():
            if isinstance(val, (str, int, float, bool)):
                flat_metadata[key] = val
            elif isinstance(val, dict):
                # Flatten single-depth nested dict structures
                for sub_key, sub_val in val.items():
                    if isinstance(sub_val, (str, int, float, bool)):
                        flat_metadata[f"{key}_{sub_key}"] = sub_val
                    else:
                        flat_metadata[f"{key}_{sub_key}"] = str(sub_val)
            else:
                flat_metadata[key] = str(val)

        return flat_metadata
