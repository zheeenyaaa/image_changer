from imghdr import what
from PIL import Image, ImageTk
import tkinter as tk
from random import randint

# logo = Image.open("logo.png")

# logo = logo.resize((100, 100))


# background.paste(logo, (50, 50), logo)

# # Сохраняем результат
# background.save("result.jpg")

# img = Image.open("capibara.jpg")


click_points = {}
min_d = 5
max_d = 10


def on_click(event):
    click_index = len(click_points) + 1
    click_points[click_index] = (event.x, event.y)

    r = 2
    canvas = event.widget
    canvas.create_oval(event.x - r, event.y - r, event.x + r, event.y + r, fill="red", outline="")

    if click_index >= 4:
        canvas.after(100, canvas.winfo_toplevel().destroy)

def getPoints(userImg: str) -> None:
    root = tk.Tk()
    root.title("Выбор точки на изображении")
    click_points.clear()
    img = Image.open(userImg)
    tk_img = ImageTk.PhotoImage(img)

    canvas = tk.Canvas(root, width=img.width, height=img.height)
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=tk_img)
    canvas.image = tk_img

    canvas.bind("<Button-1>", on_click)
    root.mainloop()


def main():
    what_image = input("Какое изображение вы хотите исковеркать: ") + ".jpg"
    getPoints(what_image)
 
    left_top = click_points[1]
    right_top = click_points[2]
    right_bottom = click_points[3]
    left_bottom = click_points[4]

    width = abs(left_top[0] - right_bottom[0])
    height = abs(right_top[1] - left_bottom[1])

    x_range = [left_top[0], left_top[0] + width]
    y_range = [left_top[1], left_top[1] + height]

    # print(f"Левый верхний: {left_top}")
    # print(f"Правый верхний: {right_top}")
    # print(f"Правый нижний: {right_bottom}")
    # print(f"Левый нижний: {left_bottom}")

    print("Ширина ", width)
    print("Высота", height)

    print("x range ", x_range)
    print("y range ", y_range)

    img = Image.open(what_image)

    for _ in range(randint(500, 700)):
        random_ejection = randint(50, 100)

        left_x = randint(x_range[0] - random_ejection, x_range[1] + random_ejection)
        left_y = randint(y_range[0] - random_ejection, y_range[1] + random_ejection)

        diameter = randint(5, 35)

        crop = img.crop((left_x, left_y, left_x + diameter, left_y + diameter))  # (left, top, right, bottom)
        crop.save("fragment.jpg")

        paste_x = randint(x_range[0] - random_ejection, x_range[1] + random_ejection)
        paste_y = randint(y_range[0] - random_ejection, y_range[1] + random_ejection)
        img.paste(crop, (paste_x, paste_y))
        img.save(f"new_{what_image[:-4]}.jpg")


if __name__ == "__main__":
    main()