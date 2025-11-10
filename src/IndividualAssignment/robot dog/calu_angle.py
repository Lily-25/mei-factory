import math

# 机械腿参数
a = 46  # 大腿长度
c = 46  # 小腿长度

# 输入关节角度
arm_angle = 59  # 髋关节角度（示例值，请根据实际情况修改）
knee_angle = 14  # 膝关节角度（示例值，请根据实际情况修改）

# 从关节角度反推几何角度
angle_B = knee_angle + 90  # 膝关节几何角度

# 使用余弦定理计算边b（脚到髋关节的直线距离）
cos_B = math.cos(math.radians(angle_B))
b = math.sqrt(a**2 + c**2 - 2 * a * c * cos_B)

# 计算角A（髋关节几何角度）
cos_A = (b**2 + c**2 - a**2) / (2 * b * c)
angle_A = math.degrees(math.acos(cos_A))

# 计算atan2的角度（髋关节相对于垂直线的角度）
atan_angle = angle_A - arm_angle

# 计算h和l
h = b * math.cos(math.radians(atan_angle))
l = b * math.sin(math.radians(atan_angle))

# 输出结果
print(f"输入参数：")
print(f"  髋关节角度 (arm_angle): {arm_angle:.2f}°")
print(f"  膝关节角度 (knee_angle): {knee_angle:.2f}°")
print(f"\n计算结果：")
print(f"  垂直高度 h: {h:.2f} mm")
print(f"  水平距离 l: {l:.2f} mm")
print(f"  直线距离 b: {b:.2f} mm")
print(f"  几何角A: {angle_A:.2f}°")
print(f"  几何角B: {angle_B:.2f}°")