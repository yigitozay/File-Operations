from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QFileDialog, QLabel

def create_file_input_section(label_text, parent=None):
    layout = QHBoxLayout()
    
    # Label
    label = QLabel(label_text)
    layout.addWidget(label)

    # Line edit for the path
    path_input = QLineEdit(parent)
    layout.addWidget(path_input)
    
    # Browse button
    browse_button = QPushButton("Browse", parent)
    browse_button.clicked.connect(lambda: browse_file(path_input))
    layout.addWidget(browse_button)
    
    return layout, path_input

def browse_file(path_input):
    file_path, _ = QFileDialog.getOpenFileName()
    if file_path:
        path_input.setText(file_path)