import textract

def count_keywords_in_file(file_path, keywords):
    # Extract text from the file
    text = textract.process(file_path).decode('utf-8')
    
    # Convert text to lowercase to make the search case-insensitive
    text_lower = text.lower()
    
    # Initialize a dictionary to store counts of each keyword
    keyword_counts = {keyword: 0 for keyword in keywords}  # Pre-fill with keywords
    
    # Count occurrences of each keyword
    for keyword in keywords:
        keyword_lower = keyword.lower()  # Case-insensitive search
        count = text_lower.count(keyword_lower)
        keyword_counts[keyword] = count
    
    return keyword_counts

# Example usage
file_path = '/Users/chenxi/Desktop/Projekt/Textract/tests11/test22/Book2.xlsx'  # Replace with your file path
keywords = ['medicine', 'health', 'treatment']  # List your keywords here
counts = count_keywords_in_file(file_path, keywords)

for keyword, count in counts.items():
    print(f"The keyword '{keyword}' appears {count} times in the document.")