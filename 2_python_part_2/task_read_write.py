"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.
Example:
    Input:
    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")
    Output:
    result.txt(content: "23, 78, 3")
"""

files_tab = []

for i in range(3):
    with open(f'files/file_{i+1}.txt') as f:
        files_tab.append(f.read())

with open('files/result.txt', 'w') as f:
    f.write(str(', '.join(files_tab)))
