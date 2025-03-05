import os
import re
import math
import shlex
import pycparser

from pycparser import c_ast
from threading import Timer
from subprocess import Popen, PIPE


TITLE = '''
   ___       __                        __
  / _ |__ __/ /____  ___  _______ ____/ /__ ____
 / __ / // / __/ _ \\/ _ \\/ __/ _ \\/ _  / -_) __/
/_/ |_\\_,_/\\__/\\___/\\_, /_/  \\_,_/\\_,_/\\__/_/
                   /___/

             Machine Structures
     Great Ideas in Computer Architecture

lab 02: C y MM
'''

class Result:
  stdout = ''
  stderr = ''
  returncode = 0
  timeout = False


def execute(cmd, timeout):
  result = Result()
  proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)

  def timeout_handler():
    proc.kill()
    result.timeout = True

  timer = Timer(timeout, timeout_handler)

  try:
    timer.start()
    stdout, stderr = proc.communicate()
    result.stdout = stdout.decode('utf-8').strip()
    result.stderr = stderr.decode('utf-8').strip()
    result.returncode = proc.returncode
  finally:
    timer.cancel()

  return result

def check_result(result):
  if result.timeout:
    return {
      'grade': 0,
      'stderr': 'Timeout',
      'stdout': result.stdout,
      'returncode': result.returncode
    }

  if result.returncode != 0:
    return {
      'grade': 0,
      'stderr': result.stderr,
      'stdout': result.stdout,
      'returncode': result.returncode
    }

# C loop visitor
class LoopCondVisitor(c_ast.NodeVisitor):

  def __init__(self):
    self.found = False

  def visit_While(self, node):
    self.found = True
    self.generic_visit(node)

  def visit_DoWhile(self, node):
    self.found = True
    self.generic_visit(node)

  def visit_Goto(self, node):
    self.found = True
    self.generic_visit(node)

  def visit_If(self, node):
    self.found = True
    self.generic_visit(node)

  def visit_Switch(self, node):
    self.found = True
    self.generic_visit(node)

  def visit_TernaryOp(self, node):
    self.found = True
    self.generic_visit(node)

  def visit_For(self, node):
    self.found = True
    self.generic_visit(node)

  def reset(self):
    self.found = False


# C free call visitor
class FreeCall(c_ast.NodeVisitor):

  def __init__(self):
    self.count = 0

  def visit_FuncCall(self, node):
    if node.name.name.lower() == 'free':
      self.count += 1
    self.generic_visit(node)

  def reset(self):
    self.count = 0


# C relloc call visitor
class ReallocCall(c_ast.NodeVisitor):

  def __init__(self):
    self.count = 0

  def visit_FuncCall(self, node):
    if node.name.name.lower() == 'realloc':
      self.count += 1
    self.generic_visit(node)

  def reset(self):
    self.count = 0


# parses a c c99 file
def parse_c(filename):
  result = execute('make clean', 5)
  error = check_result(result)
  if error is not None: return None, error

  result = execute('make ' + filename + '_conv.c', 5)
  error = check_result(result)
  if error is not None: return None, error

  with open(filename + '_conv.c', 'r') as f:
    text = ''
    p = re.compile(r'(\w)*#.*')

    for line in f:
        line = line.strip('\n')
        if line == '':
            continue
        if p.search(line):
            continue
        text += line + '\n'

    parser = pycparser.c_parser.CParser()
    return parser.parse(text), None


def find_func(ast, name):
  for f in ast.ext:
    if type(f) == pycparser.c_ast.FuncDef and f.decl.name == name:
      return f
  return None


EX1 = '''
OK
OK
OK
OK
OK
OK
OK
OK
OK
OK
OK
OK
OK
OK
OK
OK
OK
OK
OK
'''

def test_ex1():
  tree, error = parse_c('ex1/flip_bit')
  if error is not None: return error

  v = LoopCondVisitor()
  v.visit(find_func(tree, 'flip_bit'))
  if v.found:
    return {
      'grade': 0,
      'stderr': 'Using loop or conditional',
      'stdout': '',
      'returncode': 0
    }

  tree, error = parse_c('ex1/get_bit')
  if error is not None: return error

  v.visit(find_func(tree, 'get_bit'))
  if v.found:
    return {
      'grade': 0,
      'stderr': 'Using loop or conditional',
      'stdout': '',
      'returncode': 0
    }

  tree, error = parse_c('ex1/set_bit')
  if error is not None: return error

  v.visit(find_func(tree, 'set_bit'))
  if v.found:
    return {
      'grade': 0,
      'stderr': 'Using loop or conditional',
      'stdout': '',
      'returncode': 0
    }

  result = execute('make clean', 5)
  error = check_result(result)
  if error is not None: return error

  result = execute('make bit_ops_autograder', 5)
  error = check_result(result)
  if error is not None: return error

  result = execute('./bit_ops_autograder', 5)
  error = check_result(result)
  if error is not None: return error

  expected = EX1.strip().splitlines()
  output = result.stdout.splitlines()

  grade = 0
  points = (100 / 3) / 19

  for (exp, out) in zip(expected, output):
      exp = exp.strip()
      out = out.strip()

      if exp == out:
          grade += points

  return {
    'grade': math.ceil(grade),
    'stderr': result.stderr,
    'stdout': result.stdout,
    'returncode': result.returncode
  }

