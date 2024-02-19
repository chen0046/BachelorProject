###################################
##### Find keywords with docx.#####
###################################

####################################################################################
############### works for 1 document finds amount times 1 word used ################
####################################################################################

from docx import Document

def find_keyword_in_docx(file_path, keyword):
    # Load the Word document
    doc = Document(file_path)

    # Initialize a variable to keep track of occurrences
    keyword_count = 0

    # Iterate through paragraphs in the document
    for paragraph in doc.paragraphs:
        # Check if the keyword is present in the paragraph text
        if keyword.lower() in paragraph.text.lower():
            keyword_count += paragraph.text.lower().count(keyword.lower())

    # Print the total number of occurrences
    print(f"Total occurrences of '{keyword}': {keyword_count}")

# Example usage
file_path = '/Users/alexsolomon/Desktop/Bachelor/Medicine.docx'
keyword = 'medicine'
find_keyword_in_docx(file_path, keyword)

