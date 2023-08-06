json_mapper_distinct
====================

Get a non-vectored, distinct map of a JSON structure.

Better documentation to come at some point.


## Example usage

### Passing a JSON string directly
```
from json_mapper import JsonMap

json_string = """
[
    {
        "key1": 1,
        "key2": "Test"
    },
    {
        "key1": 2,
        "key2": "Another String"
    },
    {
        "key1": "Lolzstring",
        "key2": 3
    },
    {
        "key3": "Lolzstring",
        "key2": {
            "key3": "Lolzstring",
            "key2": 3
        }
    }
]
"""

jmap = JsonMap(source_json=sj, is_file=False)

```

### Passing a file location
```
from json_mapper import JsonMap

jmap = JsonMap(source_json='example.json')
```

### Output
```
jmap.print_map()

[
    {
        "key1": "int",
        "key2": "str"
    },
    {
        "key3": "str",
        "key2": {
            "key2": "int",
            "key3": "str"
        }
    },
    {
        "key2": "int",
        "key1": "str"
    }
]
```

### Interpreting the Output
This is basically a string representation of what you can find in the JSON structure.

In the example, it shows that the top level object in the structure is a list comprised of dictionaries.

These dictionaries are then mapped as to what their keys can contain - whether it's a scalar (shows the type) or another list or dictionary.

You'll also notice that it's de-duped. So the first two dictionaries in the example up top collapse down to:
```
{
    "key1": "int",
    "key2": "str"
}
```