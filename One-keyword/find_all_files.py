from docx import Document
import os

def find_keyword_in_docx_folder(folder_path, keyword):
    # Initialize a variable to keep track of occurrences across all documents
    total_keyword_count = 0

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.docx'):
            # Construct the full path for each document
            file_path = os.path.join(folder_path, filename)

            # Load the Word document
            doc = Document(file_path)

            # Initialize a variable to keep track of occurrences in the current document
            keyword_count = 0

            # Iterate through paragraphs in the document
            for paragraph in doc.paragraphs:
                # Check if the keyword is present in the paragraph text
                if keyword.lower() in paragraph.text.lower():
                    keyword_count += paragraph.text.lower().count(keyword.lower())

            # Print the occurrences for the current document
            print(f"Total occurrences of '{keyword}' in {filename}: {keyword_count}")

            # Update the total count
            total_keyword_count += keyword_count

    # Print the total number of occurrences across all documents
    print(f"Total occurrences of '{keyword}' in the entire folder: {total_keyword_count}")

# Example usage with a folder path
folder_path = '/Users/alexsolomon/Desktop/Bachelor'
keyword = 'time'
find_keyword_in_docx_folder(folder_path, keyword)


