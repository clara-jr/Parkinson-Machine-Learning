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
        if (/^[\-\d]+/){
            my @els = split(/,/);
            $pred[$i] = $els[0];
#			printf stdout "pred: %f\n",$els[0];
            ++$i;
        }
    }
    close(PRED);
    
    open(REF, "<$ref_arff") or die "$ref_arff: $!";
    my $data = 0;
    my $i2 = 0;
    while (<REF>) {
        chomp;
        if (/^[\-\d]/){
            my @els = split(/,/);
#			printf stdout "ref: %f\n",$els[0];
			$ref[$i2] = $els[0];
            ++$i2;
        }
    }
    close(REF);
    if ($i != $i2) {
        print "ERROR: Mismatched number of predictions ($i) and ground truth labels ($i2)!\n";
        exit 1;
    }
    
    #print "Data:\n";
    #print "@pred\n";
    #print "@ref\n";
    #print "\nRanks:\n";
    #print Dumper(rank(\@pred));
    #print Dumper(rank(\@ref));

    printf "Pearson correlation coefficient: %.7f\n", cor(\@pred, \@ref);
    printf "Spearman correlation coefficient: %.7f\n", cor(rank(\@pred), rank(\@ref));
}


my $pred_index = 1; # set to 2 if frame index is included

if ($#ARGV < 2) {
    print "Usage: $0 <ref_arff> <pred_arff> <lab-index> [ignore-list]\n";
    exit -1;
}

my ($ref_arff, $pred_arff, $lab_index) = @ARGV;

#printf stdout "Processing $ref_arff and $pred_arff with index: $lab_index\n";
parse_predictions_reg($ref_arff, $pred_arff, $pred_index, $lab_index);

