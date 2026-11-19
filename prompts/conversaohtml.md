I have a school project: a website that works as a hub for several games and tools I made in Python. I want you to rewrite the UI to match a specific art style. Keep all existing functionality working; this is a visual redesign, not a rewrite of the logic.

## First, before changing anything
1. Explore the project and tell me how it's structured: what framework/files are used for the website, how the Python games/tools are displayed or launched (e.g. Pyodide, pygbag, Flask, links, iframes), and where the current styles live.
2. Propose a short plan (which files you'll change, what new files you'll add) and wait for my OK before making big changes.

## The art style: "cozy retro pixel OS"
The site should look like a cute little fantasy computer desktop, like the in-game computer menus in cozy indie games or a PICO-8/Playdate-style fantasy console.

**Layout**
- The home page is a "desktop": a dark background with a grid of large pixel-art icons, each with a short lowercase label underneath (e.g. "snake", "calculator", "quiz").
- Lots of empty space, few elements, nothing cluttered.
- A light-colored taskbar fixed to the bottom of the screen: a "SETTINGS" button on the left, and a small sun/weather icon plus the current day and date on the right (e.g. "TUE.12"), updated live with JavaScript.
- Clicking an icon opens the game/tool inside a pixel-styled "window" (a title bar with the app name and a close [x] button), or navigates to its page, whichever fits how the project currently works.

**Colors (limited palette, use CSS variables)**
- Background: dark desaturated navy-purple (~#2b2838)
- Taskbar: pale cyan (~#b8ecf5) with darker blue sections (~#6cc4e0)
- Accents: peach/orange (~#f7b46a), coral red (~#e8533f), sky blue (~#5fa8d8), sunny yellow (~#f5d547), white (#ffffff) for labels
- Keep the whole site within roughly 8 colors. No gradients, no soft shadows, no blur.

**Pixel-art rules**
- Everything must look crisp and blocky: use `image-rendering: pixelated` on all images and canvases.
- No rounded corners, no anti-aliased soft edges. Borders are solid 2–4px lines, and "shadows" are hard offset blocks (e.g. `box-shadow: 4px 4px 0 #000`).
- Icons: create simple pixel-art icons as small SVGs built from `<rect>` squares on a 16×16 grid (or as small PNGs/data URIs), scaled up 3–4x. Each one should represent its game/tool (a folder, a joystick, a calculator, a picture frame, etc.) with 1–2 shading tones per color.
- Fonts: use a pixel font from Google Fonts or a free source, e.g. "Pixelify Sans" or "Silkscreen" for labels and "Press Start 2P" or "VT323" for the taskbar. Labels are lowercase, the taskbar text is uppercase.

**Interactions**
- Hovering over an icon: a small step-wise bounce or a highlight box around it (use `steps()` in CSS animations so motion feels choppy and retro, not smooth).
- Clicking: a quick "pressed" effect (shift down 2px).
- Optional extras if they're easy: a blinking cursor somewhere, a subtle CRT scanline overlay that can be toggled in Settings, a tiny click sound.

**Settings button**
Opens a small pixel window with a couple of simple options (e.g. toggle scanlines, toggle sounds, switch between 2 color themes). Save the choices in localStorage.

## Requirements
- Must stay responsive: on phones the icon grid should wrap and the taskbar should stay readable.
- Keep the code simple and well commented. This is a school project and I need to understand and explain it.
- Don't add heavy frameworks unless the project already uses them; plain HTML/CSS/JS is preferred for the UI.
- Don't break how the Python games/tools currently run.
- When you're done, give me a short summary of what you changed and how to add a new game/tool icon to the desktop in the future.

My games/tools are: [LIST THEM HERE, e.g. "snake game, quiz, unit converter, tic-tac-toe"]