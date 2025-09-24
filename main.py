import sys
import os
from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
from random import randint

images_path = Path("./img/without").resolve()
new_images_path = Path("./img/with").resolve()

class RectangleSelector:
    def __init__(self, root: tk.Tk, image_path: Path) -> None:
        self.root = root
        self.image_path = image_path

        self.root.title("Выделение области на изображении")

        self.image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(self.image)

        self.info_label = tk.Label(
            self.root,
            text="Выделите прямоугольную область мышью на изображении",
            anchor="w"
        )
        self.info_label.pack(fill="x", padx=8, pady=(8, 4))

        self.canvas = tk.Canvas(
            self.root,
            width=self.photo.width(),
            height=self.photo.height(),
            highlightthickness=0,
            background="#000000"
        )
        self.canvas.pack(padx=8, pady=8)

        # Отрисовать изображение как фон канвы
        self.canvas_img = self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

        # Состояние выделения
        self.start_x: int | None = None
        self.start_y: int | None = None
        self.rect_id: int | None = None

        # Координаты результата (левая-верхняя и правая-нижняя точки)
        self.x1: int | None = None
        self.y1: int | None = None
        self.x2: int | None = None
        self.y2: int | None = None

        # Привязка событий мыши
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event: tk.Event) -> None:
        self.start_x, self.start_y = event.x, event.y
        self.x1, self.y1, self.x2, self.y2 = None, None, None, None
        # Удалить предыдущее выделение, если было
        if self.rect_id is not None:
            self.canvas.delete(self.rect_id)
            self.rect_id = None

        # Создать новый прямоугольник
        self.rect_id = self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.start_x,
            self.start_y,
            outline="#39a0ff",
            width=2,
            dash=(6, 4),
            fill="",
        )

    def on_mouse_move(self, event: tk.Event) -> None:
        if self.rect_id is None or self.start_x is None or self.start_y is None:
            return
        # Обновляем второй угол
        cur_x, cur_y = event.x, event.y
        # Ограничим диапазоном изображения
        cur_x = max(0, min(cur_x, self.photo.width()))
        cur_y = max(0, min(cur_y, self.photo.height()))
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event: tk.Event) -> None:
        if self.rect_id is None or self.start_x is None or self.start_y is None:
            return
        end_x, end_y = event.x, event.y
        end_x = max(0, min(end_x, self.photo.width()))
        end_y = max(0, min(end_y, self.photo.height()))

        x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
        x2, y2 = max(self.start_x, end_x), max(self.start_y, end_y)

        # Минимальный размер для валидного прямоугольника
        if (x2 - x1) < 2 or (y2 - y1) < 2:
            messagebox.showinfo("Мало точек", "Слишком маленькое выделение. Повторите попытку.")
            return

        self.x1, self.y1, self.x2, self.y2 = int(x1), int(y1), int(x2), int(y2)

        # Вывести 4 угла в консоль
        points = (
            (self.x1, self.y1),
            (self.x2, self.y1),
            (self.x2, self.y2),
            (self.x1, self.y2),
        )
        print("Координаты прямоугольника (x, y):")
        for p in points:
            print(p)
        # Завершаем цикл Tk, чтобы метод run() мог вернуть координаты
        self.root.quit()

    def run(self):
        self.root.mainloop()
        # После выхода из цикла возвращаем точки, если они заданы
        if None not in (self.x1, self.y1, self.x2, self.y2):
            pts = (
                (self.x1, self.y1),
                (self.x2, self.y1),
                (self.x2, self.y2),
                (self.x1, self.y2),
            )
            try:
                self.root.destroy()
            except Exception:
                pass
            return pts
        try:
            self.root.destroy()
        except Exception:
            pass
        return None


def make_change(name = "", points = None):
    if points is None:
        points = []
 
    left_top = points[0]
    right_top = points[1]
    right_bottom = points[2]
    left_bottom = points[3]

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

    img = Image.open(images_path / name)

    for _ in range(randint(1000, 2000)):
        random_ejection = randint(20, 30)

        left_x = randint(x_range[0] - random_ejection, x_range[1] + random_ejection)
        left_y = randint(y_range[0] - random_ejection, y_range[1] + random_ejection)

        diameter = randint(3, 10)

        crop = img.crop((left_x, left_y, left_x + diameter, left_y + diameter))  # (left, top, right, bottom)


        paste_x = randint(x_range[0] - random_ejection, x_range[1] + random_ejection)
        paste_y = randint(y_range[0] - random_ejection, y_range[1] + random_ejection)
        img.paste(crop, (paste_x, paste_y))
        img.save(new_images_path / f"new_{name}")


def main() -> None:
    
    image_list = list(map(lambda x: x[:-4], os.listdir(images_path)))

    print("Какое изображение вы хотите использовать:\n")
    for ind, image_name in enumerate(image_list):
        print(f"{ind+1}. {image_name}")

    image_number = int(input("Введите номер изображения: "))
    image_name = image_list[image_number - 1] + ".jpg"
    image_path = images_path / image_name



    print("Откроется окно. Выделите прямоугольную область на изображении мышью.")

    root = tk.Tk()
    app = RectangleSelector(root, image_path)
    
    points = app.run()
    if points is not None:
        print("Точки из main():", points)
    else:
        print("Прямоугольник не был выбран.")

    make_change(name = image_name, points = points)


if __name__ == "__main__":
    main()



