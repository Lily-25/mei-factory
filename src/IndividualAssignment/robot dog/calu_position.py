import math

a = 46
c = 46

# 输入参数
h = 52.5
l = -4.5

# 计算边b
b = math.sqrt(l**2 + h**2)

# 计算角A（弧度转角度）
cos_A = (b**2 + c**2 - a**2) / (2 * b * c)
angle_A = math.degrees(math.acos(cos_A))

# 计算角B（弧度转角度）
cos_B = (a**2 + c**2 - b**2) / (2 * a * c)
angle_B = math.degrees(math.acos(cos_B))

# 计算膝角
arm_angle = angle_A - math.degrees(math.atan(l/h))
knee_angle = angle_B - 90

# 输出结果
print(f"角A：{angle_A:.2f}°")
print(f"角B：{angle_B:.2f}°")
print(f"手臂：{arm_angle:.2f}°")
print(f"膝角：{knee_angle:.2f}°")