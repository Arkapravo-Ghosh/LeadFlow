#!/usr/bin/env python3
"""Check new commit titles against Conventional Commits 1.0.0."""
import re
import sys
from pathlib import Path

message = Path(sys.argv[1]).read_text().splitlines()[0]
pattern = r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-zA-Z0-9._/-]+\))?!?: .+"
if not re.fullmatch(pattern, message):
    sys.exit("Use a Conventional Commit, e.g. feat(web): add lead search")
