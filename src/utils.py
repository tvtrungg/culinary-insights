def preprocess_text(lines):
    """
    Preprocess the text by removing punctuation and converting to lowercase.
    """
    # Remove punctuation
    lines = lines.replace('[','').replace(']','').replace("'",'').replace("",'').replace('"','').split(',')
    lines = [x.strip() for x in lines]
    lines = [x.replace(' ','_') for x in lines]
    
    return lines

def preprocess_bulk(column):
    """
    Preprocess a column of text data.
    """
    for i in range(len(column)):
        column[i] = preprocess_text(column[i])
    return column

def collect_ingredients(column):
    """
    Collect all unique ingredients from the column.
    """
    all_ingredients = []
    for i in range(len(column)):
        all_ingredients += column[i]
    all_ingredients = list(set(all_ingredients))
    return all_ingredients