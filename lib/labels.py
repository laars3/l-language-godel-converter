import re

LABELS = ["A", "B", "C", "D", "E"]
_LABEL_RE = re.compile(r"^[A-E][1-9]\d*$")


# A1..E1, A2..E2, ... -> 1, 2, 3, ... cycling through the 5 letters each round
def label_to_ordinal(label):
    letter = label[0]
    n = int(label[1:])
    letter_pos = LABELS.index(letter) + 1
    return (5 * (n - 1)) + letter_pos


# reverse of label_to_ordinal
def ordinal_to_label(ordinal):
    zero_based = ordinal - 1
    letter = LABELS[zero_based % 5]
    n = (zero_based // 5) + 1
    return f"{letter}{n}"


def is_valid_label(label):
    return bool(_LABEL_RE.match(label))
