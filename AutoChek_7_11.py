from random import randrange


class Point:
    def __init__(self, x, y):
        self.__x = None
        self.__y = None
        self.x = x
        self.y = y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        if (type(x) == int) or (type(x) == float):
            self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        if (type(y) == int) or (type(y) == float):
            self.__y = y

    def __str__(self):
        return f"Point({self.x},{self.y})"


class Vector:
    def __init__(self, coordinates: Point):
        self.coordinates = coordinates

    def __setitem__(self, index, value):
        if index == 0:
            self.coordinates.x = value
        if index == 1:
            self.coordinates.y = value

    def __getitem__(self, index):
        if index == 0:
            return self.coordinates.x
        if index == 1:
            return self.coordinates.y

    def __call__(self, value=None):
        if value:
            self.coordinates.x = self.coordinates.x * value
            self.coordinates.y = self.coordinates.y * value
        return self.coordinates.x, self.coordinates.y

    def __add__(self, vector):
        result = self.coordinates.x + vector.coordinates.x, self.coordinates.y + vector.coordinates.y
        return Vector(Point(result[0], result[1]))

    def __sub__(self, vector):
        result = self.coordinates.x - vector.coordinates.x, self.coordinates.y - vector.coordinates.y
        return Vector(Point(result[0], result[1]))

    def len(self):
        return (self.coordinates.x ** 2 + self.coordinates.y ** 2) ** 0.5

    def __eq__(self, other):
        return self.coordinates.x == other.coordinates.x and self.coordinates.y == other.coordinates.y

    def __ne__(self, other):
        return self.coordinates.x != other.coordinates.x or self.coordinates.y != other.coordinates.y

    def __lt__(self, other):
        return self.coordinates.x < other.coordinates.x or self.coordinates.y < other.coordinates.y

    def __gt__(self, other):
        return self.coordinates.x > other.coordinates.x and self.coordinates.y > other.coordinates.y

    def __le__(self, other):
        return self.coordinates.x <= other.coordinates.x and self.coordinates.y <= other.coordinates.y

    def __ge__(self, other):
        return self.coordinates.x >= other.coordinates.x and self.coordinates.y >= other.coordinates.y

    def __str__(self):
        return f"Vector({self.coordinates.x},{self.coordinates.y})"


class Iterable:
    def __init__(self, max_vectors, max_points):
        self.current_index = 0
        self.vectors = []
        self.max_vectors = max_vectors
        self.max_points = max_points

    def __next__(self):
        if self.max_vectors > len(self.vectors):
            self.vectors.append((randrange(0, self.max_points), randrange(0, self.max_points)))
            count_list = self.vectors[self.current_index]
            self.current_index += 1
            return Vector(Point(count_list[0], count_list[1]))
        raise StopIteration


class RandomVectors:
    def __init__(self, max_vectors=10, max_points=50):
        self.max_vector = max_vectors
        self.max_points = max_points

    def __iter__(self):
        return Iterable(self.max_vector, self.max_points)


point = Point(1, 10)
vector = Vector(point)
print(vector.coordinates)
print(vector.coordinates.x)  # 1
print(vector.coordinates.y)  # 10

vector[0] = 10  # Встановлюємо координату x вектора 10

vector1 = Vector(Point(1, 10))
vector2 = Vector(Point(10, 10))

vector3 = vector2 + vector1
vector4 = vector2 - vector1

print(vector3)  # Vector(11,20)
print(vector4)  # Vector(9,0)
print(vector1.len())  # 10.04987562112089
print(vector2.len())  # 14.142135623730951

print(vector1 == vector2)  # False
print(vector1 != vector2)  # True
print(vector1 > vector2)  # False
print(vector1 < vector2)  # True
print(vector1 >= vector2)  # False
print(vector1 <= vector2)  # True

vectors = RandomVectors(5, 10)
for vector in vectors:
    print(vector)
