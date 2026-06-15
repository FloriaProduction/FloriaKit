from FloriaKit import hints

# --- Векторы ---
v2: hints.vec2 = (1.5, 2.0)
v3: hints.vec3 = (1, 2, 3)
v4: hints.vec4 = (1, 2, 3, 4)
print("vec2:", v2)


# --- Кватернионы и матрицы ---
q: hints.quat = (0, 0, 0, 1)  # единичный кватернион
m: hints.mat4x4 = (
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1),
)
print("mat4x4:", m)


# --- Цвета ---
rgb_color: hints.color.color = (255, 128, 64)
rgba_color: hints.color.color = (100, 150, 200, 128)
print("RGB -> RGBA:", hints.color.get_rgba(rgb_color))  # (255, 128, 64, 255)
print("RGBA -> RGB:", hints.color.get_rgb(rgba_color))

# --- Выравнивание (Align) ---
size: hints.vec2 = (800, 600)

# Простые строковые константы
pos_center = hints.calculate_align(size, 'c')  # (400.0, 300.0)
pos_top_left = hints.calculate_align(size, 'lt')  # (0, 0)

# Детальное выравнивание со смещением
detail: hints.AlignDetail = {'left': 100, 'bottom': 50}
pos_detail = hints.calculate_align(size, detail)  # (100, 550)

print(f"Center: {pos_center}, detail: {pos_detail}")


# --- Пути ---
path: hints.PathOrStr = "data/settings.json"
path_obj = hints.get_path(path)
print("Path object:", path_obj)
