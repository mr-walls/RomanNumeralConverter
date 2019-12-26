conversion_dict = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
# store the key-value pairs from conversion_dict in the opposite direction
generator_dict = {conversion_dict[x]: x for x in conversion_dict}


# function to generate the form of each digit 0-9 in Roman numerals
def pattern_creator(digit):
    nums = [1, 5, 10]
    if digit in nums:
        return [digit]
    for i in nums:
        for j in nums:
            if i - j == digit and i != j:
                return [j, i]
    # if we had to extend to include something like 3, 30, 300... this would become a loop
    if digit > 5:
        return [5] + [1] * (digit-5)
    return [1] * digit


# the patterns could have been hardcoded, but this shows it can be done programmatically
pattern_dict = {x: pattern_creator(x) for x in range(10)}


def roman_to_modern(roman_numeral):
    result = 0
    index = 0
    numeral_length = len(roman_numeral)
    while index < numeral_length:
        curr_symbol = roman_numeral[index]
        next_symbol = "I"
        if index + 1 < numeral_length:
            next_symbol = roman_numeral[index + 1]
        try:
            if conversion_dict[curr_symbol] < conversion_dict[next_symbol]:
                result += conversion_dict[next_symbol] - conversion_dict[curr_symbol]
                index += 2
            else:
                result += conversion_dict[curr_symbol]
                index += 1
        # ensure no extra symbols are included. Could also use a defaultdict to protect this
        except KeyError:
            print("This numeral contains unknown symbols")
            return -1
    return result


"""
I originally thought that there would be a ambiguity in the specifications
that would impact the modern_to_roman function. The rule denoting that a symbol representing
10^x cannot precede a symbol representing more than 10^(x+1) does not specify
whether x is strictly an integer. I thought this would impact the conversion of
45. However, if x is an integer there is no rule saying V cannot precede L, and
if x is not an integer L is exactly 10^(x+1) for x = log 5. I thought the ambiguity
would change whether 45 was VL or XLV. In order to resolve the ambiguity I googled
the representation of this number, and found XLV to be correct. However, by the
specifications given, I did not see a rule against V preceding L. I have chosen to keep
XLV as the accepted value. If I were to allow VL, I would check for the pattern 45 in the
last 3 digits of the number and place VL or LD in the result instead of the 
current pattern according to which position 45 was found in.
"""


def modern_to_roman(modern_numeral):
    power = 0
    result = ""
    # we do not have Roman numerals past 1000, so we limit the loop to handle three digits only
    while modern_numeral > 0 and power < 3:
        digit = modern_numeral % 10
        modern_numeral //= 10
        place_value = ""
        for value in pattern_dict[digit]:
            place_value += generator_dict[value * (10 ** power)]
        result = place_value + result
        power += 1
    # at this point modern_numerals has been divided by at most 1000, so the remaining value
    # is the number of thousands in the answer
    result = ("M" * modern_numeral) + result
    return result

# for x in range(100000):
#    assert(roman_to_modern(modern_to_roman(x)) == x)
# this was used to test that roman_to_modern and modern_to_roman are in fact inverses


print("Welcome to the Roman Numeral Converter")
repeat = "yes"
while repeat != "quit":
    numeral = input("Input Roman or modern numeral: ").upper()
    try:
        numeral = int(numeral)
        if numeral < 0:
            print("This number is negative, but we can show the Roman numeral for the positive number")
            numeral *= -1
        print("Roman numeral for {} is {}".format(numeral, modern_to_roman(numeral)))
    except ValueError:
        conversion = roman_to_modern(numeral)
        if conversion != -1:
            print("Modern numeral for {} is {}".format(numeral, conversion))
    repeat = input("Input 'quit' to stop, press any key to convert another numeral: ")