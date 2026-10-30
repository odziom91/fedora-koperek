#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <upstream-tag-or-version> (example: v2.0.5)" >&2
    exit 2
fi

version="${1#v}"

if [[ ! "$version" =~ ^[0-9]+(\.[0-9]+)*([._+-][A-Za-z0-9.-]+)?$ ]]; then
    echo "Invalid version: $1" >&2
    exit 2
fi

spec_file="headsetkontrol.spec"
if [[ ! -f "$spec_file" ]]; then
    echo "Run this script from the packaging repository root." >&2
    exit 1
fi

sed -i -E "s/^Version:[[:space:]]*.*/Version:        ${version}/" "$spec_file"
echo "Updated ${spec_file} to version ${version}."
echo "Review the diff, then commit and push the packaging repository."
