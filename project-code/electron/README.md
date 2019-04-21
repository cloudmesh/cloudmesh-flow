# Info

<https://electronjs.org/docs/tutorial/first-app#trying-this-example>

run npm not as sudo

<https://github.com/sindresorhus/guides/blob/master/npm-global-without-sudo.md>

mkdir "${HOME}/.npm-packages"

##in ~/.npmrc add
prefix=${HOME}/.npm-packages

## .bash_profile

NPM_PACKAGES="${HOME}/.npm-packages"

export PATH="$NPM_PACKAGES/bin:$PATH"

# Unset manpath so we can inherit from /etc/manpath via the `manpath` command
unset MANPATH # delete if you already modified MANPATH elsewhere in your config
export MANPATH="$NPM_PACKAGES/share/man:$(manpath)"
