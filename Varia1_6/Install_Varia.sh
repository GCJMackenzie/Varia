#!/bin/bash
##stores the directory path to where script was called

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $DIR

##makes sure Varia.sh is executable
chmod 755 $DIR/Varia.sh

echo ""
echo ""
echo ""

##checks that samtools is installed and accessible via users PATH, if not it will notify the user
echo "Now Checking PATH for samtools faidx:"
echo "Now Checking PATH for samtools faidx:" >> Varia_install_log.txt

SMTLS=$(which samtools)

if [ "$SMTLS" = "" ]
then
	echo "samtools faidx is required by Varia to run. But no instance of samtools faidx can be found on your PATH, please install and add samtools to your PATH."
	echo "samtools faidx is required by Varia to run. But no instance of samtools faidx can be found on your PATH, please install and add samtools to your PATH." >> Varia_install_log.txt
else
	SMTLS="samtools faidx is required by Varia to run. Varia will use the samtools instance found in $SMTLS"
	echo $SMTLS
	echo $SMTLS >> Varia_install_log.txt
fi

echo ""
echo ""
echo ""

##checks that mcl is installed and accessible via users PATH, if not it will notify the user and ask if they want to try intall it using conda. If yes, conda will be used to try install mcl
echo "Now Checking PATH for mcl:"
echo "Now Checking PATH for mcl:" >> Varia_install_log.txt

MCL=$(which mcl)
if [ "$MCL" = "" ]
then
	echo "mcl is required by Varia to run. But no instance of mcl can be found on your PATH, please install and add mcl to your PATH."
	echo "mcl is required by Varia to run. But no instance of mcl can be found on your PATH, please install and add mcl to your PATH." >> Varia_install_log.txt
	read -n1 -p "Do you wish for Varia to try install mcl using CONDA? [y,n]" doit
	case $doit in
		y|Y) 
		echo " Attempting to install mcl:"
		conda install mcl
		MCL=$(which mcl)
		echo "new mcl installation is in: $MCL"
		echo "new mcl installation is in: $MCL" >> Varia_install_log.txt ;;

		n|N) 
		echo " Varia will not run without mcl, please consider installing manually if you do not wish to use conda."
		echo " Varia will not run without mcl, please consider installing manually if you do not wish to use conda." >> Varia_install_log.txt ;;
	esac	
else
	MCL="mcl is required by Varia to run. Varia will use the mcl instance found in $MCL"
	echo $MCL
	echo $MCL >> Varia_install_log.txt
fi
echo ""
echo ""
echo ""

##checks that Circos is installed and accessible via users PATH, if not it will notify the user and ask if they want to try intall it using conda. If yes, conda will be used to try install Circos
echo "Now Checking PATH for circos:"
echo "Now Checking PATH for circos:" >> Varia_install_log.txt

CIRC=$(which circos)
if [ "$CIRC" = "" ]
then
	echo "circos is required by Varia to produce output plots. But no instance of circos can be found on your PATH, please install and add circos to your PATH."
	echo "circos is required by Varia to produce output plots. But no instance of circos can be found on your PATH, please install and add circos to your PATH." >> Varia_install_log.txt
	read -n1 -p "Do you wish for Varia to try install circos using CONDA? [y,n]" doit
	case $doit in
		y|Y) 
		echo " Attempting to install circos:"
		conda install circos
		CIRC=$(which circos)
		echo "The new installation is in: $CIRC"
		echo "The new installation is in: $CIRC" >> Varia_install_log.txt ;;

		n|N) 
		echo " While Varia will run without circos it will not be able to produce plots, please consider installing manually if you do not wish to use conda."
		echo " While Varia will run without circos it will not be able to produce plots, please consider installing manually if you do not wish to use conda." >> Varia_install_log.txt ;;
	esac
else
	CIRC="circos is required by Varia to run. Varia will use the circos instance found in $CIRC"
	echo $CIRC
	echo $CIRC >> Varia_install_log.txt
fi
echo ""
echo ""
echo ""