def test_ex2():
  tree, error = parse_c('ex2/lfsr_calculate')
  if error is not None: return error

  v = LoopCondVisitor()
  v.visit(find_func(tree, 'lfsr_calculate'))
  if v.found:
    return {
      'grade': 0,
      'stderr': 'Using loop or conditional',
      'stdout': '',
      'returncode': 0
    }

  result = execute('make clean', 5)
  error = check_result(result)
  if error is not None: return error

  result = execute('make lfsr_autograder', 5)
  error = check_result(result)
  if error is not None: return error

  result = execute('./lfsr_autograder', 5)
  error = check_result(result)
  if error is not None: return error

  f = open('./tests/autograder/ex2.expected', 'r')
  EX2 = f.read()
  f.close()

  expected = EX2.strip().splitlines()
  output = result.stdout.strip().splitlines()

  if len(expected) != len(output):
    return {
      'grade': 0,
      'stderr': result.stderr,
      'stdout': result.stdout,
      'returncode': result.returncode
    }

  for (exp, out) in zip(expected, output):
    exp = exp.strip()
    out = out.strip()

    if exp != out:
      return {
        'grade': 0,
        'stderr': result.stderr,
        'stdout': result.stdout,
        'returncode': result.returncode
      }

  return {
    'grade': math.ceil(100 / 3),
    'stderr': result.stderr,
    'stdout': result.stdout,
    'returncode': result.returncode
  }


def test_ex3():
  tree, error = parse_c('ex3/vector')
  if error is not None: return error

  v = FreeCall()
  v.reset()
  v.visit(find_func(tree, 'vector_new'))
  if v.count == 0:
    return {
      'grade': 0,
      'stderr': '[vector new] dont forget to call free...',
      'stdout': '',
      'returncode': 0
    }

  tree, error = parse_c('ex3/vector')
  if error is not None: return error

  v.reset()
  v.visit(find_func(tree, 'vector_delete'))
  if v.count == 0:
    return {
      'grade': 0,
      'stderr': '[vector delete] dont forget to call free...',
      'stdout': '',
      'returncode': 0
    }

  tree, error = parse_c('ex3/vector')
  if error is not None: return error

  r = ReallocCall()
  v.reset()
  r.reset()
  v.visit(find_func(tree, 'vector_set'))
  r.visit(find_func(tree, 'vector_set'))
  if v.count == 0 and r.count == 0:
    return {
      'grade': 0,
      'stderr': '[vector set] dont forget to call free or use realloc...',
      'stdout': '',
      'returncode': 0
    }

  result = execute('make vector_autograder', 5)
  error = check_result(result)
  if error is not None: return error

  result = execute('./vector_autograder', 5)
  error = check_result(result)
  if error is not None: return error

  f = open('./tests/autograder/ex3.expected', 'r')
  EX3 = f.read()
  f.close()

  expected = EX3.strip().splitlines()
  output = result.stdout.strip().splitlines()

  if len(expected) != len(output):
    return {
      'grade': 0,
      'stderr': result.stderr,
      'stdout': result.stdout,
      'returncode': result.returncode
    }

  for (exp, out) in zip(expected, output):
    exp = exp.strip()
    out = out.strip()

    if exp != out:
      return {
        'grade': 0,
        'stderr': result.stderr,
        'stdout': result.stdout,
        'returncode': result.returncode
      }

  return {
    'grade': math.ceil(100 / 3),
    'stderr': result.stderr,
    'stdout': result.stdout,
    'returncode': result.returncode
  }

if __name__ == '__main__':
  ex1 = test_ex1()
  ex2 = test_ex2()
  ex3 = test_ex3()

  results = [ex1, ex2, ex3]
  names = ['1. Bitwise Operands', '2. LFSR', '3. Vector']
  grade = 0
  stdout = ''
  stderr = ''

  print(TITLE)

  for result, name in zip(results, names):
    grade += result['grade']
    prefix = f'{name}'.ljust(20)

    print(f'{prefix}: {result["grade"]}')

    if result['stdout'].strip() != '':
      stdout += f'{name}' + os.linesep * 2
      stdout += result['stdout'].strip() + os.linesep * 2

    if result['stderr'].strip() != '':
      stderr += f'{name}' + os.linesep * 2
      stderr += result['stderr'].strip() + os.linesep * 2

  print('')
  print(f'Total: {min(grade, 100)}')
  print('')
  print('---')
  print('')
  print('stdout:')
  print('')
  print(stdout.rstrip())
  print('')
  print('---')
  print('')
  print('stderr:')
  print(stderr)
