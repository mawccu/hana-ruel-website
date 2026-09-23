# Hana Ruel Paintings: handoff for Claude Code

Read this whole file before changing anything. It describes the website exactly as it stands (version 3), how it was built, what the owner (Malek) likes and dislikes, and what's still fake.

---

## 1. What this is

A one-page online shop for a fictional independent painter, **Hana Ruel**, who sells original oil paintings on canvas from a studio in Lisbon. Malek asked for an "Awwwards-level" site with wild animations for "a girl who paints and sells canvases". It went through three designs (see section 9), and the current one is **version 3: an Apple-style design with real photos**.

- Live preview (private, owner's claude.ai account): https://claude.ai/artifact/FFH7C6rCbJWkLdXdmHidJ2
- Everything is in **one HTML file** (inline CSS and inline vanilla JS, no framework, no build step), plus 10 JPEGs in `img/`.

## 2. Files in this package

| Path | What it is |
|---|---|
| `index.html` | **Open this.** The full site as a normal standalone page (doctype, head, body). Double-click to open it in a browser. |
| `artifact-source.html` | The exact file published to claude.ai Artifacts. It has no `<html>/<head>/<body>` because the Artifact host wraps it. Keep the two in sync, or edit `index.html` and regenerate this one. |
| `img/` | The 10 photos the page uses (cropped and compressed). |
| `source-photos/` | The original Unsplash downloads (1400 px wide), used to regenerate `img/`. |
| `tools/crop_photos.py` | Regenerates `img/` from `source-photos/` (needs Pillow). |
| `HANDOFF.md` | This file. |
| `CHAT-LOG.md` | A condensed record of the conversation: every request and decision in order. |

**Run it:** open `index.html` in Chrome, Edge or Safari. It needs internet for Google Fonts only; everything else is local. Some browsers restrict `file://`, so if anything looks off, serve the folder with `python -m http.server 8000` and open http://localhost:8000.

## 3. Owner preferences (important)

- **Likes:** the animations and interactions ("I like the animation and the style"). Keep every interaction listed in section 6.
- **Disliked v1:** it looked "too AI-ish" (warm neutral ground, Young Serif, mono uppercase labels, split hero).
- **Disliked v2:** "a little bit too colorful" (the butter-yellow and ultramarine riso-print look).
- **Asked for in v3:** "APPLE DESIGN LEVEL", more creative layout, real canvas photos as products for now.
- Design rule going forward: the page chrome stays neutral and quiet, and **only the paintings carry colour**. Restraint, lots of space, precise type, smooth scroll storytelling.
- He wants to share inspiration screenshots (Awwwards etc.) later. Follow them when they arrive.

## 4. Design system (v3)

### Colour tokens (on `:root`, with dark-mode overrides)
| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` | `#FBFAF8` | `#0C0C0B` | page |
| `--bg-2` | `#F1EFEB` | `#1A1917` | tiles, collection section, footer, forms |
| `--bg-3` | `#E7E4DE` | `#262522` | floor, sofa fill, image placeholders |
| `--ink` | `#1D1C1A` | `#F4F2EE` | text, primary buttons |
| `--ink-2` | `#6F6B65` | `#A19D96` | secondary text |
| `--ink-3` | `#C9C5BE` | `#45423D` | unlit words in the scroll statement |
| `--line` | `rgba(29,28,26,.1)` | `rgba(255,255,255,.12)` | hairlines |
| `--link` | `#2F5D8C` | `#8DB6E0` | text links, focus rings (the only non-neutral UI colour) |
| `--dot` | `#D23A2A` | `#FF5C47` | gallery "sold" red dot |
| `--wall` | `#EAE7E1` | `#1F1E1B` | wall behind hung paintings |
| `--band` | `#0D0D0C` | `#000` | the dark "Try the brush" section and the signature tile |

Theme handling: light palette on bare `:root`; dark under `@media (prefers-color-scheme: dark)` guarded by `:root:not([data-theme="light"])`; repeated under `:root[data-theme="dark"]`.

### Type
- **Geist** (400/500/600/700) for everything: headings 600 weight with tight tracking (`-.03em` to `-.045em`).
- **Newsreader italic** (500) for painting titles only, like a gallery wall label.
- **Homemade Apple** for the handwritten signature only ("H. Ruel '26", "Hana").
- Google Fonts link: `family=Geist:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@1,6..72,400;1,6..72,500&family=Homemade+Apple`

### Shapes and depth
- Pills (`border-radius:999px`) for buttons, 28px radius for tiles, forms, modal and room.
- Paintings never get rounded corners. They get a realistic lift shadow: `--lift: 0 1px 1px rgba(0,0,0,.06), 0 22px 36px -16px rgba(20,16,10,.38)`.
- Glass nav: `backdrop-filter: saturate(180%) blur(20px)` over 74% `--bg`.
- Easing everywhere: `cubic-bezier(.22,.8,.22,1)`.

## 5. Page structure, top to bottom

1. **Nav** (sticky, glass, hides on scroll down and returns on scroll up): "Hana Ruel" logo, six section links (hidden under 760px), and a bag icon with a count badge.
2. **Hero** (`#hero`, centred): kicker "Autumn collection · 2026", h1 "Painted by hand. / One at a time." (second line in `--ink-2`, each line rises in from a mask on load), lead text with a live available count (`#availCount`), a "Shop the collection" pill and a "Commission a painting ›" link.
3. **Zoom-out reveal** (`#zoom`, 250vh tall with a sticky 100vh stage): the painting *Harbour, Early* starts scaled to fill the screen with "Every stroke, by hand." over it. As you scroll, it scales down to its real framed size on a softly lit wall, the overlay fades out, and a caption fades in (title, "Oil on linen · 90 × 90 cm · $1,450", Add to bag, Details).
4. **Statement** (`#statement`): a big paragraph whose words darken one by one from `--ink-3` to `--ink` as you scroll through it.
5. **The collection** (`#wall`, pinned horizontal gallery on desktop): vertical scroll drives the track sideways, with a progress bar and a slight skew based on scroll speed. Paintings are **hung to scale with each other** (px per cm = `K`) and **centred on a dashed 145 cm line**, the gallery convention. Each one has a wall label: italic title, "Oil on linen, year · H × W cm", then price and Add to bag, or a red dot, "Sold" and "Commission similar". Hovering tilts a painting in 3D and shows a "View" cursor bubble; clicking opens the detail sheet. Under 760px wide, or with reduced motion, it becomes a native swipe row with scroll snapping.
6. **Why an original** (`#closer`, bento grid of 6 columns):
   - A large tile with a **magnifier**: moving over the close-up photo (`img/loupe.jpg`) shows a 220px circle at 3× zoom (fine pointers only).
   - "1 of 1": no prints, no editions.
   - "3.8 cm": painted gallery-wrap edges, with a small CSS canvas-depth drawing.
   - "5–8 days": crated and insured, with chips for Portugal 2–3 days, EU 4–6 days, US & UK 5–8 days.
   - A dark tile, "Signed on the back.", with the handwritten signature.
7. **Try the brush** (`#brush`, full-bleed dark band): a real paint canvas (`#easel`, 16:10, 4:5 on phones).
   - It **paints itself** (a small abstract seascape) the first time it scrolls into view, then shows the hint "Your turn. Drag to paint."
   - Dragging paints bristle strokes. Paint load decreases with stroke length, so bristles drop out like a drying brush.
   - Glass toolbar: 7 muted pigments (Ultramarine #2B4A8B, Cerulean grey #9DB8CC, Yellow ochre #D6A546, Burnt orange #C4643A, Green earth #3F5E52, Titanium white #F2EEE4, Ivory black #2A2B2E), brushes Round 4 (9px), Filbert 8 (22px, the default) and Flat 14 (42px), and "Start over", which sweeps gesso strokes down the canvas.
   - Over the canvas, the cursor becomes a ring the size and colour of the current brush.
8. **Will it fit** (`#sizer`): a segmented control of the available paintings. The chosen one hangs **at true scale** on a 360 cm × 270 cm wall above a 210 cm sofa (SVG) next to a floor lamp, with a 1 m scale bar and "Ceiling 2.7 m". Hanging rule: centre at 145 cm, but the bottom edge is kept at least 18 cm above the 85 cm sofa back. The caption states the numbers. The default is *Weather Report*.
9. **Process** (`#process`): a sticky canvas on the left, with six steps on the right (Stretch, Prime, Wash and sketch, Block in, Layers and light, Varnish and sign). As each step reaches the middle of the screen, the canvas wipes to that stage of a generated seascape with a ragged brush edge. Each stage builds on the previous one. The last stage adds varnish sheen and the signature "H. Ruel '26".
10. **Studio**: a studio photo (`img/studio.jpg`), "Hi, I'm Hana." with two paragraphs and a handwritten "Hana".
11. **Commissions** (`#commission`): four rate cards (Small up to 40 cm from $320, about 3 weeks; Medium up to 80 cm from $680, 5 weeks; Large up to 120 cm from $1,450, 8 weeks; Oversized, quoted, 10+ weeks), then a form with name, email, size, room, colour-palette chips and notes. Submit is handled in JS and shows a summary message; **nothing is sent**.
12. **Footer**: Shop, Studio, Contact and "Studio letters" newsletter columns, plus fine print including "Placeholder product photos from Unsplash."
13. **Overlays**: bag drawer (right side, persisted in `localStorage` key `hr-cart`, subtotal, "Check out" shows "Checkout isn't connected yet"), detail sheet (painting on a lit wall, story, specs, price, add or remove), toast messages, and a custom cursor.

## 6. Interactions checklist (don't lose any)
- [ ] Hero line mask-rise on load, plus lead and buttons fading up
- [ ] Nav hides on scroll down, shows on scroll up
- [ ] Zoom-out reveal of the featured painting, with overlay text fading out and caption fading in
- [ ] Statement words lighting up with scroll
- [ ] Pinned horizontal collection with progress bar and velocity skew
- [ ] 3D tilt on painting hover, and the "View" cursor bubble
- [ ] Detail sheet opens on click (Escape closes it, focus returns)
- [ ] Bag: add/remove anywhere, badge bump animation, drawer, persistence, toasts
- [ ] 3× magnifier on the close-up tile
- [ ] Easel: autopaint on first view, bristle-brush painting with dry-out, pigment and brush selection, gesso "Start over", brush-sized cursor ring
- [ ] Will-it-fit painting swaps with animated size and position
- [ ] Process canvas stage wipes tied to scroll
- [ ] Scroll-driven `.reveal` fade-ups (CSS `animation-timeline: view()`, visible by default when unsupported)
- [ ] Everything respects `prefers-reduced-motion` (no pinning, no zoom, words all lit, instant stages)

## 7. How the JS is organised (inside the single `<script>`)
1. `WORKS`: product data (see section 8). The image path is `img/<id>.jpg`.
2. **Paint engine** (only used for the easel and the process canvas, not the products): `rng` (mulberry32, seeded), `parse/mix/vary` colour helpers, `curve` (wobbly polyline), `brush` (bristle stroke: a soft underlay plus N offset bristle lines with random alpha, width and dry-out), `rows` (fill a rectangle with horizontal strokes), `blob` (concentric ring strokes), `spiral`, `texture` (linen weave plus grain patterns, multiplied), `sheen`.
3. **Collection wall**: builds the `.work` elements; `layoutWall()` computes `K` (px per cm), `--frameH`, image sizes, pin distance and section height.
4. **Bag**: `toggleCart`, `renderCart`, `openLayer/closeLayer`, and a delegated click handler for `[data-add]`, `[data-remove]`, `[data-open]` and `[data-close]`.
5. **Detail sheet**: `openModal(id)`, `fillModalAction(id)`.
6. **Loupe**.
7. **Easel**: object `E`; `sizeEasel` (preserves pixels on resize), `begin`, `drag`, `autopaint` (IntersectionObserver trigger), pointer events using `offsetX/offsetY`, because the canvas can be transformed.
8. **Will it fit**: `hang(id)`.
9. **Process canvas**: `STAGES[0..5]` drawing functions on an 800×1000 offscreen canvas, cached cumulatively in `procStage(k)`; `drawProc` does the ragged wipe; an IntersectionObserver with rootMargin `-45% 0px -45% 0px` calls `setStage`.
10. **Forms**: commission and newsletter, validation and messages only.
11. **Statement** word splitting.
12. **One `requestAnimationFrame` loop**: nav hide, zoom scale (`S0` = cover scale, eased over the first 80% of scroll), statement lighting, pin translation and skew, cursor easing.

## 8. Products (`WORKS`)
Sizes are height × width in cm. Prices are USD.

| id | Title | H×W | Year | Price | Status | Unsplash photo |
|---|---|---|---|---|---|---|
| harbour-early | Harbour, Early | 90×90 | 2026 | $1,450 | available (featured in the zoom) | photo-1531489956451-20957fab52f2 |
| low-tide | Low Tide, Tuesday | 60×80 | 2026 | $680 | available | photo-1552312097-8ef75595e2a2 |
| blue-hour | Blue Hour Kitchen | 80×60 | 2026 | $920 | available | photo-1618331833071-ce81bd50d300 |
| weather-report | Weather Report | 100×75 | 2026 | $1,200 | available (sizer default, also the loupe photo) | photo-1541512416146-3cf58d6b27cc |
| salt | Salt | 70×70 | 2025 | $760 | **sold** | photo-1681235014294-588fea095706 |
| cascais | Summer in Cascais | 60×90 | 2026 | $980 | available | photo-1533208087231-c3618eab623c |
| fog-study | Fog Study No. 3 | 40×30 | 2026 | $340 | available | photo-1583591900414-7031eb309cb6 |
| yellow-room | The Yellow Room | 60×40 | 2025 | $520 | **sold** | photo-1787181876151-824ed8be7b1d |
| (studio photo) | n/a | n/a | n/a | n/a | n/a | photo-1785423613154-a3f078420790 ("Creative artist's studio…" by Clay Banks) |

Image URL pattern: `https://images.unsplash.com/<photo-id>?w=1400&q=80&fm=jpg`. All are free-licence Unsplash photos, **not** Unsplash+.

## 9. Version history (why it looks like this)
- **v1: "linen studio".** Raw-linen background, ultramarine accent, Young Serif, Hanken Grotesk and DM Mono, split hero with the paint-on easel, and paintings **generated procedurally on canvas** (no photos). Malek: "perfect, but a bit too AI-ish".
- **v2: "risograph print".** Butter-yellow paper, ultramarine ink text, fluorescent-pink misregistration shadows, Caprasimo and Reenie Beanie fonts, hard offset shadows, tilted marquee, postcard-style form. Malek: "a little bit too colorful".
- **v3 (current): "Apple-level".** Neutral palette, Geist, real Unsplash photos, zoom-out reveal, word-lighting statement, bento with magnifier, dark brush band. The procedural paint engine survives only for the easel and process canvas.

## 10. Placeholders and fake parts (to replace before going live)
- The artist's name, bio, address (Rua da Padaria 14, Lisbon), email, Instagram handle, prices, stories and sold states are **all invented**.
- Product and studio photos are **other photographers' Unsplash images**. Replace them with Hana's own photos: one straight-on, evenly lit shot per painting, cropped to its H×W ratio, plus a close-up for the magnifier. Update `WORKS` and rerun `tools/crop_photos.py` or crop manually.
- **Checkout, the commission form and the newsletter don't send anything.** Suggested next step: Stripe Payment Links or Shopify Buy Button for checkout, and Formspree or a small backend for the forms.
- Artifact hosting blocks external requests. If moving to a real host (Vercel, Netlify, GitHub Pages), the page works as-is; just deploy the folder.

## 11. Rules that were followed (keep them)
- Semantic HTML: every form control has an id and label, visible focus rings, `aria-pressed` on toggles, `aria-live` on messages.
- Reading content is visible at rest; animations start from a visible state or are scroll-bound. Nothing hides content behind an observer.
- The page never scrolls horizontally. Side gutter is `--gut: clamp(16px,4vw,48px)`; full-bleed sections use `.bleed` negative margins.
- `prefers-reduced-motion` is handled throughout.
- Copy is plain and specific ("Add to bag", "In your bag", "Checkout isn't connected yet. This is a preview of the shop.").
