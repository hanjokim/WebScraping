import re 

data = """
park 800905-1049118
kim  700905-1059119
"""

pat = re.compile(r"(\d{6})[-](\d)\d{6}")
print(pat.sub(r"\1-\2******", data))