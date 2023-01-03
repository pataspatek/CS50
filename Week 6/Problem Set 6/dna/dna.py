import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py databases/FILENAME.csv sequences/FILENAME.txt")

    people = []
    # TODO: Read database file into a variable
    with open(sys.argv[1]) as database:
        reader = csv.reader(database)
        for row in reader:
            people.append(row)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2]) as sequence:
        dna = sequence.read()

    STR = []
    # TODO: Find longest match of each STR in DNA sequence
    for i in range(1, len(people[0])):
        STR.append(longest_match(dna, people[0][i]))

    # TODO: Check database for matching profiles
    print(comparison(people, STR))


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


# Compare STR to every person
def comparison(people, STR):
    '''If match is found, return that person's name, otherwise return 'No match'.'''
    for i in range(1, len(people)):
        tmp = []
        for j in range(1, len(people[i])):
            tmp.append(int(people[i][j]))

        if tmp == STR:
            return people[i][0]

    return "No match"


main()
