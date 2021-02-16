from enum import Enum

from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from app.services.contact_service import ContactService

from .ui_main_window import Ui_MainWindow


class EditMode(Enum):
    NONE = None
    EDIT = "edit"
    CREATE = "create"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.filename = "data/contacts.json"
        self.contacts_service = ContactService(self.filename)

        self.contacts_model = QStandardItemModel()
        self.contacts_model.setColumnCount(3)

        self.fill_list_view()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.contactListView.setModel(self.contacts_model)
        self.ui.nameEdit.textChanged.connect(self.on_contact_line_edit_change)
        self.ui.emailEdit.textChanged.connect(self.on_contact_line_edit_change)
        self.ui.numberEdit.textChanged.connect(self.on_contact_line_edit_change)
        self.ui.deleteButton.clicked.connect(self.on_delete)

        self.current_row = None
        self.mode = EditMode.NONE

    def fill_list_view(self):
        self.contacts_model.clear()
        self.contacts_model.setHorizontalHeaderLabels(["Name", "Email", "Number"])
        for contact in self.contacts_service.get_contacts():
            self.contacts_model.appendRow([
                QStandardItem(contact.name),
                QStandardItem(contact.email),
                QStandardItem(contact.number)
            ])

    def on_contact_line_edit_change(self, value):
        if self.mode == EditMode.EDIT or self.mode == EditMode.CREATE:
            return

        self.mode = EditMode.CREATE

        self.ui.saveButton.setEnabled(True)
        self.ui.cancelButton.setEnabled(True)

    def on_contactListView_clicked(self, index: QModelIndex):
        print(index.data())

        num_to_edit = index.row() + 1
        contact = self.contacts_service.get_contact(num_to_edit)

        self.current_row = num_to_edit
        self.mode = EditMode.EDIT

        self.ui.nameEdit.setText(contact.name)
        self.ui.emailEdit.setText(contact.email)
        self.ui.numberEdit.setText(contact.number)

        self.ui.deleteButton.setEnabled(True)
        self.ui.cancelButton.setEnabled(True)
        self.ui.saveButton.setEnabled(True)

    def on_cancelButton_clicked(self):
        self.ui.nameEdit.clear()
        self.ui.emailEdit.clear()

        self.ui.deleteButton.setEnabled(False)
        self.ui.cancelButton.setEnabled(False)
        self.ui.saveButton.setEnabled(False)

        self.ui.contactListView.clearSelection()
        self.current_row = None
        self.mode = EditMode.NONE

    def on_saveButton_clicked(self):
        name = self.ui.nameEdit.text().strip()
        email = self.ui.emailEdit.text().strip()
        number = self.ui.numberEdit.text().strip()

        if not name:
            self.ui.nameEdit.setFocus()
            self.ui.nameEdit.setToolTip("Name can't be empty")
            return

        if not email:
            self.ui.emailEdit.setFocus()
            self.ui.emailEdit.setToolTip("Email can't be empty")
            return

        if not number:
            self.ui.numberEdit.setFocus()
            self.ui.numberEdit.setFocus()
            return

        if self.mode == EditMode.EDIT:
            self.contacts_service.update(self.current_row, name, email, number)
            self.ui.statusbar.showMessage("Contact saved", 3000)
            QMessageBox.information(self, "Success", "Contact was successfully saved!")
        else:
            self.contacts_service.create(name, email, number)
            self.ui.statusbar.showMessage("Contact created", 3000)
            QMessageBox.information(self, "Success", "Contact was successfully created!")

        self.on_cancelButton_clicked()

        self.fill_list_view()

    def on_delete(self):
        response = QMessageBox.question(self, "Confirm delete", "Do you really want to delete this contact?")
        if response != QMessageBox.Yes:
            return

        self.contacts_service.remove(self.current_row)

        self.ui.statusbar.showMessage("Contact removed", 3000)
        QMessageBox.information(self, "Success", "Contact was successfully deleted!")

        self.on_cancelButton_clicked()
        self.fill_list_view()