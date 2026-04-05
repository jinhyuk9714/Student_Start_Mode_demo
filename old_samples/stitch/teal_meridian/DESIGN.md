# Design System Specification: The Fluid Financial Mentor

## 1. Overview & Creative North Star: "The Digital Sanctuary"
The financial landscape for foreigners in Korea is often perceived as a rigid, impenetrable wall of text and complex regulations. This design system seeks to dismantle that friction through **The Digital Sanctuary**—a creative north star that prioritizes breathing room, editorial elegance, and "The AI Slope."

We move beyond the "standard app" aesthetic by embracing **Organic Editorialism**. This means we reject the cluttered, grid-locked look of traditional banking apps in favor of high-fidelity whitespace and "The AI Slope"—a visual metaphor where rule-based financial data (static, structured) flows seamlessly into AI-driven guidance (fluid, ethereal, and character-led). The signature feel is achieved through tonal layering rather than harsh containment, making the user feel hosted rather than managed.

---

## 2. Color & Atmospheric Tones
We leverage the legacy of Hana Bank Teal (`#009B8D`) not as a mere accent, but as a stabilizing anchor within a sophisticated, multi-layered environment.

### The "No-Line" Rule
**Borders are a failure of hierarchy.** To maintain a premium, editorial feel, 1px solid borders are prohibited for sectioning. Boundaries must be defined solely through background shifts:
- Use `surface-container-low` (`#f3f4f5`) for secondary content blocks.
- Use `surface-container-highest` (`#e1e3e4`) to draw focus to primary interaction zones.

### Surface Hierarchy & Nesting
Treat the UI as a physical stack of fine paper.
- **Base Layer:** `surface` (`#f8f9fa`)
- **Interactive Layer:** `surface-container-lowest` (`#ffffff`) — Use this for cards to create a "lifted" effect against the base.
- **AI Slope Zone:** Utilize a `primary` to `primary-container` gradient (`#00685e` to `#008377`) to signify areas where 'Byulbeot' (the AI) is actively assisting.

### The Glass & Gradient Rule
Floating elements (modals, bottom sheets) must use **Glassmorphism**:
- **Background:** `surface` at 80% opacity.
- **Backdrop-blur:** 16px to 24px.
- **Benefit:** This allows the vibrant teal of the AI Slope to bleed through, softening the interface.

---

## 3. Typography: Editorial Authority
By utilizing **Pretendard** alongside the **Manrope** display face, we create a rhythmic hierarchy that feels both authoritative and approachable.

*   **Display (Manrope - 3.5rem / 56px):** Used for large numerical values or "Welcome" moments. This is the soul of the app.
*   **Headline (Manrope - 2rem / 32px):** Clear, bold statements that guide the user through financial tasks.
*   **Title (Plus Jakarta Sans - 1.125rem / 18px):** The primary navigational anchor for cards.
*   **Body (Plus Jakarta Sans - 0.875rem / 15px):** Optimized for readability with a generous 1.6x line-height to prevent information density fatigue.
*   **Label (Plus Jakarta Sans - 0.75rem / 12px):** Used for micro-copy and metadata.

**Note:** Always use `on-surface-variant` (`#3d4947`) for body text to reduce harsh contrast against the pure white cards, enhancing the "Sanctuary" feel.

---

## 4. Elevation & Depth: Tonal Layering
Traditional shadows are too "digital." We use **Ambient Depth**.

*   **The Layering Principle:** Instead of a shadow, place a `surface-container-lowest` (`#ffffff`) card on a `surface-container-low` (`#f3f4f5`) background. The 1% shift in value is enough for the human eye to perceive depth without visual noise.
*   **Ambient Shadows:** For floating CTAs, use a 32px blur with 4% opacity, tinted with the primary teal (`#006a60`).
*   **The Ghost Border:** If a divider is mandatory for accessibility, use `outline-variant` (`#bcc9c6`) at 15% opacity. Never use a 100% opaque border.

---

## 5. Components: The Signature Kit

### The "Byulbeot" AI Slope (Signature Component)
Unlike standard chat bubbles, AI guidance is housed in a container with a 24px radius (`xl`) and a subtle linear gradient. The 'Byulbeot' character should overlap the container edge, breaking the "box" to feel more integrated and friendly.

### Buttons: High-Fidelity Interaction
*   **Primary:** `primary` (`#00685e`) background with `on-primary` (`#ffffff`) text. Radius: 8px. Use a subtle inner-glow (top-down) to provide a tactile, premium feel.
*   **Secondary:** No background. Use a `surface-container-high` (`#e7e8e9`) fill only on hover/press.

### Cards: The Floating Sheet
*   **Radius:** 12px.
*   **Spacing:** 20px internal padding.
*   **Constraint:** No dividers. Separate sections within a card using a 12px vertical gap or a subtle change to `surface-container-low`.

### Input Fields: Minimalist Clarity
*   **State:** Default fields have no border; they are a solid fill of `surface-container-highest`.
*   **Focus State:** The field transitions to a `primary-fixed` (`#82f6e5`) background with a 2px bottom-accent of `primary`.

---

## 6. Do’s and Don’ts

### Do:
*   **Do** use asymmetrical layouts (e.g., a left-aligned headline with a right-aligned Byulbeot character) to create a custom, high-end feel.
*   **Do** embrace low information density. If a screen feels full, split it into two steps.
*   **Do** use the "Primary-Light" (`#E6F7F5`) as a background for success states to reinforce Hana Bank's brand identity.

### Don't:
*   **Don't** use 1px solid dividers to separate list items. Use 16px of whitespace instead.
*   **Don't** use pure black (`#000000`) for text. Use `on-surface` (`#191c1d`) to keep the interface soft.
*   **Don't** place "Byulbeot" in a standard square frame. The character must always feel "free-floating" or overlapping elements to signify its role as a guide.

---

## 7. Layout & Spacing Scale
*   **Screen Padding:** 20px (The "Gutter of Silence")
*   **Card Gap:** 12px
*   **Section Vertical Rhythm:** 32px / 48px / 64px
*   **Core Radius:** 12px (Cards), 8px (Buttons), 24px (AI Slope/Modals)