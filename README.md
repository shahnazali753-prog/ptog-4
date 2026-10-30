# Alien Invasion

Shoot down the alien fleet before it reaches you! A small Python game made with pygame,
with a settings menu you can change inside the game.

## How to play
```
pip install pygame
python alien_invasion.py
```

| Key | Action |
|---|---|
| Left / Right (or A / D) | Move the ship |
| Space | Shoot |
| P | Pause |
| Esc | Back to the menu (or quit from the menu) |

## Settings
Choose **Settings** in the main menu. Up and down pick a setting, and left and right change it.

- **Difficulty**: Easy, Normal, Hard or Insane (changes several settings at once)
- Lives, ship speed and ship color
- Bullet speed, bullet width and how many bullets can be on screen
- Alien rows, alien columns, alien speed and fleet drop speed
- Aliens shoot back (on or off) and how often they shoot
- How much faster each new wave gets
- Starry background (on or off)

Each alien is worth 50 points times the wave number. Clear the fleet and a faster wave arrives.

# Sky Hopper

A simple flap-through-the-gaps game made with pygame. Keep the bird in the air and fly
through the gaps between the pipes. Each pipe you pass is worth 1 point.

## How to play
```
pip install pygame
python flappy_bird.py
```

| Key | Action |
|---|---|
| Space / Up arrow / mouse click | Flap (also starts and restarts the game) |
| P | Pause |
| Esc | Quit |
