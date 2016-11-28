# pwgen -- a password / passphrase generator

Need a passphrase? Go to https://www.netmeister.org/pwgen/.

----

## What is this?

[This service](https://www.netmeister.org/pwgen/) will
generate for you -- just you! -- a unique, artisanal,
hand-crafted passphrase.  By default, the passphrase
will consist of 4 english words, hopefully allowing
you to be able to memorize it while at the same time
providing sufficient entropy to make it reasonably
secure.

You may be familiar with this concept from this [xkcd
comic](https://xkcd.com/936/).

## I don't like the HTML.

Yeah, I know. I don't even CSS, really.

If you want just your unique, artisanal, hand-crafted
passphrase pass nohtml=1 in your request.

## So these are good passwords, then?

Not necessarily. They are generated on a VM using the
operating system's PRNG which was seeded in who knows
what manner. The wordlists contains 5K words each, but
if the attacker knew that you're generating exactly
four words and they know your acrostic word (if any),
then this wouldn't be a very strong password.

However, these passphrases might still be better than
any passphrase you come up with yourself, because
unfortunately humans are rather predictable and would
generate low-entropy passphrases even using this
schema.

In the end, you shouldn't even need this generator at
all. Use a password manager, like 1Password, lastpass,
Dashlane, or something like that.

The best password is one that you don't even know.

## How was this implemented?

This site uses the
[XKCD-password-generator](https://github.com/redacted/XKCD-password-generator)
for generation of xkcd style passphrases.

For the generation of complex passwords, it basically runs:

```
 tr -dc 'A-Za-z0-9`~!@#$%^&*()_+[]{}\|;:?,./' < /dev/urandom \
         | head -c ${num} | xargs
```
