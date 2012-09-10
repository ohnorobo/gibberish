#!/usr/bin/perl
# taken from
# http://cs.fit.edu/~mmahoney/compression/textdata.html
# did not work on current wikipedia articles 
# edited by Sarah Laplante (Sept 2012)

# Program to filter Wikipedia XML dumps to "clean" text consisting only of lowercase
# letters (a-z, converted from A-Z), and spaces (never consecutive).  
# All other characters are converted to spaces.  Only text which normally appears 
# in the web browser is displayed.  Tables are removed.  Image captions are 
# preserved.  Links are converted to normal text.  Digits are spelled out.

# Written by Matt Mahoney, June 10, 2006.  This program is released to the public domain.


$/=">";                     # input record separator
while (<>) {

  if (/<p/) {$text=1;}  # remove all but between <text> ... </text>
  if (/#redirect/i) {$text=0;}  # remove #REDIRECT

  #print $_;
  #print "\n";
  #print $text;

  if ($text) {
    
    #print $_;

    # Remove any text not normally visible
    if (/<\/p>/) {$text=0;}

    s/<p>//g;               #remove <p> tags
    s/<\/p>//g;             #remove </p> tags

    s/<.*?>//g;              # remove xml tags
    #non-greedy

    s/&amp;/&/g;            # decode URL encoded chars
    s/&lt;/</g;
    s/&gt;/>/g;

    s/<ref[^<]*<\/ref>//g;  # remove references <ref...> ... </ref>
    s/<[^>]*>//g;           # remove xhtml tags
    s/\[http:[^] ]*/[/g;    # remove normal url, preserve visible text

    s/\|thumb//ig;          # remove images links, preserve caption
    s/\|left//ig;
    s/\|right//ig;
    s/\|\d+px//ig;
    s/\[\[image:[^\[\]]*\|//ig;

    s/\[\[category:([^|\]]*)[^]]*\]\]/[[$1]]/ig;  # show categories without markup
    s/\[\[[a-z\-]*:[^\]]*\]\]//g;  # remove links to other languages
    s/\[\[[^\|\]]*\|/[[/g;  # remove wiki url, preserve visible text
    s/{{[^}]*}}//g;         # remove {{icons}} and {tables}
    s/{[^}]*}//g;

    s/\[//g;                # remove [ and ]
    s/\]//g;

    s/&[^;]*;/ /g;          # remove URL encoded chars

    #print $_;

    # convert to lowercase letters and spaces
    # remove digits
    $_=" $_ ";
    tr/A-Z/a-z/;
    s/0//g;
    s/1//g;
    s/2//g;
    s/3//g;
    s/4//g;
    s/5//g;
    s/6//g;
    s/7//g;
    s/8//g;
    s/9//g;
    tr/a-z/ /cs;
    chop;

    print $_;
  }
}
