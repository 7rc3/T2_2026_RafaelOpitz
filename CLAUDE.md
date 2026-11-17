# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project context

School project for "Oficina de Multimédia" (12.º ano, CRSI, 2026/2027): a web Dashboard / Web App that brings Python exercises from class onto the web. The user is a student learning Python; the teacher expects AI assistance and asks for it to be documented. Explain changes simply, and keep code readable at a beginner level rather than using advanced abstractions.

The user writes in English, but the project content (README, page text) is in Portuguese (pt-PT).

## Running

No build step. `index.html` loads `app.py` with fetch, so opening the file directly won't work. Serve the folder over HTTP instead:

```
python -m http.server 8000   # then open http://localhost:8000
```

Deployed with GitHub Pages from the repo root (repo: github.com/7rc3/T2_2026_RafaelOpitz).

## Architecture

- `index.html`: the whole UI, styled with **Tailwind v4 browser CDN** (the user prefers Tailwind; no `style.css`). It also loads **PyScript** (Pyodide) from pinned CDN versions.
- Visual style is a "cozy retro pixel OS": a desktop of icons (`<button class="icone" data-abrir="janela-x">`) that open pixel windows (`<section class="janela" hidden>`), plus a bottom taskbar (settings, live date). The palette is defined as CSS variables in `@theme static` inside `<style type="text/tailwindcss">` (`bg-coral`, `text-tinta`, etc.). A second theme overrides a few variables under `html[data-tema="por-do-sol"]`. Use palette classes, not default Tailwind colors, and no rounded corners.
- A small plain-JS `<script>` at the end of `index.html` only handles the OS shell: windows, clock, settings saved in `localStorage` under `definicoes`, scanlines and the click sound. The widgets stay in the DOM while their window is hidden, so the ids `app.py` uses keep working.
- `Assets/icons/*.svg`: 16×16 pixel-art icons made of `<rect>` rows (`shape-rendering="crispEdges"`), shown at 4× on the desktop and 2× in the taskbar.
- `app.py`: all logic, running in the browser. It reads and writes the DOM through `pyscript.document` by element id, and binds events with `@when("event", "#id")`. Handlers decorated with `@when` are thin wrappers that call plain functions, so the plain functions can also run at startup. The last lines of `app.py` render the initial state and remove the `#loading` overlay.
- Python inserts HTML strings that contain Tailwind classes. The Tailwind browser build compiles those classes at runtime, so dynamic classes work.
- The three widgets: poem analyzer (word frequency, ficha 6.1/7), minesweeper (`minas.py` window; 2D lists, loops, if/elif; first click always safe; its "AI" hint button finds a guaranteed safe cell or mine by simple logic), and guess-the-number with hints (JOGO DA ADIVINHA). Board cells are HTML buttons built by `app.py`, styled by `.celula` / `.celula-fechada` in `index.html`, with `Assets/icons/mina.svg` and `bandeira.svg`. The "AI extensions" are code written with AI help. There are no live LLM API calls, because a static site can't hide an API key.
- Pyodide has no `wordcloud` package, so the word cloud is made of HTML spans sized by frequency.

## Old files

`old/` (gitignored) holds earlier class work kept only as a reference to copy from:
- `old/python.ipynb`, `old/parte2.ipynb`: Jupyter notebooks with the class exercises (variables, casting, if/elif/else, loops, etc.). These are the source material to adapt for the web app.
- `old/Propostas_Trabalho_Python_IA_Multimedia.pdf`: the assignment.
- `old/index.html`: an earlier static dashboard prototype ("Portefólio Multimedia e Inteligência Artificial") using a flexbox `.dashboard` of `.widget-card` elements with inline CSS.

## Expected structure (from README.md)

The README is the project report template the teacher requires. It expects this structure:
- `index.html`: main Dashboard / Web App page
- `app.py`: main application file
- `style.css`: stylesheet (optional)
- `Assets/`: images, generated word clouds, and other resources
- `README.md`: the project report. Its sections (overview, chosen proposal, AI usage log with prompts, difficulties, layout changes, critical reflection) must be filled in by the student. Don't overwrite those sections with invented content. Suggest text only when asked.

## Assignment (old/Propostas_Trabalho_Python_IA_Multimedia.pdf)

The user is leaning toward **Proposal 1**: a web dashboard (HTML/CSS, or Streamlit) with 3 widgets based on the October Python worksheets (strings, lists, flow control, games), each extended with AI. Example widgets from the PDF are only suggestions: a poem analyzer with word cloud, a resolution and aspect-ratio validator with a hex palette picker, and a quiz or guess-the-number game with hints.

Submission requirements: use the HTML5/CSS base structure taught in class, with responsive CSS. The GitHub repo should be named `<name>_dashboard_multimedia`. The app must be published publicly (GitHub Pages or Streamlit Cloud). The README must explain the project, how to run it, and the AI prompts used. GitHub Pages only serves static files, so Python there must run in the browser (e.g., PyScript/Pyodide); a Flask-style `app.py` would not work on Pages. Confirm the approach with the user before building.
