# Overview

`DataOperator` is a base class for dictionary processing. It provides the following functionality:

- returning a list of methods for a given field type and operator type
- determining a "surviving" dictionary based on an evaluation method (e.g. "keep_record_with_max_value")
- executing a method on a list of dictionaries (the dictionaries all must have the same keys) and determining the final value for a given field based on the method. (e.g. "concatenate_all_values")

## Installation

``` TODO ```

## General Usage

### Initialize DataOperator

`field_type` and `operator_type` are required. Other parameters are optional.

```python
from src.operator import DataOperator

operator = DataOperator(
    field_type="string", 
    operator_type="merge_values", 
)
```

### Get Available Methods

```python
from src.operator import DataOperator

operator = DataOperator(
    field_type="string", 
    operator_type="merge_values", 
)

methods = operator.get_methods()

print(methods)
>>> ["concatenate_all_values", "keep_max_value", "keep_min_value", "keep_recent_value", "keep_oldest_value", "keep_corporate_domains", "preserve_priority"]
```

### Merge Fields

```python
from src.operator import DataOperator

operator = DataOperator(
    field_type="string", 
    operator_type="merge_values", 
    lod=[{"name": "John"}, {"name": "Jane"}, {"name": "Bob"}], 
    field="name", 
    operator="concatenate_all_values"
)

result = operator.concatenate_all_values()

print(result)
>>> "John|Jane|Bob"
```

### Select Master Record

```python
from src.operator import DataOperator

operator = DataOperator(
    field_type="string", 
    operator_type="select_master_record", 
    lod=[{"name": "John", "age": 30}, {"name": "Jane", "age": 25}, {"name": "Bob", "age": 35}], 
    field="age", 
    operator="keep_record_with_max_value"
)

result = operator.keep_record_with_max_value()

print(result)
>>> [{"name": "Bob", "age": 35}]
