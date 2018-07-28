package main

import (
    "math"
    "github.com/veandco/go-sdl2/sdl"
)

type HSV struct {
    H uint32
    S, V float64
    A uint8
}

func RgbToHsv(rgb sdl.Color) HSV {
    var hsv HSV
    r := float64(rgb.R) / 255
    g := float64(rgb.G) / 255
    b := float64(rgb.B) / 255

    max := math.Max(math.Max(r, g), b)
    min := math.Min(math.Min(r, g), b)

    if max == min {
        hsv.H = 0
    } else if max == r {
        if g >= b {
            hsv.H = uint32(60 * ((g - b) / (max - min)))
        } else {
            hsv.H = uint32(60 * ((g - b) / (max - min)) + 360)
        }
    } else if max == g {
        hsv.H = uint32(60 * ((b - r) / (max - min)) + 120)
    } else if max == b {
        hsv.H = uint32(60 * ((r - g) / (max - min)) + 240)
    }
    hsv.H %= 360

    if max == 0 {
        hsv.S = 0
    } else {
        hsv.S = 1 - min / max
    }

    hsv.V = max
    hsv.A = rgb.A

    return hsv
}

func HsvToRgb(hsv HSV) sdl.Color {
    hue := (hsv.H / 60) % 6

    f := float64(hsv.H) / 60 - float64(hue)
    p := uint8(255 * hsv.V * (1 - hsv.S))
    q := uint8(255 * hsv.V * (1 - f * hsv.S))
    t := uint8(255 * hsv.V * (1 - (1 - f) * hsv.S))
    v := uint8(255 * hsv.V)

    switch hue {
        case 0:
            return sdl.Color{v, t, p, hsv.A}
        case 1:
            return sdl.Color{q, v, p, hsv.A}
        case 2:
            return sdl.Color{p, v, t, hsv.A}
        case 3:
            return sdl.Color{p, q, v, hsv.A}
        case 4:
            return sdl.Color{t, p, v, hsv.A}
        default:
            return sdl.Color{v, p, q, hsv.A}
    }
}
