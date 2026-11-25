import copy
from uuid import UUID

from app.domain.scheduling.dom import build_conflicts_by_section


def _reduce_and_branch_con_desempate(
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
  cruces_chosen_course = None
  for course, sections in map.items():
    count = len(sections)
    if count < min_count:
      min_count = count
      chosen_course = course
      cruces_chosen_course = None
    elif count == min_count:
      if cruces_chosen_course is None:
        cruces_chosen_course = 0
        for sections_chosen in map[chosen_course].values():
          cruces_chosen_course += len(sections_chosen)
      cruces_course = 0
      for section in sections.values():
        cruces_course += len(section)
      if cruces_chosen_course < cruces_course:
        chosen_course = course
        cruces_chosen_course = cruces_course

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

    _reduce_and_branch_con_desempate(
      map_copy, combination + (chosen_section,), combinations
    )
  return


def dom_con_desempate(
  course_sections_schedule: dict[UUID, list[tuple[UUID, str]]],
) -> list[tuple[UUID, ...]]:
  map = build_conflicts_by_section(course_sections_schedule)
  combinations: list[tuple[UUID, ...]] = []
  _reduce_and_branch_con_desempate(map, (), combinations)
  return combinations
