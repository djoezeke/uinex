"""PygameUI version."""

__all__ = ["Version", "vernum"]


class Version(tuple):
    """Version class."""

    __slots__ = ()
    fields = "major", "minor", "patch"

    def __new__(cls, major, minor, patch) -> "Version":
        return tuple.__new__(cls, (major, minor, patch))

    def __repr__(self) -> str:
        fields = (f"{fld}={val}" for fld, val in zip(self.fields, self))
        return f"{self.__class__.__name__}({', '.join(fields)})"

    def __str__(self) -> str:
        return f"{self[0]}.{self[1]}.{self[2]}"

    major = property(lambda self: self[0])
    minor = property(lambda self: self[1])
    patch = property(lambda self: self[2])


vernum = Version(0, 1, 0)
