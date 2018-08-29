package main

import (
    "fmt"
    "github.com/veandco/go-sdl2/sdl"
    "github.com/veandco/go-sdl2/ttf"
)


func MenuDraw(renderer *sdl.Renderer) {
    size := FontSize(renderer, "COUNTRY OF 3 VERTICES", 0.7)
    font, err := ttf.OpenFont("Triangles-Regular.otf", size)
    if err != nil {
        panic(fmt.Sprintf("Herný font sa nepodarilo nájsť: %s\n", err))
    }
    defer font.Close()

    heading_color := sdl.Color{255, 240, 0, 255}
    white := sdl.Color{255, 255, 255, 255}

    title := TextRender(renderer, font, heading_color, "COUNTRY OF 3 VERTICES")
    play := TextRender(renderer, font, white, "PLAY")
    quit := TextRender(renderer, font, white, "QUIT")

    elements := [...]*sdl.Texture{title, play, quit}
    y_rel := [...]float64{0.1, 0.5, 0.7}

    renderer.SetDrawColor(19, 123, 58, 255)
    renderer.Clear()
    defer renderer.Present()

    for i := range elements {
        pos := RelPoint(renderer, elements[i], 0.5, y_rel[i])
        TextDraw(renderer, pos, elements[i])
    }
}


