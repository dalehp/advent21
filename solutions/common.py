from __future__ import annotations

from dataclasses import dataclass

@dataclass
class Point:
    x: int = 0
    z: int = 0  # Depth (higher is deeper)

    def __add__(self, o: Point) -> Point:
        return Point(x=self.x + o.x, z=self.z + o.z)

    def __mul__(self, o: int) -> Point:
        return Point(x=o * self.x, z=o * self.z)

    def __rmul__(self, o: int) -> Point:
        return self.__mul__(o)