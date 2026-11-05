---
name: ui-design
description: "Use when designing, redesigning, polishing, or reviewing a website or application UI; triggered by requests such as UI design, visual redesign, frontend polish, design system, responsive layout, animations, UI revamp, or web design inspiration research."
---

# UI Design Skill

Use this skill to make interfaces feel deliberate, usable, and specific to their product rather than generic. It applies to new screens, visual redesigns, component polish, responsive behavior, accessibility, and interaction design.

## Core Workflow

### 1. Inspect before designing

- Identify the framework, routing, styling system, component library, asset pipeline, and existing design tokens.
- Read the nearest page, layout, shared components, and styles before editing.
- Check existing routes and neighboring screens so the new work belongs to the product.
- Preserve established patterns in an existing product unless the request explicitly asks for a visual reset.
- State one local design hypothesis before editing, such as: "The page feels flat because hierarchy is expressed only through borders; stronger type scale and spacing should improve scanning."

### 2. Research design inspiration on the web

When the request asks for inspiration, references, or a more distinctive visual direction, use the available web search or page-fetch tools before implementing:

- Search for a small set of relevant references using the product domain and interface type, for example `editorial chess learning dashboard UI`, `premium education SaaS course workspace`, or `blue operations dashboard interaction design`.
- Prefer high-quality product pages, design-system documentation, award galleries, and real applications over generic template collections.
- Review three to five references, not dozens. Capture the useful pattern from each: typography scale, navigation model, spacing rhythm, color relationship, content density, table/card treatment, motion, and responsive behavior.
- Separate observations from implementation decisions. Create a short inspiration board in working notes such as: `Reference A: narrow rail + strong title`, `Reference B: warm accent on blue`, `Reference C: staggered list reveal`.
- Treat references as design research, not source material to copy. Do not reproduce a brand, logo, exact layout, distinctive illustration, proprietary copy, or near-identical component composition. Combine general patterns into an original direction suited to the current product.
- If a referenced page is inaccessible, blocked, or image-only, use its publicly visible principles as a loose signal and continue with accessible references. Do not claim to have inspected content that could not be fetched.
- Convert the research into a local design brief before coding: audience, desired feeling, three visual principles, palette, typography, layout model, and two or three motion ideas.

### 3. Define a visual direction

Choose a clear direction before writing CSS. Record the choices briefly:

- **Audience and task:** Who uses the screen, and what action should feel easiest?
- **Tone:** For example, quiet operations workspace, editorial learning studio, energetic game surface, or premium analytics tool.
- **Typography:** Use an expressive, purposeful font family that fits the product. Avoid default-only stacks such as Arial, Roboto, or Inter when a better local or web font is available.
- **Color:** Define semantic variables for background, surface, text, muted text, border, primary action, secondary action, focus, success, warning, and danger. Avoid a one-hue interface and avoid purple-on-white defaults unless the existing brand requires it.
- **Shape and depth:** Use a small, consistent radius scale and intentional borders/shadows. Do not put cards inside cards or turn every page section into a floating panel.
- **Motion:** Choose a few meaningful animations, such as page-load reveals, list staggering, hover lift, or a progress transition. Do not animate every element.

### 4. Design the information hierarchy

- Put the primary task in the first viewport.
- Use display-scale type only for true hero content. Use compact headings in dashboards, sidebars, tables, and tool panels.
- Prefer full-width bands and unframed layouts for page sections; reserve cards for repeated records, framed tools, and modal content.
- Make status, ownership, dates, and next actions scannable.
- Use familiar icons for icon-only actions and include tooltips or accessible labels for unfamiliar icons.
- Use segmented controls, tabs, toggles, menus, sliders, and steppers when they match the interaction instead of plain text links.

### 5. Implement responsively

- Design desktop and mobile states together.
- Use stable dimensions for boards, grids, tables, toolbars, counters, and icon buttons so content cannot shift the layout.
- Let long labels wrap or adapt instead of overflowing or overlapping.
- Collapse navigation and multi-column layouts intentionally at narrow widths.
- Keep tap targets comfortable and preserve keyboard focus visibility.
- Respect `prefers-reduced-motion` and provide a reduced-motion path for non-essential animation.

### 6. Build complete states

