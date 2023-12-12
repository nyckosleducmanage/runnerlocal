#!/bin/bash

echo "Running tests for $(basename $(pwd)) ..."

declare -A tool_map=(
    ["terraform"]="terraform -version"
    ["terragrunt"]="terragrunt -version"
    ["go"]="go version"
    ["docker"]="docker --version"
    ["python"]="python --version"
    ["pip"]="pip --version"
    ["git"]="git --version"
    ["jq"]="jq --version"
    ["az"]="az --version"
    ["js-yaml"]="node -e 'require(\"js-yaml\")'"
)

failure=0

# Continue on failure so we see all errors in one run
for tool in "${!tool_map[@]}"; do
    version_cmd="${tool_map[$tool]}"
    echo -e "\n>> Checking $tool"
    eval "$version_cmd" || { failure=1; echo "Failed $tool check"; }
done

[ "$failure" -eq 1 ] && exit 1 || echo "All checks passed!"