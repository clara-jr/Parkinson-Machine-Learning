#!/usr/bin/perl

use strict;

# please set
my $site_name = "TUM_baseline";

my ($arff, $pred, $out, $lab_index) = @ARGV;
if (!$arff || !$pred || !$out || !$lab_index) {
    print "Usage: $0 <arff> <pred> <out_arff> <lab-index>\n";
    exit 1;
}

my $include_frame_index = 0;

open(ARFF, $arff) or die "$arff: $!";
open(PRED, $pred) or die "$pred: $!";
open(OUT, '>', $out) or die "$out: $!";
print OUT "\@relation ComParE2015_Parkinson_$site_name\n";
print OUT "\@attribute instance_name string\n";
#print OUT "\@attribute frame_index numeric\n";
print OUT "\@attribute prediction numeric\n";
print OUT "\@data\n";


my $data = 0;
my $npred = 0;
while (<ARFF>) {
    if (/\@data/) {
        $data = 1;
    }
    elsif ($data && !/^\s*$/) {
        my @els = split(/,/);
        my $inst = $els[0];
        my $fi = $els[1];
        if (eof(PRED)) {
            print "ERROR: Wrong number of lines in $pred!\n";
            exit -1;
        }
        my $ok = 0;
        while (!eof(PRED)) {
            my $line = <PRED>;
            chomp($line);
            $line =~ s/^\s+//;
            my @els = split(/\s+/, $line);
            if ($els[0] =~ /^\d+/) {
                my $pred  = $els[2];
                print OUT $inst;
                if ($include_frame_index) {
                    print OUT ",$fi";
                }
                print OUT ",$pred\n";
                $ok = 1;
                ++$npred;
                last;
            }
        }
        #last if ($npred == 100);
        if (!$ok) {
            print "ERROR: No prediction found for $inst in $pred!\n";
            exit -1;
        }
    }
}
#print "npred = $npred\n";

close(ARFF);
close(PRED);
close(OUT);
