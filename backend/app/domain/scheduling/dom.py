import copy
from itertools import combinations
from uuid import UUID

from app.domain.scheduling.conflicts import schedule_to_bitset


def schedules_to_bitsets(
  course_sections_schedule: dict[UUID, list[tuple[UUID, str]]],
) -> dict[UUID, list[tuple[UUID, int]]]:
  course_sections_bitset: dict[UUID, list[tuple[UUID, int]]] = {}
  for course, sections in course_sections_schedule.items():
    # Una lista para asignarla despues de llenarla
    section_bitsets: list[tuple[UUID, int]] = []
    for section, schedule in sections:
      section_bitsets.append((section, schedule_to_bitset(schedule)))
    course_sections_bitset[course] = section_bitsets
  return course_sections_bitset


def build_conflicts_by_section(
  course_sections_schedule: dict[UUID, list[tuple[UUID, str]]],
) -> dict[UUID, dict[UUID, list[tuple[UUID, UUID]]]]:  # map
  course_sections_bitset = schedules_to_bitsets(course_sections_schedule)

  conflicts_by_section: dict[UUID, dict[UUID, list[tuple[UUID, UUID]]]] = {
    course: {section: [] for section, _ in sections}
    for course, sections in course_sections_bitset.items()
  }

  for (course_a, sections_a), (course_b, sections_b) in combinations(
    course_sections_bitset.items(), 2
  ):
    for section_a, bitset_a in sections_a:
      for section_b, bitset_b in sections_b:
        if bitset_a & bitset_b:
          conflicts_by_section[course_a][section_a].append(
            (course_b, section_b)
          )
          conflicts_by_section[course_b][section_b].append(
            (course_a, section_a)
          )
  return conflicts_by_section


def _reduce_and_branch(
  map: dict[
    UUID, dict[UUID, list[tuple[UUID, UUID]]]
  ],  # list[tuple[curso, section]]
  combination: tuple[UUID, ...],
  combinations: list[tuple[UUID, ...]],
) -> None:
  if map == {}:
    combinations.append(combination)
    return
  chosen_course = next(iter(map))  # list(map.keys())[0]
  min_count = len(map[chosen_course].keys())
  for course, sections in map.items():
    count = len(sections)
    if count < min_count:
      min_count = count
      chosen_course = course

  for chosen_section, conflicts in map[chosen_course].items():
    map_copy = copy.deepcopy(map)

    for course, section in conflicts:
      for course_selected, section_selected in map_copy[course][section]:
        if (
          course_selected == chosen_course
          and section_selected == chosen_section
        ):
          continue
        map_copy[course_selected][section_selected].remove((course, section))

    for rest_section, rest_conflicts in map_copy[chosen_course].items():
      if rest_section == chosen_section:
        continue
      for other_course, other_section in rest_conflicts:
        map_copy[other_course][other_section].remove(
          (chosen_course, rest_section)
        )

    branch_valid = True
    for course, section in conflicts:
      del map_copy[course][section]
      if not map_copy[course]:
        branch_valid = False
        break

    if not branch_valid:
      continue

    del map_copy[chosen_course]

    _reduce_and_branch(
      map_copy, combination + (chosen_section,), combinations
    )
  return


def dom(
  course_sections_schedule: dict[UUID, list[tuple[UUID, str]]],
) -> list[tuple[UUID, ...]]:
  map = build_conflicts_by_section(course_sections_schedule)
  combinations: list[tuple[UUID, ...]] = []
  _reduce_and_branch(map, (), combinations)
  return combinations
