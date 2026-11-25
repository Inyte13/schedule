import time
from uuid import uuid4

from app.domain.scheduling.dom import dom
from app.domain.scheduling.dom_con_desempate import dom_con_desempate
from app.domain.scheduling.solver import solve

data_text = {
  'CALCULO': [
    ('A', 'L:1,2;X:1,2,3;V:3,4'),
    ('B', 'L:13,14,15;X:14,15;V:13,14'),
    ('C', 'L:7,8;J:7,8;V:5,6,7'),
  ],
  'EDII': [
    ('A', 'L:3,4;J:3,4'),
    ('B', 'X:12,13;J:12,13'),
    ('C', 'L:11,12;V:13,14'),
  ],
  'DSOO': [
    ('A', 'L:5,6;J:5,6'),
    ('B', 'L:9,10;M:12,13'),
    ('C', 'M:7,8;X:7,8'),
  ],
  'LCRA': [
    ('A', 'M:1,2,3;J:1,2'),
    ('B', 'X:9,10,11;V:9,10'),
    ('C', 'M:1,2,3;J:1,2'),
  ],
  'RN': [
    ('A', 'M:4,5,6'),
    ('B', 'J:9,10,11'),
    ('C', 'M:4,5,6'),
  ],
  'TND': [
    ('A', 'X:4,5,6'),
    ('B', 'M:9,10,11'),
    ('C', 'J:4,5,6'),
  ],
  'IDW': [
    ('A', 'V:1,2'),
    ('B', 'M:14,15'),
    ('C', 'J:14,15'),
  ],
}

course_sections_schedule = {
  uuid4(): [(uuid4(), schedule) for _, schedule in sections]
  for sections in data_text.values()
}

n = 100
start = time.perf_counter()
for _ in range(n):
  dom(course_sections_schedule)
end = time.perf_counter()
print('dom:', (end - start) / n)

start = time.perf_counter()
for _ in range(n):
  dom_con_desempate(course_sections_schedule)
end = time.perf_counter()
print('dom_con_desempate:', (end - start) / n)

start = time.perf_counter()
for _ in range(n):
  solve(course_sections_schedule)
end = time.perf_counter()
print('solve:', (end - start) / n)
