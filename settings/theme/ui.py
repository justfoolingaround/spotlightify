from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QWidget, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont, QIcon

from settings.theme.themes import themes, Theme
from definitions import ASSETS_DIR
from os import sep


class ThemeUI(QDialog):
    def __init__(self):
        QDialog.__init__(self, None, Qt.WindowTitleHint)

        self.theme_dict = {
            "name": "",
            "foreground": "",
            "background": "",
            "accent": "",
            "hover": "",
            "focus": ""
        }

        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(450, 383)
        self.setWindowTitle("Spotlightify - Theme Config - New Theme")
        self.setWindowIcon(QIcon(f"{ASSETS_DIR}svg{sep}theme-icon"))

        self.setStyleSheet(f"background-color: {themes['Dark'].background}; color: {themes['Dark'].foreground}")

        self.layout_widget = VerticalLayout(self)
        self.layout_widget.setGeometry(QRect(10, 10, 440, 343))

        self.layout_widget.add(InputField(label="Theme Name", store=self.theme_dict, field="name", required_length=2, max_length=19))
        self.layout_widget.add(
            InputField(label="Background Color", store=self.theme_dict, field="background", required_length=7, max_length=7))
        self.layout_widget.add(
            InputField(label="Accent Color", store=self.theme_dict, field="accent", required_length=7, max_length=7))
        self.layout_widget.add(
            InputField(label="Foreground Color", store=self.theme_dict, field="foreground", required_length=7, max_length=7))
        self.layout_widget.add(
            InputField(label="Hover Color", store=self.theme_dict, field="hover", required_length=7, max_length=7))
        self.layout_widget.add(
            InputField(label="Focus Color", store=self.theme_dict, field="focus", required_length=7, max_length=7))

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(10, 347, 300, 23))
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        self.buttonBox.accepted.connect(self.save_changes)
        self.buttonBox.rejected.connect(self.close)

    def new_theme(self):
        self.setWindowTitle("Spotlightify Theme Config - New Theme")
        # update theme dict without changing instance variable reference
        new_dict = {
            "name": "",
            "foreground": "",
            "background": "",
            "accent": "",
            "hover": "",
            "focus": ""
        }
        self.theme_dict.update(new_dict)
        for w in self.layout_widget.children():
            w.textbox.clear()  # erase contents of text boxes
        self.show()

    def edit_theme(self, theme):
        self.setWindowTitle(f"Spotlightify Theme Config - {theme.name}")
        # update theme dict without changing instance variable reference
        new_dict = theme.to_dict()
        self.theme_dict.update(new_dict)
        for w in self.layout_widget.children():
            w.textbox.setText(self.theme_dict[w.field])  # add content to text boxes
        self.show()

    def save_changes(self):
        checks = self.check_validity()
        if checks == "":
            th = Theme.dict_to_theme(self.theme_dict)
            Theme.save_theme(th)
            self.close()
        else:
            QMessageBox.warning(self, "Error", "The fields below have not been filled in correctly:\n" +
                                checks, QMessageBox.Ok)

    def check_validity(self) -> str:
        self.checks = [self.character_checks(), self.name_checks()]  # gets errors as an array of strings
        if not any(self.checks):
            return ""
        else:
            return "\n".join([err for err in self.checks])

    def character_checks(self) -> str:
        widgets = self.layout_widget.children()
        err = []
        if not all([w.text_complete for w in widgets]):
            err.extend([w.label.text() for w in widgets if not w.text_complete])
        elif not all([w.textbox.text()[0] == "#" for w in widgets if w.label.text() != "Theme Name"]):
            err.append("'#' must be put before each hex color value")
        if len(err) == 0:
            return ""
        else:
            return "\n".join(err)

    def hex_check(self):
        pass

    def name_checks(self) -> str:
        return ""

        # if self.theme_dict["name"] in themes.keys():
        #     self.buttonBox = QDialogButtonBox(self)
        #     self.buttonBox.setGeometry(QRect(10, 347, 300, 23))
        #     self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        #     self.buttonBox.accepted.connect(lambda: self.checks.append("Theme name is already in use"))
        #     self.buttonBox.rejected.connect(self.close)
        # return


class VerticalLayout(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent=parent)
        self.vertical_layout = QVBoxLayout(self)

    def add(self, widget: QWidget):
        self.vertical_layout.addWidget(widget)

    def children(self):
        return super(VerticalLayout, self).children()[1:]


class InputField(QWidget):
    def __init__(self, label: str, store: dict, field: str, max_length=32, required_length=1):
        QWidget.__init__(self)
        self.setFixedSize(400, 300)

        self.max_length = max_length
        self.required_length = required_length
        self.text_complete = False
        self.store = store
        self.field = field

        self.font = QFont()
        self.font.setFamily("SF Pro Display")
        self.font.setPointSize(11)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(25, 5, 190, 30))
        self.label.setFont(self.font)
        self.label.setText(label)

        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(QRect(185, 5, 190, 30))
        self.textbox.setFont(self.font)
        self.textbox.textChanged.connect(self.field_changed)
        self.textbox.setText(store[field])
        self.textbox.setMaxLength(max_length)

    def field_changed(self):
        text = self.textbox.text()

        self.store[self.field] = text

        if len(text) >= self.required_length:
            self.text_complete = True
            self.textbox.setStyleSheet("border: 1px solid #006600;")
        else:
            self.text_complete = False
            self.textbox.setStyleSheet("border: 1px solid #4d0000;")
