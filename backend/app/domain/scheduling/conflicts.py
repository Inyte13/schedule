DAY_POSITIONS = {'L': 0, 'M': 1, 'X': 2, 'J': 3, 'V': 4}


def schedule_to_bitset(schedule: str) -> int:
  mask = 0
  for day_str in schedule.split(';'):
    day, blocks = day_str.split(':')
    day_position = DAY_POSITIONS[day]
    for block_str in blocks.split(','):
      block = int(block_str)
      bit_position = day_position * 15 + block - 1
      # Prendemos el bit
      mask |= 1 << bit_position
  return mask
