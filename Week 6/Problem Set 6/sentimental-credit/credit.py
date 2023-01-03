def main():
    # Ask user for the credit card number
    number = input("Number: ")

    # Checksum return true if the math is correct with the given card number
    if checksum(number):
        # Checks for the company that made the card
        print(company(number))
    else:
        print("INVALID")


def checksum(number):
    '''Special formula for calculating the digit in a card number'''
    sum = 0
    for i in range(len(number) - 2, -1, -2):
        for j in number[i]:
            sum += multiply(j)

    for k in range(len(number) - 1, -1, -2):
        sum += int(number[k])

    if sum % 10 == 0:
        return True


def multiply(string):
    '''Multiply every other digit by 2, starting with the number's second-to-last digit,
    and then add those product's digits together.'''
    sum = 0
    number = int(string)
    number *= 2
    digit = str(number)
    for i in digit:
        sum += int(i)

    return sum


def company(number):
    # Based on given rules, figure out, which company card is it
    if len(number) == 15 and number[0] == "3" and (number[1] == "4" or number[1] == "7"):
        return "AMEX"
    elif (len(number) == 16) and (number[0] == "5") and (int(number[1]) in range(1, 6)):
        return "MASTERCARD"
    elif (len(number) == 13 or len(number) == 16) and (number[0] == "4"):
        return "VISA"
    else:
        return "INVALID"


if __name__ == "__main__":
    main()
