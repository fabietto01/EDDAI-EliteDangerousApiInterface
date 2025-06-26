from dataclasses import dataclass, field
import uuid

@dataclass(frozen=True)
class IncomingData:

    guiid: str = field(
        init=False, compare=True,
        repr=False, metadata={"description": "Unique identifier for the incoming data"},
        default=lambda: str(uuid.uuid4())
    )
    source: str = field(
        default_factory=str, compare=False,
        metadata={"description": "Source of the incoming data, e.g., 'eddn' or 'capi_api'"}
    )
    data: dict = field(
        default_factory=dict, compare=False,
        metadata={"description": "Data payload of the incoming message"}
    )

    def __post_init__(self):
        if self.source not in ["eddn", "capi_api"]:
            raise ValueError(f"Invalid source '{self.source}'. Valid sources are: {self._souce_valid}")
        
    def __str__(self) -> str:
        return str(self.guiid)