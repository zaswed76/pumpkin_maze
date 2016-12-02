
import enum

class Directions(enum.Enum):
    left = False
    top = False
    right = False
    down = False

    def set_left(b):
        left = b


print(Directions.left.value)
Directions.set_left(True)
print(Directions.left.value)