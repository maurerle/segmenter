import os
import re
import unicodedata

# https://gist.github.com/berlotto/6295018
_slugify_strip_re = re.compile(r"[^\w\s-]")
_slugify_hyphenate_re = re.compile(r"[-\s]+")


def slugify(value: str):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    From Django's "django/template/defaultfilters.py".
    """
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = _slugify_strip_re.sub("", value).strip().lower()
    return _slugify_hyphenate_re.sub("-", value)


def write_moves(public_key_to_interface: dict[str, str], repo: str) -> list[str]:
    # create folders for interfaces
    for intf in public_key_to_interface.values():
        os.makedirs(os.path.join(repo, intf), exist_ok=True)

    to_delete = []
    to_create = {}
    for root, subdirs, files in os.walk(repo):
        if ".git" in root:
            continue
        for filename in files:
            cur_path = os.path.join(root, filename)
            with open(cur_path, "r") as f:
                key = f.read().strip()
                if key in public_key_to_interface.keys():
                    seg = public_key_to_interface[key]
                    to_create[os.path.join(repo, seg, filename)] = key
                    to_delete.append(cur_path)
                # workaround for v2019 firmware - use nodename
                if filename[:-5] in public_key_to_interface.keys():
                    seg = public_key_to_interface[filename[:-5]]
                    to_create[os.path.join(repo, seg, filename)] = key
                    to_delete.append(cur_path)
    # remove old key
    for file in to_delete:
        os.remove(file)
    # write new keys
    for file, content in to_create.items():
        with open(file, "w") as f:
            f.write(content + "\n")

    committed = to_delete
    committed.extend(to_create.keys())
    return committed
