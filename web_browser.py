import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout,QCompleter,QListWidgetItem,QHBoxLayout,QDialog,QListWidget, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl,QStringListModel
from PyQt5.QtWidgets import QMessageBox

class BrowserWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Web Browser")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.search_label = QLabel("Search here:")
        self.search_bar = QLineEdit()
        self.search_bar.setMaximumHeight(50)
        self.search_bar.returnPressed.connect(self.search)


        self.load_page_button = QPushButton("Search Page")
        
        self.load_page_button.clicked.connect(self.load_page)
        self.load_page_button.setMaximumWidth(100)


        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.search_label)
        search_layout = QHBoxLayout()  # New layout for search bar and load button
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.load_page_button)
        self.layout.addLayout(search_layout)  # Adding the new layout
        self.layout.addWidget(self.search_label)
        
        self.layout.addWidget(self.tabs)
        self.central_widget.setLayout(self.layout)

        self.setCentralWidget(self.central_widget)

        self.add_tab("https://www.indiatv.in/livetv", "India Tv")
        self.bookmark_button = QPushButton("Add Bookmark")
        self.bookmark_button.clicked.connect(self.add_bookmark)

# Add the bookmark button to the layout
        search_layout.addWidget(self.bookmark_button)

    # Initialize a list to store bookmarks
        self.bookmarks = []
        self.show_bookmarks_button = QPushButton("Show Bookmarks")
        self.show_bookmarks_button.clicked.connect(self.show_bookmarks)
        search_layout.addWidget(self.show_bookmarks_button)
        
        # Implement smart suggestions
        self.model = QStringListModel()
        self.completer = QCompleter()
        self.completer.setModel(self.model)
        self.search_bar.setCompleter(self.completer)


        # Set initial suggestions
        self.set_suggestions(["https://www.google.com/", "https://www.wikipedia.org/", "https://www.youtube.com/","https://www.instagram.com/","https://www.facebook.com/","https://www.linkedin.com/","https://www.amazon.com/","https://www.flipkart.com/","https://www.myntra.com/","https://www.netflix.com/","https://web.whatsapp.com/","https://twitter.com/","https://www.amazon.com/","https://forms.gle/","file:///C:/Users/Lenovo/Desktop/learning%20html/forms.html" ])
   
    def add_tab(self, url, label):
     tab = QWidget()
     layout = QVBoxLayout()
     browser = QWebEngineView()
     browser.setUrl(QUrl(url))  # Convert string URL to QUrl object
     layout.addWidget(browser)
     tab.setLayout(layout)
     self.tabs.addTab(tab, label)

    def close_tab(self, index):
        self.tabs.removeTab(index)

    def search(self):
        search_query = self.search_bar.text()
        self.search_result.clear()
        self.search_result.append(f"Search results for: {search_query}")

    def load_page(self):
        url = self.search_bar.text()
        self.add_tab(url, url)


    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;HTML Files (*.html)", options=options)
        if file_path:
            with open(file_path, "r") as file:
                html_content = file.read()
                tab_label = file_path.split("/")[-1]
                self.add_tab(html_content, tab_label)
    def add_bookmark(self):
         current_tab_index = self.tabs.currentIndex()
         current_tab_widget = self.tabs.widget(current_tab_index)
         current_tab_browser = current_tab_widget.findChild(QWebEngineView)
         current_url = current_tab_browser.url().toString()


         if current_url not in self.bookmarks:
              self.bookmarks.append(current_url)
              QMessageBox.information(self, "Bookmark Added", f"Bookmark added for {current_url}")
         else:
              QMessageBox.warning(self, "Bookmark Exists", "This URL is already bookmarked")
    def show_bookmarks(self):
         dialog = QDialog(self)
         dialog.setWindowTitle("Bookmarks")
         layout = QVBoxLayout(dialog)
         list_widget = QListWidget(dialog)
         for bookmark in self.bookmarks:
            item = QListWidgetItem(bookmark)
            list_widget.addItem(item)
         layout.addWidget(list_widget)
         dialog.exec_()
         
    def set_suggestions(self, suggestions):
        self.model.setStringList(suggestions)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())


        

