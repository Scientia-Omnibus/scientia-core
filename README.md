# Usage

## Interface

The application has three main areas:

- **Omnibox** (top bar) — command input, works like a browser address bar.
- **Navigation** (side panel) — four tabs: Contents, Local, Bookmarks, History.
- **Viewer** (main area) — Markdown document viewer.

The side panel can be hidden/shown (`Ctrl+N`), tabs can be switched,
and it can be docked to the opposite side (`\`).

## Global shortcuts

| Key | Action |
| -- | -- |
| `/` or `:` | Focus the omnibox |
| `Escape` | Return to omnibox / clear omnibox / quit |
| `Ctrl+N` | Show/hide the navigation sidebar |
| `Ctrl+B` | Show bookmarks |
| `Ctrl+L` | Show local files |
| `Ctrl+T` | Show table of contents |
| `Ctrl+Y` | Show history |
| `Ctrl+Left` | Go backward in history |
| `Ctrl+Right` | Go forward in history |
| `Ctrl+D` | Bookmark the current document |
| `Ctrl+R` | Reload the current document |
| `Ctrl+Q` | Quit the application |
| `F1` | Help |
| `F2` | About |
| `F10` | Toggle dark/light theme |

## Navigation panel

| Key | Action |
| -- | -- |
| `,` / `a` / `h` / `Ctrl+Left` / `Shift+Left` | Previous tab |
| `.` / `d` / `l` / `Ctrl+Right` / `Shift+Right` | Next tab |
| `\` | Dock the panel left/right |

## Document viewer

When the viewer is focused:

| Key | Action |
| -- | -- |
| `w` / `k` | Scroll up |
| `s` / `j` | Scroll down |
| `Space` | Page down |
| `b` | Page up |

## Bookmarks

| Key | Action |
| -- | -- |
| `Delete` | Delete bookmark |
| `r` | Rename bookmark |

## History

| Key | Action |
| -- | -- |
| `Delete` | Delete history entry |
| `Backspace` | Clear all history |

## Commands

Press `/` or click the omnibox, then enter a command:

| Command | Aliases | Description |
| -- | -- | -- |
| `about` | `a` | Show information about the application |
| `bookmarks` | `b`, `bm` | Show the bookmarks list |
| `contents` | `c`, `toc` | Show the table of contents |
| `help` | `?` | Show this help |
| `history` | `h` | Show the history |
| `local` | `l` | Show local files |
| `quit` | `q` | Quit the application |

You can also type a path to a `.md` file to open it directly.
