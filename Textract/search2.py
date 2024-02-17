import textract

def count_keyword_in_file(file_path, keyword):
    # Extract text from the file
    text = textract.process(file_path).decode('utf-8')
    
    # Convert text and keyword to lowercase to make the search case-insensitive
    text_lower = text.lower()
    keyword_lower = keyword.lower()
    
    # Count occurrences of the keyword
    keyword_count = text_lower.count(keyword_lower)
    
    return keyword_count

# Example usage
file_path = '/Users/chenxi/Desktop/Projekt/test.pdf'  # Change this to the path of your file
keyword = 'medicine'
count = count_keyword_in_file(file_path, keyword)
print(f"The keyword '{keyword}' appears {count} times in the document.")