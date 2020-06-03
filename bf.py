# bf.py is a Brainfuck interpreter
# Copyright (C) 2020  Josias Alvarado
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import getch

def execute(filename):
    with open(filename, 'r') as file:
        evaluate(file.read())

def build_loop_map(code):
    # A list and a dictionary
    start_loop, loop_map = [], {}
    # Now we loop over the string `code` | var position contains the index and command the actual character
    for position, command in enumerate(code):
        if command == "[":
            start_loop.append(position)
        if command == "]":
            start = start_loop.pop()
            loop_map[start] = position
            loop_map[position] = start
    return loop_map

def evaluate(code):
    code = cleanup(list(code))
    loop_map = build_loop_map(code)
    
    cells = [0]
    codeptr = 0
    cellptr = 0
    
    while codeptr < len(code):
        command = code[codeptr]
        
        if command == ">":
            cellptr += 1
        if cellptr == len(cells):
            cells.append(0)
        if command == "<":
            cellptr = 0 if cellptr <= 0 else cellptr - 1
        if command == "+":
            cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0
        if command == "-":
            cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255
        if command == "[" and cells[cellptr] == 0: codeptr = loop_map[codeptr]
        if command == "]" and cells[cellptr] != 0: codeptr = loop_map[codeptr]
        if command == ".": sys.stdout.write(chr(cells[cellptr]))
        if command == ",": cells[cellptr] = ord(getch.getch())
      
        codeptr += 1

def cleanup(code):
    return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code))

def main():
    if len(sys.argv) == 2:
        execute(sys.argv[1])
    else:
        print("Usage:", sys.argv[0], "file.bf")

if __name__ == "__main__":
    main()