##database setup
echo "Now checking database"
echo "Now checking database" >> Varia_install_log.txt
CANCEL=false
HERE=$(pwd)

cd $HERE/domains
##checks domains directory for a domains file
VDM=$(find vardb_domains.txt 2> /dev/null)
##if one is not fount it asks user if they want to designate one and for the name of the file to be used
##if yes it will loop until a valid domain file path is entered or the user quits.
if [ "$VDM" = "" ]
then
	echo "vardb_domains.txt was not found in $HERE/domains."
	echo "vardb_domains.txt was not found in $HERE/domains." >> Varia_install_log.txt
	read -p "Do you wish to enter a file to be used as vardb_domains.txt? [y,n]" doit
	case $doit in
		y|Y)
		VALID=false
		while [ $VALID = false ]
		do 		
		echo "Checking $HERE/domains for text files which could be used as vardb_domains.txt: "
		VDM=$(find *.txt 2> /dev/null)
		echo $VDM
		read -p "Enter text file to use as vardb_domains.txt, if it is in another directory include the full path to it or quit to cancel: " INP
		if [ "$INP" = "Quit" ] || [ "$INP" = "quit" ]
		then
			VALID=true
			CANCEL=true
			
		fi
		VCHCK=$(head $INP 2> /dev/null)
		if [ "$VCHCK" = "" ] && [ $CANCEL = false ]
		then
			echo "Cannot find or access $INP, please re-enter the file you wish to use."
		elif [ $CANCEL = false ]
		then
##makes soft link to the domains file in domains directory
			echo "Creating soft link to $INP, this will be called $HERE/domains/vardb_domains.txt"
			echo "Creating soft link to $INP, this will be called $HERE/domains/vardb_domains.txt" >> $HERE/Varia_install_log.txt
			ln -s $INP vardb_domains.txt
			echo "Creating Varia_GEM domains file"
			cut -f 1 vardb_domains.txt | sort | uniq > seqlist.txt
			while read p ;

				do grep -w $p vardb_domains.txt | sort -n -k 2 > tempstore.txt
				echo $p
				INLINE=""
				while read q ;
					do INPUT=$(echo -e "$q" | cut -f 4)
					INLINE="${INLINE}-${INPUT}"
					done<tempstore.txt
				INLINE=$(echo $INLINE | cut -d '-' -f 2- )
				echo "${p}\t$INLINE" >> vardb_GEM_domains.txt
				done<seqlist.txt

			rm seqlist.txt
			rm tempstore.txt
			VALID=true
		fi
		done ;;
		n|N) 
		echo " Domains file can be set up manually by putting a domains file in $HERE/domains and renaming it vardb_domains.txt."
		echo "Domains file can be set up manually by putting a domains file in $HERE/domains and renaming it vardb_domains.txt" >> $HERE/Varia_install_log.txt
		CANCEL=true ;;
	esac

else
	echo "vardb_domains.txt is in $HERE/domains, if you wish to use a different file as the domains file, delete vardb_domains.txt from $HERE/domains, then rerun the install script."
	echo "vardb_domains.txt is in $HERE/domains, if you wish to use a different file as the domains file, delete vardb_domains.txt from $HERE/domains, then rerun the install script." >> $HERE/Varia_install_log.txt
fi

echo ""
echo ""
echo ""
echo "Now Checking PATH for megablast:"
echo "Now Checking PATH for megablast:" > Varia_install_log.txt
echo ""

##checks that megablast is installed and accessible via users PATH, if not it will notify the user 
MGBLST=$(which megablast)

if [ "$MGBLST" = "" ]
then
	echo "megablast is required by Varia to run. But no instance of megablast can be found on your PATH, please install and add megablast to your PATH."
	echo "megablast is required by Varia to run. But no instance of megablast can be found on your PATH, please install and add megablast to your PATH." >> Varia_install_log.txt
else
	MGBLST="megablast is required by Varia to run. Varia will use the megablast instance found in $MGBLST"
	echo $MGBLST
	echo $MGBLST >> Varia_install_log.txt
