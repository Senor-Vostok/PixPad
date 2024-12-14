from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QMenu, QAction
import PyQt5.Qt


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем QGridLayout
        self.layout = QGridLayout(self)

        # Добавляем несколько кнопок
        for i in range(5):
            for j in range(5):
                button = QPushButton(f"Button {i},{j}")
                button.setContextMenuPolicy(Qt.CustomContextMenu)  # Разрешаем кастомное меню
                button.customContextMenuRequested.connect(self.show_context_menu)  # Подключаем сигнал
                self.layout.addWidget(button, i, j)

        self.setLayout(self.layout)
        self.show()

    def show_context_menu(self, pos):
        button = self.sender()  # Получаем кнопку, на которой было нажато правой кнопкой

        # Создаем контекстное меню
        context_menu = QMenu(self)

        # Создаем действие для удаления кнопки
        delete_action = QAction("Удалить", self)
        delete_action.triggered.connect(lambda _, x=button: self.delete_button(x))

        # Добавляем действие в контекстное меню
        context_menu.addAction(delete_action)

        # Показываем меню в позиции клика
        context_menu.exec_(self.mapToGlobal(pos))

    def delete_button(self, button):
        # Удаляем кнопку
        self.layout.removeWidget(button)
        button.deleteLater()  # Удаляем виджет из памяти

app = QApplication([])
window = MyWidget()
app.exec_()
