# Chessflow Design Tokens & Visual Architecture
**Version**: 2.0 (Dual-Mode: Analytical Light & Nocturnal Grandmaster Dark)  
**System Designation**: `Chessflow Master Design Tokens`  
**Brand**: Chessflow Analytics Inc. — Precision Grandmaster Pedagogy & Computational Engine

---

## 1. Brand Identity & Design Rationale
Chessflow is an intellectual sanctuary engineered for master-level players, analytical aspirants, and titled coaches. The interface balances high-density data visualizations (engine telemetry, FEN notation, centipawn delta charts, Syzygy tablebase indicators) with calm, distraction-free typographic hierarchy.

---

## 2. Color System & Token Mapping

### 2.1 Core Brand & Accent Tokens
| Token | Hex (Light Mode) | Hex (Dark Mode) | Purpose / Semantic Role |
| :--- | :--- | :--- | :--- |
| `--color-primary` | `#0f172a` (Slate 900) | `#2563eb` (Royal Blue) | Primary brand accents, key action triggers, focused interactive states |
| `--color-primary-container` | `#1e293b` (Slate 800) | `#1d4ed8` (Deep Blue) | Hero action buttons, prominent CTAs |
| `--color-on-primary` | `#ffffff` | `#ffffff` | Foreground text/icons on primary containers |
| `--color-secondary` | `#0284c7` (Sky 600) | `#38bdf8` (Electric Cyan) | Stockfish engine telemetry, depth tags, active move highlights |
| `--color-secondary-container` | `#e0f2fe` (Sky 100) | `#0284c7` (Sky 600) | Engine status badges, active analysis chips |
| `--color-on-secondary` | `#0369a1` | `#082f49` | High-contrast text on secondary accent badges |

### 2.2 Neutral Surfaces & Backgrounds
| Token | Hex (Light Mode) | Hex (Dark Mode) | Usage Context |
| :--- | :--- | :--- | :--- |
| `--color-surface` | `#f8f9ff` / `#ffffff` | `#090d16` (Obsidian) | Global application background canvas |
| `--color-surface-dim` | `#cbdbf5` | `#060910` | Recessed areas, backdrop overlays, modal backdrops |
| `--color-surface-bright` | `#ffffff` | `#0f172a` | Elevated active panels, toolbars |
| `--color-surface-container-lowest` | `#ffffff` | `#080c14` | Recessed board trays, deep code blocks |
| `--color-surface-container-low` | `#eff4ff` | `#0f172a` | Card containers, list items |
| `--color-surface-container` | `#e5edfb` | `#131c2e` | Secondary cards, floating action drawers |
| `--color-surface-container-high` | `#dbe6f7` | `#1a263d` | Modals, elevated dialogs, popovers |
| `--color-surface-container-highest` | `#d0dff2` | `#22324f` | Active selections, highlighted table rows |

### 2.3 Typography & Text Contrast
| Token | Hex (Light Mode) | Hex (Dark Mode) | Hierarchy / Usage |
| :--- | :--- | :--- | :--- |
| `--color-on-surface` | `#0f172a` (Slate 900) | `#f1f5f9` (Slate 100) | Primary headers, article titles, critical metrics |
| `--color-on-surface-variant` | `#475569` (Slate 600) | `#94a3b8` (Slate 400) | Secondary body copy, subtitle annotations, timestamps |
| `--color-outline` | `#cbd5e1` (Slate 300) | `#334155` (Slate 700) | Card boundaries, chessboard frames, input borders |
| `--color-outline-variant` | `#e2e8f0` (Slate 200) | `#1e293b` (Slate 800) | Divider rules, table gridlines, notation delimiters |

