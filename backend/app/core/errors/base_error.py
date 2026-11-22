class AppError(Exception):
  status_code = 500
  base_code = 'INTERNAL_ERROR'
  code = 'INTERNAL_ERROR'
  message = 'Ocurrió un error inesperado'

  def __init__(self, message: str | None = None):
    self.message = message or self.message
    super().__init__(self.message)


class DomainError(AppError):
  pass


class AuthError(AppError):
  pass
