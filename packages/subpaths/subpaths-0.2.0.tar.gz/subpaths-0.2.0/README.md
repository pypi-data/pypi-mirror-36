# Subpaths
Finding common subpaths and counting occurrences of all subpaths between paths.


## Examples

### Finding common subpaths between paths

```
from pprint import pprint
from subpaths.subpaths import find_all_common_subpaths_between

path_a = [1, 2, 3, 4, 5]
path_b = [3, 4, 5, 7]
path_c = [2, 3, 4, 8, 9, 7]

pprint(find_all_common_subpaths_between(path_a, path_b, path_c))
```

Will return:

```
{(3, 4)}
```


### Counting all subpaths between paths

```
from pprint import pprint
from subpaths.subpaths import find_all_subpath_occurrences

path_a = [1, 2, 3, 4, 5]

pprint(find_all_subpath_occurrences(path_a))

path_b = [3, 4, 5, 7]
path_c = [2, 3, 4, 8, 9, 7]

pprint(find_all_subpath_occurrences(path_a, path_b, path_c))

```

Will return:
```
defaultdict(<class 'int'>,
            {(1, 2): 1,
             (1, 2, 3): 1,
             (1, 2, 3, 4): 1,
             (1, 2, 3, 4, 5): 1,
             (2, 3): 1,
             (2, 3, 4): 1,
             (2, 3, 4, 5): 1,
             (3, 4): 1,
             (3, 4, 5): 1,
             (4, 5): 1})
defaultdict(<class 'int'>,
            {(1, 2): 1,
             (1, 2, 3): 1,
             (1, 2, 3, 4): 1,
             (1, 2, 3, 4, 5): 1,
             (2, 3): 2,
             (2, 3, 4): 2,
             (2, 3, 4, 5): 1,
             (2, 3, 4, 8): 1,
             (2, 3, 4, 8, 9): 1,
             (2, 3, 4, 8, 9, 7): 1,
             (3, 4): 3,
             (3, 4, 5): 2,
             (3, 4, 5, 7): 1,
             (3, 4, 8): 1,
             (3, 4, 8, 9): 1,
             (3, 4, 8, 9, 7): 1,
             (4, 5): 2,
             (4, 5, 7): 1,
             (4, 8): 1,
             (4, 8, 9): 1,
             (4, 8, 9, 7): 1,
             (5, 7): 1,
             (8, 9): 1,
             (8, 9, 7): 1,
             (9, 7): 1})
```

## Download

```
pip install subpaths
```


## Future Improvements

- Bound the shorted and longest paths to generate and count
