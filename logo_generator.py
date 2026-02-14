import os

# Fix for loading Cairo DLLs on Windows with Python 3.8+
if os.name == 'nt':
    os.add_dll_directory(os.getcwd())

import gizeh
import random
import numpy as np
import json
import math
from datetime import datetime
from itertools import combinations


class ColorPalette:
    """Advanced color palette generator with harmony rules."""

    HARMONY_RULES = {
        "complementary": lambda h: [(h + 0.5) % 1.0],
        "triadic": lambda h: [(h + 1/3) % 1.0, (h + 2/3) % 1.0],
        "analogous": lambda h: [(h + 1/12) % 1.0, (h - 1/12) % 1.0],
        "split_complementary": lambda h: [(h + 5/12) % 1.0, (h + 7/12) % 1.0],
        "tetradic": lambda h: [(h + 0.25) % 1.0, (h + 0.5) % 1.0, (h + 0.75) % 1.0],
        "monochromatic": lambda h: [h],
    }

    PRESET_PALETTES = {
        "sunset": [(0.98, 0.4, 0.2), (0.95, 0.6, 0.1), (0.85, 0.2, 0.3), (0.4, 0.1, 0.3)],
        "ocean": [(0.0, 0.3, 0.6), (0.1, 0.5, 0.8), (0.2, 0.7, 0.9), (0.0, 0.2, 0.4)],
        "forest": [(0.1, 0.4, 0.1), (0.2, 0.6, 0.2), (0.4, 0.7, 0.3), (0.05, 0.3, 0.05)],
        "neon": [(1.0, 0.0, 0.5), (0.0, 1.0, 0.8), (0.5, 0.0, 1.0), (1.0, 1.0, 0.0)],
        "pastel": [(0.9, 0.7, 0.7), (0.7, 0.9, 0.7), (0.7, 0.7, 0.9), (0.9, 0.9, 0.7)],
        "corporate": [(0.1, 0.2, 0.5), (0.2, 0.4, 0.7), (0.8, 0.8, 0.85), (0.95, 0.95, 0.95)],
        "retro": [(0.9, 0.5, 0.2), (0.7, 0.3, 0.3), (0.3, 0.5, 0.5), (0.9, 0.8, 0.6)],
        "dark_elegance": [(0.1, 0.1, 0.15), (0.8, 0.7, 0.4), (0.3, 0.25, 0.3), (0.6, 0.5, 0.3)],
    }

    @staticmethod
    def hsv_to_rgb(h, s, v):
        """Convert HSV to RGB color space."""
        i = int(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        i %= 6
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        return (v, p, q)

    @classmethod
    def generate_harmonious(cls, base_hue=None, rule="triadic", saturation=0.7, value=0.85):
        """Generate harmonious color palette."""
        if base_hue is None:
            base_hue = random.random()

        harmony_func = cls.HARMONY_RULES.get(rule, cls.HARMONY_RULES["triadic"])
        hues = [base_hue] + harmony_func(base_hue)

        colors = []
        for h in hues:
            s = saturation + random.uniform(-0.1, 0.1)
            v = value + random.uniform(-0.1, 0.1)
            colors.append(cls.hsv_to_rgb(h, max(0, min(1, s)), max(0, min(1, v))))

        return colors

    @classmethod
    def get_preset(cls, name):
        """Get a preset color palette."""
        return cls.PRESET_PALETTES.get(name, cls.PRESET_PALETTES["corporate"])

    @staticmethod
    def generate_gradient_colors(color1, color2, steps=10):
        """Generate gradient color steps between two colors."""
        return [
            tuple(c1 + (c2 - c1) * t for c1, c2 in zip(color1, color2))
            for t in np.linspace(0, 1, steps)
        ]

    @staticmethod
    def adjust_brightness(color, factor):
        """Adjust brightness of a color."""
        return tuple(min(1.0, max(0.0, c * factor)) for c in color)

    @staticmethod
    def adjust_opacity(color, alpha):
        """Return color with alpha channel."""
        return (*color[:3], alpha)


class PatternGenerator:
    """Generate background patterns and textures."""

    @staticmethod
    def draw_dots(surface, width, height, color, spacing=20, radius=2):
        """Draw dot pattern."""
        for x in range(0, width + spacing, spacing):
            for y in range(0, height + spacing, spacing):
                dot = gizeh.circle(r=radius, xy=(x, y), fill=color)
                dot.draw(surface)

    @staticmethod
    def draw_lines(surface, width, height, color, spacing=15, stroke_width=1, angle=45):
        """Draw line pattern at specified angle."""
        rad = math.radians(angle)
        length = max(width, height) * 2

        for offset in range(-length, length, spacing):
            x1 = offset
            y1 = 0
            x2 = offset + length * math.cos(rad)
            y2 = length * math.sin(rad)
            line = gizeh.polyline(
                points=[(x1, y1), (x2, y2)],
                stroke=color,
                stroke_width=stroke_width
            )
            line.draw(surface)

    @staticmethod
    def draw_grid(surface, width, height, color, spacing=25, stroke_width=0.5):
        """Draw grid pattern."""
        for x in range(0, width + spacing, spacing):
            line = gizeh.polyline(
                points=[(x, 0), (x, height)],
                stroke=color,
                stroke_width=stroke_width
            )
            line.draw(surface)
        for y in range(0, height + spacing, spacing):
            line = gizeh.polyline(
                points=[(0, y), (width, y)],
                stroke=color,
                stroke_width=stroke_width
            )
            line.draw(surface)

    @staticmethod
    def draw_concentric_circles(surface, cx, cy, max_radius, color, count=8, stroke_width=1):
        """Draw concentric circles pattern."""
        for i in range(1, count + 1):
            r = max_radius * i / count
            circle = gizeh.circle(
                r=r, xy=(cx, cy),
                stroke=color,
                stroke_width=stroke_width
            )
            circle.draw(surface)

    @staticmethod
    def draw_hexagon_pattern(surface, width, height, color, size=20, stroke_width=0.5):
        """Draw hexagonal pattern."""
        hex_height = size * math.sqrt(3)
        for row in range(-1, int(height / hex_height) + 2):
            for col in range(-1, int(width / (size * 1.5)) + 2):
                cx = col * size * 1.5
                cy = row * hex_height + (col % 2) * hex_height / 2
                points = [
                    (cx + size * math.cos(math.radians(60 * i)),
                     cy + size * math.sin(math.radians(60 * i)))
                    for i in range(6)
                ]
                hex_shape = gizeh.polyline(
                    points=points + [points[0]],
                    stroke=color,
                    stroke_width=stroke_width
                )
                hex_shape.draw(surface)

    @staticmethod
    def draw_wave_pattern(surface, width, height, color, amplitude=10, frequency=0.05, stroke_width=1):
        """Draw wave pattern."""
        for y_offset in range(0, height + 40, 20):
            points = []
            for x in range(0, width + 5, 5):
                y = y_offset + amplitude * math.sin(frequency * x * 2 * math.pi)
                points.append((x, y))
            if len(points) > 1:
                wave = gizeh.polyline(
                    points=points,
                    stroke=color,
                    stroke_width=stroke_width
                )
                wave.draw(surface)


class ShapeFactory:
    """Advanced shape creation with effects and transformations."""

    @staticmethod
    def create_polygon(sides, radius, xy, fill=None, stroke=None, stroke_width=0, rotation=0):
        """Create a regular polygon with any number of sides."""
        points = [
            (radius * math.cos(2 * math.pi * i / sides + rotation),
             radius * math.sin(2 * math.pi * i / sides + rotation))
            for i in range(sides)
        ]
        return gizeh.polyline(
            points=points + [points[0]],
            xy=xy,
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            close_path=True
        )

    @staticmethod
    def create_star(points_count, outer_radius, inner_radius, xy, fill=None, stroke=None, stroke_width=0, rotation=0):
        """Create a star shape."""
        points = []
        for i in range(points_count * 2):
            angle = math.pi * i / points_count + rotation - math.pi / 2
            r = outer_radius if i % 2 == 0 else inner_radius
            points.append((r * math.cos(angle), r * math.sin(angle)))
        return gizeh.polyline(
            points=points + [points[0]],
            xy=xy,
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            close_path=True
        )

    @staticmethod
    def create_rounded_rectangle(w, h, corner_radius, xy, fill=None, stroke=None, stroke_width=0):
        """Create a rounded rectangle using arc approximation."""
        # Approximate with a regular rectangle for gizeh compatibility
        rect = gizeh.rectangle(lx=w, ly=h, xy=xy, fill=fill, stroke=stroke, stroke_width=stroke_width)
        return rect

    @staticmethod
    def create_ring(outer_r, inner_r, xy, fill=None, stroke=None, stroke_width=2):
        """Create a ring (donut) shape."""
        elements = []
        if fill:
            outer = gizeh.circle(r=outer_r, xy=xy, fill=fill)
            elements.append(outer)
        if stroke:
            outer_stroke = gizeh.circle(r=outer_r, xy=xy, stroke=stroke, stroke_width=stroke_width)
            inner_stroke = gizeh.circle(r=inner_r, xy=xy, stroke=stroke, stroke_width=stroke_width)
            elements.extend([outer_stroke, inner_stroke])
        return elements

    @staticmethod
    def create_spiral(center, max_radius, turns, xy, stroke=(0, 0, 0), stroke_width=2):
        """Create a spiral shape."""
        points = []
        steps = int(turns * 100)
        for i in range(steps):
            t = i / steps
            angle = turns * 2 * math.pi * t
            r = max_radius * t
            x = center[0] + r * math.cos(angle)
            y = center[1] + r * math.sin(angle)
            points.append((x, y))
        if len(points) > 1:
            return gizeh.polyline(points=points, xy=xy, stroke=stroke, stroke_width=stroke_width)
        return None

    @staticmethod
    def create_diamond(size, xy, fill=None, stroke=None, stroke_width=0):
        """Create a diamond shape."""
        points = [
            (0, -size),
            (size * 0.6, 0),
            (0, size),
            (-size * 0.6, 0)
        ]
        return gizeh.polyline(
            points=points + [points[0]],
            xy=xy,
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            close_path=True
        )

    @staticmethod
    def create_cross(size, thickness, xy, fill=None, stroke=None, stroke_width=0):
        """Create a cross/plus shape."""
        half = thickness / 2
        points = [
            (-half, -size), (half, -size), (half, -half),
            (size, -half), (size, half), (half, half),
            (half, size), (-half, size), (-half, half),
            (-size, half), (-size, -half), (-half, -half)
        ]
        return gizeh.polyline(
            points=points + [points[0]],
            xy=xy,
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            close_path=True
        )

    @staticmethod
    def create_arrow(size, xy, direction="right", fill=None, stroke=None, stroke_width=0):
        """Create an arrow shape."""
        if direction == "right":
            points = [
                (-size, -size * 0.3), (size * 0.3, -size * 0.3),
                (size * 0.3, -size * 0.6), (size, 0),
                (size * 0.3, size * 0.6), (size * 0.3, size * 0.3),
                (-size, size * 0.3)
            ]
        elif direction == "up":
            points = [
                (-size * 0.3, size), (-size * 0.3, -size * 0.3),
                (-size * 0.6, -size * 0.3), (0, -size),
                (size * 0.6, -size * 0.3), (size * 0.3, -size * 0.3),
                (size * 0.3, size)
            ]
        else:
            points = [
                (-size, -size * 0.3), (size * 0.3, -size * 0.3),
                (size * 0.3, -size * 0.6), (size, 0),
                (size * 0.3, size * 0.6), (size * 0.3, size * 0.3),
                (-size, size * 0.3)
            ]
        return gizeh.polyline(
            points=points + [points[0]],
            xy=xy,
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            close_path=True
        )


class TextRenderer:
    """Advanced text rendering with effects."""

    @staticmethod
    def render_text(surface, text, xy, fontsize=36, fontfamily="Arial",
                    fill=(0, 0, 0), angle=0, font_weight="normal"):
        """Render basic text."""
        text_elem = gizeh.text(
            text, fontfamily=fontfamily, fontsize=fontsize,
            xy=xy, fill=fill, angle=angle, fontweight=font_weight
        )
        text_elem.draw(surface)

    @staticmethod
    def render_text_with_shadow(surface, text, xy, fontsize=36, fontfamily="Arial",
                                 fill=(1, 1, 1), shadow_color=(0, 0, 0),
                                 shadow_offset=(3, 3), angle=0):
        """Render text with shadow effect."""
        shadow_xy = (xy[0] + shadow_offset[0], xy[1] + shadow_offset[1])
        shadow = gizeh.text(
            text, fontfamily=fontfamily, fontsize=fontsize,
            xy=shadow_xy, fill=shadow_color, angle=angle
        )
        shadow.draw(surface)

        main_text = gizeh.text(
            text, fontfamily=fontfamily, fontsize=fontsize,
            xy=xy, fill=fill, angle=angle
        )
        main_text.draw(surface)

    @staticmethod
    def render_text_with_outline(surface, text, xy, fontsize=36, fontfamily="Arial",
                                  fill=(1, 1, 1), outline_color=(0, 0, 0),
                                  outline_width=2, angle=0):
        """Render text with outline effect."""
        offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in offsets:
            for mult in range(1, outline_width + 1):
                outline_xy = (xy[0] + dx * mult, xy[1] + dy * mult)
                outline = gizeh.text(
                    text, fontfamily=fontfamily, fontsize=fontsize,
                    xy=outline_xy, fill=outline_color, angle=angle
                )
                outline.draw(surface)

        main_text = gizeh.text(
            text, fontfamily=fontfamily, fontsize=fontsize,
            xy=xy, fill=fill, angle=angle
        )
        main_text.draw(surface)

    @staticmethod
    def render_curved_text(surface, text, center_xy, radius, start_angle=0,
                           fontsize=24, fontfamily="Arial", fill=(0, 0, 0)):
        """Render text along a curve."""
        total_angle = len(text) * fontsize * 0.6 / radius
        current_angle = start_angle - total_angle / 2

        for char in text:
            char_angle = current_angle
            x = center_xy[0] + radius * math.cos(char_angle)
            y = center_xy[1] + radius * math.sin(char_angle)

            char_elem = gizeh.text(
                char, fontfamily=fontfamily, fontsize=fontsize,
                xy=(x, y), fill=fill, angle=char_angle + math.pi / 2
            )
            char_elem.draw(surface)
            current_angle += fontsize * 0.6 / radius

    @staticmethod
    def render_multi_line(surface, lines, start_xy, fontsize=24, fontfamily="Arial",
                          fill=(0, 0, 0), line_spacing=1.4, align="center"):
        """Render multi-line text."""
        for i, line in enumerate(lines):
            y = start_xy[1] + i * fontsize * line_spacing
            text_elem = gizeh.text(
                line, fontfamily=fontfamily, fontsize=fontsize,
                xy=(start_xy[0], y), fill=fill
            )
            text_elem.draw(surface)


class EffectsEngine:
    """Visual effects engine for logo enhancement."""

    @staticmethod
    def draw_gradient_circle(surface, center, max_radius, color1, color2, steps=30):
        """Draw a gradient-filled circle."""
        for i in range(steps, 0, -1):
            t = i / steps
            r = max_radius * t
            color = tuple(c1 + (c2 - c1) * (1 - t) for c1, c2 in zip(color1, color2))
            circle = gizeh.circle(r=r, xy=center, fill=color)
            circle.draw(surface)

    @staticmethod
    def draw_gradient_background(surface, width, height, color1, color2, direction="vertical", steps=50):
        """Draw a gradient background."""
        for i in range(steps):
            t = i / steps
            color = tuple(c1 + (c2 - c1) * t for c1, c2 in zip(color1, color2))

            if direction == "vertical":
                y = height * t
                h = height / steps + 1
                rect = gizeh.rectangle(lx=width + 2, ly=h, xy=(width / 2, y + h / 2), fill=color)
            elif direction == "horizontal":
                x = width * t
                w = width / steps + 1
                rect = gizeh.rectangle(lx=w, ly=height + 2, xy=(x + w / 2, height / 2), fill=color)
            elif direction == "diagonal":
                y = height * t
                h = height / steps + 1
                rect = gizeh.rectangle(lx=width * 2, ly=h, xy=(width / 2, y + h / 2), fill=color)
            else:
                y = height * t
                h = height / steps + 1
                rect = gizeh.rectangle(lx=width + 2, ly=h, xy=(width / 2, y + h / 2), fill=color)

            rect.draw(surface)

    @staticmethod
    def draw_radial_gradient(surface, center, max_radius, color1, color2, steps=40):
        """Draw a radial gradient background."""
        for i in range(steps, 0, -1):
            t = i / steps
            r = max_radius * t
            color = tuple(c1 + (c2 - c1) * (1 - t) for c1, c2 in zip(color1, color2))
            circle = gizeh.circle(r=r, xy=center, fill=color)
            circle.draw(surface)

    @staticmethod
    def draw_glow(surface, center, radius, color, intensity=5, steps=15):
        """Draw a glow effect around a point."""
        for i in range(steps, 0, -1):
            t = i / steps
            r = radius + intensity * (1 - t) * 3
            alpha = t * 0.3
            glow_color = (*color[:3], alpha) if len(color) >= 3 else (*color, alpha)
            circle = gizeh.circle(r=r, xy=center, fill=glow_color)
            circle.draw(surface)

    @staticmethod
    def draw_shadow(surface, shape_func, offset=(5, 5), blur_steps=8, shadow_color=(0, 0, 0)):
        """Draw shadow effect for shapes."""
        for i in range(blur_steps, 0, -1):
            alpha = 0.1 * (blur_steps - i) / blur_steps
            spread = i * 0.5
            shadow_c = (*shadow_color, alpha)
            shape_func(
                offset=(offset[0] + spread, offset[1] + spread),
                color=shadow_c
            )

    @staticmethod
    def draw_particle_burst(surface, center, count=30, max_radius=80, colors=None):
        """Draw a particle burst effect."""
        if colors is None:
            colors = [(1, 1, 1)]

        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(10, max_radius)
            x = center[0] + distance * math.cos(angle)
            y = center[1] + distance * math.sin(angle)
            r = random.uniform(1, 4)
            color = random.choice(colors)
            alpha = random.uniform(0.3, 1.0)
            fill = (*color[:3], alpha)
            particle = gizeh.circle(r=r, xy=(x, y), fill=fill)
            particle.draw(surface)

    @staticmethod
    def draw_lens_flare(surface, center, size=50, color=(1, 1, 0.8)):
        """Draw a simple lens flare effect."""
        for i in range(5, 0, -1):
            alpha = 0.1 * i / 5
            r = size * i / 3
            flare_color = (*color[:3], alpha)
            flare = gizeh.circle(r=r, xy=center, fill=flare_color)
            flare.draw(surface)

        # Starburst lines
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            length = size * 1.5
            x2 = center[0] + length * math.cos(rad)
            y2 = center[1] + length * math.sin(rad)
            line = gizeh.polyline(
                points=[center, (x2, y2)],
                stroke=(*color[:3], 0.15),
                stroke_width=1
            )
            line.draw(surface)


class LogoTemplate:
    """Pre-designed logo templates."""

    @staticmethod
    def minimal_circle(surface, width, height, colors, text="LOGO", fontfamily="Arial"):
        """Minimal circle-based logo."""
        cx, cy = width / 2, height / 2
        radius = min(width, height) * 0.3

        # Outer circle
        gizeh.circle(r=radius, xy=(cx, cy), fill=colors[0]).draw(surface)
        # Inner circle
        gizeh.circle(r=radius * 0.7, xy=(cx, cy), fill=colors[1] if len(colors) > 1 else (1, 1, 1)).draw(surface)

        # Text
        text_color = colors[2] if len(colors) > 2 else (1, 1, 1)
        gizeh.text(text, fontfamily=fontfamily, fontsize=radius * 0.5,
                   xy=(cx, cy), fill=text_color, fontweight="bold").draw(surface)

    @staticmethod
    def shield_badge(surface, width, height, colors, text="BRAND", fontfamily="Arial"):
        """Shield/badge style logo."""
        cx, cy = width / 2, height / 2
        size = min(width, height) * 0.35

        # Shield shape
        points = [
            (0, -size),
            (size * 0.8, -size * 0.5),
            (size * 0.8, size * 0.3),
            (0, size),
            (-size * 0.8, size * 0.3),
            (-size * 0.8, -size * 0.5)
        ]
        shield = gizeh.polyline(
            points=points + [points[0]], xy=(cx, cy),
            fill=colors[0], stroke=colors[1] if len(colors) > 1 else (1, 1, 1),
            stroke_width=3, close_path=True
        )
        shield.draw(surface)

        text_color = colors[2] if len(colors) > 2 else (1, 1, 1)
        gizeh.text(text, fontfamily=fontfamily, fontsize=size * 0.35,
                   xy=(cx, cy), fill=text_color, fontweight="bold").draw(surface)

    @staticmethod
    def geometric_abstract(surface, width, height, colors, text="", fontfamily="Arial"):
        """Abstract geometric logo."""
        cx, cy = width / 2, height / 2
        size = min(width, height) * 0.25

        for i in range(3):
            angle = i * 2 * math.pi / 3
            x = cx + size * 0.3 * math.cos(angle)
            y = cy + size * 0.3 * math.sin(angle)
            color = colors[i % len(colors)]
            fill_color = (*color[:3], 0.7)
            gizeh.circle(r=size * 0.5, xy=(x, y), fill=fill_color).draw(surface)

        if text:
            gizeh.text(text, fontfamily=fontfamily, fontsize=size * 0.4,
                       xy=(cx, cy + size * 0.9), fill=colors[0], fontweight="bold").draw(surface)

    @staticmethod
    def monogram(surface, width, height, colors, text="AB", fontfamily="Arial"):
        """Monogram style logo."""
        cx, cy = width / 2, height / 2
        size = min(width, height) * 0.35

        # Background square rotated 45 degrees
        points = [(0, -size), (size, 0), (0, size), (-size, 0)]
        diamond = gizeh.polyline(
            points=points + [points[0]], xy=(cx, cy),
            fill=colors[0], close_path=True
        )
        diamond.draw(surface)

        # Border
        border = gizeh.polyline(
            points=points + [points[0]], xy=(cx, cy),
            stroke=colors[1] if len(colors) > 1 else (1, 1, 1),
            stroke_width=2, close_path=True
        )
        border.draw(surface)

        text_color = colors[2] if len(colors) > 2 else (1, 1, 1)
        gizeh.text(text[:2], fontfamily=fontfamily, fontsize=size * 0.7,
                   xy=(cx, cy), fill=text_color, fontweight="bold").draw(surface)

    @staticmethod
    def tech_hexagon(surface, width, height, colors, text="TECH", fontfamily="Arial"):
        """Tech-style hexagon logo."""
        cx, cy = width / 2, height / 2
        size = min(width, height) * 0.32

        # Hexagon
        points = [
            (size * math.cos(math.radians(60 * i - 30)),
             size * math.sin(math.radians(60 * i - 30)))
            for i in range(6)
        ]
        hex_shape = gizeh.polyline(
            points=points + [points[0]], xy=(cx, cy),
            fill=colors[0], close_path=True
        )
        hex_shape.draw(surface)

        # Inner hexagon
        inner_points = [
            (size * 0.7 * math.cos(math.radians(60 * i - 30)),
             size * 0.7 * math.sin(math.radians(60 * i - 30)))
            for i in range(6)
        ]
        inner_hex = gizeh.polyline(
            points=inner_points + [inner_points[0]], xy=(cx, cy),
            stroke=colors[1] if len(colors) > 1 else (1, 1, 1),
            stroke_width=2, close_path=True
        )
        inner_hex.draw(surface)

        # Connection lines
        for i in range(6):
            line = gizeh.polyline(
                points=[inner_points[i], points[i]],
                xy=(cx, cy),
                stroke=colors[1] if len(colors) > 1 else (1, 1, 1),
                stroke_width=1
            )
            line.draw(surface)

        text_color = colors[2] if len(colors) > 2 else (1, 1, 1)
        gizeh.text(text, fontfamily=fontfamily, fontsize=size * 0.35,
                   xy=(cx, cy), fill=text_color, fontweight="bold").draw(surface)

    @staticmethod
    def circular_badge(surface, width, height, colors, text="PREMIUM", fontfamily="Arial"):
        """Circular badge with decorative elements."""
        cx, cy = width / 2, height / 2
        radius = min(width, height) * 0.35

        # Outer ring
        gizeh.circle(r=radius, xy=(cx, cy), fill=colors[0]).draw(surface)
        gizeh.circle(r=radius * 0.85, xy=(cx, cy),
                     stroke=colors[1] if len(colors) > 1 else (1, 1, 1),
                     stroke_width=2).draw(surface)
        gizeh.circle(r=radius * 0.75, xy=(cx, cy),
                     fill=colors[1] if len(colors) > 1 else (0.2, 0.2, 0.2)).draw(surface)

        # Decorative dots
        dot_color = colors[2] if len(colors) > 2 else (1, 1, 1)
        for i in range(12):
            angle = math.radians(30 * i)
            dx = cx + radius * 0.8 * math.cos(angle)
            dy = cy + radius * 0.8 * math.sin(angle)
            gizeh.circle(r=3, xy=(dx, dy), fill=dot_color).draw(surface)

        # Star
        star = ShapeFactory.create_star(5, radius * 0.3, radius * 0.15, (cx, cy),
                                         fill=colors[2] if len(colors) > 2 else (1, 1, 1),
                                         stroke_width=0)
        star.draw(surface)

        text_color = colors[0]
        gizeh.text(text, fontfamily=fontfamily, fontsize=radius * 0.2,
                   xy=(cx, cy + radius * 0.55), fill=text_color, fontweight="bold").draw(surface)


class LogoGenerator:
    """Main logo generator engine with all features combined."""

    AVAILABLE_TEMPLATES = [
        "minimal_circle", "shield_badge", "geometric_abstract",
        "monogram", "tech_hexagon", "circular_badge"
    ]

    AVAILABLE_PATTERNS = [
        "dots", "lines", "grid", "concentric",
        "hexagon", "wave", "none"
    ]

    AVAILABLE_EFFECTS = [
        "gradient_bg", "radial_gradient", "glow",
        "particles", "lens_flare", "shadow", "none"
    ]

    AVAILABLE_HARMONY = list(ColorPalette.HARMONY_RULES.keys())
    AVAILABLE_PRESETS = list(ColorPalette.PRESET_PALETTES.keys())

    def __init__(self, width=500, height=500):
        self.width = width
        self.height = height
        self.config = {}
        self.palette = ColorPalette()
        self.pattern_gen = PatternGenerator()
        self.shape_factory = ShapeFactory()
        self.text_renderer = TextRenderer()
        self.effects = EffectsEngine()

    def generate(self, config=None):
        """Generate a logo based on configuration."""
        if config is None:
            config = self._random_config()

        self.config = config
        bg_color = config.get("bg_color", (0.1, 0.1, 0.15))
        surface = gizeh.Surface(width=self.width, height=self.height, bg_color=bg_color)

        # Step 1: Background effects
        self._apply_background(surface, config)

        # Step 2: Pattern overlay
        self._apply_pattern(surface, config)

        # Step 3: Pre-effects
        self._apply_pre_effects(surface, config)

        # Step 4: Main logo template
        self._apply_template(surface, config)

        # Step 5: Additional shapes
        self._apply_extra_shapes(surface, config)

        # Step 6: Text elements
        self._apply_text(surface, config)

        # Step 7: Post-effects
        self._apply_post_effects(surface, config)

        return surface

    def _random_config(self):
        """Generate a random configuration."""
        harmony = random.choice(self.AVAILABLE_HARMONY)
        colors = self.palette.generate_harmonious(rule=harmony)

        return {
            "bg_color": ColorPalette.adjust_brightness(colors[0], 0.3),
            "colors": colors,
            "template": random.choice(self.AVAILABLE_TEMPLATES),
            "pattern": random.choice(self.AVAILABLE_PATTERNS),
            "effects": random.sample(self.AVAILABLE_EFFECTS, k=random.randint(0, 3)),
            "text": "LOGO",
            "subtitle": "",
            "fontfamily": random.choice(["Arial", "Helvetica", "Georgia", "Verdana"]),
            "fontsize": 36,
            "text_effect": random.choice(["none", "shadow", "outline"]),
            "extra_shapes": random.choice([True, False]),
            "gradient_direction": random.choice(["vertical", "horizontal", "diagonal"]),
        }

    def _apply_background(self, surface, config):
        """Apply background effects."""
        effects = config.get("effects", [])
        colors = config.get("colors", [(0.2, 0.3, 0.5), (0.1, 0.1, 0.2)])

        if "gradient_bg" in effects and len(colors) >= 2:
            direction = config.get("gradient_direction", "vertical")
            self.effects.draw_gradient_background(
                surface, self.width, self.height,
                colors[0], colors[-1], direction=direction
            )
        elif "radial_gradient" in effects and len(colors) >= 2:
            max_radius = max(self.width, self.height) * 0.8
            self.effects.draw_radial_gradient(
                surface, (self.width / 2, self.height / 2),
                max_radius, colors[0], colors[-1]
            )

    def _apply_pattern(self, surface, config):
        """Apply background pattern."""
        pattern = config.get("pattern", "none")
        colors = config.get("colors", [(0.5, 0.5, 0.5)])
        pattern_color = ColorPalette.adjust_brightness(colors[0], 0.5)
        pattern_color = (*pattern_color[:3], 0.15)

        if pattern == "dots":
            self.pattern_gen.draw_dots(surface, self.width, self.height, pattern_color, spacing=25, radius=2)
        elif pattern == "lines":
            self.pattern_gen.draw_lines(surface, self.width, self.height, pattern_color, spacing=20)
        elif pattern == "grid":
            self.pattern_gen.draw_grid(surface, self.width, self.height, pattern_color, spacing=30)
        elif pattern == "concentric":
            self.pattern_gen.draw_concentric_circles(
                surface, self.width / 2, self.height / 2,
                max(self.width, self.height) * 0.6, pattern_color, count=10
            )
        elif pattern == "hexagon":
            self.pattern_gen.draw_hexagon_pattern(surface, self.width, self.height, pattern_color, size=25)
        elif pattern == "wave":
            self.pattern_gen.draw_wave_pattern(surface, self.width, self.height, pattern_color)

    def _apply_pre_effects(self, surface, config):
        """Apply effects before main logo."""
        effects = config.get("effects", [])
        colors = config.get("colors", [(1, 1, 1)])
        cx, cy = self.width / 2, self.height / 2

        if "glow" in effects:
            glow_color = colors[0] if colors else (1, 1, 1)
            self.effects.draw_glow(surface, (cx, cy), 30, glow_color, intensity=8)

    def _apply_template(self, surface, config):
        """Apply the main logo template."""
        template_name = config.get("template", "minimal_circle")
        colors = config.get("colors", [(0.2, 0.4, 0.8), (1, 1, 1), (1, 1, 1)])
        text = config.get("text", "LOGO")
        fontfamily = config.get("fontfamily", "Arial")

        templates = {
            "minimal_circle": LogoTemplate.minimal_circle,
            "shield_badge": LogoTemplate.shield_badge,
            "geometric_abstract": LogoTemplate.geometric_abstract,
            "monogram": LogoTemplate.monogram,
            "tech_hexagon": LogoTemplate.tech_hexagon,
            "circular_badge": LogoTemplate.circular_badge,
        }

        template_func = templates.get(template_name, LogoTemplate.minimal_circle)
        template_func(surface, self.width, self.height, colors, text, fontfamily)

    def _apply_extra_shapes(self, surface, config):
        """Apply additional decorative shapes."""
        if not config.get("extra_shapes", False):
            return

        colors = config.get("colors", [(0.5, 0.5, 0.5)])
        cx, cy = self.width / 2, self.height / 2

        # Random decorative elements
        num_elements = random.randint(3, 8)
        for _ in range(num_elements):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(min(self.width, self.height) * 0.35,
                                       min(self.width, self.height) * 0.45)
            x = cx + distance * math.cos(angle)
            y = cy + distance * math.sin(angle)
            color = random.choice(colors)
            alpha_color = (*color[:3], random.uniform(0.3, 0.7))

            shape_type = random.choice(["circle", "square", "diamond", "triangle"])
            size = random.uniform(3, 10)

            if shape_type == "circle":
                gizeh.circle(r=size, xy=(x, y), fill=alpha_color).draw(surface)
            elif shape_type == "square":
                gizeh.square(l=size * 2, xy=(x, y), fill=alpha_color,
                             angle=random.uniform(0, math.pi)).draw(surface)
            elif shape_type == "diamond":
                self.shape_factory.create_diamond(size, (x, y), fill=alpha_color).draw(surface)

    def _apply_text(self, surface, config):
        """Apply additional text elements."""
        subtitle = config.get("subtitle", "")
        if not subtitle:
            return

        colors = config.get("colors", [(1, 1, 1)])
        fontfamily = config.get("fontfamily", "Arial")
        cx = self.width / 2
        cy = self.height * 0.82

        text_color = colors[-1] if colors else (1, 1, 1)
        text_effect = config.get("text_effect", "none")

        if text_effect == "shadow":
            self.text_renderer.render_text_with_shadow(
                surface, subtitle, (cx, cy), fontsize=18,
                fontfamily=fontfamily, fill=text_color
            )
        elif text_effect == "outline":
            self.text_renderer.render_text_with_outline(
                surface, subtitle, (cx, cy), fontsize=18,
                fontfamily=fontfamily, fill=text_color
            )
        else:
            self.text_renderer.render_text(
                surface, subtitle, (cx, cy), fontsize=18,
                fontfamily=fontfamily, fill=text_color
            )

    def _apply_post_effects(self, surface, config):
        """Apply effects after main logo."""
        effects = config.get("effects", [])
        colors = config.get("colors", [(1, 1, 1)])
        cx, cy = self.width / 2, self.height / 2

        if "particles" in effects:
            self.effects.draw_particle_burst(
                surface, (cx, cy), count=40,
                max_radius=min(self.width, self.height) * 0.45,
                colors=colors
            )

        if "lens_flare" in effects:
            flare_x = cx + random.uniform(-self.width * 0.2, self.width * 0.2)
            flare_y = cy + random.uniform(-self.height * 0.2, self.height * 0.2)
            self.effects.draw_lens_flare(surface, (flare_x, flare_y), size=30)

    def save(self, surface, filename="logo.png"):
        """Save the generated logo."""
        surface.write_to_png(filename)
        print(f"Logo saved to: {filename}")

    def save_config(self, filename="logo_config.json"):
        """Save current configuration to JSON."""
        # Convert tuples to lists for JSON serialization
        serializable_config = {}
        for key, value in self.config.items():
            if isinstance(value, tuple):
                serializable_config[key] = list(value)
            elif isinstance(value, list):
                serializable_config[key] = [
                    list(v) if isinstance(v, tuple) else v for v in value
                ]
            else:
                serializable_config[key] = value

        with open(filename, 'w') as f:
            json.dump(serializable_config, f, indent=2)
        print(f"Configuration saved to: {filename}")

    def load_config(self, filename="logo_config.json"):
        """Load configuration from JSON."""
        with open(filename, 'r') as f:
            config = json.load(f)

        # Convert lists back to tuples where needed
        for key in ["bg_color"]:
            if key in config and isinstance(config[key], list):
                config[key] = tuple(config[key])

        if "colors" in config:
            config["colors"] = [tuple(c) if isinstance(c, list) else c for c in config["colors"]]

        return config

    def batch_generate(self, count=10, output_dir="logos", prefix="logo"):
        """Generate multiple logo variations."""
        os.makedirs(output_dir, exist_ok=True)

        generated_files = []
        for i in range(count):
            config = self._random_config()
            surface = self.generate(config)
            filename = os.path.join(output_dir, f"{prefix}_{i + 1:03d}.png")
            self.save(surface, filename)
            generated_files.append(filename)

        print(f"\nGenerated {count} logos in '{output_dir}/' directory")
        return generated_files

    def generate_variations(self, base_config, count=5, output_dir="variations"):
        """Generate variations of a base design."""
        os.makedirs(output_dir, exist_ok=True)

        generated_files = []
        for i in range(count):
            config = base_config.copy()

            # Vary colors slightly
            if "colors" in config:
                varied_colors = []
                for color in config["colors"]:
                    varied = tuple(
                        max(0, min(1, c + random.uniform(-0.1, 0.1)))
                        for c in color
                    )
                    varied_colors.append(varied)
                config["colors"] = varied_colors

            # Vary some settings
            config["extra_shapes"] = random.choice([True, False])
            config["pattern"] = random.choice(self.AVAILABLE_PATTERNS)

            surface = self.generate(config)
            filename = os.path.join(output_dir, f"variation_{i + 1:03d}.png")
            self.save(surface, filename)
            generated_files.append(filename)

        print(f"\nGenerated {count} variations in '{output_dir}/' directory")
        return generated_files

    def generate_size_variants(self, config, sizes=None, output_dir="sizes"):
        """Generate logos at different sizes."""
        if sizes is None:
            sizes = [(64, 64), (128, 128), (256, 256), (512, 512), (1024, 1024)]

        os.makedirs(output_dir, exist_ok=True)

        original_w, original_h = self.width, self.height
        generated_files = []

        for w, h in sizes:
            self.width = w
            self.height = h
            surface = self.generate(config)
            filename = os.path.join(output_dir, f"logo_{w}x{h}.png")
            self.save(surface, filename)
            generated_files.append(filename)

        self.width, self.height = original_w, original_h
        print(f"\nGenerated {len(sizes)} size variants in '{output_dir}/' directory")
        return generated_files

    def interactive_generate(self):
        """Interactive logo generation with user input."""
        print("=" * 60)
        print("    ADVANCED LOGO GENERATOR - Interactive Mode")
        print("=" * 60)

        # Get text
        text = input("\nEnter logo text (default: 'LOGO'): ").strip() or "LOGO"
        subtitle = input("Enter subtitle (optional): ").strip()

        # Choose template
        print(f"\nAvailable templates: {', '.join(self.AVAILABLE_TEMPLATES)}")
        template = input("Choose template (or 'random'): ").strip()
        if template not in self.AVAILABLE_TEMPLATES:
            template = random.choice(self.AVAILABLE_TEMPLATES)

        # Choose color scheme
        print(f"\nAvailable presets: {', '.join(self.AVAILABLE_PRESETS)}")
        print(f"Available harmonies: {', '.join(self.AVAILABLE_HARMONY)}")
        color_choice = input("Choose preset name, harmony rule, or 'random': ").strip()

        if color_choice in self.AVAILABLE_PRESETS:
            colors = self.palette.get_preset(color_choice)
        elif color_choice in self.AVAILABLE_HARMONY:
            colors = self.palette.generate_harmonious(rule=color_choice)
        else:
            colors = self.palette.generate_harmonious(rule=random.choice(self.AVAILABLE_HARMONY))

        # Choose pattern
        print(f"\nAvailable patterns: {', '.join(self.AVAILABLE_PATTERNS)}")
        pattern = input("Choose pattern (or 'random'): ").strip()
        if pattern not in self.AVAILABLE_PATTERNS:
            pattern = random.choice(self.AVAILABLE_PATTERNS)

        # Choose effects
        print(f"\nAvailable effects: {', '.join(self.AVAILABLE_EFFECTS)}")
        effects_input = input("Choose effects (comma-separated, or 'random'): ").strip()
        if effects_input == "random" or not effects_input:
            effects = random.sample(self.AVAILABLE_EFFECTS, k=random.randint(0, 3))
        else:
            effects = [e.strip() for e in effects_input.split(",") if e.strip() in self.AVAILABLE_EFFECTS]

        # Choose size
        size_input = input("\nEnter size WxH (default: 500x500): ").strip()
        if "x" in size_input:
            try:
                w, h = map(int, size_input.split("x"))
                self.width, self.height = w, h
            except ValueError:
                pass

        # Build config
        config = {
            "bg_color": ColorPalette.adjust_brightness(colors[0], 0.3),
            "colors": colors,
            "template": template,
            "pattern": pattern,
            "effects": effects,
            "text": text,
            "subtitle": subtitle,
            "fontfamily": "Arial",
            "fontsize": 36,
            "text_effect": random.choice(["none", "shadow", "outline"]),
            "extra_shapes": True,
            "gradient_direction": random.choice(["vertical", "horizontal", "diagonal"]),
        }

        # Generate
        surface = self.generate(config)
        filename = input("\nOutput filename (default: 'logo.png'): ").strip() or "logo.png"
        self.save(surface, filename)
        self.save_config(filename.replace(".png", "_config.json"))

        # Ask for variations
        variations = input("\nGenerate variations? (y/n): ").strip().lower()
        if variations == "y":
            count = int(input("How many? (default: 5): ").strip() or "5")
            self.generate_variations(config, count=count)

        print("\nDone! Your logo has been generated.")
        return config


class LogoComposer:
    """Compose multiple elements into complex logos."""

    def __init__(self, width=500, height=500):
        self.width = width
        self.height = height
        self.layers = []

    def add_layer(self, draw_func, z_index=0):
        """Add a drawing layer with z-index for ordering."""
        self.layers.append({"func": draw_func, "z_index": z_index})

    def compose(self, bg_color=(0.1, 0.1, 0.15)):
        """Compose all layers into final surface."""
        surface = gizeh.Surface(width=self.width, height=self.height, bg_color=bg_color)

        # Sort by z-index
        sorted_layers = sorted(self.layers, key=lambda l: l["z_index"])

        for layer in sorted_layers:
            layer["func"](surface)

        return surface

    def clear(self):
        """Clear all layers."""
        self.layers = []


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def demo_all_templates():
    """Generate demos of all available templates."""
    generator = LogoGenerator(width=500, height=500)
    os.makedirs("demo_templates", exist_ok=True)

    for template in LogoGenerator.AVAILABLE_TEMPLATES:
        colors = ColorPalette.generate_harmonious(rule="triadic")
        config = {
            "bg_color": ColorPalette.adjust_brightness(colors[0], 0.25),
            "colors": colors,
            "template": template,
            "pattern": "none",
            "effects": ["gradient_bg"],
            "text": "DEMO",
            "subtitle": template.replace("_", " ").title(),
            "fontfamily": "Arial",
            "fontsize": 36,
            "text_effect": "shadow",
            "extra_shapes": False,
            "gradient_direction": "vertical",
        }
        surface = generator.generate(config)
        generator.save(surface, f"demo_templates/{template}.png")

    print("All template demos generated!")


def demo_all_patterns():
    """Generate demos of all available patterns."""
    generator = LogoGenerator(width=500, height=500)
    os.makedirs("demo_patterns", exist_ok=True)

    for pattern in LogoGenerator.AVAILABLE_PATTERNS:
        colors = ColorPalette.get_preset("corporate")
        config = {
            "bg_color": (0.95, 0.95, 0.97),
            "colors": colors,
            "template": "minimal_circle",
            "pattern": pattern,
            "effects": [],
            "text": "PAT",
            "subtitle": pattern.replace("_", " ").title(),
            "fontfamily": "Arial",
            "fontsize": 36,
            "text_effect": "none",
            "extra_shapes": False,
            "gradient_direction": "vertical",
        }
        surface = generator.generate(config)
        generator.save(surface, f"demo_patterns/{pattern}.png")

    print("All pattern demos generated!")


def demo_color_palettes():
    """Generate demos of all color presets."""
    generator = LogoGenerator(width=500, height=500)
    os.makedirs("demo_palettes", exist_ok=True)

    for preset_name in ColorPalette.PRESET_PALETTES:
        colors = ColorPalette.get_preset(preset_name)
        config = {
            "bg_color": ColorPalette.adjust_brightness(colors[0], 0.3),
            "colors": colors,
            "template": "tech_hexagon",
            "pattern": "none",
            "effects": ["gradient_bg", "particles"],
            "text": preset_name[:4].upper(),
            "subtitle": preset_name.replace("_", " ").title(),
            "fontfamily": "Arial",
            "fontsize": 36,
            "text_effect": "shadow",
            "extra_shapes": True,
            "gradient_direction": "vertical",
        }
        surface = generator.generate(config)
        generator.save(surface, f"demo_palettes/{preset_name}.png")

    print("All palette demos generated!")


def main():
    """Main entry point."""
    print("=" * 60)
    print("    ADVANCED LOGO GENERATOR TOOL v2.0")
    print("=" * 60)
    print("\nOptions:")
    print("  1. Interactive mode - Design your logo step by step")
    print("  2. Random single logo - Generate one random logo")
    print("  3. Batch generate - Generate multiple random logos")
    print("  4. Demo all templates - Preview all templates")
    print("  5. Demo all patterns - Preview all patterns")
    print("  6. Demo color palettes - Preview all color presets")
    print("  7. Generate from config file - Load and generate")
    print("  8. Generate size variants - Multiple sizes")
    print("  9. Custom composed logo - Layer-based composition")
    print("  0. Exit")

    # choice = input("\nEnter your choice (0-9): ").strip()
    # For non-interactive run, we will use choice "2" by default if not specified
    choice = os.environ.get("LOGO_CHOICE", "2")

    generator = LogoGenerator(width=500, height=500)

    if choice == "1":
        generator.interactive_generate()

    elif choice == "2":
        surface = generator.generate()
        generator.save(surface, "random_logo.png")
        generator.save_config("random_logo_config.json")

    elif choice == "3":
        # count = int(input("How many logos? (default: 10): ").strip() or "10")
        count = 5
        generator.batch_generate(count=count)

    elif choice == "4":
        demo_all_templates()

    elif choice == "5":
        demo_all_patterns()

    elif choice == "6":
        demo_color_palettes()

    elif choice == "7":
        filename = input("Config file path: ").strip()
        if os.path.exists(filename):
            config = generator.load_config(filename)
            surface = generator.generate(config)
            generator.save(surface, "loaded_logo.png")
        else:
            print(f"File not found: {filename}")

    elif choice == "8":
        config = generator._random_config()
        # config["text"] = input("Logo text: ").strip() or "LOGO"
        generator.generate_size_variants(config)

    elif choice == "9":
        # Custom composed logo example
        composer = LogoComposer(500, 500)
        colors = ColorPalette.generate_harmonious(rule="triadic")

        # Background layer
        def bg_layer(surface):
            EffectsEngine.draw_gradient_background(
                surface, 500, 500,
                ColorPalette.adjust_brightness(colors[0], 0.3),
                ColorPalette.adjust_brightness(colors[0], 0.6),
                direction="diagonal"
            )
        composer.add_layer(bg_layer, z_index=0)

        # Pattern layer
        def pattern_layer(surface):
            PatternGenerator.draw_hexagon_pattern(
                surface, 500, 500,
                (*colors[1][:3], 0.1), size=30
            )
        composer.add_layer(pattern_layer, z_index=1)

        # Main shape layer
        def shape_layer(surface):
            gizeh.circle(r=80, xy=(250, 250), fill=colors[0]).draw(surface)
            gizeh.circle(r=60, xy=(250, 250), fill=colors[1]).draw(surface)
            star = ShapeFactory.create_star(
                6, 40, 20, (250, 250),
                fill=colors[2] if len(colors) > 2 else (1, 1, 1)
            )
            star.draw(surface)
        composer.add_layer(shape_layer, z_index=2)

        # Text layer
        def text_layer(surface):
            TextRenderer.render_text_with_shadow(
                surface, "COMPOSED", (250, 350),
                fontsize=28, fill=(1, 1, 1)
            )
        composer.add_layer(text_layer, z_index=3)

        # Effects layer
        def effects_layer(surface):
            EffectsEngine.draw_particle_burst(
                surface, (250, 250), count=50,
                max_radius=150, colors=colors
            )
        composer.add_layer(effects_layer, z_index=4)

        surface = composer.compose(bg_color=(0.1, 0.1, 0.15))
        surface.write_to_png("composed_logo.png")
        print("Composed logo saved to: composed_logo.png")

    elif choice == "0":
        print("Goodbye!")
        return
    else:
        print("Invalid choice. Generating random logo...")
        surface = generator.generate()
        generator.save(surface, "logo.png")


if __name__ == "__main__":
    main()
