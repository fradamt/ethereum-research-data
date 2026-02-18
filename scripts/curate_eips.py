#!/usr/bin/env python3
"""curate_eips.py — Copy all EIPs into corpus/eips/.

Copies every eip-*.md file from the given EIPs directory, using mtime
checks to skip files that haven't changed. Removes stale files that no
longer exist in the source.

Usage:
    python3 scripts/curate_eips.py --eips-dir /path/to/EIPs/EIPS
"""

import argparse
import os
import shutil
import sys
import tempfile


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Copy all EIPs to corpus/eips/"
    )
    parser.add_argument(
        "--eips-dir",
        required=True,
        help="Path to the EIPs directory containing eip-*.md files",
    )
    args = parser.parse_args()

    eips_dir = os.path.abspath(args.eips_dir)
    if not os.path.isdir(eips_dir):
        print(f"Error: {eips_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    repo_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    out_dir = os.path.normpath(os.path.join(repo_root, "corpus", "eips"))
    os.makedirs(out_dir, exist_ok=True)

    copied = 0
    skipped = 0
    source_filenames: set[str] = set()

    for filename in sorted(os.listdir(eips_dir)):
        if not filename.startswith("eip-") or not filename.endswith(".md"):
            continue

        source_filenames.add(filename)
        src = os.path.join(eips_dir, filename)
        dest = os.path.join(out_dir, filename)

        # Only copy if source is newer or dest doesn't exist.
        # Use atomic write (tempfile + os.replace) so a crash mid-copy
        # never leaves a truncated file that passes the mtime check.
        if not os.path.exists(dest) or os.path.getmtime(src) > os.path.getmtime(dest):
            fd, tmp = tempfile.mkstemp(dir=out_dir, suffix=".tmp")
            try:
                os.close(fd)
                shutil.copy2(src, tmp)
                os.replace(tmp, dest)
            except BaseException:
                try:
                    os.unlink(tmp)
                except OSError:
                    pass
                raise
            copied += 1
        else:
            skipped += 1

    # Remove stale files (EIPs deleted from source)
    removed = 0
    for existing in os.listdir(out_dir):
        if existing.startswith("eip-") and existing.endswith(".md"):
            if existing not in source_filenames:
                os.remove(os.path.join(out_dir, existing))
                removed += 1

    total = copied + skipped
    print("EIP sync complete:")
    print(f"  {total} EIPs in corpus/eips/")
    print(f"  {copied} copied (new/updated)")
    print(f"  {skipped} already up to date")
    if removed:
        print(f"  {removed} stale files removed")


if __name__ == "__main__":
    main()
