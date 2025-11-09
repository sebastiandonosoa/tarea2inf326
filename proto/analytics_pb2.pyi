from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HitRequest(_message.Message):
    __slots__ = ("short_url", "long_url", "timestamp", "hash")
    SHORT_URL_FIELD_NUMBER: _ClassVar[int]
    LONG_URL_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    short_url: str
    long_url: str
    timestamp: int
    hash: str
    def __init__(self, short_url: _Optional[str] = ..., long_url: _Optional[str] = ..., timestamp: _Optional[int] = ..., hash: _Optional[str] = ...) -> None: ...

class HitResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class StatsRequest(_message.Message):
    __slots__ = ("hash",)
    HASH_FIELD_NUMBER: _ClassVar[int]
    hash: str
    def __init__(self, hash: _Optional[str] = ...) -> None: ...

class StatsResponse(_message.Message):
    __slots__ = ("stats",)
    STATS_FIELD_NUMBER: _ClassVar[int]
    stats: _containers.RepeatedCompositeFieldContainer[URLStats]
    def __init__(self, stats: _Optional[_Iterable[_Union[URLStats, _Mapping]]] = ...) -> None: ...

class URLStats(_message.Message):
    __slots__ = ("hash", "short_url", "long_url", "hit_count", "last_accessed", "created_at")
    HASH_FIELD_NUMBER: _ClassVar[int]
    SHORT_URL_FIELD_NUMBER: _ClassVar[int]
    LONG_URL_FIELD_NUMBER: _ClassVar[int]
    HIT_COUNT_FIELD_NUMBER: _ClassVar[int]
    LAST_ACCESSED_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    hash: str
    short_url: str
    long_url: str
    hit_count: int
    last_accessed: int
    created_at: int
    def __init__(self, hash: _Optional[str] = ..., short_url: _Optional[str] = ..., long_url: _Optional[str] = ..., hit_count: _Optional[int] = ..., last_accessed: _Optional[int] = ..., created_at: _Optional[int] = ...) -> None: ...
