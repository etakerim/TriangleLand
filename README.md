## Triangle Land

Strategic board game about conquering the greatest number of triangle areas on the map.

### Development build
In order to run the game you need to first install `SDL2` (Simple DIrectmedia Library) with golang bindings (`go-sdl2`). Instructions available [here](https://github.com/veandco/go-sdl2).

After you sucessfully installed graphics library, run the game while in cloned repository.
``` bash
$ go run *.go 
```

### Help welcome :)
Pull requests or Issues are encouraged to bring this game to live as there is still a lot to be done. In part about game mechanics you can check where help is needed, if you can't wait to see the end result.


### Game theme
In the world of digital 3D graphics all objects are marked as points connected with lines creating triangles. This imaginary world now comes to live (at least when you create yourself "real board game"). 

Gameboard is composed of equilateral triangles and game pieces are  	tetrahedrons to really immerse you to into the game. Goal is to get the greatest influence on the map by owning the most strategic landmass.

### Gameplay mechanics

#### Conquer
**Status done: 100% **

After game pieces have been randomly places into the world, quest of conquering can begin. You can claim one new region at the time. You are presented with nearby areas. You can claim one by clicking on it. When you do so it turns white. Then your task is to visit all of its tips to conquer it (Changes color to that of your piece). If you leave region is automatically freed.

#### Move
**Status done: 90% ** 
**TODO:**  Place pieces randomly / pick position at the start of game

On every your turn you can move only to the neighbouring vertex by one step. You are not allowed to walk on the "road" between two enemy regions (as though players are building fences around their consecutive regions) or step on the vertex which is already occupied.

#### Trade
**Status done: 0% **
When two pieces stand on nearby vertices they can trade any of their areas to maybe gain strategic influence.

#### Ranking
**Status done: 0% **
- Player's score is determined by summing the number of all edges (roads) connecting vertices of given player's areas (triangles). 
- If two areas of the same player touch by edge then the sum is multiplied by the number of touching triangles. 
- If triangle is bordering whit enemy's triangles, this triangles is penalized (loosing points), -1pt for 2 enemy edges, -2pt for 3 enemy edges (completely besieged). 

For example - When you own **hexagon like area** composed of 6 triangles and surounded by enemy's regions then score for this connected region is:
+ 12 edges in total = **12 points**
+ 6 triangles are touching at least by one edge = **6 multiplier**
+ No points are taken because every triangle touches only 1 edge of enemy triangle. 
**Total: 72 points** : *(12 x 6) - 0*

#### Menu a HUD
**Status done: 10% **


#### Have fun!




