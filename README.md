# Varia

Varia is a tool to predict the full sequences of genes from 150-200 base pair sequences (like PCR fragments). We applied and optimised it to run on the <i>var</i> gene familly and using DBL domains, especially the DBLa domain. It is composed of two modules Varia VIP and Varia GEM.

To install Varia you can download a pre-compiled virtual machine (VM) or install it from scratch (you also need to then download the databases). <b>We would encourage user with limited experience in Linux to use the VM!</b>

## Testing

After the installation, to test the installation, go to the directory:<BR>
  ~/Varia/Varia1_6/example<BR>
  VIP: <BR>
   rm -rf IT05_1-99-Varia_Out/ # remove existing run<BR>
   Varia.sh VIP -i IT05_1.fasta  # will start Varia<BR>
   Read the instruction on screen where the files are
   
  <BR><BR>
    GEM: <BR>
     mkdir GEM # generate a directory <BR>
     cp *fasta GEM/       # copy fasta files of interest to directory<BR>
     Varia.sh GEM        # Will run GEM module using default parameters <BR>
     Read the instruction on screen. The result files, including the xls file will be in the GEM / diretory. <BR>
   

## Installation

### Virtual machine
Users without a bioinformatics setup can use our Linux virtual machine (https://tinyurl.com/VMVariaV1). You will need to install VirtualBox (https://www.oracle.com/virtualization/technologies/vm/downloads/virtualbox-downloads.html), set up Ubuntu x64 and mount the downloaded disc (.vdi). To install the virtual machine, please have look at 'VM.install.pdf' for further help. The username is 'bioinfo' and the password 'Glasgow2020'. The user has sudo rights. <BR>
Some Mac users might have problems installing the VM or Virtual Box. Normally, by googling the mistake, the problems can be overcome. Often the issue is the graph acceleration settings and must be changed. <BR>Note: At the moment, there is no support for the M1 process of a Mac for Virtual Box and Linux machines.
	  

### Git-hub installation
To install Varia, and download the current version:

First, please install all the dependencies. Especially is the legacy version of blast is not installed, the installation will fail. 

1. git clone https://github.com/GCJMackenzie/Varia.git
2. Move to directory "cd Varia/Varia1_6"
Next you need to download two files with var genes data. You can obviously provide your own, see manual, but download:
3. (a) download vardb_domains.txt.gz from https://github.com/ThomasDOtto/varDB/tree/master/Datasets/Varia/ into the directory <B>domains/</B> and unzip it

   (b) download mega_var.fasta.gz from https://github.com/ThomasDOtto/varDB/tree/master/Datasets/Varia/ into the directory <b>vardb/</b> and unzip it
4. change the attributes of executable files: chmod 755 *.sh<BR>
5. Run the installation script ./Install_Varia.sh. This will install all the needed packages.<BR>

   During installation you will be prompted to enter the names of the domains file and then the database file downloaded in steps 3(a) and 3(b) respectively. If using files from directories outside of Varia1_6/domains and Varia1_6/vardb respectively then full paths to files are required.

   The Varia_GEM domains file: Vardb_GEM_domains.txt file is automatically generated when a new domains file is specified, this may take some time with large domain files.
6. Set the path as suggested in the last line of the varia installation script: PATH=$PATH:<...Varia/Varia1_6> export PATH
7. Finally install vsearch:
conda install -c bioconda vsearch
conda install -c bioconda/label/cf201901 vsearch
8. Make a blast database from the downloaded megavardb.fasta file, using; makeblastdb -in megavardb.fasta -parse_seqids -dbtype nucl inside Varua1.6/vardb
with Varia.sh VIP -h you should get information how to run the first module.


We tested Varia on a linux and Mac (10.13) environment.



## Pre-requisites 

Varia is run in a Linux environment. To run module 1, Varia requires the following tools be installed and be included in the user’s path: (The installation script will ask permission to try and install circos and mcl using conda if they are not found on the users path.)<BR> 
-mcl v12-135: https://micans.org/mcl/<BR>
-megablast + formatdb v2.2.26: https://ftp.ncbi.nlm.nih.gov/blast/executables/legacy.NOTSUPPORTED/2.2.26/ - on a ubuntu system it can be installed easily with:<BR>
  apt install ncbi-blast+-legacy<BR>
-samtools v1.7: http://samtools.sourceforge.net/<BR>
-Vsearch 2.14.2 <BR>
-circos v 0.69-6, perl v 5.022000: http://circos.ca/software/download/circos/<BR>
  If on Ubuntu, use: apt install circos for the installation. For the VM, we had to install some perl modules (SVG.pm), which we did over CPAN - apt install circos http://circos.ca/documentation/tutorials/configuration/perl_and_modules/<BR>
- in install the python-tk library  sudo apt-get install python-tk

<BR>
The script Install_Varia.sh, has been included to help check the required tools are installed. Varia has two pipelines, the var identification and prediction, Varia_VIP, and the var gene expression analysis module, (2) Varia_GEM. 
<BR>
##Run the script

   ## VIP module
Arguments<BR>
Varia_VIP is run using the following command line:<BR>
<BR>
Varia.sh [optional arguments] -i [input tag file]<BR>
<BR>
-i is the only mandatory argument required to run Varia_VIP as this specifies the input file to be used. Varia_VIP also has a number of optional arguments, which can be used to change the output directory and change various filters used throughout the module, a detailed list of these options and their default settings can be found in the readme file, or by using:
<BR>
Varia.sh -h<BR>
<BR>

### Outputs
Varia_VIP stores it's outputs in a directory named using the -o option. In this folder are several sub-folders, the Circos plots can be found in "plots", the cluster and final summaries are in "summaries". The Domain distance plots are in "Domain_Dist_plots" with their custom config scripts in "Domain_Dist_configs". The "filedump" folder contains any intermediary files generated by Varia, kept by default but can be deleted if -d is specified. All other subfolders contain the various files used to generate the circos plots.

   ## GEM module
   Create a "GEM" directory and copy your fasta files of interest with the DBLa domains into that directory and run:<BR>
   Varia.sh GEM<BR>
   
   ### Outputs
   Varia_GEM generates inside the GEM folder cluster folder for each fasts file and a excel sheet containing all results. 
   The resulting excel sheet contains multiple tabs with the first being a summary of all the files analysed and the rest being individual results for each fasta file.  
   Each resulting tab is divided into three sections, where the the last section contains the final predicted domain composition for each cluster in ascending order. 
	
   
## Databases
Varia is building on existing var gene databases can that be found at:<BR>
ftp://ftp.sanger.ac.uk/pub/project/pathogens/Plasmodium/falciparum/PF3K/varDB/FullDataset/<BR>
and<BR>
https://github.com/ThomasDOtto/varDB<BR>


