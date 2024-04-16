from spellwise import (CaverphoneOne, CaverphoneTwo, Editex, Levenshtein,
                       Soundex, Typox)

def fuzzy_searcher(input):
    algorithm = Levenshtein()
    algorithm.add_from_path("data/fuzzy_dictionary_unique.txt")
    suggestions = algorithm.get_suggestions(input,max_distance=1)
    print(suggestions)
    if len(suggestions) > 0:
        return(suggestions[0]['word'])
    else:
        return(input)

if __name__ == "__main__":
    inpu=input("Enter the word to search:")
    fuzzy_searcher(input=inpu)