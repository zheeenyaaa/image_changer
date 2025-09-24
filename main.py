import sys
from pathlib import Path

try:
    from PIL import Image, ImageTk
except ImportError as exc:
    print("Не установлен Pillow. Установите командой: pip install pillow", file=sys.stderr)
    raise

import tkinter as tk
from tkinter import messagebox


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

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:

    filename = input("Введите имя файла изображения (например, awa.jpg): ").strip()
    filename = Path("./img/without").resolve() / filename


    image_path = Path(filename)
    if not image_path.is_file():
        # Попробуем поискать рядом с текущим скриптом
        alt_path = Path(__file__).resolve().parent / filename
        if alt_path.is_file():
            image_path = alt_path
        else:
            print(f"Файл не найден: {filename}")
            return

    print("Откроется окно. Выделите прямоугольную область на изображении мышью.")

    root = tk.Tk()
    app = RectangleSelector(root, image_path)
    app.run()


if __name__ == "__main__":
    main()


