from uuid import UUID

from ortools.sat.python import cp_model

from app.domain.scheduling.conflicts import (
  schedule_to_bitset,
)


class SolutionCollector(cp_model.CpSolverSolutionCallback):
  def __init__(self, course_vars: list[cp_model.IntVar]):
    super().__init__()
    self.course_vars = course_vars
    self.combinations: list[tuple[int, ...]] = []

  # override
  def on_solution_callback(self) -> None:
    self.combinations.append(
      tuple(self.value(course_var) for course_var in self.course_vars)
    )


# course_id: [(section_id, "L:2;M:3"), ...]
def _build_conflicts_int(
  course_sections_schedule: dict[UUID, list[tuple[UUID, str]]],
) -> tuple[
  dict[UUID, list[UUID]],  # course_sections
  list[int],  # section_counts
  list[tuple[tuple[int, int], tuple[int, int]]],  # conflicts
]:
  course_sections: dict[UUID, list[UUID]] = {}
  section_counts = [
    len(sections) for sections in course_sections_schedule.values()
  ]

  bitsets_split_by_course: list[list[int]] = []

  for course_id, section_schedule in course_sections_schedule.items():
    bitsets_of_course: list[int] = []
    section_ids: list[UUID] = []
    for section_id, schedule in section_schedule:
      bitsets_of_course.append(schedule_to_bitset(schedule))
      section_ids.append(section_id)
    bitsets_split_by_course.append(bitsets_of_course)
    course_sections[course_id] = section_ids

  # [((0, 1), (1, 2)), ...], [((CALCULO, B), (EDA, B)), ...]
  conflicts: list[tuple[tuple[int, int], tuple[int, int]]] = []
  # Todos combinaciones pares entre todos los cursos
  for course_a in range(len(bitsets_split_by_course)):
    for course_b in range(course_a + 1, len(bitsets_split_by_course)):
      bitsets_of_course_a = bitsets_split_by_course[course_a]
      bitsets_of_course_b = bitsets_split_by_course[course_b]
      for i, section_of_bitset_a in enumerate(bitsets_of_course_a):
        for j, section_of_bitset_b in enumerate(bitsets_of_course_b):
          if section_of_bitset_a & section_of_bitset_b:
            conflicts.append(((course_a, i), (course_b, j)))

  return (course_sections, section_counts, conflicts)


def _solve_by_int(
  section_counts: list[int],
  conflicts: list[tuple[tuple[int, int], tuple[int, int]]],
) -> list[tuple[int, ...]]:
  model = cp_model.CpModel()
  # Variables
  course_vars: list[cp_model.IntVar] = []
  for i, sections in enumerate(section_counts):
    # Definimos el dominio (secciones) de la variable (curso)
    course_vars.append(model.new_int_var(0, sections - 1, f'course_{i}'))

  # Restricciones
  for (course_a, section_a), (course_b, section_b) in conflicts:
    model.add_forbidden_assignments(
      [course_vars[course_a], course_vars[course_b]],
      [(section_a, section_b)],
    )

  solver = cp_model.CpSolver()
  solver.parameters.enumerate_all_solutions = True
  collector = SolutionCollector(course_vars)
  solver.solve(model, collector)
  return collector.combinations


def _ints_to_uuid(
  course_sections: dict[UUID, list[UUID]],
  combinations: list[tuple[int, ...]],
):
  section_ids_split_by_course = list(course_sections.values())
  uuid_combinations: list[tuple[UUID, ...]] = []
  for combination in combinations:
    uuid_combination: list[UUID] = []
    for i, section in enumerate(combination):
      uuid_combination.append(section_ids_split_by_course[i][section])
    uuid_combinations.append(tuple(uuid_combination))
  return uuid_combinations


def solve(
  course_sections_schedule: dict[UUID, list[tuple[UUID, str]]],
) -> list[tuple[UUID, ...]]:
  course_sections, section_counts, conflicts = _build_conflicts_int(
    course_sections_schedule
  )
  combinations = _solve_by_int(section_counts, conflicts)
  return _ints_to_uuid(course_sections, combinations)
