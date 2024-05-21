import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QStackedLayout, QLayout, \
    QSizePolicy, QComboBox, QLabel, QSpacerItem
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView  # Import QWebEngineView


class ToDoQtWindows(QWidget):
    def __init__(self, todo, mainwindows):
        super().__init__()
        # self.setWindowTitle("My App")
        self.mw = mainwindows

        # Create a new widget container for buttons
        self.button_container = QWidget()
        self.button_container.setFixedSize(800, 80)  # Set a fixed size for the container (adjusted width)

        # Set the layout of the button container to QHBoxLayout
        main_button_layout = QHBoxLayout(self.button_container)
        main_button_layout.setSpacing(10)  # Set a 10px spacing between buttons
        self.stacklayout = QStackedLayout()

        btn_size = (130, 25)  # Set a fixed size for buttons (adjusted height)

        # Render htmls:
        html_list = todo.render_tasks([todo.get_all_task(), todo.get_all_completed()])

        # Tab 1
        btn_todo = QPushButton("To do")
        btn_todo.setFixedSize(*btn_size)  # Apply the fixed size
        btn_todo.pressed.connect(self.activate_tab_1)
        main_button_layout.addWidget(btn_todo)

        # Replace the colored widget with a QWebEngineView widget for tab 1
        self.web_view = QWebEngineView()

        # Make background transparent
        self.web_view.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.web_view.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
        self.web_view.page().setBackgroundColor(Qt.GlobalColor.transparent)

        todo_html = str(html_list[0])
        # Remove absolute position statements
        todo_html = todo_html.replace("position: absolute;", "")
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
        btn_completed = QPushButton("Completed")
        btn_completed.setFixedSize(*btn_size)  # Apply the fixed size
        btn_completed.pressed.connect(self.activate_tab_2)
        main_button_layout.addWidget(btn_completed)
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

        self.stacklayout.addWidget(self.completed_web_view)

        btn_settings = QPushButton("Settings")
        btn_settings.setFixedSize(*btn_size)  # Apply the fixed size
        btn_settings.pressed.connect(self.activate_tab_3)
        main_button_layout.addWidget(btn_settings)

        # Tab 3
        # Create a widget for the "Settings" tab
        self.settings_widget = QWidget()
        settings_widget_layout = QVBoxLayout(self.settings_widget)

        # Add spacers to center elements vertically
        settings_widget_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.pause_deck_config_label = QLabel("Pause deck config")
        self.pause_deck_config_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_widget_layout.addWidget(self.pause_deck_config_label)

        pause_deck_config_dropdown_container = QWidget()
        pause_deck_config_dropdown_layout = QHBoxLayout(pause_deck_config_dropdown_container)
        pause_deck_config_dropdown_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pause_deck_config_dropdown = QComboBox()
        self.pause_deck_config_dropdown.setFixedWidth(300)  # Set fixed width

        # Get all configs than add each to the list
        configs = todo.getAllDeckConfigNames()
        for e in configs:
            self.pause_deck_config_dropdown.addItem(e)

        pause_deck_config_dropdown_layout.addWidget(self.pause_deck_config_dropdown)
        settings_widget_layout.addWidget(pause_deck_config_dropdown_container)

        # Add some spacing between the widgets
        settings_widget_layout.addSpacing(5)

        add_deck_button_container = QWidget()
        add_deck_button_layout = QHBoxLayout(add_deck_button_container)
        add_deck_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_deck_button = QPushButton("Set pause deck config")
        self.add_deck_button.setFixedWidth(300)  # Set fixed width
        add_deck_button_layout.addWidget(self.add_deck_button)
        settings_widget_layout.addWidget(add_deck_button_container)
        self.add_deck_button.pressed.connect(lambda: todo.setPauseConfig(self.pause_deck_config_dropdown.currentText()))

        # Add another spacer to center elements vertically
        settings_widget_layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.stacklayout.addWidget(self.settings_widget)

        # Add a stretch to push the "Add Task" button to the right
        main_button_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Tab 4
        # Add the "Add Task" tab
        self.btn_add_task = QPushButton("Manage tasks")
        self.btn_add_task.setFixedSize(*btn_size)  # Apply the fixed size
        self.btn_add_task.pressed.connect(self.activate_tab_4)
        main_button_layout.addWidget(self.btn_add_task)

        # Create a widget for the "Add Task" tab
        self.add_task_widget = QWidget()
        add_task_layout = QVBoxLayout(self.add_task_widget)

        # Add spacers to center elements vertically
        add_task_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Create the dropdowns and the button with fixed width and margins
        self.deck_label = QLabel("Deck")
        self.deck_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        add_task_layout.addWidget(self.deck_label)

        deck_dropdown_container = QWidget()
        deck_dropdown_layout = QHBoxLayout(deck_dropdown_container)
        deck_dropdown_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.deck_dropdown = QComboBox()
        self.deck_dropdown.setFixedWidth(300)  # Set fixed width

        # Get all decks than add each to the list
        decks = todo.get_deck_names()
        for e in decks:
            self.deck_dropdown.addItem(e)
        deck_dropdown_layout.addWidget(self.deck_dropdown)
        add_task_layout.addWidget(deck_dropdown_container)

        # Add some spacing between the widgets
        add_task_layout.addSpacing(5)

        self.future_config_label = QLabel("Future Config")
        self.future_config_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        add_task_layout.addWidget(self.future_config_label)

        future_config_dropdown_container = QWidget()
        future_config_dropdown_layout = QHBoxLayout(future_config_dropdown_container)
        future_config_dropdown_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.future_config_dropdown = QComboBox()
        self.future_config_dropdown.setFixedWidth(300)  # Set fixed width

        # Get all configs than add each to the list
        configs = todo.getAllDeckConfigNames()
        for e in configs:
            self.future_config_dropdown.addItem(e)

        future_config_dropdown_layout.addWidget(self.future_config_dropdown)
        add_task_layout.addWidget(future_config_dropdown_container)

        # Add some spacing between the widgets
        add_task_layout.addSpacing(5)

        add_deck_button_container = QWidget()
        add_deck_button_layout = QHBoxLayout(add_deck_button_container)
        add_deck_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_deck_button = QPushButton("Add task")
        self.add_deck_button.setFixedWidth(300)  # Set fixed width
        add_deck_button_layout.addWidget(self.add_deck_button)
        add_task_layout.addWidget(add_deck_button_container)
        self.add_deck_button.pressed.connect(lambda: self.add_deck_button_pressed(todo))

        add_task_layout.addSpacing(20)

        # Remove task
        self.remove_task_label = QLabel("Remove task")
        self.remove_task_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        add_task_layout.addWidget(self.remove_task_label)

        remove_task_dropdown_container = QWidget()
        remove_task_dropdown_layout = QHBoxLayout(remove_task_dropdown_container)
        remove_task_dropdown_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.remove_task_dropdown = QComboBox()
        self.remove_task_dropdown.setFixedWidth(300)  # Set fixed width

        # Get all tasks
        configs = todo.get_all_task()
        for e in configs:
            self.remove_task_dropdown.addItem(e)

        remove_task_dropdown_layout.addWidget(self.remove_task_dropdown)
        add_task_layout.addWidget(remove_task_dropdown_container)

        # Add some spacing between the widgets
        add_task_layout.addSpacing(5)

        remove_task_button_container = QWidget()
        remove_task_button_layout = QHBoxLayout(remove_task_button_container)
        remove_task_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.remove_task_button = QPushButton("Remove task")
        self.remove_task_button.setFixedWidth(300)  # Set fixed width
        remove_task_button_layout.addWidget(self.remove_task_button)
        add_task_layout.addWidget(remove_task_button_container)
        self.remove_task_button.pressed.connect(lambda: self.remove_task_button_pressed(todo))

        # Add another spacer to center elements vertically
        add_task_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.stacklayout.addWidget(self.add_task_widget)

        main_button_layout.setSizeConstraint(
            QLayout.SizeConstraint.SetFixedSize)  # Prevent the layout from resizing the buttons

        # Create a new main layout
        main_layout = QVBoxLayout()

        # Add the button container and the stacklayout to the main layout
        main_layout.addWidget(self.button_container)
        main_layout.addLayout(self.stacklayout)

        # Set the alignment of the button container to Qt.AlignmentFlag.AlignCenter
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

    def activate_tab_4(self):
        self.stacklayout.setCurrentIndex(3)

    def add_deck_button_pressed(self, todo):
        # fetch current texts
        selected_deck = self.deck_dropdown.currentText()
        selected_config = self.future_config_dropdown.currentText()

        todo.add_new_deck_to_task(selected_deck, selected_config)
        self.mw.reset()

    def remove_task_button_pressed(self, todo):
        todo.removeTask(self.remove_task_dropdown.currentText())
        self.mw.reset()

# Uncomment the lines below to run the application
# app = QApplication(sys.argv)
# window = ToDoQtWindows(todo)
# window.show()
# app.exec()
