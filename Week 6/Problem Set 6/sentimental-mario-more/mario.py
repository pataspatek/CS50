# Ask user for the height of the pyramid until he provides a positive integer less than 8
while True:
    try:
        height = int(input("Height: "))
        if height <= 8 and height > 0:
            break
    except:
        pass

# For each row print correct forumla for a pyramid
for i in range(1, height + 1):
    print(" " * (height - i) + "#" * (i) + "  " + "#" * (i))