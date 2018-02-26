import pygame
import math
from collections import namedtuple


Vertex = namedtuple('Vertex', ['coords', 'faces'])
Face = namedtuple('Face', ['vertices', 'color'])


EQUILATERAL = math.sqrt(3) / 2
ISOCELES_RIGHT = 0.5


class Board:
    def __init__(self, x, y, width, height, a, tri=EQUILATERAL):
        # Using Face-Vertex mesh datastructure
        self.vertices = []
        self.faces = []

        # Create vertices
        h = tri * a
        a_half = a / 2
        v = [float(x), float(y)]

        for row in range(1, height + 1):
            for col in range(width):
                self.vertices.append(Vertex(v, []))
                v = [v[0] + h, v[1] - a_half]
            v = [x + row * h, y + row * a_half]

        # Generate faces pointing to vertex array by index
        i = lambda row, col: col + row * width
        for r in range(height - 1):
            for c in range(width):
                if c - 1 >= 0:
                    face = [i(r, c), i(r + 1, c), i(r + 1, c - 1)]
                    self.faces.append(Face(face, ''))
                if c + 1 < width:
                    face = [i(r, c), i(r + 1, c), i(r, c + 1)]
                    self.faces.append(Face(face, ''))

        # For each vertex put a list of its neighbouring faces
        for i, face in enumerate(self.faces):
            for v in face.vertices:
                self.vertices[v].faces.append(i)

    def rotate(self, angle):
        a = self.vertices[0].coords
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)

        for i, v in enumerate(self.vertices):
            b = v.coords
            vector = [b[0] - a[0], b[1] - a[1]]
            new_vector = [vector[0] * cos_angle - vector[1] * sin_angle,
                          vector[0] * sin_angle + vector[1] * cos_angle]
            new_pos = [a[0] + new_vector[0], a[1] + new_vector[1]]
            self.vertices[i] = Vertex(new_pos, self.vertices[i].faces)

    def vertex_neighbours(self, v):
        neighbours = []
        for f_ref in self.vertices[v].faces:
            for v_ref in self.faces[f_ref].vertices:
                if v_ref != i_vertex and v_ref not in neighbours:
                    neighbours.append(v_ref)
        return neighbours

    def vertex_coords(self, v):
        return self.vertices[v].coords

    def vertex_faces(self, v):
        return self.vertices[v].faces

    def faces_of_edge(self, v0, v1):
        return list(set(self.vertex_faces(v0)) & set(self.vertex_faces(v1)))

    def draw(self, surface):
        r = 5
        for triangle in self.faces:
            a = self.vertex_coords(triangle.vertices[0])
            b = self.vertex_coords(triangle.vertices[1])
            c = self.vertex_coords(triangle.vertices[2])
            pygame.draw.aalines(surface, WHITE, True, (a, b, c))
            # pygame.draw.polygon(surface, (rnd(255), rnd(255), rnd(255)), (a, b, c))

        for v in self.vertices:
            x, y = v.coords
            pygame.draw.ellipse(surface, BLUE, (x - r, y - r, 2 * r, 2 * r))
