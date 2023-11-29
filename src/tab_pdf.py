from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog,QSpacerItem, QSizePolicy,QHBoxLayout,QMessageBox)
import PyPDF2
from PyQt5.QtGui import QIcon
import fitz
import os
class PdfTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.stylesheet = """
          QPushButton {
        border: 2px solid #A0A0A0; /* Adjust the border thickness here */
        border-radius: 5px; /* Rounded corners, set to 0 for square corners */
        background-color: #E6E6E6;
        min-width: 120px; /* Minimum width */
        min-height: 40px; /* Minimum height */
        max-height: 40px; /* Maximum height to ensure the button is square */
          },
        QPushButton:hover {
        background-color: #CCCCCC !important;
        }
         
        """
    
        
        self.setup_file_input_ui()
        self.setup_text_extraction_ui()
        self.setup_merge_pdfs_ui()
        self.setup_text_display_ui()
        
        self.setup_watermark_ui()



        self.setLayout(self.layout)
        
    def setup_file_input_ui(self):
        self.file_input_layout, self.file_input = self.create_file_input_section('PDF File path:', self)
        self.layout.addLayout(self.file_input_layout)
        
    def setup_text_extraction_ui(self):
        button_layout = QHBoxLayout()

        # Button to extract text from the first page
        self.extract_text_button = QPushButton('Extract Text from First Page', self)
        self.extract_text_button.clicked.connect(self.extract_text)
        self.extract_text_button.setStyleSheet(self.stylesheet)
        button_layout.addWidget(self.extract_text_button)

        # Button to extract text from all pages
        self.extract_alltext_button = QPushButton('Extract Text from All Pages', self)
        self.extract_alltext_button.clicked.connect(self.extract_alltext)
        self.extract_alltext_button.setStyleSheet(self.stylesheet)
        button_layout.addWidget(self.extract_alltext_button)

        self.layout.addLayout(button_layout)
        button_layout.setSpacing(30)
    def setup_merge_pdfs_ui(self):
    # Add PDF button
        self.add_pdf_button = QPushButton('Add PDF', self)
        self.add_pdf_button.setStyleSheet(self.stylesheet)
        self.add_pdf_button.clicked.connect(self.add_pdf_path_input)
        self.layout.addWidget(self.add_pdf_button)

        # Initialize the list for PDF path line edits
        self.pdf_path_inputs = []

        # Output path controls
        self.output_path_input = QLineEdit(self)
        self.output_path_input.setPlaceholderText('Output PDF path')
        self.select_output_path_button = QPushButton('Select Output', self)
        self.select_output_path_button.clicked.connect(self.select_output_path)

        output_path_layout = QHBoxLayout()
        output_path_layout.addWidget(self.output_path_input)
        output_path_layout.addWidget(self.select_output_path_button)
        self.layout.addLayout(output_path_layout)

        # Merge button
        self.merge_button = QPushButton('Merge PDFs', self)
        self.merge_button.setStyleSheet(self.stylesheet)
        self.merge_button.clicked.connect(self.merge_pdfs)
        self.layout.addWidget(self.merge_button)
    def setup_text_display_ui(self):
    # Text displays
        self.extracted_text_display = QTextEdit(self)
        self.extracted_text_display.setReadOnly(True)
        self.extracted_text_display.hide()
        self.layout.addWidget(self.extracted_text_display)
        
        self.extract_alltext_display = QTextEdit(self)
        self.extract_alltext_display.setReadOnly(True)
        self.extract_alltext_display.hide()
        self.layout.addWidget(self.extract_alltext_display)
    



    def create_file_input_section(self, label_text, parent):
        layout = QHBoxLayout()
        
        label = QLabel(label_text)
        layout.addWidget(label)
        
        file_input = QLineEdit(parent)
        layout.addWidget(file_input, 1)  # The '1' here makes the line edit expandable

        browse_button = QPushButton(parent)
        browse_button.setIcon(QIcon('path/to/icon.png'))  # Replace with the path to your icon
        browse_button.setFixedSize(30, 30)  # Makes the button smaller
        browse_button.clicked.connect(lambda: self.browse_file(file_input))
        layout.addWidget(browse_button)

        
        return layout, file_input  # Return both the layout and the file_input

    def browse_file(self, file_input):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF file", "", "PDF files (*.pdf)")
        if file_path:
            file_input.setText(file_path)
    def add_pdf_path_input(self):
        # Horizontal layout for the new line edit and browse button
        pdf_input_layout = QHBoxLayout()
        
        # Line edit for the new PDF path
        pdf_path_input = QLineEdit(self)
        pdf_path_input.setStyleSheet(self.stylesheet)  # Apply the stylesheet
        self.pdf_path_inputs.append(pdf_path_input)


        pdf_input_layout.addWidget(pdf_path_input)
        self.pdf_path_inputs.append(pdf_path_input)
        
        # Button to browse for the PDF
        browse_button = QPushButton('Browse', self)
        browse_button.setStyleSheet(self.stylesheet)  # Apply the stylesheet
        browse_button.clicked.connect(lambda: self.browse_file(pdf_path_input))
        pdf_input_layout.addWidget(browse_button)
        
        # "+" Button to add more PDFs
        add_button = QPushButton('+', self)
        add_button.setStyleSheet(self.stylesheet)  # Apply the stylesheet
        add_button.clicked.connect(self.add_pdf_path_input)
        pdf_input_layout.addWidget(add_button)

        # Add the new horizontal layout to the main layout
        insert_position = self.layout.indexOf(self.add_pdf_button) + 1

        self.layout.insertLayout(insert_position,pdf_input_layout)
    def browse_file(self, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF file", "", "PDF files (*.pdf)")
        if file_path:
            line_edit.setText(file_path)      
    def extract_text(self):
        self.extracted_text_display.show()  # Make sure to show the display
        pdf_path = self.file_input.text()
        try:
            with open(pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfFileReader(f)
                if pdf_reader.isEncrypted:
                    pdf_reader.decrypt('')
                    print("PDF was encrypted; attempted to decrypt")
                
                first_page = pdf_reader.getPage(0)
                text = first_page.extractText()
                if not text:
                    print("No text extracted; may be an image-based PDF")
                self.extracted_text_display.setText(text)
        except Exception as e:
            print(f"An error occurred: {e}")
            self.extracted_text_display.setText(f"An error occurred: {e}")
    
    def extract_alltext(self):
        self.extract_alltext_display.show()
        pdf_path = self.file_input.text()
        try:
            with open(pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfFileReader(f)
                all_text = ""
                for page in pdf_reader.pages:
                    text = page.extractText()
                    all_text+= text
                    
                self.extract_alltext_display.setText(all_text)
        except Exception as e:
            self.extract_alltext_display.setText(f"An error occurred: {e}")
    def select_output_path(self):
        output_path, _ = QFileDialog.getSaveFileName(self, "Select Output PDF file", "", "PDF files (*.pdf)")
        if output_path:
            self.output_path_input.setText(output_path)

    def merge_pdfs(self):
        pdf_paths = [pdf_path_input.text() for pdf_path_input in self.pdf_path_inputs if pdf_path_input.text()]
        output_path = self.output_path_input.text()
        if pdf_paths and output_path:
            try:
                merger = PyPDF2.PdfFileMerger()
                for pdf_path in pdf_paths:
                    merger.append(pdf_path)
                merger.write(output_path)
                merger.close()
                QMessageBox.information(self, "Success", "PDFs merged successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred: {e}")
        else:
            QMessageBox.warning(self, "Error", "Please add PDF files and specify an output file.")
    def apply_watermark(self):
        pdf_path = self.watermark_pdf_input.text()
        watermark_path = self.watermark_image_input.text()
        if pdf_path and watermark_path:
            try:
                self.add_watermark(pdf_path, watermark_path)
                QMessageBox.information(self, "Success", "Watermark applied successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred: {e}")
        else:
            QMessageBox.warning(self, "Error", "Please specify both PDF and watermark image paths.")
        # Create a horizontal layout for the PDF path to watermark
        

        # Add the watermark layout to the main layout
    def setup_watermark_ui(self):
    # Create a vertical layout for the watermark section
        watermark_layout = QVBoxLayout()

        # Create a horizontal layout for the PDF path to watermark
        pdf_path_layout = QHBoxLayout()
        self.watermark_pdf_input = QLineEdit(self)
        self.watermark_pdf_input.setPlaceholderText('Path to PDF to watermark')
        self.select_pdf_button = QPushButton('Select PDF', self)
        self.select_pdf_button.clicked.connect(lambda: self.browse_file(self.watermark_pdf_input))
        pdf_path_layout.addWidget(self.watermark_pdf_input)
        pdf_path_layout.addWidget(self.select_pdf_button)

        # Create a horizontal layout for the watermark image path
        image_path_layout = QHBoxLayout()
        self.watermark_image_input = QLineEdit(self)
        self.watermark_image_input.setPlaceholderText('Path to watermark image')
        self.select_watermark_button = QPushButton('Select Image', self)
        self.select_watermark_button.clicked.connect(lambda: self.browse_file(self.watermark_image_input))
        image_path_layout.addWidget(self.watermark_image_input)
        image_path_layout.addWidget(self.select_watermark_button)

        # Add the horizontal layouts to the vertical watermark layout
        watermark_layout.addLayout(pdf_path_layout)
        watermark_layout.addLayout(image_path_layout)

        # Apply Watermark button
        self.apply_watermark_button = QPushButton('Apply Watermark', self)
        self.apply_watermark_button.clicked.connect(self.apply_watermark)
        watermark_layout.addWidget(self.apply_watermark_button)

        # Insert the watermark layout into the main layout at the desired position
        merge_button_index = self.layout.indexOf(self.merge_button) + 1  # Assuming the merge button is already in the layout
        self.layout.insertLayout(merge_button_index, watermark_layout)
    def add_watermark(self, pdf_path, watermark_path):
    # Open the PDF to be watermarked
        pdf_document = fitz.open(pdf_path)

        # Open the image to be used as the watermark
        watermark = fitz.open("pdf", fitz.new_pixmap(fitz.csRGB, watermark_path))

        # Iterate through each page in the PDF and add the watermark
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]

            # Calculate dimensions to place the watermark
            rect = fitz.Rect(page.rect.width - watermark.width, page.rect.height - watermark.height, page.rect.width, page.rect.height)

            # Add the watermark to the current page
            page.insert_image(rect, pixmap=watermark)

        # Save the watermarked PDF to a new file
        output_pdf_path = "watermarked_" + os.path.basename(pdf_path)
        pdf_document.save(output_pdf_path)
        pdf_document.close()
        watermark.close()