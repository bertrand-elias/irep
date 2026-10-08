# Stage 0: Foundations — Review Questions

## 1. Why does a `src` layout catch packaging mistakes that a flat layout hides?

In a flat layout (where the package directory sits directly in the root alongside `pyproject.toml`), running tests or Python scripts automatically adds the current working directory to `sys.path`. Python can import the local folder directly, masking critical packaging errors such as missing files in the build configuration, broken entrypoints, or flawed wheel metadata.

A `src/` layout (where code lives under `src/package_name/`) forces an explicit boundary: Python cannot import the module from the project root unless it has been properly installed into the virtual environment (e.g., via editable install). This guarantees that what passes in testing matches what gets packaged and distributed to users.

## 2. What does `mypy --strict` reject that the default settings allow? Give one concrete example

By default, `mypy` silently ignores functions that lack type annotations—it treats untyped functions as dynamic code and skips type verification on their bodies and return values.

`mypy --strict` turns on `--disallow-untyped-defs` and `--check-untyped-defs`, requiring explicit type signatures on every function parameter and return value. A concrete example occurred in our initial CLI implementation:

```python
def version_callback(value: bool):
    ...
