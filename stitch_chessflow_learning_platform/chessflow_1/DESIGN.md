---
name: Chessflow
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#45464d'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#76777d'
  outline-variant: '#c6c6cd'
  surface-tint: '#565e74'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#131b2e'
  on-primary-container: '#7c839b'
  inverse-primary: '#bec6e0'
  secondary: '#0051d5'
  on-secondary: '#ffffff'
  secondary-container: '#316bf3'
  on-secondary-container: '#fefcff'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#2f1500'
  on-tertiary-container: '#c76c00'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2fd'
  primary-fixed-dim: '#bec6e0'
  on-primary-fixed: '#131b2e'
  on-primary-fixed-variant: '#3f465c'
  secondary-fixed: '#dbe1ff'
  secondary-fixed-dim: '#b4c5ff'
  on-secondary-fixed: '#00174b'
  on-secondary-fixed-variant: '#003ea8'
  tertiary-fixed: '#ffdcc3'
  tertiary-fixed-dim: '#ffb77d'
  on-tertiary-fixed: '#2f1500'
  on-tertiary-fixed-variant: '#6e3900'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Newsreader
    fontSize: 48px
    fontWeight: '500'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Newsreader
    fontSize: 36px
    fontWeight: '500'
    lineHeight: 44px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Newsreader
    fontSize: 32px
    fontWeight: '500'
    lineHeight: 40px
    letterSpacing: -0.015em
  headline-lg-mobile:
    fontFamily: Newsreader
    fontSize: 26px
    fontWeight: '500'
    lineHeight: 34px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Newsreader
    fontSize: 24px
    fontWeight: '500'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
    letterSpacing: -0.005em
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
    letterSpacing: 0em
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
    letterSpacing: 0em
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0.005em
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.04em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 2.5rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style
The design system crafts an intellectually serene, deeply focused, and contemporary digital sanctuary for grandmaster-level study and amateur progression alike. It departs from the tired skeuomorphic wood-grain tropes and chaotic gamified aesthetics of legacy chess software, adopting a philosophy of **Scholarly Modernism**—a synthesis of high-modernist editorial structure, technical SaaS precision, and quiet tactile depth.

### Target Audience & Emotional Intent
- **Audience:** Serious learners, ambitious tournament competitors, analytical thinkers, and aesthetics-conscious chess enthusiasts seeking clarity over sensory overload.
- **Atmosphere:** Deeply calm, undistracted, authoritative, and sharp. The interface feels like an architect-designed private study illuminated by natural morning light—instilling cognitive focus, strategic patience, and intellectual momentum.

### Core Visual Principles
- **Atmospheric Restraint:** Heavy whitespace, balanced density ratios, and strict hierarchy eliminate analytical fatigue.
- **Architectural Precision:** Razor-thin structural borders and deliberate grid alignments mimic the Cartesian geometry of the 64-square board.
- **Strategic Illumination:** Color is reserved for state changes, tactical clarity (blunders, brilliancies, forks), and cognitive progression, never purely decorative noise.

## Colors
The palette leverages a high-contrast, cerebral light baseline engineered to support extended study sessions without eyestrain, using crisp structural slates and clean surface depths.

### Hierarchy & Application
- **Primary (`#0F172A`):** Deep Scholarly Navy. Deployed for high-emphasis typography, critical structural chrome, primary navigational anchors, and dark-square piece definitions.
- **Secondary (`#2563EB`):** Vibrant Cobalt. Represents machine intelligence, engine analysis paths, active turn rings, primary action states, and interactive movement vectors.
- **Tertiary (`#D97706`):** Warm Amber. Reserved strictly for tactical alerts, brilliant move notations, streak multipliers, evaluation swing warnings, and premium status markers.
- **Neutral (`#64748B`):** Slate. Forms the secondary text layer, algebraic move coordinates, evaluation gauges, and inactive icons.
- **Surfaces & Borders:** Base canvas sits at clean light atmospheric tones, stepping to elevated modular cards and active engine feedback panes. Structural divisions use subtle hairline tones.

## Typography
The typographic architecture juxtaposes the editorial, classical heritage of the game with cutting-edge analytical software usability.

### Pairing Logic
- **Headlines & Editorial Marks (Newsreader):** A refined, literary serif that gives grandmaster game studies, masterclass theory modules, and high-level headings an enduring, scholarly prestige. It evokes the feel of high-end chess monographs and tournament journals.
- **Interface, Notation, & Body (Plus Jakarta Sans):** A geometric, modern sans-serif tuned for legibility. Its clean apertures ensure rapid reading of PGN move records (`1. e4 e5 2. Nf3 Nc6`), engine depths, centipawn evaluations, and analysis logs.

### Application Notes
- Move listings and engine telemetry use tabular numerals (`tnum`) to eliminate micro-jittering during live analysis calculations.
- Display sizes utilize slight negative tracking to balance Newsreader's natural stroke contrast.

## Layout & Spacing
The layout relies on a rationalized, modular multi-pane architecture inspired by dedicated analysis consoles.

