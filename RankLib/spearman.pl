#!/usr/bin/perl

# Scoring according to Pearson's and Spearman's CC
# Written by Felix Weninger, TUM <weninger@tum.de>

use strict;
use Data::Dumper;

# Sort 2-D array descendingly after first column
sub sort_first
{
    return $b->[0] <=> $a->[0];
}

# Compute ranks of array values, respecting ties
# Complexity: O(N log N) due to sorting
# Parameter: [0] array ref containing numerical values
# Result: [0] array ref containing ranks
sub rank
{
    my $ar = shift;
    my @atmp;
    my $i = 0;
    # get raw ranks in second column of array
    for (@$ar) {
        $atmp[$i][0] = $ar->[$i];
        $atmp[$i][1] = $i;
        ++$i;
    }
    @atmp = sort sort_first @atmp;
    # group ranks into equivalence classes by value;
    # store start and end indices of equivalence classes
    my $last_val = 0;
    my @rank = (-1) x scalar(@atmp);
    my @grp = ();
    for (my $i = 0; $i <= $#atmp; ++$i) {
        my $val = $atmp[$i][0];
        if ($i == 0 || $last_val != $val) {
            push(@grp, [ $i, $i ]);
        }
        elsif ($last_val == $val) {
            $grp[$#grp][1] = $i;
        }
        $last_val = $val;
    }
    #print Dumper(@grp);
    # replace equivalent ranks by mean
    for (my $g = 0; $g <= $#grp; ++$g) {
        my $r = ($grp[$g][0] + $grp[$g][1]) / 2;
        for (my $j = $grp[$g][0]; $j <= $grp[$g][1]; ++$j) {
            $rank[$atmp[$j][1]] = $r;
        }
    }
    return \@rank;
}

# Simple, clean implementation of Pearson CC
# Parameters:
# [0] Prediction array reference
# [1] Ground truth array reference
# Result:
# [0] Scalar containing Pearson's CC
sub cor {
    my $pred = shift;
    my $ref = shift;
  
    my $i;
    my $N = $#{$pred} + 1;
    if ($#{$ref} + 1 != $N) {
        print "Incompatible dimension: $N vs. ", $#{$ref} + 1, "\n";
        return 0;
    }
    if ($N == 0) { 
        return 0; 
    }
    my $cc = 0; my $mP = 0; my $mR = 0; 
    for ($i = 0; $i < $N; ++$i) {
         $mP += $pred->[$i];
         $mR += $ref->[$i];
    }
    $mP /= $N; $mR /= $N;
    my $sP = 0; my $sR = 0;
    for ($i = 0; $i < $N; ++$i) {
        $cc += ($pred->[$i] - $mP) * ($ref->[$i] - $mR);
        $sP += ($pred->[$i] - $mP) * ($pred->[$i] - $mP);
        $sR += ($ref->[$i] - $mR) * ($ref->[$i] - $mR);
    }
    $sR /= $N; 
    $sR = sqrt($sR);
    $sP /= $N; 
    $sP = sqrt($sP);
    if ($sP * $sR == 0) { 
        $cc = 0.0;
    }
    else {
        $cc /= ($N * $sP * $sR);
    }

    return $cc;
}

my $unit_test = $ARGV[0] eq "--test";

# test against R reference implementation
if ($unit_test) {
    # Test data
    my @a = (7, 5, 3, 4, 5, 5, 8, 3);
    my @b = (6, 4, 4, 5.5, 5.5, 5.5, 9, 2);

    print "Data:\n";
    print "@a\n";
    print "@b\n";
    print "\nRanks:\n";
    print Dumper(rank(\@a));
    print Dumper(rank(\@b));

    printf "Pearson correlation coefficient: %.7f\n", cor(\@a, \@b);
    printf "Spearman correlation coefficient: %.7f\n", cor(rank(\@a), rank(\@b));

    my $tmp = "/tmp/tmp$$.R";
    open(T, ">$tmp") or die;
    print T "a <- c(", join(",", @a), ")\n";
    print T "b <- c(", join(",", @b), ")\n";
    print T "cat(\"Pearson correlation coefficient (R):\", cor(a, b), \"Spearman correlation coefficient (R):\", cor(a, b, method=\"spearman\"), sep=\"\\n\")\n";
    close(T);
    system("R --slave --vanilla < $tmp");
    unlink($tmp);
}

# return 1 to be useful as included script
1;
