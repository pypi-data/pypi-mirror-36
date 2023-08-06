# Sqla-filters-yaml

Add yaml parser to the sqla-filters package.

## Introduction 

Add YAML support to sqla-filters.


## Requirements

This package use the python package `pyyaml`. To install pyyaml you need to have the **yaml.h** header file. If it's not
present on your system you need to install the libyaml-dev package.

- On Fedora
```bash
sudo dnf install libyaml-devel
```

- On Debian based distribution (Ubuntu, ...)
```bash
sudo apt install libyaml-dev
```

## Installation

```bash
pip install sqla-filter-yaml
```

## Getting Started

### YAML format

```yml
---
type: and
data:
- type: or
  data:
  - type: operator
    data:
      attribute: name
      operator: eq
      value: toto
  - type: operator
    data:
      attribute: name
      operator: eq
      value: tata
- type: operator
  data:
    attribute: age
    operator: eq
    value: 21
```

:warning: Yaml format can change in the futur. :warning:

### Example code

Create an instance of the YAMLilterParser from the yaml string / document.

Example:
```python
# Sqlalchemy setup + model definition

# Create a YAML parser instance
parser = YAMLiltersParser(raw_json_string)

# You can finaly filter your query
query = session.query(Post)
filtered_query = parser.tree.filter(query)

# Get the results
query.all()
```

### Result tree

```
                                      +----------------------+
                                      |                      |
                                      |          and         |
                                      |                      |
                                      -----------------------+
                                                 ||
                                                 ||
                                                 ||
                    +----------------------+     ||     +----------------------+
                    |                      |     ||     |                      |
                    |          or          <------------>      age == 21       |
                    |                      |            |                      |
                    +----------------------+            +----------------------+
                               ||
                               ||
                               ||
+----------------------+       ||       +----------------------+
|                      |       ||       |                      |
|     name == toto     <---------------->     name == tata     |
|                      |                |                      |
+----------------------+                +----------------------+
```

# Contribute

Fork the repository and run the following command to install the dependencies and the dev dependencies.

`pip install -e '.[dev]'`
