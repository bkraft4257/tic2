# Path to your oh-my-zsh installation.
export ZSH=/home/sunny/medeng/bkraft/.oh-my-zsh

# Set name of the theme to load.
# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
ZSH_THEME="bkraft"

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git rsync)

# User configuration 

#export PATH="/home/sunny/medeng/bkraft/scripts/:/gandg/infinite3/infinite/icGit/release/ic/studies/cenc/:/gandg/infinite3/infinite/icGit/release/ic/studies/cenc//scripts:/gandg/infinite3/infinite/icGit/release/ic/studies/nhp/:/gandg/infinite3/infinite/icGit/release/ic/studies/nhp//scripts:/gandg/infinite3/infinite/icGit/release/ic/studies/wbi/:/gandg/infinite3/infinite/icGit/release/ic/studies/wbi//scripts/:/gandg/infinite3/infinite/icGit/release/ic/studies/msk//scripts:/gandg/infinite3/infinite/icGit/release/ic/studies/msk//scripts:/gandg/infinite3/infinite/icGit/release/ic/studies/infinite/:/gandg/infinite3/infinite/icGit/release/ic/studies/infinite//scripts:/aging1/software/matlab/bin/:/aging1/software/freesurfer/bin:/aging1/software/freesurfer/fsfast/bin:/aging1/software/freesurfer/tktools:/aging1/software/fsl/bin:/aging1/software/freesurfer/mni/bin:/aging1/software/fsl/bin:/aging1/software/itksnap/bin:/opt/software/mricron:/aging1/software/ants/bin/:/gandg/infinite3/infinite/icGit/release/ic//workflows:/gandg/infinite3/infinite/icGit/release/ic//scripts:/gandg/infinite3/infinite/icGit/release/ic//interfaces:/gandg/infinite3/infinite/icGit/release/ic//environment:/gandg/infinite3/infinite/icGit/release/ic/:/usr/lib64/qt-3.3/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin"



# export MANPATH="/usr/local/man:$MANPATH"

source $ZSH/oh-my-zsh.sh

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/dsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"


#source $HOME/.imagewake2rc.sh
export TIC_PATH=/gandg/tic/

source $TIC_PATH/tic_aliases.sh
source $HOME/.tic/tic_zshrc.sh
source $HOME/.tic/studies.sh
source $HOME/.alias

export PATH="$HOME/python:/home/sunny/medeng/bkraft/scripts/:$PATH"
export PYTHONSTARTUP=$HOME/python/startup.py


# TIC NIPYPE Workflows

PATH=/gandg/bkraft/tic_workflows/nipype_workflows/workflows:$PATH

PYTHONDONTWRITEBYTECODE=1