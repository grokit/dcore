let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

" Losely based on:
" http://candidtim.github.io/vim/2017/08/11/write-vim-plugin-in-python.html

python3 << EOF
import sys
import os.path 
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = os.path.normpath(os.path.join(plugin_root_dir, '..', 'python3'))
sys.path.insert(0, python_root_dir)
import main
EOF

function! DextTest()
    python3 main.test_print()
endfunction

function! DextOpenLink()
    python3 main.open_link()
endfunction

function! DextNotify_FileOpened()
    python3 main.notify_file_opened_or_created()
endfunction

function! DextNotify_FileMisc()
    python3 main.notify_file_opened_or_created()
endfunction
