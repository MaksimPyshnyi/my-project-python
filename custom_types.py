import mimetypes
from itertools import takewhile
from typing import NamedTuple
from typing import Optional
from urllib.parse import urlsplit
from utils import get_content_type


class HttpRequest(NamedTuple):
    original: str
    normal: str
    method: str = "get"
    file_name: Optional[str] = None
    query_string: Optional[str] = None
    content_type: Optional[str] = "text/html"

    @classmethod
    def default(cls):
        return HttpRequest(original="", normal="/")

    @classmethod
    def from_path(cls, path: str, method: Optional[str] = None) -> "HttpRequest":
        if not path:
            return cls.default()

        components = urlsplit(path)

        segments = tuple(filter(bool, components.path.split("/")))
        non_file_segments = takewhile(lambda part: "." not in part, segments)

        compiled = "/".join(non_file_segments)
        normal = f"/{compiled}/" if compiled not in {"", "/"} else "/"

        last = segments[-1] if segments else ""
        file_name = last if "." in last else None

        content_type = mimetypes.guess_type(file_name  or "index.html")

        return HttpRequest(
            method=method or "get",
            original=path,
            normal=normal,
            file_name=file_name,
            query_string=components.query or None,
            content_type=content_type,
        )

class User(NamedTuple):
    name: str
    age: int

    @classmethod
    def default(cls):
        return User(name="anonymous", age=0)

    @classmethod
    def from_query(cls, query: str) -> "User":
        anonymous = cls.default()

        try:
            key_value_pairs = parse_qs(query, strict_parsing=True)
        except ValueError:
            return anonymous

        name_values = key_value_pairs.get("name", [anonymous.name])
        name = name_values[0]

        age_values = key_value_pairs.get("age", [anonymous.age])
        age = age_values[0]
        if isinstance(age, str) and age.isdecimal():
            age = int(age)

        return User(name=name, age=age)