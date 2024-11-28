class Layer:
    def __init__(self, frames, visibility=100):
        self.frames = frames
        self.visibility = visibility

    def change_visibility(self, new_visibility):  # Изменить прозрачность слоя
        pass

    def update(self):  # Обновить слой
        pass

    def show(self):  # Показать слой
        pass

    def hide(self):  # Скрыть слой
        pass

    def add_frame(self, frame):  # Добавить кадр
        self.frames.append(frame)

    def del_frame(self):  # Удалить последний кадр
        del_frame = self.frames.pop(-1)
        del del_frame
