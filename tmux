#tmux config

#couldnt upload file github said hidden file anyway

# Remap prefix from 'C-b' to 'C-a'
unbind C-b                  # remove bind for C-b
set-option -g prefix C-a    
bind-key C-a send-prefix

set -g mode-mouse on
set -g mouse-select-pane on
set -g mouse-select-window on

set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'

set -g @plugin "arcticicestudio/nord-tmux"



run "~/.tmux/plugins/tpm/tpm"