### 2.4 Diagnostic & Chess Telemetry Palette
| Token | Hex | Usage in Engine Diagnostics |
| :--- | :--- | :--- |
| `--color-eval-advantage-white` | `#3b82f6` | White positive centipawn evaluation bar fill |
| `--color-eval-advantage-black` | `#0f172a` | Black territory balance on engine eval meter |
| `--color-diagnostic-brilliant` | `#06b6d4` | Brilliant moves (!!), pawn breakthrough sacrifices |
| `--color-diagnostic-success` | `#10b981` | Optimal moves, book theoretical perfection, mastered lines |
| `--color-diagnostic-warning` | `#f59e0b` | Inaccuracies (?!), dubious alternatives, spaced repetition due |
| `--color-diagnostic-danger` | `#f43f5e` | Blunders (??), tactical tripwires, tactical autopsies |

### 2.5 Chessboard Specific Tokens
| Token | Light Theme Value | Nocturnal Dark Value | Purpose |
| :--- | :--- | :--- | :--- |
| `--board-square-light` | `#f0d9b5` (Warm Cream) | `#273549` (Muted Slate Ivory) | Light chessboard squares |
| `--board-square-dark` | `#b58863` (Classic Walnut) | `#162032` (Deep Obsidian Blue) | Dark chessboard squares |
| `--board-square-highlight` | `rgba(59, 130, 246, 0.45)` | `rgba(56, 189, 248, 0.45)` | Active move source & destination |
| `--board-square-tripwire` | `rgba(244, 63, 94, 0.45)` | `rgba(244, 63, 94, 0.55)` | Engine blunder / trap visualization |

---

## 3. Typography Scale & Font Tokens

### 3.1 Font Families
- **Editorial / Serif (`--font-display`)**: `Newsreader`, `Charter`, `Georgia`, serif  
  *Application*: Page titles, hero value propositions, grandmaster quote callouts, monograph headings.
- **Interface / Sans (`--font-sans`)**: `Inter`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, Roboto, sans-serif  
  *Application*: General UI, buttons, table data, navigation links, filters, form fields.
- **Engine Telemetry / Monospace (`--font-mono`)**: `JetBrains Mono`, `Fira Code`, `Consolas`, monospace  
  *Application*: Move notation ledger (e.g. `14. Ndb5!`), FEN strings, Stockfish NNUE depth counters, ply depths, hash statistics.

### 3.2 Type Hierarchy
| Scale Name | Size | Line Height | Letter Spacing | Font Family | Default Weight |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `display-large` | `48px` (`3.0rem`) | `1.1` | `-0.025em` | Newsreader | 700 / Bold |
| `display-medium` | `36px` (`2.25rem`) | `1.15` | `-0.02em` | Newsreader | 700 / SemiBold |
| `display-small` | `28px` (`1.75rem`) | `1.2` | `-0.015em` | Newsreader | 600 / SemiBold |
| `title-large` | `22px` (`1.375rem`) | `1.3` | `-0.01em` | Newsreader / Inter | 600 / SemiBold |
| `title-medium` | `18px` (`1.125rem`) | `1.35` | `-0.005em` | Inter | 600 / Medium |
| `title-small` | `15px` (`0.9375rem`) | `1.4` | `0` | Inter | 600 / Medium |
| `body-large` | `16px` (`1.0rem`) | `1.55` | `0` | Inter | 400 / Regular |
| `body-medium` | `14px` (`0.875rem`) | `1.5` | `0` | Inter | 400 / Regular |
| `body-small` | `12px` (`0.75rem`) | `1.4` | `+0.01em` | Inter | 400 / Regular |
| `label-telemetry` | `12px` (`0.75rem`) | `1.25` | `+0.05em` | JetBrains Mono | 500 / Medium |
| `caption-mono` | `11px` (`0.6875rem`) | `1.2` | `+0.08em` | JetBrains Mono | 600 / Uppercase |

---

## 4. Spacing, Radii & Grid System

### 4.1 Spacing Scale (4px Base Grid)
| Token | Value | Common Usage |
| :--- | :--- | :--- |
| `--space-1` | `4px` | Fine badge margins, indicator pip offsets |
| `--space-2` | `8px` | Icon-to-label gaps, chip padding, pill spacing |
| `--space-3` | `12px` | Compact button padding, card header sub-gaps |
| `--space-4` | `16px` | Standard button padding, standard card gutters |
| `--space-6` | `24px` | Standard container padding, dashboard column gap |
| `--space-8` | `32px` | Section margins, large card padding |
| `--space-12` | `48px` | Major section breaks, hero inner vertical padding |
| `--space-16` | `64px` | Page section breaks |

