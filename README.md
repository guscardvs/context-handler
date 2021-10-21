# Context Handler
Gerenciador de contexto para garantir um ciclo de vida completo do cliente

# Usage:
- Exemplo com sqlalchemy.Connection
```python
from context_handler import get_factory, SyncContext
from contextlib import contextmanager

class ConnectionProvider:
  def __init__(self):
      self.engine = create_engine("sqlite://:memory:")
  
  @contextmanager
  def acquire(self):
      with self.engine.connect() as conn:
          with conn.begin():
            yield conn
```
