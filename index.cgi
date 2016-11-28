#! /usr/pkg/bin/perl -Tw
#
# Originally written by Jan Schaumann
# <jschauma@netmeister.org> in May 2015.
#
# This trivial little CGI merely shells out to
# 'xkcdpassword' (see
# https://github.com/redacted/XKCD-password-generator).
#
# Copyright 2016 Yahoo Inc.
# Licensed under the terms of the New-BSD license.
# Please see LICENSE file in the project root for
# terms.

use strict;
use CGI qw(:standard);

print "Content-Type: text/html; charset=utf-8\n\n";

###
### Globals
###

my $PWGEN = "/usr/pkg/bin/xkcdpass";
my @ARGS;
my $CWD = ".";

$ENV{'PATH'} = "/home/y/bin:/usr/bin:/bin:/usr/sbin:/sbin";

my $CGI = new CGI;

###
### Functions
###

sub generatePassphrase() {
	my $num = "32";
	my $count = 1;
	my $wordfile = "$CWD/en.txt";

	if ($CGI->param('num')) {
		my $n = $CGI->param('num');
		if ($n =~ m/^(\d+)$/) {
			$num = $1;
		}
	}
	push(@ARGS, "-n", $num);

	if ($CGI->param('lang')) {
		my $lang = $CGI->param('lang');
		if ($lang =~ m/^([a-z]+)$/) {
			my $file = "$CWD/$1.txt";
			if ( -e $file ) {
				$wordfile = $file;
			}
		}
	}
	push(@ARGS, "-w", $wordfile);

	if ($CGI->param('count')) {
		my $n = $CGI->param('count');
		if ($n =~ m/^(\d+)$/) {
			$count = $1;
		}
		push(@ARGS, "-c", $count);
	}

	if ($CGI->param('acrostic')) {
		my $acrostic = '""';
		my $a = $CGI->param('acrostic');
		if ($a =~ m/^([a-z]+)$/i) {
			$acrostic = $1;
		}
		push(@ARGS, "-a", $acrostic);
	}


	if (!$CGI->param('nohtml')) {
		print <<EOD
    <h3><pre>
EOD
;
	}

	binmode STDOUT, ":utf8"; 

	if ($CGI->param('complex')) {
		if (!$CGI->param('num')) {
			$num = 50;
		}

		my $i = 0;
		while ($i < $count) {
			system("dd if=/dev/urandom count=${num} 2>/dev/null | tr -dc 'A-Za-z0-9`~!@#$%^&*()_+[]{}\|;:?,./' | head -c ${num} | xargs");
			$i++;
		}
	} else {
		my $cmdl = join(" ", $PWGEN, @ARGS);
		my $line = `$cmdl`;
		print "$line\n";
	}
	if (!$CGI->param('nohtml')) {
		print "</pre></h3>\n";
	}
}

sub printHead() {
	print <<EOD
<HTML>
  <HEAD>
    <TITLE>pwgen -- a password/passphrase generator</TITLE>
    <link rel="stylesheet" type="text/css" href="pwgen.css">
  </HEAD>
  <BODY>
  <h2>Here is your custom, artisanal, hand-crafted passphrase:</h2>
  <hr>
EOD
;
}

sub printFoot() {
	print <<EOD
  <HR>
  <FORM ACTION="index.cgi">
EOD
;

	my %whitelist = ( "acrostic" => 1,
				"complex" => 1,
				"count" => 1,
				"lang" => 1,
				"num" => 1);
	if ($CGI->param) {
		foreach my $k ($CGI->param) {
			if ($whitelist{$k} and ($CGI->param($k) =~ m/^[a-z0-9]*$/i)) {
				print "<input type='hidden' name='$k' value='" . $CGI->param($k) . "'>\n";
			}
		}
	}

	print <<EOD
    <input type="submit" value="Again.">
  </FORM>
  <hr>
  <FORM ACTION="index.cgi">
    <table border="0">
      <tr>
        <td>Number of words:</td>
        <td><input type="text" name="num" width="5" value="
EOD
;
	if ($CGI->param('num')) {
		print $CGI->param('num') . "\"></td>\n";
	} else {
		print "4\"></td>\n";
	}

	print <<EOD
        <td>or acrostic:</td>
        <td><input name="acrostic" type="text" width="5" value="
EOD
;
	if ($CGI->param('acrostic')) {
		print $CGI->param('acrostic') . "\"></td>\n";
	} else {
		print "\"></td>\n";
	}

	print <<EOD
      </tr>
      <tr>
        <td>How many?</td>
        <td><input name="count" value="5"></td>
        <td>What language?</td>
        <td><select name="lang">
EOD
;
	foreach my $lang ("en", "de", "fr", "nl") {
		print "            <option value=\"$lang\" ";
		if ((!$CGI->param && $lang eq "en") ||
		    ($CGI->param && $CGI->param('lang') && $CGI->param('lang') eq $lang)) {
			print "selected";
		}
		print ">$lang\n";
	}

	print <<EOD
            </select></td>
      </tr>
      <tr>
        <td colspan="4">
          <input type="submit" value="Generate specified passphrases.">
        </td>
      </tr>
    </table>
  </FORM>
  <hr>
  <FORM ACTION="index.cgi">
    <table border="0">
      <tr>
        <td>Number of characters:</td>
        <td><input type="text" name="num" width="5" value="50"></td>
      </tr>
      <tr>
        <td>How many?</td>
        <td colspan="4"><input name="count" value="1"></td>
      </tr>
      <tr>
        <td colspan="2">
          <input type="hidden" name="complex" value="1">
          <input type="submit" value="Gimme a complex password.">
        </td>
      </tr>
    </table>
  </FORM>
  <hr>
  [Made by <a href="https://twitter.com/jschauma">\@jschauma</a>&nbsp;|&nbsp;[<a href="about.html">about</a>]&nbsp;|&nbsp;[<a href="/blog/">Other Signs of Triviality</a>]
EOD
;
	print <<EOD
  </BODY>
</HTML>
EOD
;
}

###
### Main
###

if (!$CGI->param('nohtml')) {
	printHead();
}

generatePassphrase();

if (!$CGI->param('nohtml')) {
	printFoot();
}
