// TODO: Obsadzovanie územia
// Relatívne veľkosti a ľahká zmena a prerendrovnie textúry
package main

import (
    "math"
    "github.com/veandco/go-sdl2/sdl"
    "github.com/veandco/go-sdl2/gfx"
)

type Player struct {
    Cell *Vertex
    Claim struct {
        Area *Face
        FenceStart *Vertex
    }
    // Uloženie nárokovaného územia + jeho zrušenie a opustí jeho hranu
    // + poznačenie kde sa má späť dostať
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

    player.Radius = int16(float64(width) / math.Sqrt(3))
    player.Width = int32(2 * player.Radius)
    player.Color = color
    player.Texture = MakeTexture(renderer, player.PaintTexture,
                                 player.Width, player.Width)
    return player
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
