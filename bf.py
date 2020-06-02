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

import pdb
import sys
import getch

def execute(filename):
  with open(filename, 'r') as file:
      evaluate(file.read())

def build_loop_map(code):
  
  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "[":
        temp_bracestack.append(position)
    if command == "]":
        start = temp_bracestack.pop()
        bracemap[start] = position
        bracemap[position] = start
  return bracemap

def evaluate(code):
    # array = [0][0][0][0][0]
    # >>++[<<+]

    bf_code   = cleanup(list(code))
    loop_map = build_loop_map(bf_code)

    cells     = [0] #cells
    cellptr   = 0   #cellptr
    codeptr   = 0   #codeptr

    # +[-[<<[+[--->]-[<<<]]]>>>-]>-.---.>..>.<<<<-.<+.>>>>>.>.<<.<-.

    #pdb.set_trace()
    while codeptr < len(bf_code):
        command = bf_code[codeptr]

        if command == '>':
            cellptr += 1
            if cellptr == len(cells):
                cells.append(0)
        
        if command == '<':
            if cellptr <= 0:
                cellptr = 0
            else:
                cellptr - 1
        
        if command == '+':
            cells[cellptr] = cells[cellptr] + 1
        
        if command == '-':
            if cells[cellptr] > 0:
                cells[cellptr] = cells[cellptr] - 1
            else:
                cells[cellptr] = 255
        
        if command == '.':
            sys.stdout.write(chr(cells[cellptr]))
        
        if command == ',':
            cells[cellptr] = ord(getch.getch())
        
        #if command == '[' and cells[cellptr] == 0:
        #    codeptr = loop_map[codeptr]

        #if command == ']' and cells[cellptr] != 0:
        #    codeptr = loop_map[codeptr]

        if command == '[':
            codeptr = loop_map[codeptr]
        
        if command == ']':
            codeptr = loop_map[codeptr]
        codeptr += 1
        #print(codeptr)

def cleanup(code):
    return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code))
  
def main():
    if len(sys.argv) == 2:
      execute(sys.argv[1])
    else:
      print("Usage:", sys.argv[0], "filename")

if __name__ == "__main__": 
    main()