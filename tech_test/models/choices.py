import enum


class State(str, enum.Enum):
    UnDefined = "UNDEFINED"
    Start = "STARTED"
    Done = "DONE"
    Failed = "FAILED"
    Rollback = "ROLLBACK"

