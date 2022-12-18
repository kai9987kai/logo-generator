import gizeh
import random

# Set the size of the logo
width, height = 200, 200

# Choose a random background color
bg_color = (random.random(), random.random(), random.random())

# Create a new surface to draw on
surface = gizeh.Surface(width=width, height=height, bg_color=bg_color)

# Choose a random shape to draw
shape = random.choice([gizeh.circle, gizeh.rectangle, gizeh.triangle])

# Draw the shape on the surface
shape(r=50, xy=(100, 100), fill=(1, 0, 0)).draw(surface)

# Add some text to the surface
text = gizeh.text("Logo", fontfamily="Arial", fontsize=36, xy=(100, 100), fill=(0, 0, 0))
text.draw(surface)

# Save the surface as a SVG file
surface.write_to_png("logo.png")
