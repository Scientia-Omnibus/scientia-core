# scientia-core

Offline terminal knowledge reader. Download Markdown knowledge packs once, read without internet. Built with [Textual](https://textual.textualize.io/).

Ships under 10 MB. Runs on anything with a terminal — from a $5 Raspberry Pi to a 15-year-old netbook.

---

## Install

```bash
# via uv (recommended)
uv tool install scientia-core

# via pip
pip install scientia-core
```

Then run:

```bash
scientia-core
```

> For keybindings and commands, see **[USAGE.md](USAGE.md)**.

## Features

- **Fully offline** — download once, read anywhere, no network required
- **Keyboard-driven** — omnibox (`/` or `:`), tab navigation, commands
- **4 navigation tabs** — Contents, Local Files, Bookmarks, History
- **Fuzzy search** across all document titles in your knowledge pack
- **GitHub sync** — pull knowledge base updates with `Ctrl+G`
- **Dark / light themes** — toggle with `F10`

## Tech

- Python 3.12+, [Textual](https://textual.textualize.io/) TUI framework
- [rapidfuzz](https://github.com/maxbachmann/RapidFuzz) for fuzzy matching
- [GitPython](https://github.com/gitpython-developers/GitPython) for sync

## TODO

- [ ] BM25 full-text search across document contents
- [x] Auto-update mechanism
- [ ] Standalone Windows package (`.exe`)
- [ ] Linux AppImage build
- [ ] More knowledge pack sources

## License

MIT
