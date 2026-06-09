---
name: Epicurean Modern
colors:
  surface: '#f9f9ff'
  surface-dim: '#d3daea'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f0f3ff'
  surface-container: '#e7eefe'
  surface-container-high: '#e2e8f8'
  surface-container-highest: '#dce2f3'
  on-surface: '#151c27'
  on-surface-variant: '#534434'
  inverse-surface: '#2a313d'
  inverse-on-surface: '#ebf1ff'
  outline: '#867461'
  outline-variant: '#d8c3ad'
  surface-tint: '#855300'
  primary: '#855300'
  on-primary: '#ffffff'
  primary-container: '#f59e0b'
  on-primary-container: '#613b00'
  inverse-primary: '#ffb95f'
  secondary: '#555f6f'
  on-secondary: '#ffffff'
  secondary-container: '#d6e0f3'
  on-secondary-container: '#596373'
  tertiary: '#a83639'
  on-tertiary: '#ffffff'
  tertiary-container: '#ff9290'
  on-tertiary-container: '#831a22'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffddb8'
  primary-fixed-dim: '#ffb95f'
  on-primary-fixed: '#2a1700'
  on-primary-fixed-variant: '#653e00'
  secondary-fixed: '#d9e3f6'
  secondary-fixed-dim: '#bdc7d9'
  on-secondary-fixed: '#121c2a'
  on-secondary-fixed-variant: '#3d4756'
  tertiary-fixed: '#ffdad8'
  tertiary-fixed-dim: '#ffb3b0'
  on-tertiary-fixed: '#410006'
  on-tertiary-fixed-variant: '#881d24'
  background: '#f9f9ff'
  on-background: '#151c27'
  surface-variant: '#dce2f3'
  surface-glass: rgba(255, 255, 255, 0.8)
  appetite-orange-light: '#FEF3C7'
  charcoal-muted: '#374151'
typography:
  display-lg:
    fontFamily: Montserrat
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Montserrat
    fontSize: 36px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-lg:
    fontFamily: Montserrat
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-md:
    fontFamily: Montserrat
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 1280px
  gutter: 1.5rem
  margin-mobile: 1rem
  margin-desktop: 2.5rem
  stack-sm: 0.5rem
  stack-md: 1rem
  stack-lg: 2rem
---

## Brand & Style

The brand identity for the design system is centered on "Epicurean Modernity"—a fusion of high-end culinary sophistication and cutting-edge digital performance. It targets a discerning audience that values both the artisanal quality of food and the frictionless efficiency of a premium tech platform.

The design style is a refined mix of **Minimalism** and **Glassmorphism**, leveraging heavy whitespace to let high-resolution food photography act as the primary visual driver. The aesthetic is "Next.js + Tailwind" ready, prioritizing clean lines, functional clarity, and subtle depth. It evokes an emotional response of hunger and trust, positioning the platform as a concierge-level service rather than just a utility.

Key visual pillars include:
- **Breathable Layouts:** Expansive margins and gutters to prevent cognitive overload.
- **Micro-interactions:** Smooth, purposeful transitions (inspired by Framer Motion) that provide tactile feedback.
- **Intentional Depth:** Using soft shadows and translucent layers to establish a clear spatial hierarchy.

## Colors

The palette is designed to be "appetizing yet professional." The **Primary Orange (#F59E0B)** is the "Action Color," used for critical paths like "Add to Cart" and "Place Order." It is vibrant enough to stimulate appetite while maintaining high legibility against white and dark backgrounds.

**Secondary Deep Charcoal (#1F2937)** provides the sophisticated "anchor." It is used for typography, navigation bars, and footer elements to ground the vibrant primary color. **Tertiary Coral/Red** is reserved for status-driven elements like "Hot Deals," live tracking icons, or heart/favorite interactions.

The design defaults to a **Light Mode** to maintain a fresh, "kitchen-clean" aesthetic, utilizing a neutral scale derived from cool grays to manage secondary information and borders.

## Typography

Typography follows a strict hierarchy to ensure readability during the fast-paced "discovery" phase of food ordering. 

**Montserrat** is used for all headlines and display text. Its geometric construction feels modern and confident. **Inter** is used for body copy and interface labels, chosen for its exceptional legibility at small sizes and its "system-native" feel which aligns with the Next.js architectural goals.

On mobile devices, headline sizes scale down to prevent awkward word wrapping, while body sizes remain constant (minimum 16px) to ensure touch targets and readability are preserved for users on the move.

## Layout & Spacing

The layout utilizes a **12-column fluid grid** for desktop and a **single-column fluid grid** for mobile. The system emphasizes a "Bento Box" approach for the home page, where different categories and promotions are housed in cards of varying column spans (e.g., 4-span for small promos, 8-span for hero features).

**Spacing Rhythm:**
- **Desktop:** 24px (1.5rem) gutters and 40px (2.5rem) outer margins.
- **Mobile:** 16px (1rem) outer margins with vertical stacking of all grid elements.
- **Vertical Rhythm:** Elements are spaced using a base-8 scale (8px, 16px, 32px, 64px) to ensure consistent "breathing room" between sections.

## Elevation & Depth

This design system eschews harsh lines in favor of **Tonal Layers** and **Ambient Shadows**. 

1.  **Level 0 (Surface):** The main background, using `#FFFFFF` or a very faint off-white.
2.  **Level 1 (Cards):** Low-opacity, extra-diffused shadows (`box-shadow: 0 10px 25px -5px rgba(31, 41, 55, 0.05)`). This creates a "lifted" feel without looking heavy.
3.  **Level 2 (Active/Hover):** Increased shadow spread and a subtle 1px border using the primary color at 10% opacity.
4.  **Level 3 (Modals/Cart Drawers):** Incorporates **Glassmorphism** with a `backdrop-filter: blur(12px)` and a semi-transparent white fill (`surface-glass`). This maintains the user's context of the food menu underneath.

## Shapes

The shape language is friendly and approachable, utilizing a **Rounded (2)** setting. 

In practice, this means primary interface components like buttons and inputs use a **0.5rem (8px)** radius, while larger structural components like product cards and category banners use the **2xl (1.5rem / 24px)** radius requested for the "premium" aesthetic. 

Search bars and promotional badges should use **Pill (full-round)** shapes to distinguish them as high-interaction or high-attention elements.

## Components

### Buttons
- **Primary:** Solid Orange (#F59E0B) with white text. 0.5rem radius. Subtle scale-down effect (98%) on click.
- **Secondary:** Deep Charcoal (#1F2937) with white text for high-contrast actions (e.g., "Checkout").
- **Ghost:** No background, primary color text. Used for "Cancel" or "View Details" to maintain hierarchy.

### Cards
- Product cards must feature a "2xl" (1.5rem) top border radius for images and a 1rem radius for the container. 
- Content within cards should have generous 1.5rem internal padding.

### Inputs
- Floating label pattern.
- 1px border in a muted neutral, shifting to a 2px primary orange border on focus.
- 0.5rem corner radius.

### Badges & Chips
- Use the primary orange or tertiary coral with 10% opacity backgrounds for "Tagging" (e.g., "Vegan," "Fast Delivery").
- Fully rounded (pill) shape for a modern, "app-like" feel.

### Lists & Navigation
- Navigation items in the header should use `label-md` typography with an animated orange underline on hover.
- Lists (like the order tracker) should use "Tonal Layers" to separate individual status steps.