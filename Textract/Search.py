from docx import Document


def find_keyword_in_docx(file_path, keyword):
    # Load the Word document
    doc = Document(file_path)

    # Initialize a variable to keep track of occurrences
    keyword_count = 0

    # Iterate through paragraphs in the document
    for paragraph in doc.paragraphs:
        # Count how many times the keyword appears in the paragraph text
        occurrences = paragraph.text.lower().count(keyword.lower())
        if occurrences > 0:
            keyword_count += occurrences
            # Print the paragraph where the keyword was found along with the number of occurrences in that paragraph
            print(f"Found keyword '{keyword}' {occurrences} times in paragraph: {paragraph.text}")

    # Print the total number of occurrences
    print(f"Total occurrences of '{keyword}': {keyword_count}")

# Example usage
file_path = '/Users/chenxi/Desktop/Projekt/medicalexam.docx'
keyword = 'medicine'
find_keyword_in_docx(file_path, keyword)
