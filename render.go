package main

import (
	"fmt"
	"github.com/veandco/go-sdl2/sdl"
	"github.com/veandco/go-sdl2/ttf"
)

func FontSize(renderer *sdl.Renderer, text string, rel float64) int {
	w, _, _ := renderer.GetOutputSize()
	return int(2 * ((float64(w) * rel) / float64(len(text))))
}

func RelPoint(renderer *sdl.Renderer, texture *sdl.Texture,
	x_rel, y_rel float64) sdl.Point {

	_, _, wt, ht, _ := texture.Query()
	w, h, _ := renderer.GetOutputSize()
	return sdl.Point{
		X: int32(x_rel * float64(w-wt)),
		Y: int32(y_rel * float64(h-ht)),
	}
}

type Drawable interface {
	pos() sdl.Point
	texture() *sdl.Texture
}

func Draw(obj Drawable, renderer *sdl.Renderer, alpha uint8) {

	renderer.SetDrawBlendMode(sdl.BLENDMODE_BLEND)
	defer renderer.SetDrawBlendMode(sdl.BLENDMODE_NONE)

	texture := obj.texture()
	texture.SetAlphaMod(alpha)
	p := obj.pos()
	_, _, w, h, _ := texture.Query()
	renderer.Copy(texture, nil, &sdl.Rect{p.X, p.Y, w, h})
}

func CreateSDL(title string, w, h int32) (*sdl.Window, *sdl.Renderer) {
	var (
		err      error
		window   *sdl.Window
		renderer *sdl.Renderer
	)

	err = sdl.Init(sdl.INIT_EVERYTHING)
	if err != nil {
		panic(fmt.Sprintf("Chyba pri načítaní SDL: %s\n", err))
	}
	window, err = sdl.CreateWindow(title, 0, 0, w, h,
		sdl.WINDOW_MAXIMIZED|sdl.WINDOW_RESIZABLE)
	if err != nil {
		panic(fmt.Sprintf("Chyba pri vytváraní okna: %s\n", err))
	}
	renderer, err = sdl.CreateRenderer(window, -1,
		sdl.RENDERER_ACCELERATED|sdl.RENDERER_PRESENTVSYNC)
	if err != nil {
		panic(fmt.Sprintf("Chyba pri vytváraní vykreslovača: %s\n", err))
	}
	err = ttf.Init()
	if err != nil {
		panic(fmt.Sprintf("Chyba pri načítaní knižnice fontov: %s\n", err))
	}

	return window, renderer
}

func DestroySDL(window *sdl.Window, renderer *sdl.Renderer) {
	renderer.Destroy()
	window.Destroy()
	ttf.Quit()
	sdl.Quit()
}

func MakeTexture(renderer *sdl.Renderer, drawer func(*sdl.Renderer),
	w, h int32) *sdl.Texture {

	texture, err := renderer.CreateTexture(sdl.PIXELFORMAT_RGBA8888,
		sdl.TEXTUREACCESS_TARGET, w, h)
	if err != nil {
		panic(fmt.Sprintf("Nebolo možné vytvoriť textúru: %s\n", err))
	}
	RenderTexture(renderer, texture, drawer)
	return texture
}

func RenderTexture(renderer *sdl.Renderer, texture *sdl.Texture,
	drawer func(*sdl.Renderer)) {

	renderer.SetRenderTarget(texture)
	defer renderer.SetRenderTarget(nil)
	texture.SetBlendMode(sdl.BLENDMODE_BLEND)
	renderer.SetDrawColor(0, 0, 0, 0)
	renderer.Clear()
	drawer(renderer)
}

func TextRender(renderer *sdl.Renderer, font *ttf.Font,
	color sdl.Color, text string) *sdl.Texture {

	surface, err := font.RenderUTF8Solid(text, color)
	if err != nil {
		panic(fmt.Sprintf("Rendrovanie textu neúspešné ('%s'): %s\n", text, err))
	}
	t, err := renderer.CreateTextureFromSurface(surface)
	return t
}

func TextDraw(renderer *sdl.Renderer, pos sdl.Point, text *sdl.Texture) {
	_, _, w, h, _ := text.Query()
	renderer.Copy(text, nil, &sdl.Rect{pos.X, pos.Y, w, h})
}

func Abs(x int32) int32 {
	if x < 0 {
		x *= -1
	}
	return x
}

func lerp(a, b, t float64) int32 {
	return int32((1-t)*a + t*b)
}

func Lerp2D(pos sdl.Point, end sdl.Point, t float64) sdl.Point {
	return sdl.Point{
		X: lerp(float64(pos.X), float64(end.X), t),
		Y: lerp(float64(pos.Y), float64(end.Y), t),
	}
}
