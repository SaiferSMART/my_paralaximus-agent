# PARALAXIMUS

PARALAXIMUS is a Cursor subagent for creating layered parallax hero blocks from a single 2K image atlas.

It is designed for local prototyping of high-impact hero sections: the agent generates one 2x2 atlas, slices it into layers, removes backgrounds from overlay layers when needed, and assembles a scroll and mouse reactive parallax scene.

## Demo

Demo video:

`media/demo.mp4`

The included `boilerplate/` folder contains a working local prototype.

## What Is Included

- `.cursor/agents/paralaximus.md` - the Cursor subagent definition.
- `boilerplate/index.html` - local hero page.
- `boilerplate/style.css` - parallax styling, typography, z-index layering, theme colors.
- `boilerplate/script.js` - scroll and mouse parallax engine.
- `boilerplate/prepare_layers.py` - crops one 2K atlas into four layers.
- `boilerplate/assets/` - current demo assets.
- `media/demo.mp4` - demo video.

## Install In Cursor

1. Copy `.cursor/agents/paralaximus.md` into your project's `.cursor/agents/` folder.
2. Open a new Cursor chat, or reload Cursor if the agent does not appear.
3. Invoke it with:

```text
/paralaximus Create a parallax hero about Naruto in the local folder sloi-hero.
```

## Required MCP Tools

The workflow expects MCP tools equivalent to:

- `gpt-image-2` - generate one 2K 16:9 atlas.
- `recraft_remove_background` - remove backgrounds from cropped overlay layers if alpha is missing.

## Local Requirements

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Then run the prototype from `boilerplate/`:

```bash
python -m http.server 8123
```

Open:

```text
http://127.0.0.1:8123/index.html
```

## Atlas Layout

PARALAXIMUS uses a single 2K 16:9 image atlas split into a 2x2 grid:

- top-left: background
- top-right: distant overlay details
- bottom-left: foreground overlay
- bottom-right: main object or character

The generated layers become:

- `background.png`
- `far.png`
- `near.png`
- `mug.png`

## Design Principles

- One atlas, never four separate generations.
- Strong composition contract before image generation.
- Transparent overlay layers.
- No local DIY background removal.
- Foreground should add depth, not hide the main subject.
- Typography, colors, buttons, and motion should match the user's theme.
- Big title can sit behind the main subject for a 3D editorial effect.

## License

MIT
