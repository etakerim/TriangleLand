package main

import (
    "fmt"
    "github.com/veandco/go-sdl2/sdl"
)

func Abs(x int32) int32 {
    if x < 0 {
        x *= -1
    }
    return x
}

func lerp(a, b, t float64) int32 {
    return int32((1 - t) * a + t * b)
}

func Lerp2D(pos sdl.Point, end sdl.Point, t float64) sdl.Point {
    return sdl.Point{
        X: lerp(float64(pos.X), float64(end.X), t),
        Y: lerp(float64(pos.Y), float64(end.Y), t),
    }
}

func CreateSDL(title string, w, h int32) (*sdl.Window, *sdl.Renderer) {
    err := sdl.Init(sdl.INIT_EVERYTHING)
    window, err := sdl.CreateWindow(title, 0, 0, w, h, sdl.WINDOW_RESIZABLE)
    renderer, err := sdl.CreateRenderer(window, -1,
                        sdl.RENDERER_ACCELERATED | sdl.RENDERER_PRESENTVSYNC)

    if err != nil {
        panic(fmt.Sprintf("Chyba pri načítavaní SDL: %s\n", err))
    }

    return window, renderer
}

func DestroySDL(window *sdl.Window, renderer *sdl.Renderer) {
    renderer.Destroy()
    window.Destroy()
    sdl.Quit()
}

func MakeTexture(renderer *sdl.Renderer, drawer func(*sdl.Renderer),
                 w, h int32) *sdl.Texture {

    texture, _ := renderer.CreateTexture(sdl.PIXELFORMAT_RGBA8888,
                                         sdl.TEXTUREACCESS_TARGET, w, h)
    RenderTexture(renderer, texture, drawer)
    return texture
}

func RenderTexture(renderer *sdl.Renderer, texture *sdl.Texture,
                   drawer func(*sdl.Renderer)) {

    renderer.SetRenderTarget(texture)
    defer renderer.SetRenderTarget(nil)
    texture.SetBlendMode(sdl.BLENDMODE_BLEND)
    renderer.SetDrawColor(0, 0, 0, 0);
    renderer.Clear();
    drawer(renderer)
}


type Drawable interface {
    pos() sdl.Point
    texture() *sdl.Texture
}

func Draw(obj Drawable, renderer *sdl.Renderer, alpha uint8) {

    texture := obj.texture()
    _, _, w, h, _ := texture.Query()
    p := obj.pos()

    renderer.SetDrawBlendMode(sdl.BLENDMODE_BLEND)
    defer renderer.SetDrawBlendMode(sdl.BLENDMODE_NONE)
    texture.SetAlphaMod(alpha)
    renderer.Copy(texture, nil, &sdl.Rect{p.X, p.Y, w, h})
}


func main() {
    window, renderer := CreateSDL("COUNTRY OF 3 VERTICES", 800, 500)
    defer DestroySDL(window, renderer)

    board := NewBoard(renderer, sdl.Point{0, 0}, 60, 8, 8)
    on_turn := 0
    players := [4]Player{NewPlayer(renderer, 40, sdl.Color{255, 0, 0, 255}),
                         NewPlayer(renderer, 40, sdl.Color{0, 255, 0, 255}),
                         NewPlayer(renderer, 40, sdl.Color{255, 240, 0, 255}),
                         NewPlayer(renderer, 40, sdl.Color{255, 255, 255, 255})}

    for i := range players {
        players[i].Cell = board.RandomVertex()
        players[i].Move(board.VertexPixel(players[i].Cell))
    }

    ValidMoves := func(player Player) []*Vertex {
        var moves []*Vertex

        for _, cell := range board.VertexNeighbours(player.Cell) {
            add := true
            for _, p := range players {
                if cell == p.Cell {
                    add = false
                    break
                }
            }
            if add {
                moves = append(moves, cell)
            }
        }
        return moves
    }

    refresh := func() {
        renderer.SetDrawColor(0, 0, 0, 255)
        renderer.Clear()
        Draw(board, renderer, 255)
        for i, player := range players {
            var alpha uint8 = 180
            if i == on_turn {
                alpha = 255
            }
            Draw(player, renderer, alpha)
        }
        renderer.Present()
    }

    var event sdl.Event
    running := true;
    refresh()

    for running {
        for event = sdl.PollEvent(); event != nil; event = sdl.PollEvent() {
            switch t := event.(type) {
            case *sdl.QuitEvent:
                running = false
            case *sdl.WindowEvent:
                if t.Event == sdl.WINDOWEVENT_RESIZED {
                    refresh()
                }
            case *sdl.KeyboardEvent:
                if t.Type == sdl.KEYDOWN {
                    if t.Keysym.Sym == sdl.K_x {
                    }
                }

            case *sdl.MouseButtonEvent:
                if t.Type == sdl.MOUSEBUTTONDOWN {
                    for _, move := range ValidMoves(players[on_turn]) {
                        move_pos := board.VertexPixel(move)

                        if (Abs(t.X - move_pos.X) <= board.CellRadius &&
                            Abs(t.Y - move_pos.Y) <= board.CellRadius) {

                            start := board.VertexPixel(players[on_turn].Cell)
                            for i := 0.0; i <= 1.0; i += 0.05 {
                                players[on_turn].Move(Lerp2D(start, move_pos, i))
                                refresh()
                            }
                            players[on_turn].Move(move_pos)
                            players[on_turn].Cell = move
                            on_turn = (on_turn + 1) % len(players)
                            refresh()
                        }
                    }
                }
            }
        }

        sdl.Delay(16)
    }
}