### 4.2 Border Radius System
| Token | Value | Component Application |
| :--- | :--- | :--- |
| `--radius-sm` | `4px` | Mini badges, table cells, telemetry chips |
| `--radius-md` | `8px` | Buttons, text inputs, candidate move rows |
| `--radius-lg` | `12px` | Chessboard wrapper, sub-cards, drill preview cards |
| `--radius-xl` | `16px` | Primary dashboard containers, analysis cockpits |
| `--radius-full` | `9999px` | Round avatars, status badges, toggle switches |

### 4.3 Elevation & Shadow Tokens
- `--shadow-sm`: `0 1px 2px 0 rgba(0, 0, 0, 0.05)`
- `--shadow-md`: `0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)`
- `--shadow-lg`: `0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)`
- `--shadow-dark-elevated`: `0 8px 24px -4px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.05)` (Provides clean edge definition in dark mode)

---

## 5. Reusable Component Patterns

### 5.1 Global Navigation Header
- **Height**: `64px` (Desktop), `56px` (Mobile)
- **Structure**: Brand Emblem + Title ("Chessflow") | Center Navigation Links (Courses, Chess Lab, Play, Blog, Plans) | Right Actions (Search input, Dark/Light Mode Switcher, Engine Status Pip `Stockfish 16.1 NNUE Active`, Profile Avatar / Pro Tier badge)

### 5.2 Stockfish 16.1 Engine Status Pip
- **Default State**: Dot `8px` diameter (`#10b981`), Text `12px JetBrains Mono` (`Stockfish 16.1 NNUE (Active)` / `0.0ms ping`).
- **Processing State**: Pulse animation (`opacity: 0.4` to `1.0`), Sky Blue (`#38bdf8`).

### 5.3 Interactive Move Notation Ledger
- Two-column fixed tabular alignment for White & Black plies.
- Active ply indicator: Background `--color-surface-container-highest`, font-weight `600`, with evaluation glyph tags (`!`, `!!`, `?!`, `??`).

---

## 6. Implementation Code Snippet (CSS Variables)

```css
:root {
  /* Light Mode Default */
  --color-primary: #0f172a;
  --color-primary-container: #1e293b;
  --color-on-primary: #ffffff;
  --color-secondary: #0284c7;
  --color-secondary-container: #e0f2fe;
  --color-on-secondary: #0369a1;
  --color-surface: #f8f9ff;
  --color-surface-dim: #cbdbf5;
  --color-surface-bright: #ffffff;
  --color-surface-container: #e5edfb;
  --color-on-surface: #0f172a;
  --color-on-surface-variant: #475569;
  --color-outline: #cbd5e1;
  --color-outline-variant: #e2e8f0;
  
  /* Telemetry & Board */
  --board-square-light: #f0d9b5;
  --board-square-dark: #b58863;
  --color-eval-white: #3b82f6;
  --color-eval-black: #0f172a;
  --font-display: 'Newsreader', serif;
  --font-sans: 'Inter', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --radius-default: 8px;
}

.dark {
  /* Nocturnal Grandmaster Dark Mode */
  --color-primary: #2563eb;
  --color-primary-container: #1d4ed8;
  --color-on-primary: #ffffff;
  --color-secondary: #38bdf8;
  --color-secondary-container: #0284c7;
  --color-on-secondary: #082f49;
  --color-surface: #090d16;
  --color-surface-dim: #060910;
  --color-surface-bright: #0f172a;
  --color-surface-container: #131c2e;
  --color-on-surface: #f1f5f9;
  --color-on-surface-variant: #94a3b8;
  --color-outline: #334155;
  --color-outline-variant: #1e293b;
  
  /* Nocturnal Board */
  --board-square-light: #273549;
  --board-square-dark: #162032;
  --color-eval-white: #38bdf8;
  --color-eval-black: #080c14;
}
```
