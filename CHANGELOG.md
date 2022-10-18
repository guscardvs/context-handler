## 5.0.1 (2022-10-18)

### Fix

- fixed bugs in interface
- **metadata**: fixed license year and build now does not uses development libs

## 5.0.0 (2022-09-27)

### BREAKING CHANGE

- breaks all compatibility with <5.0.0

### Feat

- **context_handler**: refactored all code to be more concise and less intrusive with the handlers

### Refactor

- refactored all files and created ext module, tests missing

## 4.0.2 (2022-02-07)

### Fix

- **ensure_context**: uses typing instead of typing extensions if pyversion > 3.9

## 4.0.1 (2022-02-03)

### Fix

- **fastapi**: removed middleware from using isinstance with protocol

## 4.0.0 (2022-01-22)

### Feat

- **ensure_context**: created helper function to reduce verbosity
- **ensure_context**: added helper methods (instance, view and context)

## 2.0.2 (2021-11-11)

### Fix

- **ensure_context**: added is_coroutine flag to decorator to correctly describe coroutines at introspection

## 2.0.1 (2021-11-11)

### Fix

- **datastructures**: fixed provider type on abstract async context

## 2.0.0 (2021-11-11)

### Fix

- **_datastructures**: changed provider type from async and sync contexts in abstract

### Feat

- **generics**: fixed bug in generics with fastapi where no signature was generated and added a fastapi specific generic

## 1.2.1 (2021-10-31)

### Fix

- **git**: missing generic files

## 1.2.0 (2021-10-30)

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