fi
echo ""
echo ""
echo ""
echo "Now Checking PATH for formatdb:"
echo "Now Checking PATH for formatdb:" >> Varia_install_log.txt

##checks that formatdb is installed and accessible via users PATH, if not it will notify the user
MGDB=$(which formatdb)
if [ "$MGDB" = "" ]
then
	echo "formatdb is required by Varia to run. But no instance of formatdb can be found on your PATH, please install and add formatdb to your PATH."
	echo "formatdb is required by Varia to run. But no instance of formatdb can be found on your PATH, please install and add formatdb to your PATH." >> Varia_install_log.txt

else
	MGDB="formatdb is required by Varia to run. Varia will use the formatdb instance found in $MGDB"
	echo $MGDB
	echo $MGDB >> Varia_install_log.txt
fi
cd $HERE
echo ""
echo ""
echo ""

##checks that a file is present to be used as megavardb.fasta is present in megadb
echo "Now checking megablast database"
echo "Now checking megablast database" >> Varia_install_log.txt
CANCEL=false
cd $HERE/vardb
MDB=$(find megavardb.fasta 2> /dev/null)
##if its not present it asks the user if they want to designate a file to be megavardb
##if yes, it will ask user to enter full pathway to file to be used as megavardb, will loop until a valid file path is entered or the user quits.
if [ "$MDB" = "" ]
then
	echo "megavardb.fasta was not found in $HERE/vardb."
	echo "megavardb.fasta was not found in $HERE/vardb." >> $HERE/Varia_install_log.txt
	read -p "Do you wish to enter a database to be used as megavardb.fasta? [y,n]" doit
	case $doit in
		y|Y)
		VALID=false
		while [ $VALID = false ]
		do 		
		echo "Checking $HERE/vardb for fasta files which could be used as megavardb.fasta: "
		MDB=$(find *.fasta 2> /dev/null)
		echo $MDB
		read -p "Enter fasta file to use as megavardb, if it is in another directory include the full path to it or quit to
cancel: " INP
		if [ "$INP" = "Quit" ] || [ "$INP" = "quit" ]
		then
			VALID=true
			CANCEL=true
		fi
		VCHCK=$(head $INP 2> /dev/null)
		if [ "$VCHCK" = "" ] && [ $CANCEL = false ]
		then
			echo "Cannot find or access $INP, please re-enter the file you wish to use."
		elif [ $CANCEL = false ]
		then
			echo "Creating soft link to $INP, this will be called $HERE/vardb/megavardb.fasta"
			echo "Creating soft link to $INP, this will be called $HERE/vardb/megavardb.fasta" >> $HERE/Varia_install_log.txt
			ln -s $INP megavardb.fasta
			VALID=true
		fi
		done ;;
		n|N) 
		echo " Database can be set up manually by putting a fasta file in $HERE/vardb, renaming it megavardb.fasta, running it through formatdb and samtools faidx."
		echo " Database can be set up manually by putting a fasta file in $HERE/vardb, renaming it megavardb.fasta, running it through formatdb and samtools faidx." >> $HERE/Varia_install_log.txt
		CANCEL=true ;;
	esac
else
	echo "megavardb.fasta is in $HERE/vardb, if you wish to use a different fasta file as a database, delete megavardb.fasta from $HERE/vardb, then rerun the install script."
	echo "megavardb.fasta is in $HERE/vardb, if you wish to use a different fasta file as a database, delete megavardb.fasta from $HERE/vardb, then rerun the install script." >> $HERE/Varia_install_log.txt
fi
if [ $CANCEL = false ]
then
##creates fasta index and database files for new megavardb
	echo "Configuring database:"
	samtools faidx megavardb.fasta
	formatdb -i megavardb.fasta -p F -o T -t megavardb.fasta 
fi

cd $HERE
echo ""
echo ""
echo ""
echo "Installation complete: please add $DIR to your PATH before running Varia.sh"
echo "Installation complete: please add $DIR to your PATH before running Varia.sh" >> Varia_install_log.txt
