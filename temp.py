def process_file(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'w') as f:
        for line in lines:
            # Split the line by space
            words = line.split()
            # Create a set to keep track of seen words
            seen = set()
            for word in sorted(words):
                # Write the word if it's not a duplicate
                if word not in seen:
                    f.write(word + '\n')
                    # Add the word to the set of seen words
                    seen.add(word)
input_file = 'data/fuzzy_dictionary.txt'
output_file = 'data/fuzzy_ditionary_unique.txt'
process_file(input_file, output_file)
