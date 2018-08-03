package main

import (
    "math"
    "github.com/veandco/go-sdl2/sdl"
    "github.com/veandco/go-sdl2/gfx"
)

type Player struct {
    Cell *Vertex
    Claim struct {
        Active bool
        Area *Face
        Fence map[*Vertex]bool
    }
    Territory []*Face
    Pos sdl.Point
    Radius int16
    Width int32
    Color sdl.Color
    Texture *sdl.Texture
}

func (player Player) pos() sdl.Point {
    return player.Pos
}

func (player Player) texture() *sdl.Texture {
    return player.Texture
}


func NewPlayer(renderer *sdl.Renderer, width int, color sdl.Color) Player {

    var player Player

    player.Color = color
    player.Resize(renderer, width)
    return player
}


func (player *Player) Resize(renderer *sdl.Renderer, width int) {

    player.Radius = int16(float64(width) / math.Sqrt(3))
    player.Width = int32(2 * player.Radius)
    player.Texture = MakeTexture(renderer, player.PaintTexture,
                                 player.Width, player.Width)
}

func (player *Player) PaintTexture(renderer *sdl.Renderer) {
    var smooth float64 = 10
    hsv := RgbToHsv(player.Color)
    hsv.V = 0.3

    for ri := float64(player.Radius); ri >= 0; ri -= float64(player.Radius) / smooth {
        r := int16(ri)
        x := []int16{player.Radius - r, player.Radius + r, player.Radius}
        y := []int16{player.Radius + r, player.Radius + r, player.Radius - r}
        gfx.FilledPolygonColor(renderer, x, y, HsvToRgb(hsv))
        hsv.V += (1 - 0.3) / smooth
    }
}

func (player *Player) Move(pos sdl.Point) {
    player.Pos.X = pos.X - int32(player.Radius)
    player.Pos.Y = pos.Y - int32(player.Radius)
}

func (player *Player) CanOccupy() []*Face {

    var areas []*Face
    neighbours := player.Cell.NextFaces

    for _, face := range neighbours {
        if face.Owner == nil {
            areas = append(areas, face)
        }
    }

    return areas
}

func (player *Player) CheckOccupation() bool {
    touching := false
    finished := true

    if player.Claim.Active {
        player.Claim.Fence[player.Cell] = true

        for _, v := range player.Claim.Fence {
            if !v {
                finished = false
            }
        }
        if finished {
            player.TakeClaim()
            return true
        }

        for _, face := range player.Cell.NextFaces {
            if face == player.Claim.Area {
                touching = true
            }
        }
        if !touching {
            player.LoseClaim()
            return true
        }
    }

    return false
}

func (player *Player) MakeClaim(face *Face) {
    face.Owner = player
    face.Color = sdl.Color{240, 240, 240, 255}

    player.Claim.Active = true
    player.Claim.Area = face
    player.Claim.Fence = make(map[*Vertex]bool)
    for _, v := range face.NextVertices {
        player.Claim.Fence[v] = false
    }
}

func (player *Player) TakeClaim() {
    player.Claim.Area.Owner = player
    player.Claim.Area.Color = player.Color
    player.Territory = append(player.Territory, player.Claim.Area)
    player.Claim.Active = false
}

func (player *Player) LoseClaim() {
    player.Claim.Area.Owner = nil
    player.Claim.Area.Color = sdl.Color{0, 0, 0, 255}
    player.Claim.Active = false
}
