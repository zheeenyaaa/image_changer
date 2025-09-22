from PIL import Image, ImageTk
import tkinter as tk

# logo = Image.open("logo.png")

# logo = logo.resize((100, 100))


# background.paste(logo, (50, 50), logo)

# # Сохраняем результат
# background.save("result.jpg")

# img = Image.open("capibara.jpg")


click_points = {}


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
    getPoints("capibara.jpg")
    # x = int(input("Введите координату x: "))
    # y = int(input("Введите координату y: "))
    # print(x, y)

    # img = Image.open("capibara.jpg")
    # crop = img.crop((x, y, x+100, y+100))  # (left, top, right, bottom)
    # crop.save("fragment.jpg")
    # img.paste(crop, (200, 300))
    # img.save("new_img.jpg")

    print(click_points)
if __name__ == "__main__":
    main()