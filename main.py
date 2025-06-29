import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox, QFileDialog, QStackedWidget, QHBoxLayout,
    QCheckBox, QComboBox
)
from PyQt5.QtGui import QIcon, QTextDocument
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtCore import Qt, QTimer
from link_scanner import is_suspicious_url
from file_scanner import is_suspicious_file
from utils import log_scan, read_logs


class SafeScanApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 SafeScan - Virus & Link Detector")
        self.setGeometry(300, 100, 800, 600)
        self.setWindowIcon(QIcon("icon.png"))

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.tabs = QTabWidget()
        self.init_tabs()

        self.clipboard_monitor = False
        self.dark_mode = False
        self.init_home_page()
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.tabs)
        self.stack.setCurrentWidget(self.home_page)

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_clipboard)

    def init_home_page(self):
        self.home_page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("🔐 <b>SafeScan - Virus & Link Detector</b>")
        title.setStyleSheet("font-size: 20px; text-align: center;")
        title.setAlignment(Qt.AlignCenter)

        start_button = QPushButton("🚀 Start Scanning")
        start_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.tabs))
        start_button.setStyleSheet("padding: 10px 20px; font-size: 16px; background-color: #28a745; color: white;")

        self.clipboard_checkbox = QCheckBox("📋 Enable Clipboard Monitoring")
        self.clipboard_checkbox.stateChanged.connect(self.toggle_clipboard_monitoring)

        self.theme_toggle = QPushButton("🌓 Toggle Theme")
        self.theme_toggle.clicked.connect(self.toggle_theme)

        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(start_button)
        layout.addWidget(self.clipboard_checkbox)
        layout.addWidget(self.theme_toggle)

        self.home_page.setLayout(layout)

    def toggle_clipboard_monitoring(self):
        self.clipboard_monitor = self.clipboard_checkbox.isChecked()
        if self.clipboard_monitor:
            self.timer.start(3000)  # check every 3 seconds
        else:
            self.timer.stop()

    def check_clipboard(self):
        clipboard_text = QApplication.clipboard().text()
        if clipboard_text and is_suspicious_url(clipboard_text):
            QMessageBox.warning(self, "Suspicious Link Detected in Clipboard", clipboard_text)

    def toggle_theme(self):
        if self.dark_mode:
            self.setStyleSheet("")
        else:
            self.setStyleSheet("background-color: #121212; color: white;")
        self.dark_mode = not self.dark_mode

    def init_tabs(self):
        self.link_tab = QWidget()
        self.init_link_tab()

        self.file_tab = QWidget()
        self.init_file_tab()

        self.report_tab = QWidget()
        self.init_report_tab()

        self.help_tab = QWidget()
        self.init_help_tab()

        self.tabs.addTab(self.link_tab, "🔗 Link Scanner")
        self.tabs.addTab(self.file_tab, "📁 File Scanner")
        self.tabs.addTab(self.report_tab, "📄 Reports")
        self.tabs.addTab(self.help_tab, "ℹ️ Help")

    def add_back_button(self, layout):
        back_btn = QPushButton("⬅️ Back to Home")
        back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.home_page))
        back_btn.setStyleSheet("padding: 5px; background-color: #dc3545; color: white;")
        layout.addWidget(back_btn)

    def init_link_tab(self):
        layout = QVBoxLayout()

        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("Enter or paste the URL to scan")
        self.link_input.setStyleSheet("padding: 8px; font-size: 14px;")

        self.scan_button = QPushButton("Scan Link")
        self.scan_button.clicked.connect(self.scan_link)
        self.scan_button.setStyleSheet("padding: 6px; background-color: #2d89ef; color: white;")

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setStyleSheet("background-color: #f0f0f0;")

        export_btn = QPushButton("🧾 Export to PDF")
        export_btn.clicked.connect(self.export_pdf)

        layout.addWidget(QLabel("🔍 Paste a link to check if it's suspicious:"))
        layout.addWidget(self.link_input)
        layout.addWidget(self.scan_button)
        layout.addWidget(QLabel("🧠 Scan Result:"))
        layout.addWidget(self.result_area)
        layout.addWidget(export_btn)
        self.add_back_button(layout)

        self.link_tab.setLayout(layout)

    def init_file_tab(self):
        layout = QVBoxLayout()

        self.file_result_area = QTextEdit()
        self.file_result_area.setReadOnly(True)
        self.file_result_area.setStyleSheet("background-color: #f0f0f0;")

        self.choose_file_button = QPushButton("📁 Choose File")
        self.choose_file_button.clicked.connect(self.select_file)
        self.choose_file_button.setStyleSheet("padding: 6px; background-color: #2d89ef; color: white;")

        layout.addWidget(QLabel("🔍 Select a file to scan for virus/malware:"))
        layout.addWidget(self.choose_file_button)
        layout.addWidget(QLabel("🧠 Scan Result:"))
        layout.addWidget(self.file_result_area)
        self.add_back_button(layout)

        self.file_tab.setLayout(layout)

    def init_report_tab(self):
        layout = QVBoxLayout()

        self.report_area = QTextEdit()
        self.report_area.setReadOnly(True)
        self.report_area.setStyleSheet("background-color: #f9f9f9;")

        self.refresh_button = QPushButton("🔄 Refresh Logs")
        self.refresh_button.clicked.connect(self.load_logs)
        self.refresh_button.setStyleSheet("padding: 6px; background-color: #777; color: white;")

        layout.addWidget(QLabel("📄 Scan History:"))
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.report_area)
        self.add_back_button(layout)

        self.report_tab.setLayout(layout)
        self.load_logs()

    def init_help_tab(self):
        layout = QVBoxLayout()

        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setStyleSheet("background-color: #fdfdfd; font-size: 14px;")

        help_content = """
            🛡️ <b>SafeScan - Virus & Link Detector</b><br>
            <b>Version:</b> 1.0.0<br><br>
            <b>What it does:</b><br>
            • Scans suspicious or phishing URLs<br>
            • Scans files for malicious extensions and known virus hashes<br>
            • Maintains scan history in <code>report_log.txt</code><br>
            • Works offline — no API key required<br>
            • Optional icon support for professional look<br><br>
            <b>How to Use:</b><br>
            1. <b>Link Scanner:</b> Paste a link, click 'Scan Link', and check result.<br>
            2. <b>File Scanner:</b> Select a file and let it check for threats.<br>
            3. <b>Reports:</b> View previous scan history anytime.<br>
            4. <b>Help:</b> You're here 🙂<br><br>
            <b>Made for educational & security awareness purposes only.</b><br>
            Use responsibly!<br><br>
            <b>Developed by:</b> Sunil Jat 😉
            """

        help_text.setHtml(help_content)
        layout.addWidget(help_text)
        self.add_back_button(layout)

        self.help_tab.setLayout(layout)

    def scan_link(self):
        url = self.link_input.text().strip()
        if not url:
            QMessageBox.warning(self, "No Link", "Please enter a link to scan.")
            return

        result = ""
        if is_suspicious_url(url):
            result = "⚠️ This link seems suspicious! Avoid clicking it.\n\n🔎 Link: " + url
        else:
            result = "✅ This link looks safe.\n\n🔎 Link: " + url

        self.result_area.setText(result)
        log_scan(f"Link Scan - {url} - {'SUSPICIOUS' if is_suspicious_url(url) else 'SAFE'}")

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Scan")
        if file_path:
            result = is_suspicious_file(file_path)
            self.file_result_area.setText(f"🔎 File: {file_path}\n\n{result}")
            log_scan(f"File Scan - {file_path} - {result.splitlines()[-1]}")

    def load_logs(self):
        logs = read_logs()
        self.report_area.setText(logs)

    def export_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export Result to PDF", "scan_result.pdf", "PDF Files (*.pdf)")
        if filename:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(filename)
            doc = QTextDocument()
            doc.setPlainText(self.result_area.toPlainText())
            doc.print_(printer)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SafeScanApp()
    window.show()
    sys.exit(app.exec_())

