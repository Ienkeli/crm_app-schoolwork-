from PyQt5 import QtWidgets, QtGui, QtCore
from ..db import connection
from ..utils import normalize_phone, format_phone_for_db
from .add_client_dialog import AddClientDialog
from .add_order_dialog import AddOrderDialog

class DatabaseWindow(QtWidgets.QWidget):
    def __init__(self, user_id, full_name: str):
        super().__init__()
        self.user_id = user_id
        self.full_name = full_name
        self.setWindowTitle("CRM — Клиенты / Заказы")
        self.resize(1100, 700)

        main_layout = QtWidgets.QVBoxLayout()
        header_layout = QtWidgets.QHBoxLayout()
        lbl = QtWidgets.QLabel(f"Вы вошли как: {self.full_name}")
        lbl.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
        header_layout.addWidget(lbl)
        header_layout.addStretch()
        self.btn_my_orders = QtWidgets.QPushButton("Мои заказы")
        self.btn_my_orders.clicked.connect(self.load_my_orders)
        header_layout.addWidget(self.btn_my_orders)
        main_layout.addLayout(header_layout)

        self.tabs = QtWidgets.QTabWidget()
        main_layout.addWidget(self.tabs)

        # Clients tab
        self.tab_clients = QtWidgets.QWidget()
        self.tabs.addTab(self.tab_clients, "Клиенты")
        clients_layout = QtWidgets.QVBoxLayout()
        clients_toolbar = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Поиск: ФИО, телефон или email...")
        self.search_input.textChanged.connect(self.filter_clients_table)
        clients_toolbar.addWidget(self.search_input)
        self.btn_add_client = QtWidgets.QPushButton("Добавить клиента")
        self.btn_add_client.clicked.connect(self.add_client)
        clients_toolbar.addWidget(self.btn_add_client)
        clients_layout.addLayout(clients_toolbar)

        self.table_clients = QtWidgets.QTableWidget()
        self.table_clients.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_clients.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_clients.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_clients.doubleClicked.connect(self.on_client_double_click)
        clients_layout.addWidget(self.table_clients)
        self.tab_clients.setLayout(clients_layout)

        # Orders tab
        self.tab_orders = QtWidgets.QWidget()
        self.tabs.addTab(self.tab_orders, "Заказы")
        orders_layout = QtWidgets.QVBoxLayout()
        orders_toolbar = QtWidgets.QHBoxLayout()
        self.btn_refresh_orders = QtWidgets.QPushButton("Обновить заказы")
        self.btn_refresh_orders.clicked.connect(self.load_orders)
        orders_toolbar.addWidget(self.btn_refresh_orders)
        orders_toolbar.addStretch()
        orders_layout.addLayout(orders_toolbar)
        self.btn_add_order = QtWidgets.QPushButton("Добавить заказ")
        self.btn_add_order.clicked.connect(self.add_order)
        orders_toolbar.addWidget(self.btn_add_order)
        self.table_orders = QtWidgets.QTableWidget()
        self.table_orders.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_orders.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        orders_layout.addWidget(self.table_orders)
        self.tab_orders.setLayout(orders_layout)

        self.setLayout(main_layout)
        self.apply_style()
        self.load_clients()
        self.load_orders()

    def add_order(self):
        dlg = AddOrderDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            data = dlg.get_data()

            try:
                with connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            INSERT INTO zakazi (client_id, description, weight, created_at)
                            VALUES (%s, %s, %s, %s);
                        """, (data["client_id"], data["description"], data["weight"], data["date"]))

                self.load_orders()
                QtWidgets.QMessageBox.information(self, "OK", "Заказ добавлен")

            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось добавить заказ:\n{e}")

    # ---------- DB methods ----------
    def load_clients(self):
        try:
            with connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, full_name, phone, mail, request_date, note FROM clients ORDER BY id DESC;")
                    rows = cur.fetchall()
                    cols = [d[0] for d in cur.description] if cur.description else []
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить клиентов:\n{e}")
            rows, cols = [], []
        self.populate_table(self.table_clients, rows, cols)

    def load_orders(self):
        try:
            with connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, client_id, description, weight, created_at FROM zakazi ORDER BY id DESC;")
                    rows = cur.fetchall()
                    cols = [d[0] for d in cur.description] if cur.description else []
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить заказы:\n{e}")
            rows, cols = [], []
        self.populate_table(self.table_orders, rows, cols)

    def load_my_orders(self):
        try:
            with connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, client_id, description, weight, created_at FROM zakazi WHERE client_id=%s ORDER BY id DESC;", (self.user_id,))
                    rows = cur.fetchall()
                    cols = [d[0] for d in cur.description] if cur.description else []
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить ваши заказы:\n{e}")
            rows, cols = [], []
        self.tabs.setCurrentWidget(self.tab_orders)
        self.populate_table(self.table_orders, rows, cols)

    # ---------- UI helpers ----------
    def populate_table(self, table, rows, columns):
        table.clear()
        table.setRowCount(len(rows))
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                table.setItem(r, c, QtWidgets.QTableWidgetItem("" if val is None else str(val)))
        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)

    def filter_clients_table(self):
        text = self.search_input.text().strip().lower()
        for r in range(self.table_clients.rowCount()):
            visible = any(text in (self.table_clients.item(r, c).text().lower() if self.table_clients.item(r, c) else "") for c in range(self.table_clients.columnCount()))
            self.table_clients.setRowHidden(r, not visible)

    def add_client(self):
        dlg = AddClientDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            data = dlg.get_data()
            norm = normalize_phone(data["phone"])
            if not norm:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Телефон некорректен")
                return
            db_phone = format_phone_for_db(norm)
            try:
                with connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("INSERT INTO clients (full_name, phone, mail, request_date, note) VALUES (%s,%s,%s,%s,%s);",
                                    (data["full_name"], db_phone, data["email"], data["request_date"], data["note"]))
                self.load_clients()
                QtWidgets.QMessageBox.information(self, "OK", "Клиент добавлен")
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось добавить клиента:\n{e}")

    def on_client_double_click(self, idx):
        row = idx.row()
        client_id = self.table_clients.item(row, 0).text() if self.table_clients.item(row, 0) else None
        if not client_id: return
        try:
            with connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, client_id, description, weight, created_at FROM zakazi WHERE client_id=%s ORDER BY id DESC;", (client_id,))
                    rows = cur.fetchall()
                    cols = [d[0] for d in cur.description] if cur.description else []
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить заказы клиента:\n{e}")
            return
        self.tabs.setCurrentWidget(self.tab_orders)
        self.populate_table(self.table_orders, rows, cols)

    def apply_style(self):
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: #e6e6e6; font-family: Arial; font-size: 13px; }
            QTabWidget::pane { border:0; }
            QTabBar::tab { background: #1f1f1f; color: #e6e6e6; padding: 10px; border-radius:6px; min-width:140px; }
            QTabBar::tab:selected { background:#222; color:#fff; }
            QLineEdit, QDateEdit, QTextEdit { background:#1b1b1b; border:1px solid #333; padding:6px; border-radius:6px; color:#e6e6e6; }
            QPushButton { background:#2b2b2b; border:1px solid #444; padding:8px 12px; border-radius:6px; }
            QPushButton:hover { background:#3a3a3a; }
            QTableWidget { background:#0f0f0f; gridline-color:#2a2a2a; }
            QHeaderView::section { background:#1e1e1e; padding:6px; border:none; }
        """)