### Spatial System
- **12-Column Responsive Grid:** Centers workspace layouts on desktop, collapsing to an asymmetric 3-column analysis cockpit (Navigation / Board / Move Log & Engine) at wide screens (>1280px).
- **Breakpoint Framework:**
  - *Desktop (≥1280px):* Fixed aspect-ratio board workspace anchored centrally or left-aligned, accompanied by persistent multi-tab notation panes. Margin: `2.5rem`, Gutter: `1.5rem`.
  - *Tablet (768px - 1279px):* Stacked 2-column or master-detail layout where the board commands the viewport top half, and notation/clocks flex beneath. Margin: `1.5rem`, Gutter: `1rem`.
  - *Mobile (<768px):* 1-column vertically flowing stack. The chessboard automatically pins edge-to-edge with a preserved safe margin (`1rem`), and control drawers expand upwards via bottom sheets.

### Rhythm
Component internals follow a disciplined 4px/8px modular base scale. Whitespace around analytical content is deliberate and uncrowded to optimize positional pattern recognition.

## Elevation & Depth
Elevation avoids noisy, muddy dropshadows in favor of crisp architectural separation, subtle tonal stacking, and luminous micro-depth adapted for a light-mode environment.

### Depth Hierarchy
1. **Level 0 (Base Canvas):** Flat light surfaces. The quiet desk upon which cards, boards, and tools rest.
2. **Level 1 (Structural Panels & Move Logs):** Elevated light surfaces bounded by precise hairlines. Zero shadow, creating quiet, paper-like organization.
3. **Level 2 (Interactive Cards & Floating Toolbars):** Elevated slightly with a subtle ambient shadow and tonal contrast.
4. **Level 3 (Tactile Chessboard & Lifted Pieces):** Chessboard frame features a clean inset hairline boundary with an external lift. Lifted pieces during drag-and-drop operations trigger a sharp drop shadow accompanied by a subtle scale transform (`1.08`) to deliver physical tactility.
5. **Level 4 (Modals & Overlays):** Deep translucent backdrops softened with `backdrop-filter: blur(8px)`, overlaid with focused dialogue panes.

## Shapes
A disciplined, soft geometry (`roundedness: 1`) preserves structural rigor. Because the primary subject of the platform is an 8x8 orthogonal square matrix, excessively bubbly or pill-shaped containers introduce visual dissonance.

### Shape Scale
- **Micro Elements (Tags, Badges, Coordinates):** `0.25rem` (`rounded-sm`) for an exact, tailored stamp look.
- **Interactive Elements (Buttons, Inputs, Evaluation Gauges):** `0.25rem` to `0.375rem` (`rounded`), echoing the crisp profiles of chiselled luxury chess pieces.
- **Structural Containers (Cards, Analysis Windows, Board Frame):** `0.5rem` (`rounded-lg`), softening terminal corners without compromising modular docking.
- **Chess Squares:** Strictly square (`0px` border radius) within the inner boundary to maintain mathematical clarity during piece navigation and square highlighting.

## Components

### Buttons
- **Primary:** Deep navy fill (`#0F172A`) with crisp white label (`#FFFFFF`). On hover, transitions with micro-lift.
- **Secondary (Engine/Action):** Vibrant cobalt (`#2563EB`) with white text. Reserved for primary operational steps ("Analyze Game", "Find Best Move").
- **Subtle/Ghost:** Transparent fill, hover states with border transitions.
- **Tactical (Alert/Retry):** Amber tint with deep amber text, shifting to solid amber on active states.

### Chips & Tactical Badges
- **PGN Classification Tags:** Ultra-compact, uppercase `label-sm`.
  - *Brilliant:* Soft cyan/cobalt tint.
  - *Blunder / Inaccuracy:* Warm rose/amber indicator chips designed with high textual clarity.
  - *Book Move:* Muted slate.

### Lists & Notation Trees
- Move history behaves like an interactive typographic ledger.
- Split-column layout (White / Black) with active move indicated by an asymmetric left-border accent and soft background fill.
- Monospaced move numbers in neutral slate.

### Chessboard & Squares
- **Light Squares:** Crisp off-white / light tones.
- **Dark Squares:** Muted, desaturated slate-tinted navy providing comfortable piece silhouette contrast.
- **Move Destinations & Targets:** Radial destination dots and soft cobalt corner accents for capture targets.
- **Last Move Highlights:** Subtle translucent yellow-amber wash, preventing visual vibration with board squares.

### Evaluation Bar (Eval Gauge)
- Slim vertical or horizontal indicator with hairline divisions. White advantage rendered in `#FFFFFF`, Black in `#0F172A`.
- Dynamic numeric readouts centered and rendered in high-legibility tabular figures (`+1.4`, `-0.8`, `M3`).

### Input Fields
- Single-line inputs and FEN/PGN importers feature a clean light background, a 1px slate border, and `space-sm` vertical padding.
- Focused state eliminates generic glow rings, replacing them with a definitive 1.5px `#2563EB` hairline perimeter.

### Cards & Study Modules
- Clean, structured cards with hairline outlines.
- Header structures utilize Newsreader for module titles paired with micro metadata tags in Plus Jakarta Sans.