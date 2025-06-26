class NotSourceError(Exception):
    """Raised when the source is not found in the database."""
    def __init__(self, source: str):
        super().__init__(f"Source '{source}' not found in the database.")
        self.source = source