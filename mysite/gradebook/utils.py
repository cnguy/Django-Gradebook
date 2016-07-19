import bisect


def to_percent(points, points_possible):
    return "{0:.0f}%".format(points / points_possible * 100)


def get_letter_grade(percent_score):
    breakpoints = [60, 70, 80, 90]
    grades = 'FDCBA'
    return grades[bisect.bisect(breakpoints, percent_score)]