#!/usr/bin/perl

use strict;

use Data::Dumper qw(Dumper);
use FindBin qw($Bin);
use File::Basename qw(basename dirname);

use File::Path qw(mkpath rmtree);
use File::Copy qw(copy);

################################################################################
### Options 
################################################################################

use Getopt::Long;


my $ImgDir = "$Bin/images";
my $OutDir = "$Bin/../mock";
my $HelpFlag;

my @Categories = 
 (
   "wings",  
   "fuselage", 
   "empennage", 
   "firewall-forward", 
   "panel",
   "electrical", 
   "fabric", 
   "paint", 
   "blog",
 );

my $Count = @Categories;

my $Ret = Getopt::Long::GetOptions("help" => \$HelpFlag, 
                                   "count=i" => \$Count,
                                   "images=s" => \$ImgDir, 
                                   "out=s" => \$OutDir);
Usage() unless($Ret);
Usage() if($HelpFlag);

unless(-d $ImgDir)
{
  print "$ImgDir not found\n";
  Usage();
}

unless($Count >= 1)
{
  print "Count `$Count' invalid\n";
  Usage();
}

@Categories = @ARGV if(@ARGV);

################################################################################
## Main
################################################################################

my $Images = GetImages($ImgDir);
my $Date = time() - ($Count * 3600 * 25);

ResetDir($OutDir);

print "\n ";
select STDERR;
$| = 1;

for(0..$Count-1)
{
  print ".";
  print $_+1 unless($_+1 % 100);



  my $Cat = $Categories[$_ % @Categories];
  my $Img = $Images->[$_ % @$Images];

  my @Tags;
  my $CatIdx = 0;

  for(0..int(rand(@Categories)))
  {
    push(@Tags, $Categories[ $CatIdx++ % @Categories ]);
  }


  GenArticle(cat => $Cat, 
             img => $Img, 
             date => $Date, 
             tags => join(', ', @Tags)
            );

  $Date += 3600*25;
}

print("\n");




################################################################################
## Functions
################################################################################

sub GenArticle
{
  my %Args = @_;

  my $WorkTime = sprintf("%.2f", rand(4));

  my ($Sec, $Min, $H, $Day, $Month, $Year) = localtime($Args{date});

  $Year += 1900;
  $Month += 1;

  my $DateStr = "$Year-$Month-$Day";

  my $OutPath = "$OutDir/$Args{cat}/$DateStr";
  mkpath($OutPath);

  my $Text = GetText(%Args, logged => $WorkTime, date => $DateStr);

  open(F, ">$OutPath/build.rst");
  print F $Text;
  close(F);

  copy($Args{img}, $OutPath);
}

sub GetText
{
  my %Args = @_;

  my $Img = basename($Args{img});
  my $ExtraMeta;

  if($Args{cat} ne 'blog')
  {
    $ExtraMeta .= ":logged: $Args{logged}";
  }

<< "END"

Doing Stuff
###########

:tags: $Args{tags}
:summary: Summary of doing stuff
:date: $Args{date}
$ExtraMeta

I did some stuff today. 

This is stuff
-------------

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, 
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo 
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse 
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat 
non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

.. fig:: $Img
   
   This is a figure

And so stuff goes.
END
}

sub GetImages
{
  my $Dir = shift;

  opendir(D, $Dir);
  my @Ret = map { "$Dir/$_" } grep { (-f "$Dir/$_") } readdir(D);
  closedir(D);

  return(\@Ret);
}

sub ResetDir
{
  my $Dir = shift;
  rmtree($Dir);
  mkpath($Dir);
}

sub Usage
{
  my $Base = basename($0);
  print STDERR << "END";

Usage: $Base 
         [-count <count of articles per log category>]
         [-images <images dir>]
         [-out <output dir>]

         [category 1 [, category 2 ... ]]

END
  exit(1);
}



