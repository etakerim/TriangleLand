package main

import (
    "math"
    "math/rand"
    "time"
    "github.com/veandco/go-sdl2/sdl"
    "github.com/veandco/go-sdl2/gfx"
)


type GraphicalCoordinate struct {
    X, Y float64
}

type Vertex struct {
    Pos GraphicalCoordinate
    NextFaces []*Face
}

type Face struct {
    NextVertices []*Vertex
    Occupied bool
    Color sdl.Color
}

type Board struct {
    Pos sdl.Point
    Scale int
    CellRadius int32
    Vertices []Vertex
    Faces []Face
    Texture *sdl.Texture
}

func (board Board) pos() sdl.Point {
    return board.Pos
}

func (board Board) texture() *sdl.Texture {
    return board.Texture
}

func NewBoard(renderer *sdl.Renderer, v sdl.Point, a, rows, cols int) Board {
    var board Board
    var virt_dim Vertex

    virt_dim.Pos = board.create_vertices(rows, cols)
    board.link_vertices_faces(rows, cols)

    board.Pos = v
    board.Scale = a
    board.CellRadius = int32(board.Scale / 10)
    dim := board.VertexPixel(&virt_dim)
    board.Texture = MakeTexture(renderer, board.PaintTexture, dim.X, dim.Y)

    return board
}

func (board *Board) PaintTexture(renderer *sdl.Renderer) {

    for _, face := range board.Faces {
        x := make([]int16, len(face.NextVertices))
        y := make([]int16, len(face.NextVertices))

        for i, v := range face.NextVertices {
            pos := board.VertexPixel(v)
            x[i] = int16(pos.X)
            y[i] = int16(pos.Y)
        }
        gfx.FilledPolygonColor(renderer, x, y, face.Color)
        gfx.AAPolygonColor(renderer, x, y, sdl.Color{255, 255, 255, 255})
    }

    for _, v := range board.Vertices {
        pos := board.VertexPixel(&v)
        gfx.FilledCircleColor(renderer, pos.X, pos.Y, board.CellRadius,
                              sdl.Color{0, 0, 255, 255})
    }
}

func (board Board) VertexPixel(v *Vertex) sdl.Point {
    return sdl.Point{
        X: int32(v.Pos.X * float64(board.Scale)),
        Y: int32(v.Pos.Y * float64(board.Scale)),
    }
}

func (board Board) RandomVertex() *Vertex{
    n := int32(len(board.Vertices))
    s := rand.NewSource(time.Now().UnixNano())
    rnd := rand.New(s)

    return &board.Vertices[rnd.Int31n(n)]
}

func (board *Board) VertexNeighbours(v *Vertex) []*Vertex {
    found := make(map[*Vertex]bool)
    var neighbours []*Vertex

    for _, f := range v.NextFaces {
        for _, v1 := range f.NextVertices {
            if v != v1 && !found[v1] {
                found[v1] = true
                neighbours = append(neighbours, v1)
            }
        }
    }

    return neighbours
}


func (board *Board) FacesOfEdge(v0, v1 *Vertex) []*Face {

    var intersect []*Face
    a := make(map[*Face]bool)
    b := make(map[*Face]bool)

    for _, v := range v0.NextFaces {
        a[v] = true
    }

    for _, v := range v1.NextFaces {
        b[v] = true
    }

    for k := range a {
        if b[k] {
            intersect = append(intersect, k)
        }
    }

    return intersect
}

func (board *Board) PointInTriangle(face *Face, p sdl.Point) bool {

    if len(face.NextVertices) != 3 {
        return false
    }

    p0 := board.VertexPixel(face.NextVertices[0])
    p1 := board.VertexPixel(face.NextVertices[1])
    p2 := board.VertexPixel(face.NextVertices[2])

    dX := p.X - p2.X
    dY := p.Y - p2.Y
    dX21 := p2.X - p1.X
    dY12 := p1.Y - p2.Y
    d :=  dY12 * (p0.X - p2.X) + dX21 * (p0.Y - p2.Y)
    s := dY12 * dX + dX21 * dY
    t := (p2.Y - p0.Y) * dX + (p0.X - p2.X) * dY

    if d < 0 {
        return s <= 0 && t <= 0 && s + t >= d
    } else {
        return s >= 0 && t >= 0 && s + t <= d
    }
}

func (board *Board) create_vertices(rows, cols int) GraphicalCoordinate {

    v := GraphicalCoordinate{0.2, float64(cols) * 0.5}
    x, y := v.X, v.Y
    ht := math.Sqrt(3) / 2

    for r := 1; r <= rows; r++ {
        for c := 0; c < cols; c++ {
            var vertex Vertex
            vertex.Pos = v
            board.Vertices = append(board.Vertices, vertex)
            v = GraphicalCoordinate{
                X: v.X + ht,
                Y: v.Y - 0.5,
            }
        }
        v = GraphicalCoordinate{
            X: x + float64(r) * ht,
            Y: y + float64(r) * 0.5,
        }
    }

    return GraphicalCoordinate{
        X: (x + float64(rows) * ht) * 2,
        Y: (y + float64(rows) * 0.5) - (y - float64(cols) * 0.5),
    }
}

func (board *Board) link_vertices_faces(w, h int) {

    i := func(row, col int) *Vertex {
        return &board.Vertices[col + row * w]
    }

    for r := 0; r < h - 1; r++ {
        for c := 0; c < w; c++ {
            if c - 1 >= 0 {
                face := Face{
                    NextVertices: []*Vertex{i(r, c), i(r + 1, c), i(r + 1, c - 1)},
                    Color: sdl.Color{0, 0, 0, 255},
                }
                board.Faces = append(board.Faces, face)
            }

            if c + 1 < w {
                face := Face{
                    NextVertices: []*Vertex{i(r, c), i(r + 1, c), i(r, c + 1)},
                    Color: sdl.Color{0, 0, 0, 255},
                }
                board.Faces = append(board.Faces, face)
            }
        }
    }

    // For each vertex put a list of its neighbouring face
    for i, f := range board.Faces {
        for _, v := range f.NextVertices {
            v.NextFaces = append(v.NextFaces, &board.Faces[i])
        }
    }
}
