from dataclasses import dataclass, field, asdict
import uuid

@dataclass(frozen=True)
class IncomingData:

    guid: str = field(
        compare=True,
        repr=False, metadata={"description": "Unique identifier for the incoming data"},
        default_factory=lambda: str(uuid.uuid4())
    )
    source: str = field(
        default_factory=str, compare=False,
        metadata={"description": "Source of the incoming data, e.g., 'eddn' or 'capi_api'"}
    )
    data: dict = field(
        default_factory=dict, compare=False,
        metadata={"description": "Data payload of the incoming message"}
    )

    _souce_valid = ["eddn", "capi_api"]

    def __post_init__(self):
        if self.source not in self._souce_valid:
            raise ValueError(f"Invalid source '{self.source}'. Valid sources are: {self._souce_valid}")
        
    def to_dict(self) -> dict:
        return asdict(self)
        
    def __str__(self) -> str:
        return str(self.guid)