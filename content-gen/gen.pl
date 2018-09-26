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

my @Projects = qw(project.one project.two .);
my @Categories = 
 (
   "wings",  
   "fuselage", 
   "firewall-forward", 
   "no-articles",
 );

my @Tags = qw(tagone tagtwo tagthree);

my $BaseCount = @Categories * @Projects;
my $Count = 1;

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

my $No = 0;

foreach my $Proj(@Projects)
{
  my @Extras = ($Proj eq '.') ? qw(blog) : ();

  foreach my $Cat((@Categories, @Extras))
  {
    for(0..$Count-1)
    {
      unless($Cat eq 'no-articles')
      {
        my @ArticleTags;
        my $TagIdx = 0;

        for(0..int(rand(@Tags)))
        {
          push(@ArticleTags, $Tags[ $TagIdx++ % @Tags ]);
        }

        GenArticle(cat => $Cat, 
                   prj => $Proj,
                   img => $Images->[$No % @$Images],
                   no => $No,
                   date => $Date, 
                   tags => join(', ', @ArticleTags)
                  );
      }

      if($Cat ne 'blog')
      {
        AddLogEntry(cat => $Cat, 
                    prj => $Proj,
                    no => $No,
                    date => $Date, 
                   );
      }

      $No++;
      $Date += 3600*25;
    }
  }
}

print("\n");


################################################################################
## Functions
################################################################################

sub AddLogEntry
{
  my %Args = @_;

  my $WorkTime = sprintf("%.2f", rand(4));
  my ($Sec, $Min, $H, $Day, $Month, $Year) = localtime($Args{date});

  $Year += 1900;
  $Month += 1;

  my $DateStr = "$Year-$Month-$Day";
  my $OutPath = "$OutDir/$Args{prj}/$Args{cat}/";
  mkpath($OutPath) unless (-e $OutPath);

  open(F, ">>$OutPath/$Args{cat}.log");
  print F 
    "$DateStr| Log $Args{prj} entry $Args{no} work on $Args{cat}| $WorkTime\n";
  close(F);
}

sub GenArticle
{
  my %Args = @_;

  my $WorkTime = sprintf("%.2f", rand(4));

  my ($Sec, $Min, $H, $Day, $Month, $Year) = localtime($Args{date});

  $Year += 1900;
  $Month += 1;

  my $DateStr = "$Year-$Month-$Day";

  my $OutPath = "$OutDir/$Args{prj}/$Args{cat}/$DateStr-description";
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

$Args{prj}: working on $Args{cat} category, entry $Args{no}
###############################################################################

:tags: $Args{tags}
:summary: summary on $Args{cat}
:date: $Args{date}
$ExtraMeta

I did some stuff today. 
Category for this article: $Args{cat}
Project for this article: $Args{prj}
No for this article: $Args{no}

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



