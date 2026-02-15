import zipfile
import re
import os

xlsx_path = "Ass5/expextions 12-2.xlsx"

with zipfile.ZipFile(xlsx_path, "r") as z:
    strings = []
    try:
        with z.open("xl/sharedStrings.xml") as f:
            strings = re.findall(r"<t[^>]*>(.*?)</t>", f.read().decode("utf-8"))
    except:
        pass
    with z.open("xl/worksheets/sheet1.xml") as f:
        sheet = f.read().decode("utf-8")

print("Shared strings (first 20):")
for i, s in enumerate(strings[:20]):
    print(f"  {i}: {s}")

print()
print("Header row:")
rows = sheet.split("<row")
if len(rows) > 1:
    vals = re.findall(r"<v>(.*?)</v>", rows[1])
    header = []
    for v in vals:
        try:
            idx = int(float(v))
            if 0 <= idx < len(strings):
                header.append(strings[idx])
            else:
                header.append(v)
        except:
            header.append(v)
    print(f"  {header}")

print()
print("Rows containing 209288588:")
for r in rows:
    if "209288588" not in r:
        continue
    vals = re.findall(r"<v>(.*?)</v>", r)
    decoded = []
    for v in vals:
        try:
            fv = float(v)
            # Check if it could be a shared string index
            if fv == int(fv) and 0 <= int(fv) < len(strings) and fv < 100:
                decoded.append(strings[int(fv)])
            else:
                decoded.append(fv)
        except:
            decoded.append(v)
    print(f"  {decoded}")

# Also re-check leaderboard 9-2 for the user
print()
print("=== Leaderboard 9-2 ===")
csv_path = "Ass5/Leaderboard-9-2.csv"
with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
    header = f.readline().strip()
    print(f"  Header: {header}")
    for line in f:
        if "209288588" in line:
            print(f"  Data:   {line.strip()}")

# Leaderboard 12-2 row
print()
print("=== Leaderboard 12-2 ===")
xlsx_path2 = "Ass5/leaderbord 12-2.xlsx"
with zipfile.ZipFile(xlsx_path2, "r") as z:
    strings2 = []
    try:
        with z.open("xl/sharedStrings.xml") as f:
            strings2 = re.findall(r"<t[^>]*>(.*?)</t>", f.read().decode("utf-8"))
    except:
        pass
    with z.open("xl/worksheets/sheet1.xml") as f:
        sheet2 = f.read().decode("utf-8")

rows2 = sheet2.split("<row")
# header
if len(rows2) > 1:
    vals = re.findall(r"<v>(.*?)</v>", rows2[1])
    header = []
    for v in vals:
        try:
            idx = int(float(v))
            if 0 <= idx < len(strings2):
                header.append(strings2[idx])
            else:
                header.append(v)
        except:
            header.append(v)
    print(f"  Header: {header}")

for r in rows2:
    if "209288588" in r:
        vals = re.findall(r"<v>(.*?)</v>", r)
        decoded = []
        for v in vals:
            try:
                fv = float(v)
                if fv == int(fv) and 0 <= int(fv) < len(strings2) and fv < 100:
                    decoded.append(strings2[int(fv)])
                else:
                    decoded.append(fv)
            except:
                decoded.append(v)
        print(f"  Data:   {decoded}")

# Exceptions 9-2
print()
print("=== Exceptions 9-2 ===")
csv_path2 = "Ass5/Exceptions-9-2.csv"
with open(csv_path2, "r", encoding="utf-8", errors="ignore") as f:
    header = f.readline().strip()
    print(f"  Header: {header}")
    for line in f:
        if "209288588" in line:
            print(f"  Data:   {line.strip()}")
