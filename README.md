# Varia
Varia is a tool to predict var genes based on short 150-200 base pair sequences (like PCR fragments). It is composed of two module Varia VIP and Varia GEM.

To install Varia, and first download the current version, eg.
1. git clone https://github.com/GCJMackenzie/Varia.git
2. Move to direcory "cd Varia/Varia1_6"
3. Next you need to download two files with var genes data. You can obviously provide your own, see manual, but download:<BR>
3a: download vardb_domains.txt.gz from https://github.com/ThomasDOtto/varDB/tree/master/Datasets/Varia/ into the directory domains and unzip it<BR>
  Run next:  cat vardb_domains.txt | perl -e 'while(<STDIN>){@ar=split(/\t/); chomp($ar[3]); $h{$ar[0]}.=$ar[3]."-"}; foreach $k (keys %h){ print "$k\t$h{$k}\n"}'  > vardb_GEM_domains.txt to generate a different version of the domains
3b download mega_var.fasta.gz from https://github.com/ThomasDOtto/varDB/tree/master/Datasets/Varia/ into the directory vardb and unzip it
4. change the attributes of executable files: chmod 755 *.sh
5. Run the installation scrip ./Install_Varia.sh. This will install all the needed packages.
6. Set the path as suggested in the last line of the varia installation script:
PATH=$PATH:<...Varia/Varia1_6> export PATH
7. Finally install vsearch: <BR>
  conda install -c bioconda vsearch<BR>
conda install -c bioconda/label/cf201901 vsearch 

with Varia.sh VIP -h you should get information how to run the first module. 

We tested Varia on a linux enviroment, (not Mac yet).




#Pre-requisites 

Varia is run in a Linux environment. To run module 1, Varia requires the following tools be installed and be included in the user’s path: (The installation script will try to install some of them)<BR> 
-mcl v12-135: https://micans.org/mcl/<BR>
-megablast + formatdb v2.2.26: https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download<BR>
-samtools v1.7: http://samtools.sourceforge.net/<BR>
-Vsearch 2.14.2 <BR>
-circos v 0.69-6, perl v 5.022000: http://circos.ca/software/download/circos/<BR>
<BR>
The script Install_Varia.sh, has been included to help check the required tools are installed. Varia has two pipelines, the var identification and prediction, Varia_VIP, and the var gene expression analysis module, (2) Varia_GEM. 
<BR>
#Run the script

Arguments<BR>
Varia_VIP is run using the following command line:<BR>
<BR>
Varia.sh [optional arguments] -i [input tag file]<BR>
<BR>
-i is the only mandatory argument required to run Varia_VIP as this specifies the input file to be used. Varia_VIP also has a number of optional arguments, which can be used to change the output directory and change various filters used throughout the module, a detailed list of these options and their default settings can be found in the readme file, or by using:
<BR>
Varia.sh -h<BR>
<BR>
# Databases
Varia is building on existing var gene databases can that be found at:<BR>
ftp://ftp.sanger.ac.uk/pub/project/pathogens/Plasmodium/falciparum/PF3K/varDB/FullDataset/<BR>
and<BR>
https://github.com/ThomasDOtto/varDB<BR>


