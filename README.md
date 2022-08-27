# github-repo-diff

A simple tool to check differences between forks of a repo

## Build the tool

To build the tool you need to have `python3.9` and `build` installed

Run `python3 -m build --wheel`

## Binaries

Download the binary file from the releases page

Run `pip install github_repo_diff-0.0.1-py3-none-any.whl`

## Executing a comparison

Run `compare-forks -la {First Author} -ra {Seccond Author} -r {Repo Name}` to print the results to stdout
Run `compare-forks -la {First Author} -ra {Seccond Author} -r {Repo Name} -of result.txt` to save results to a file
