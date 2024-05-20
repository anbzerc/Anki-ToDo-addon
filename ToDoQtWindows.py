import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QStackedLayout, QLayout, \
    QLabel, QSizePolicy
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView  # Import QWebEngineView

class ToDoQtWindows(QWidget):
    def __init__(self, todo):
        super().__init__()
        self.setWindowTitle("My App")

        # Create a new widget container
        self.button_container = QWidget()
        self.button_container.setFixedSize(600, 80)  # Set a fixed size for the container (adjusted width)

        # Set the layout of the button container to QHBoxLayout
        button_layout = QHBoxLayout(self.button_container)
        button_layout.setSpacing(10)  # Set a 10px spacing between buttons
        self.stacklayout = QStackedLayout()

        btn_size = (120, 25)  # Set a fixed size for buttons (adjusted height)

        # Render htmls :
        html_list = todo.render_tasks([todo.get_all_task(), todo.get_all_completed()])

        # Tab 1

        btn = QPushButton("To do")
        btn.setFixedSize(*btn_size)  # Apply the fixed size
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        # Replace the colored widget with a QWebEngineView widget for tab 1
        self.web_view = QWebEngineView()

        # Make background transparent
        self.web_view.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.web_view.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
        self.web_view.page().setBackgroundColor(Qt.GlobalColor.transparent)

        todo_html = str(html_list[0])
        # Remove absolute position statements
        todo_html =  todo_html.replace("position: absolute;", "")
        todo_html = todo_html.replace("""height: 385.06px;
            width: 400px;""", """height: 100%;
            width: 100%;""")
        todo_html = todo_html.replace("""top: 225px;
              left: 15%;
              transform: translate(-50%, -50%);""", """display: flex;
              justify-content: center;
              align-items: center;
              """)
        todo_html = todo_html.replace("""border: solid rgb(189, 199, 207)""", "")
        self.web_view.setHtml(todo_html)  # Set the HTML content
        self.stacklayout.addWidget(self.web_view)

        # Tab 2

        btn = QPushButton("Completed")
        btn.setFixedSize(*btn_size)  # Apply the fixed size
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        self.completed_web_view = QWebEngineView()

        # Make background transparent
        self.completed_web_view.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.completed_web_view.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
        self.completed_web_view.page().setBackgroundColor(Qt.GlobalColor.transparent)

        todo_completed_html = str(html_list[1])
        # Remove absolute position statements
        todo_completed_html = todo_completed_html.replace("position: absolute;", "")
        # Change height and width
        todo_completed_html = todo_completed_html.replace("""height: 385.06px;
                            width: 400px;""", """height: 100%;
                            width: 100%;""")
        todo_completed_html = todo_completed_html.replace("transform: translate(-50%, -50%);", "")
        todo_completed_html = todo_completed_html.replace("height: 385.06px;", "height: 100%;")
        todo_completed_html = todo_completed_html.replace("width: 400px;", "width: 100%;")
        todo_completed_html = todo_completed_html.replace(""".example{
                visibility: hidden;""", """.example{""")
        # Hide remaining time
        todo_completed_html = todo_completed_html.replace(""".remainingtime {
            font: 0.95rem "Fira Sans", sans-serif;
            margin: 15px;
            margin-top: 8px;
            margin-left: 25px;
            }""", ".remainingtime {display: none;}")
        todo_completed_html = todo_completed_html.replace("""border: solid rgb(189, 199, 207)""", "")
        self.completed_web_view.setHtml(todo_completed_html)

        todo_completed_html = todo_completed_html.replace("""border: solid rgb(189, 199, 207)""", "")
        self.completed_web_view.setHtml(todo_completed_html)
        # Set the HTML content
        self.stacklayout.addWidget(self.completed_web_view)

        btn = QPushButton("Settings")
        btn.setFixedSize(*btn_size)  # Apply the fixed size
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)
        self.add_colored_widget("yellow")

        button_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)  # Prevent the layout from resizing the buttons

        # Create a new main layout
        main_layout = QVBoxLayout()

        # Add the button container and the stacklayout to the main layout
        main_layout.addWidget(self.button_container)
        main_layout.addLayout(self.stacklayout)

        # Set the alignment of the button container to Qt.AlignCenter
        main_layout.setAlignment(self.button_container, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

        self.setGeometry(100, 100, 800, 600)  # Adjust the values as needed
        self.activate_tab_1()  # Activate the first tab by default

    def add_colored_widget(self, color):
        widget = QWidget()
        palette = widget.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        widget.setPalette(palette)
        widget.setAutoFillBackground(True)
        self.stacklayout.addWidget(widget)

    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(2)

"""app = QApplication(sys.argv)
window = ToDoQtWindow()
window.show()
app.exec()"""
