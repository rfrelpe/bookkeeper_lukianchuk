import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QPushButton,
    QDialog,
    QFormLayout,
    QLineEdit,
    QWidget,
    QLabel,
    QFileDialog,
    QMessageBox,
)

from datetime import date

from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("My Silly Prog")

        self.day_budget = 0
        self.week_budget = 0
        self.month_budget = 0

        self.path = "../../databases/test_sql.db"
        self.repo = SQLiteRepository(db_name=self.path, entry_cls=Expense)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["pk", "Date", "amount", "Category", "Comment"]
        )
        self.table_update()

        add_button = QPushButton("Add Row")
        add_button.clicked.connect(self.add_row)
        remove_button = QPushButton("Remove Selected Row")
        remove_button.clicked.connect(self.remove_row)
        set_budget_button = QPushButton("Set budget")
        set_budget_button.clicked.connect(self.set_budget)
        set_file_button = QPushButton("Load file")
        set_file_button.clicked.connect(self.set_load_path)

        button_layout = QVBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(set_budget_button)
        button_layout.addWidget(set_file_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table)
        main_layout.addLayout(button_layout)

        self.sum_widget = QWidget()
        sum_layout = QFormLayout()

        today_label = QLabel("Today:")
        self.today_sum_label = QLabel("0.00")
        week_label = QLabel("This Week:")
        self.week_sum_label = QLabel("0.00")
        month_label = QLabel("This Month:")
        self.month_sum_label = QLabel("0.00")

        sum_layout.addRow(today_label, self.today_sum_label)
        sum_layout.addRow(week_label, self.week_sum_label)
        sum_layout.addRow(month_label, self.month_sum_label)

        self.sum_widget.setLayout(sum_layout)
        main_layout.addWidget(self.sum_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.upperiodsums()

    def add_row(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Row")
        layout = QFormLayout()

        periodinput = QLineEdit()
        layout.addRow("Date (YYYY-MM-DD):", periodinput)
        summ_input = QLineEdit()
        layout.addRow("amount:", summ_input)
        category_input = QLineEdit()
        layout.addRow("Category:", category_input)
        comment_input = QLineEdit()
        layout.addRow("Comment:", comment_input)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(
            lambda: self.submit_row(
                dialog,
                periodinput.text(),
                summ_input.text(),
                category_input.text(),
                comment_input.text(),
            )
        )
        layout.addRow(submit_button)

        dialog.setLayout(layout)
        dialog.exec()

    def submit_row(
        self, dialog, periodval, summ_val, category_val, comment_val
    ) -> None:
        try:
            periodval = date.fromisoformat(periodval)
            summ_val = float(summ_val)
            assert summ_val > 0
            assert isinstance(category_val, str)
            assert isinstance(comment_val, str)
        except (ValueError, AssertionError):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wrong data!")
            msg.setWindowTitle("Error")
            msg.exec()
            dialog.reject()
            return

        obj = Expense(
            expense_date=str(periodval),
            amount=str(summ_val),
            category=category_val,
            comment=comment_val,
        )

        self.repo.add(obj)

        self.table_update()
        self.upperiodsums()

        dialog.accept()

    def remove_row(self):
        selected = self.table.currentRow()
        print(selected)
        if selected != -1:
            self.repo.delete(int(self.table.item(selected, 0).text()))
            self.table_update()
        self.upperiodsums()

    def upperiodsums(self):
        today = date.today()
        today_sum = 0
        week_sum = 0
        month_sum = 0

        for row in range(self.table.rowCount()):
            periodstr = self.table.item(row, 1).text()
            amount_str = self.table.item(row, 2).text()
            try:
                amount = float(amount_str)
            except ValueError:
                continue

            periodval = date.fromisoformat(periodstr)

            if periodval == today:
                today_sum += amount

            if (
                periodval.isocalendar()[1] == today.isocalendar()[1]
                and periodval.year == today.year
            ):
                week_sum += amount

            if periodval.month == today.month and periodval.year == today.year:
                month_sum += amount

        self.today_sum_label.setText(
            "{:.2f} / {:.2f}".format(today_sum, self.day_budget)
        )
        if today_sum > self.day_budget:
            self.today_sum_label.setStyleSheet("QLabel { color : red; }")
        else:
            self.today_sum_label.setStyleSheet("")

        self.week_sum_label.setText(
            "{:.2f} / {:.2f}".format(week_sum, self.week_budget)
        )
        if week_sum > self.week_budget:
            self.week_sum_label.setStyleSheet("QLabel { color : red; }")
        else:
            self.week_sum_label.setStyleSheet("")

        self.month_sum_label.setText(
            "{:.2f} / {:.2f}".format(month_sum, self.month_budget)
        )
        if month_sum > self.month_budget:
            self.month_sum_label.setStyleSheet("QLabel { color : red; }")
        else:
            self.month_sum_label.setStyleSheet("")

    def set_budget(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Set Budget")
        layout = QFormLayout()

        day_budget_input = QLineEdit()
        layout.addRow("Day budget:", day_budget_input)
        week_budget_input = QLineEdit()
        layout.addRow("Week budget:", week_budget_input)
        month_budget_input = QLineEdit()
        layout.addRow("Month budget:", month_budget_input)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(
            lambda: self.submit_budget(
                dialog,
                day_budget_input.text(),
                week_budget_input.text(),
                month_budget_input.text(),
            )
        )
        layout.addRow(submit_button)

        dialog.setLayout(layout)
        dialog.exec()

    def submit_budget(self, dialog, day_budget, week_budget, month_budget):
        try:
            day_budget = float(day_budget)
            week_budget = float(week_budget)
            month_budget = float(month_budget)
            assert day_budget > 0
            assert week_budget > 0
            assert month_budget > 0
        except (ValueError, AssertionError):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wrong budget!")
            msg.setWindowTitle("Error")
            msg.exec()
            dialog.reject()
            return

        self.day_budget = day_budget
        self.week_budget = week_budget
        self.month_budget = month_budget
        self.upperiodsums()

        dialog.accept()

    def set_load_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Table File", "", "Table Files (*.db)", options=options
        )

        if file_name:
            self.path = file_name
            self.repo = SQLiteRepository(db_name=self.path, entry_cls=Expense)

    def table_update(self):

        self.table.clearContents()
        self.table.setRowCount(0)

        if self.repo.get_all_where() is not None:
            L = [
                [str(x.pk), x.expense_date, x.amount, x.category, x.comment]
                for x in self.repo.get_all_where()
            ]
            for row in L:
                # Add new row to table
                row_count = self.table.rowCount()
                self.table.setRowCount(row_count + 1)

                item0 = QTableWidgetItem(row[0])
                item1 = QTableWidgetItem(row[1])
                item2 = QTableWidgetItem(row[2])
                item3 = QTableWidgetItem(row[3])
                item4 = QTableWidgetItem(row[4])

                self.table.setItem(row_count, 0, item0)
                self.table.setItem(row_count, 1, item1)
                self.table.setItem(row_count, 2, item2)
                self.table.setItem(row_count, 3, item3)
                self.table.setItem(row_count, 4, item4)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
