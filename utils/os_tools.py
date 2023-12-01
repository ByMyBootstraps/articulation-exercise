import os
import re

def generateID( path_template: str ):
    import uuid
    import os

    id = uuid.uuid4()
    path = path_template.format(id=id)
    while os.path.exists(path):
        id = uuid.uuid4()
        path = path_template.format(id=id)
    return id

def lastVersion( root_dir: str, pattern: str ):
    """
    Given a target filename pattern, returns the last existing file in the series.

    root_dir: directory in which target series of files is stored
    pattern: pattern of filenames to match. looks like f"fn_prefix_{n}_fn_postfix"
    """

    pre, post = pattern.split("{n}")

    last = None
    last_n = -1
    for f in os.listdir(root_dir):
        if re.match(f"{pre}(\d+){post}", f):
            n = int(re.match(f"{pre}(\d+){post}", f).group(1))
            if n > last_n:
                last_n = n
                last = f
    return last, last_n

def nextVersion( root_dir: str, pattern: str, make_dirs: bool = False ):
    """
    Given a target filename pattern, returns the next available filename in the series.

    root_dir: directory in which target series of files is stored
    pattern: pattern of filenames to match. looks like f"fn_prefix_{n}_fn_postfix"
    """

    pre, post = pattern.split("{n}")

    if make_dirs:
        os.makedirs(root_dir, exist_ok=True)

    _, last_n = lastVersion(root_dir, pattern)

    return f"{pre}{last_n+1}{post}"