For every new flow, cover the states a real user will encounter:

- Loading and pending states
- Empty state with a useful next action
- Validation errors and inline field feedback
- Success and failure feedback
- Disabled, hover, focus, active, and selected states
- Long content, missing data, and permission-restricted views
- Mobile navigation and narrow viewport behavior

Do not use visible instructional prose to explain obvious controls. Let labels, hierarchy, icons, tooltips, and feedback communicate the interaction.

### 7. Implement and verify the result

Translate the design brief into the existing codebase rather than leaving inspiration as a moodboard:

- Add or update shared design tokens first, then implement the layout, components, content, and motion in that order.
- Reuse existing components when they already express the needed pattern; create a new component only when it removes real duplication or establishes a meaningful reusable pattern.
- Keep web-sourced assets within their usage rights. Prefer the repository's existing assets, open-licensed assets, generated assets, or CSS/HTML treatments when appropriate. Never scrape or hotlink a proprietary site's assets as a shortcut.
- Keep external font, icon, and image dependencies intentional. Confirm that they load in the target environment and provide a fallback.
- Run the narrowest available lint, typecheck, build, or test for the touched surface.
- Start the development server when the project requires one and provide the local URL.
- Inspect the rendered page at desktop and mobile widths when browser tools are available.
- Compare the implementation against the design brief, not against a copied reference. Check for horizontal overflow, clipped text, overlapping controls, unreadable contrast, broken images, missing focus states, and console errors.
- Confirm that new UI does not break existing routes or authentication/permission boundaries.
- If visual verification is unavailable, state that limitation instead of claiming the UI was visually checked.

### 8. Iterate after visual review

- Identify the most visible mismatch after the first implementation: hierarchy, density, contrast, alignment, motion, or responsive behavior.
- Make the smallest high-impact correction and recheck the same viewport and interaction.
- Stop when the design brief is satisfied and additional changes would be taste-only rather than improving usability or product fit.

## Existing Product Rules

When working in an existing application:

- Reuse its layout, tokens, form partials, icons, and component conventions where they are sound.
- Keep public APIs, routes, and server-side behavior stable unless the UI request requires a change.
- Prefer a small shared component or token update over duplicated one-off styles.
- Do not rewrite an entire CSS file to change one component.
- Keep content text concise, specific to the domain, and free of placeholder marketing language.

## New Product Rules

When building a page from scratch:

- Make the usable product surface the first screen; do not lead with a generic marketing hero unless explicitly requested.
- Establish tokens before component styling.
- Use real or generated visual assets when imagery is central to the product. Do not use decorative gradients or abstract blobs as the only visual content.
- Make the most important object, state, or action visible in the first viewport.
- Build the main workflow before secondary polish.

## Examples

### Example: Operations dashboard

Use a quiet, dense layout with a persistent staff sidebar, clear page title, KPI strip, searchable tables, status pills, and obvious create/edit actions. Use restrained motion on page entry and row hover. Avoid oversized hero text, decorative cards, and marketing copy.

### Example: Learning course page

Lead with the course promise, difficulty, progress, and next lesson. Keep lesson navigation stable, show locked versus available states clearly, and make the primary continuation action prominent. Use a progress transition and subtle section reveals, not constant animation.

### Example: Game or interactive tool

Keep the board or main interactive surface dominant and stable. Put controls close to the interaction, show loading/error states without shifting the board, and use animation to communicate moves or state changes. Verify touch behavior and reduced motion.

### Example: Existing CSS change

```css
:root {
	--color-bg: #f5f7fb;
	--color-surface: #ffffff;
	--color-ink: #17233b;
	--color-muted: #68758a;
	--color-primary: #235a96;
	--color-focus: #66aef2;
	--radius-sm: 10px;
	--shadow-panel: 0 16px 40px rgba(31, 76, 130, 0.1);
}

@media (prefers-reduced-motion: no-preference) {
	.reveal {
		animation: rise-in 420ms ease both;
	}
}
```

The variables establish a coherent system, while the media query keeps motion respectful for users who disable it.

## Output Expectations

When completing a UI task, report:

1. The visual direction and the main interaction improvements.
2. The files or components changed.
3. The responsive and accessibility considerations handled.
4. The validation performed, including the URL used for visual review when applicable.