import math

# Settings
amplitude = 60        # height of wave in mm
frequency = 1         # number of complete cycles over 50cm
length = 500          # 50cm in mm
num_points = 1000     # more points = smoother curve

lines = []
lines.append("0\nSECTION\n2\nENTITIES")

points = []
for i in range(num_points + 1):
    x = (i / num_points) * length
    # maps x from 0->500 through 'frequency' full cycles
    y = amplitude * math.cos(frequency * 2 * math.pi * (x / length))
    points.append((x, y))

for i in range(len(points) - 1):
    x1, y1 = points[i]
    x2, y2 = points[i + 1]
    lines.append(f"0\nLINE\n8\n0\n10\n{x1}\n20\n{y1}\n30\n0.0\n11\n{x2}\n21\n{y2}\n31\n0.0")

lines.append("0\nENDSEC\n0\nEOF")

with open("coswave.dxf", "w") as f:
    f.write("\n".join(lines))

print("Done! Open coswave.dxf in LibreCAD.")