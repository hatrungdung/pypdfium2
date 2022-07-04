#! /usr/bin/env python3
# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: Apache-2.0 OR BSD-3-Clause

import sys
import shutil
import argparse
from os.path import dirname, abspath, join

sys.path.insert(0, dirname(dirname(abspath(__file__))))
from pl_setup.packaging_base import (
    SourceTree,
    run_cmd,
    get_changelog_staging,
)


RepositoryURL = "https://github.com/pypdfium2-team/pypdfium2"

def get_url(tag):
    return RepositoryURL + "/tree/%s" % tag

def generate_tags_list(Git, count=10):
    tags_str = run_cmd([Git, "for-each-ref", "--count=%s" % count, "--sort=-creatordate", "--format", "%(refname)", "refs/tags"], cwd=SourceTree, capture=True)
    tags_list = tags_str.split("\n")
    return tags_list


def get_tag(tags_list, n_descends, skip_beta=False):
    i = 0
    for line in tags_list:
        tag = line.split("/")[-1].strip()
        if skip_beta and i > 0 and "b" in tag:
            continue
        if i >= n_descends:
            break
        i += 1
    return tag


def parse_args():
    parser = argparse.ArgumentParser(
        description = "Release note generator script.",
    )
    parser.add_argument(
        "--flush",
        action = "store_true",
        help = "Clean up `changelog_staging.md` after extracting its content.",
    )
    return parser.parse_args()


def main():
    
    args = parse_args()
    changelog_kws = dict()
    if args.flush:
        changelog_kws["flush"] = True
    summary = get_changelog_staging(**changelog_kws)
    if summary:
        summary += "\n"
    
    Git = shutil.which("git")
    tags_list = generate_tags_list(Git)
    current_tag, prev_tag = get_tag(tags_list, 0), get_tag(tags_list, 1, True)
    print(current_tag, prev_tag)
    
    relnotes = "Release %s\n\n" % current_tag
    relnotes += "## Changes\n\n"
    relnotes += "### Manual Summary\n\n"
    relnotes += summary
    relnotes += "### Git History\n\nCommits between "
    relnotes += "[`%s`](%s) and [`%s`](%s) " % (prev_tag, get_url(prev_tag), current_tag, get_url(current_tag))
    relnotes += "(latest commit first):\n\n"
    relnotes += run_cmd([Git, "log", "%s..%s" % (prev_tag, current_tag), "--pretty=format:* %H %s"], cwd=SourceTree, capture=True)
    relnotes += "\n"
    
    with open(join(SourceTree, "RELEASE.md"), "w") as fh:
        fh.write(relnotes)


if __name__ == "__main__":
    main()
