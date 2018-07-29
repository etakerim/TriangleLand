package main

import (
    "github.com/veandco/go-sdl2/sdl"
)

type Game struct {
    Window *sdl.Window
    Renderer *sdl.Renderer
    Board Board
    Players []Player
    OnTurn int
    Claiming bool
}

func (game *Game) ValidMoves(player *Player) []*Vertex {
    var moves []*Vertex
    var valid bool

    for _, cell := range game.Board.VertexNeighbours(player.Cell) {
        valid = true
        for _, p := range game.Players {
            if cell == p.Cell {
                valid = false
                break
            }
        }

        if valid {
            moves = append(moves, cell)
        }
    }

    return moves
}

func (game *Game) ActivePlayer() *Player {
    return &game.Players[game.OnTurn]
}

func (game *Game) TakeTurn() {
    game.OnTurn = (game.OnTurn + 1) % len(game.Players)
    game.ScreenRefresh()
}

func (game *Game) ScreenRefresh() {

    game.Renderer.SetDrawColor(0, 0, 0, 255)
    game.Renderer.Clear()
    Draw(game.Board, game.Renderer, 255)

    for i, player := range game.Players {
        var alpha uint8 = 150
        if i == game.OnTurn {
            alpha = 255
        }
        Draw(player, game.Renderer, alpha)
    }

    game.Renderer.Present()
}

func (game *Game) PieceMove(click sdl.Point) {
    player := game.ActivePlayer()

    for _, move := range game.ValidMoves(player) {
        move_pos := game.Board.VertexPixel(move)

        if (Abs(click.X - move_pos.X) <= game.Board.CellRadius &&
            Abs(click.Y - move_pos.Y) <= game.Board.CellRadius) {

            start := game.Board.VertexPixel(player.Cell)
            for i := 0.0; i <= 1.0; i += 0.05 {
                player.Move(Lerp2D(start, move_pos, i))
                game.ScreenRefresh()
            }
            player.Move(move_pos)
            player.Cell = move
            game.TakeTurn()
        }
    }
}

func (game *Game) HighlightClaimable() {
    game.Claiming = !game.Claiming

    for _, face := range game.ActivePlayer().Cell.NextFaces {
        if game.Claiming && !face.Occupied {
            face.Color = sdl.Color{150, 150, 150, 150}
        } else {
            face.Color = sdl.Color{0, 0, 0, 255}
        }
    }
    RenderTexture(game.Renderer, game.Board.Texture, game.Board.PaintTexture)
    game.ScreenRefresh()
}

func (game *Game) ClaimArea(click sdl.Point) {
    if !game.Claiming {
        return
    }
    // nastav veci pre playera na obsadzoavnie v structe
    for _, face := range game.ActivePlayer().Cell.NextFaces {

        if game.Board.PointInTriangle(face, click) {
            for _, f := range game.ActivePlayer().Cell.NextFaces {
                f.Color = sdl.Color{0, 0, 0, 255}
            }
            face.Color = sdl.Color{240, 240, 240, 255}
            face.Occupied = true

            RenderTexture(game.Renderer, game.Board.Texture, game.Board.PaintTexture)
            game.Claiming = false
            game.TakeTurn()
            break
        }
    }
}

func main() {
    var game Game
    PLAYER_COLORS := [4]sdl.Color{sdl.Color{250, 50, 50, 255},
                                  sdl.Color{85, 255, 30, 255},
                                  sdl.Color{30, 255, 200, 255},
                                  sdl.Color{50, 35, 255, 255}}

    game.Window, game.Renderer = CreateSDL("Country of 3 Vertices", 800, 500)
    defer DestroySDL(game.Window, game.Renderer)

    game.Board = NewBoard(game.Renderer, sdl.Point{0, 0}, 60, 8, 8)
    game.Players = make([]Player, len(PLAYER_COLORS))
    for i, color := range PLAYER_COLORS {
        game.Players[i] = NewPlayer(game.Renderer, 40, color)
    }

    for i := range game.Players {
        game.Players[i].Cell = game.Board.RandomVertex()
        game.Players[i].Move(game.Board.VertexPixel(game.Players[i].Cell))
    }
    game.ScreenRefresh()

    var event sdl.Event
    running := true;

    for running {
        for event = sdl.PollEvent(); event != nil; event = sdl.PollEvent() {
            switch t := event.(type) {
            case *sdl.QuitEvent:
                running = false
            case *sdl.WindowEvent:
                if t.Event == sdl.WINDOWEVENT_RESIZED {
                    game.ScreenRefresh()
                }
            case *sdl.KeyboardEvent:
                if t.Type == sdl.KEYDOWN {
                    if t.Keysym.Sym == sdl.K_x {
                        game.HighlightClaimable()
                    }
                }

            case *sdl.MouseButtonEvent:
                if t.Type == sdl.MOUSEBUTTONDOWN {
                    click := sdl.Point{t.X, t.Y}
                    game.ClaimArea(click) // TODO: break if done
                    game.PieceMove(click)
                }
            }
        }
        sdl.Delay(16)
    }
}
