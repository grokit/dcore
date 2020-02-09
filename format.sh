# sudo apt install yapf
# see https://github.com/google/yapf
find . | grep \.py$ | xargs yapf --in-place --style='{based_on_style: pep8, indent_width: 4}' 
