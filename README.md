# Shahnaz Ali · Portfolio & Games

My personal portfolio website, plus the Python games it shows off.

**🌐 Live website:** https://shahnazali753-prog.github.io/ptog-4/

## The website

A modern, fully responsive one-page portfolio. It's built with plain HTML, CSS and JavaScript, with no frameworks and no build step.

**Features**
- Light and dark mode (your choice is remembered)
- Smooth scroll animations, a typing effect and animated stats
- Mobile menu that works well on iPhone and Android
- Project cards with filters (All / Python / Web)
- **Playable Sky Hopper** in the browser, a JavaScript remake of `flappy_bird.py` that saves your best score
- Share button (opens the phone's share menu, or copies the link on a computer)
- Reading progress bar, back-to-top button and a custom 404 page
- Accessible: keyboard friendly, screen-reader labels, and respects "reduce motion"

**Files**
```
index.html        the page content
css/style.css     all the design and animations
js/main.js        menu, theme, animations and the Sky Hopper game
assets/           the site icon
404.html          "page not found" page
.nojekyll         tells GitHub Pages to serve the files as they are
```

**Editing the site:** open a file on GitHub, tap the ✏️ pencil icon, make your change and tap **Commit changes**. The live site updates about a minute later.

---

## Alien Invasion

Shoot down the alien fleet before it reaches you! A small Python game made with pygame,
with a settings menu you can change inside the game.

### How to play
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

### Settings
Choose **Settings** in the main menu. Up and down pick a setting, and left and right change it.

- **Difficulty**: Easy, Normal, Hard or Insane (changes several settings at once)
- Lives, ship speed and ship color
- Bullet speed, bullet width and how many bullets can be on screen
- Alien rows, alien columns, alien speed and fleet drop speed
- Aliens shoot back (on or off) and how often they shoot
- How much faster each new wave gets
- Starry background (on or off)

Each alien is worth 50 points times the wave number. Clear the fleet and a faster wave arrives.

---

## Sky Hopper

A simple flap-through-the-gaps game made with pygame. Keep the bird in the air and fly
through the gaps between the pipes. Each pipe you pass is worth 1 point.

### How to play
```
pip install pygame
python flappy_bird.py
```

| Key | Action |
|---|---|
| Space / Up arrow / mouse click | Flap (also starts and restarts the game) |
| P | Pause |
| Esc | Quit |
