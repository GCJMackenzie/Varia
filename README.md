# Varia
Repository for Varia package, containing Varia VIP and Varia GEM

#Pre-requisites

Varia is run in a Linux environment. To run module 1, Varia requires the following tools be installed and be included in the user’s path:
-mcl v12-135: https://micans.org/mcl/
-megablast + formatdb v2.2.26: https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download
-samtools v1.7: http://samtools.sourceforge.net/
-Vsearch 2.14.2 
-circos v 0.69-6, perl v 5.022000: http://circos.ca/software/download/circos/

The script Install_Varia.sh, has been included to help check the required tools are installed. Varia has two pipelines, the var identification and prediction, Varia_VIP, and the var gene expression analysis module, (2) Varia_GEM. 

#Run the script

Arguments
Varia_VIP is run using the following command line:

Varia.sh [optional arguments] -i [input tag file]

-i is the only mandatory argument required to run Varia_VIP as this specifies the input file to be used. Varia_VIP also has a number of optional arguments, which can be used to change the output directory and change various filters used throughout the module, a detailed list of these options and their default settings can be found in the readme file, or by using:

Varia.sh -h

# Databases
Varia is building on existing var gene databases can that be found at:
ftp://ftp.sanger.ac.uk/pub/project/pathogens/Plasmodium/falciparum/PF3K/varDB/FullDataset/
and
https://github.com/ThomasDOtto/varDB


