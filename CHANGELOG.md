## 1.3.0 (2021-11-02)

### Feat

- **generics**: fixed bug in generics with fastapi where no signature was generated and added a fastapi specific generic

## 1.2.1 (2021-10-31)

### Fix

- **git**: missing generic files

## 1.2.0 (2021-10-31)

### Feat

- **getters**: created getters to use abstract interfaces instead of concrete implementations

## 1.1.0 (2021-10-27)

### Feat

- **global**: added support to python3.8 and forward versions

## 1.0.1 (2021-10-27)

### Fix

- **context**: fixed typing

## 1.0.0 (2021-10-24)

### Feat

- **global**: changed ensure_context, created immutable provider classes to prevent provider mutation at runtime and added tests
- **adapters**: created middleware adapters to clean contexts in request.ctx and request.state in sanic and fastapi

## 0.2.0 (2021-10-21)

### Feat

- **utils**: created decorators to open context automatically before function calls

## 0.1.0 (2021-10-21)

### Feat

- **initial**: created factory, sync and asynccontext classes and typeshed
