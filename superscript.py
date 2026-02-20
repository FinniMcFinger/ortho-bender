def convert_digit_to_superscript(number: int) -> str | None:
    match number:
        case 0:
            return '\u2070'
        case 1:
            return '\u00B9'
        case 2:
            return '\u00B2'
        case 3:
            return '\u00B3'
        case 4:
            return '\u2074'
        case 5:
            return '\u2075'
        case 6:
            return '\u2076'
        case 7:
            return '\u2077'
        case 8:
            return '\u2078'
        case 9:
            return '\u2079'

    return None


def convert_num_to_super(number: int) -> str:
    super = ''

    for char in str(number):
        if char.isdigit():
            super += convert_digit_to_superscript(int(char))

    return super


if __name__ == '__main__':
    print(convert_num_to_super(12345))