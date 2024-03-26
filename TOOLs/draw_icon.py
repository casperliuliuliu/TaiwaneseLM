from PIL import Image, ImageDraw

# Create a transparent image
image_size = (125, 125)
image = Image.new("RGBA", image_size, (255, 0, 0, 0))

# Initialize the drawing context
draw = ImageDraw.Draw(image)

# Circle parameters
circle_center = (75, 75)
circle_radius = 50
circle_outline = "yellow"
circle_width = 10

# Draw a hollow circle
draw.ellipse((circle_center[0]-circle_radius, circle_center[1]-circle_radius,
              circle_center[0]+circle_radius, circle_center[1]+circle_radius), 
             outline=circle_outline, width=circle_width)

# Save the image with a transparent background
filename = "hollow_circle.png"
image.save(filename)

filename
