# Enable bash programmable completion features in interactive shells
if [ -f /usr/share/bash-completion/bash_completion ]; then
        . /usr/share/bash-completion/bash_completion
elif [ -f /etc/bash_completion ]; then
        . /etc/bash_completion
fi

alias ll='ls -alh'
alias dnsdist='/opt/dnsdist/dnsdist'
alias dnsdist_console='/opt/dnsdist/dnsdist -c 127.0.0.1:5199 -C /etc/dnsdist/console.conf'
