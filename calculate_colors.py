from colour import Color

red = Color("#FE4A49")
yellow = Color("#FDE74C")
green = Color("#6BD425")

colors = list(green.range_to(Color(yellow),50)) + list(yellow.range_to(Color(red),50))

print(colors)