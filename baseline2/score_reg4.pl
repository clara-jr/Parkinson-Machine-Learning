#!/usr/bin/perl

use strict;
require "spearman.pl";


sub parse_predictions_reg {
    my $ref_arff = shift;
    my $pred_arff = shift;
    my $pred_index = shift;
    my $lab_index = shift;
    my @pred;
    my @ref;
    my $i = 0;
    my $data = 0;
    open(PRED, "<$pred_arff") or die "$pred_arff: $!";
    while(<PRED>) {
        chomp;
        if (/^[\s\t]+\d+[\s\t]+/){
            my @els = split(/[\s\t]+/);
            $pred[$i] = $els[$pred_index];
	    $ref[$i] = $els[$pred_index-1];
	    printf stdout "$i pred: %f ref: %f\n",$pred[$i],$ref[$i];
            ++$i;
        }
    }
    close(PRED);
    
   
    printf "Pearson correlation coefficient: %.7f\n", cor(\@pred, \@ref);
    printf "Spearman correlation coefficient: %.7f\n", cor(rank(\@pred), rank(\@ref));

}


my $pred_index = 3; # set to 2 if frame index is included

if ($#ARGV < 2) {
    print "Usage: $0 <ref_arff> <pred_arff> <lab-index> [ignore-list]\n";
    exit -1;
}

my ($ref_arff, $pred_arff, $lab_index) = @ARGV;

#printf stdout "Processing $ref_arff and $pred_arff with index: $lab_index\n";
parse_predictions_reg($ref_arff, $pred_arff, $pred_index, $lab_index);

