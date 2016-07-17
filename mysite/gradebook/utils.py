def to_percent(points, points_possible):
    return "{0:.0f}%".format(points / points_possible * 100)


def get_letter_grade(float_percentage):
    if float_percentage > 90:
        return 'A'
    elif 80.0 <= float_percentage < 90.0:
        return 'B'
    elif 70.0 <= float_percentage < 80.0:
        return 'C'
    elif 60.0 <= float_percentage < 70.0:
        return 'D'
    elif 0.0 <= float_percentage < 60.0:
        return 'F'