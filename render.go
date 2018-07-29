package main

import (
    "fmt"
    "github.com/veandco/go-sdl2/sdl"
)

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
