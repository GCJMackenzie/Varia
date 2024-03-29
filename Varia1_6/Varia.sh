#!/bin/bash

echo "Checking Parameters."

##obtains current path to Varia1_6 directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ "$1" = "VIP" ]
	then
	echo "Activating VIP module."

	##full name of input file. No default, must be user specified.
	INFILE=""

	##Identity filter for initial blast hit. Default 99%.
	IDENTA=99

	##Identity filter for pre-clustering filter. Default 99%.
	IDENTB=99

	##Length filter for initial blast hit. Default 200 base pairs.
	LENGTH=200

	## Percentage length filter for pre-clustering filter. Default 80%.
	PERCENT=80

	##Check value for whether to keep filedump contents. Default false.
	DUMPCHECK=false

	##Check value for whether to generate plots. Config files generated regardless Default true
	GRAPHCHECK=true

	##Name of output directory. Default [Input file basename]-[IDENTA]-Varia_Out, (value set later in program).
	OUTDIR=""

	##Loop starts to check user provided arguements.
	while [ -n "$2" ]; do # while loop starts
	 
		case "$2" in

		## -f provides the initial identity filter.  
		-f) 
			shift
			IDENTA=$2
	 
			##Checks -f is a numeric value.
			echo $IDENTA 
			if ! echo $IDENTA | egrep -q '^[0-9]+\.?[0-9]*$';
			then
				echo "Identity score must be between 0 and 100"
				exit
			fi
			##Checks -f is not greater than 100. (Can't be below zero as this would require non-numeric characters, which check above prevents).
			UPCHECK=$(echo "$IDENTA > 100" | bc -l)
			
			if [ "$UPCHECK" = "1" ]
			then
				echo "Identity score out of range, keep identity score between 0 and 100"
				exit
			fi 
			;;


		## -l sets the length filter for initial blast hit. 
		-l)
			shift
			LENGTH=$2

			##Ensures -l is a positive integer.
			if ! echo $LENGTH | egrep -q '^[0-9]*$';
			then
				echo "Length must be a positive integer value"
				exit
			fi

			##Ensures -l is not blank.
			if [ "$LENGTH" = "" ]
			then
				echo "No length value detected"
				exit
			fi

			;;

		## -c sets the identity value for pre-clustering filter.
		-c)  

			shift
			IDENTB=$2
	
			##Checks -c is a positive numeric value.
			if ! echo $IDENTB | egrep -q '^[0-9]+\.?[0-9]*$';
			then
				echo "Identity score must be between 0 and 100."
				exit
			fi

			##Checks -c is not greater than 100.
			UPCHECK=$(echo "$IDENTB > 100" | bc -l)
			
			if [ "$UPCHECK" = "1" ]
			then
				echo "Identity score out of range, keep identity score between 0 and 100."
				exit
			fi 
			;;

		## -p sets the percentage of length used in the pre-clustering filter. 
		-p)

			shift
			PERCENT=$2

			##Checks -p is a positive numeric value.
			if ! echo $PERCENT | egrep -q '^[0-9]+\.?[0-9]*$';
			then
				echo "Identity score must be between 0 and 100."
				exit
			fi

			##Checks -c is not greater than 100.
			UPCHECK=$(echo "$PERCENT > 100" | bc -l)
			
			if [ "$UPCHECK" = "1" ]
			then
				echo "Identity score out of range, keep identity score between 0 and 100."
				exit
			fi 
			;;

		## -i sets the input file name.
		-i)		
			shift
			INFILE=$2
			
			##Prevents other options from being mistaken as file name, when -i is blank.
			if echo $INFILE | grep -q '\-[flcpgiodhv]$';
			then
				echo "No input file specified."
				exit
			fi
			
			##Checks -i is not blank.
			if [ "$INFILE" = "" ]
			then
				echo "No input file specified."
				exit
			fi

			##Checks -i is a fasta file.
			if ! echo $INFILE | grep -q '.fasta';
			then
				echo "Input files must be in the .fasta format."
				exit
			fi
			##Stores file name without path to it.
			FILENAME=$(echo $INFILE | rev | cut -d '/' -f 1 | rev)
			##Stores path to input file.
			FILEPATH=$(echo $INFILE | rev | cut -d '/' -f 2- | rev)
			if [ "$FILENAME" = "$FILEPATH" ]
			then
				FILEPATH="."
			fi
			##Stores file name without .fasta.
			FILE=$(basename $FILENAME .fasta)
			##Checks input file exists.
			FILECHECK=$(ls $FILEPATH | awk -v filename="$FILENAME" '$1 == filename')
			if [ "$FILECHECK" = "" ]
			then
				echo "$INFILE not found."
				exit
			fi
			;; 

		## -o sets the name of the output directory.
		-o)
			shift
			OUTDIR=$2

			##Prevents other options from being mistaken as directory name, when -o is blank.
			if echo $OUTDIR | grep -q '\-[flcpgiodhv]$';
			then
				echo "No directory name specified."
				exit
			fi
			
			##Checks -o is not blank.
			if [ "$OUTDIR" = "" ]
			then
				echo "No directory name specified."
				exit
			fi

			;;

		##If -d is specified, the check value for deleting filedump is set to true.
		-d)
			DUMPCHECK=true
			;;

		##If -g is specified, the check value for generating plots is set to false.
		-g)
			GRAPHCHECK=false
			;;

		##If -h is specified, the contents of the help file is printed to console.
		-h)
			echo ""
			echo ""
			echo ""
			cat $DIR/Readme_VIP.txt
			echo ""
			echo ""
			echo ""
			exit
			;;

		GEM)
			echo "Cannot specify both modules at the same time."
			exit
			;;

		VIP)
			echo "Same module Specified more than once."
			exit
			;;


		--)
		shift # The double dash makes them parameters
	 
		break
		;;
	 
		*) echo "Option $2 not recognized." ;;
	 
		esac
	 
		shift
	 
	done

	##Ensures input file has been specified even when -i has not been set.
	if [ "$INFILE" = "" ]
	then
		echo "No input file specified."
		exit
	fi

	##If the user did not specify an output directory name with -d, one is generated using input file name and first identity filter.
	if [ "$OUTDIR" = "" ]
	then
		OUTDIR="${FILE}-${IDENTA}-Varia_Out"
	fi


	##Stores directory name without path to it.
	DIRNAME=$(echo $OUTDIR | rev | cut -d '/' -f 1 | rev)
	##Stores path to output directory.
	DIRPATH=$(echo $OUTDIR | rev | cut -d '/' -f 2- | rev)
	if [ "$DIRNAME" = "$DIRPATH" ]
	then
		DIRPATH=""
	fi
	##Checks output directory does not exist.

	DIRCHECK=$(ls $DIRPATH | awk -v dirname="$DIRNAME" '$1 == dirname')
	if [ "$DIRCHECK" != "" ]
	then
		echo "$OUTDIR already exists, please choose different name or move other directory."
		exit
	fi
	 
	echo "Setting up environment."
	##makes directories to sort output files
	mkdir $OUTDIR
	mkdir $OUTDIR/cluster_files
	mkdir $OUTDIR/length
	mkdir $OUTDIR/chromosomes
	mkdir $OUTDIR/links
	mkdir $OUTDIR/labels
	mkdir $OUTDIR/domains
	mkdir $OUTDIR/coverage
	mkdir $OUTDIR/filedump
	mkdir $OUTDIR/plots
	mkdir $OUTDIR/axis
	mkdir $OUTDIR/axis_label
	mkdir $OUTDIR/summaries
	mkdir $OUTDIR/Domain_Dist_plots
	mkdir $OUTDIR/Domain_Dist_configs

	echo "Parameters used:"
	echo "Database filters: identity: ${IDENTA}%, length: $LENGTH base pairs."
	echo "Self hit filters: identity: ${IDENTB}%, length: ${PERCENT}%."
	echo "Delete filedump files: ${DUMPCHECK}."
	echo "Comparing sample to database."
	##temporary copy of input file made
	cp ${FILEPATH}/$FILE.fasta $FILE.alt.fasta
	##end of file line added to temp copy
	echo '>END OF FILE' >> $FILE.alt.fasta
	##list of sample names and their starting lines added to names .txt
	grep -n '>' $FILE.alt.fasta > names.txt

	##counter set to 1, total sample names set to the number of lines in names.txt
	COUNT=1
	TOT=$(wc -l names.txt| head -n1| awk '{print $1;}')
	##this loop runs for each name in names.txt not including the end of file line
	while [ $COUNT -lt $TOT ]
	do
		PROGRESS=0
		##sample name extracted from names.txt
		NAME=$(awk -v line="$COUNT" 'NR==line {print}' names.txt| head -n1| cut -d ">" -f2)
		echo "now working on sample: ${NAME}"
		##the line where the sample begins is set
		BLINE=$(awk -v line="$COUNT" 'NR==line {print}' names.txt| head -n1| cut -d ":" -f1)
		
		##the line where the sample ends is set
		ELINE=$(awk -v line="$((COUNT +1))" 'NR==line {print}' names.txt| head -n1| cut -d ":" -f1)
		ELINE=$((ELINE -1))
		
		##the current sample is copied into a temporary fasta file
		awk -v first="$BLINE" -v last="$ELINE" 'NR>=first&&NR<=last' $FILE.alt.fasta > $NAME.fasta
		
		##sample is blast searched against the database, then the length of the sequence is added

		megablast -b 2000 -v 2000 -e 1e-10 -m 8 -F F -d $DIR/vardb/megavardb.fasta -i $NAME.fasta -o $NAME.blast
		
		##if no hits to db were found the program notifies user and moves to next sample.
		HITCHECK=true
		FIRSTHIT=$(wc -l $NAME.blast | awk '{ print $1 }' )
		if [ $FIRSTHIT -eq 0 ]
		then
			echo "no hits found for $NAME in the database, moving to next sample."
			echo $NAME >> no_hits.txt
			HITCHECK=false
		fi
		if [ $HITCHECK = true ]
		then
			PROGRESS=1
			perl $DIR/scripts/helper.putlengthfasta2Blastm8.pl $NAME.fasta $DIR/vardb/megavardb.fasta $NAME.blast
			##fasta index made for temp fasta file
			samtools faidx $NAME.fasta
		
			##genes of interest added to genes.fasta file
			n=$(awk -v identity="$IDENTA" -v hitlength="$LENGTH" '$3>=identity && $4>=hitlength' $NAME.blast.length | cut -f 2 | awk ' {n=n" "$FILE } END {print n}')
			samtools faidx $DIR/vardb/megavardb.fasta $n >> ${NAME}_genes.fasta
				
			##checks that there are hits remaining after the filter is applied.
			##if not then moves on to the next sample.
			FIRSTHIT=$(wc -l ${NAME}_genes.fasta | awk '{ print $1 }' )
			if [ $FIRSTHIT -eq 0 ]
			then
				echo "no hits found for $NAME in the database, that met the length and identity cutoff moving to next sample."
				echo $NAME >> no_hits.txt
				HITCHECK=false
			fi
		fi
		if [ $HITCHECK = true ]
		then
			PROGRESS=2
			echo "Generating cluster values."

			##genes file blast searched against itself and lengths added
			formatdb -i ${NAME}_genes.fasta -p F -o T -t ${NAME}_db.fasta
			megablast -b 2000 -v 2000 -e 1e-10 -m 8 -F F -d ${NAME}_genes.fasta -i ${NAME}_genes.fasta -o $NAME.Self.blast
			perl $DIR/scripts/helper.putlengthfasta2Blastm8.pl ${NAME}_genes.fasta ${NAME}_genes.fasta $NAME.Self.blast
			##genes to be passed to mcl added to txt file
			DECPERCENT=$(bc <<<"scale=4; $PERCENT / 100")
			awk -v identity="$IDENTB" -v hitlength="$DECPERCENT" '$3>identity && ($4>= ($13 * hitlength) || $4 >= ($14 * hitlength))' $NAME.Self.blast.length  | cut -f 1,2,4 > $NAME.formcl.txt
			##checks that there are hits remaining after the filter is applied to self blast.
			##if not then moves on to the next sample.
			FIRSTHIT=$(wc -l $NAME.formcl.txt | cut -d ' ' -f 1)
			if [ $FIRSTHIT -eq 0 ]
			then
				echo "no self hits for $NAME in the database that met the length and identity cutoff, moving to next sample."
				echo $NAME >> no_hits.txt
				HITCHECK=false
			fi
		fi
		if [ $HITCHECK = true ]
		then
			echo "Clustering with mcl."	
			## mcl forms cluster groups of the genes
			mcl $NAME.formcl.txt -q x -V all --abc -o $NAME.clusters.txt
			echo "Generating files for plot configuration."	
			##finds total number of lines in cluster file
			CTOT=$(wc -l $NAME.clusters.txt| head -n1| awk '{print $1;}')
		
			##cluster counter set to 1
			CCOUNT=1
		
			##variables storing the number of clusters and lone genes are set to 0
			CCLUSTER=0
			CSINGLE=0
			
			##loops through lines in the cluster file
			while [ $CCOUNT -le $CTOT ]
			do
				##counts the number of genes on each line, if it is 1 then 1 is added to the lone genes counter, if it is >1 then 1 is added to the cluster counter
				CHECK=$(awk -v line="$CCOUNT" 'NR==line {print}' $NAME.clusters.txt| wc -w)
				if [ $CHECK == 1 ]
				then
					CSINGLE=$((CSINGLE + 1))
				else
					CCLUSTER=$((CCLUSTER + 1))
				fi
					
				CCOUNT=$((CCOUNT +1))
			done
		
			##sends line summarising the cluster counter and lone genes counter to cluster summary file
			CRESULT="$NAME has $CCLUSTER cluster(s) and $CSINGLE lone match(es)."
			echo $CRESULT >> mcl_summary_$FILE.txt
			##runs the pythonsort script to make the chromosomes file for sample and the fasta file for blast to use to make a links file
			mv ${NAME}_genes.fasta $NAME.genes.fasta
			python $DIR/scripts/pythonsort.py $NAME
			mv $NAME.forblast.fasta ${NAME}_forblast.fasta
			formatdb -i ${NAME}_forblast.fasta -p F -o T -t ${NAME}_forblast.fasta
			##blast run to perform self comparison of fasta file generated from pythonsort
			megablast -b 2000 -v 2000 -e 1e-10 -m 8 -F F -d ${NAME}_forblast.fasta -i ${NAME}_forblast.fasta -o $NAME.link.blast
			perl $DIR/scripts/helper.putlengthfasta2Blastm8.pl ${NAME}_forblast.fasta ${NAME}_forblast.fasta $NAME.link.blast

			##runs the labelfile python script to create file containing domain names for sample
			python $DIR/scripts/add_domain.py $NAME $DIR

		
			##adds blast entries to the links file then re-orders the columns into correct format for the link file
			##awk -v identity="$IDENT" '$3>identity && $4>200 && $1!=$2' $NAME.link.blast.length | cut -f 1,7,8,2,9,10 >> 	$NAME.links.txt
			awk -v identity="$IDENT" '$3>99 && $4>200 && $1!=$2' $NAME.link.blast.length | cut -f 1,7,8,2,9,10 >> 			$NAME.links.txt
			awk '{print $1 "\t" $3 "\t" $4 "\t" $2 "\t" $5 "\t" $6}' $NAME.links.txt > $NAME.linked.txt
			## colour added to links using add_color.py
			python $DIR/scripts/add_color.py $NAME
		
			##coverage files for each cluster generated using add_coverage.py
			python $DIR/scripts/add_coverage.py $NAME
		
			##abridges coverage files for each cluster using give_median.py
			while read p; do
				for x in depth.$p.plot; do
				python $DIR/scripts/give_median.py $x 
				done
				mv depth.$p.plot $OUTDIR/filedump/$NAME.depth.$p.plot
				##adds each clusters coverage file to the main coverage file for Circos
				cat plotme.txt >> $NAME.Plot.median.coverage.plot
			done <$NAME.plotlist.txt
		
			##generates the Y axis for each clusters coverage plot
			python $DIR/scripts/add_axis.py $NAME
		
			## removes any mirrored links generated by the self blast 
			python $DIR/scripts/remove_twins.py $NAME
		
			##finds max coverage value
			MAX=$(awk '{print $4}' $NAME.axis_label_max.txt | head -n1)
			MAX=$((MAX + 1))
			##calculates how many lines should be present on coverage plot by dividing 1 by the value of MAX
			RANGE=$(bc <<<"scale=4; 1 / $MAX")
			RANGE=0${RANGE}r
		
			echo "Generating summary files."
			##cluster summary genrated
			python $DIR/scripts/get_clusters.py $NAME $DIR
			##each cluster is blast searched against its largest sequence to help find how many samples in the cluster are 80% length of the largest sequence
			while read p; do
				mv $p.db_seq.txt ${p}_db_seq.fasta
				mv $p.query_seq.txt ${p}_query_seq.fasta
				formatdb -i ${p}_db_seq.fasta -p F -o T -t ${p}_db_seq.fasta
				megablast -b 2000 -v 2000 -e 1e-10 -m 8 -A 100 -F F -d ${p}_db_seq.fasta -i ${p}_query_seq.fasta -o $p.80.blast
			##coverage file generated for the regions of similarity between genes in a single cluster.
				cut -f 1,2,7,8 $p.80.blast | sort -k 4 -n -r  > $p.cover.txt
				python $DIR/scripts/cluster_coverage.py $p
				rm $p.cover.txt
				python $DIR/scripts/give_median.py $p.plotcov.txt
				rm $p.plotcov.txt
				cat plotme.txt >> $NAME.intraclustcoverage.plot
				rm plotme.txt
			done <$NAME.listclust.txt
			INTRAMAX=$(cut -f 4 $NAME.intraclustcoverage.plot | sort -n | tail -n 1 | awk '{printf "%.0f\n", $1}')
			INTRARANGE=$(bc <<<"scale=4; 1 / $INTRAMAX")
			INTRARANGE=0${INTRARANGE}r
			while read p; do
				MSTORE=$(echo $p | awk '{print $1 "\t" $2 "\t" $3}')
				NSTORE=$(echo $p | awk '{print $1}')
				echo -e "$MSTORE\t0\tr0=1.045r,r1=1.055r" >> $NAME.axis_label_min2.txt
				echo -e "$MSTORE\t$INTRAMAX\tr0=1.125r,r1=1.145r" >> $NAME.axis_label_max2.txt
				echo -e "$NSTORE\t0\t0\t0" >> $NAME.axis_line2.txt
				echo -e "$NSTORE\t0\t0\t$INTRAMAX" >> $NAME.axis_line2.txt
			done <$NAME.axis_label_max.txt
			##final summary file generated
			python $DIR/scripts/give_final.py $NAME
			echo ">${NAME}_tag" > tag.fasta
			sed -n 2p $NAME.fasta >> tag.fasta
			TAGLEN=$(sed -n 2p tag.fasta | wc -c)
			TAGLEN=$(($TAGLEN - 1))
			megablast -b 2000 -v 2000 -e 1e-10 -m 8 -F F -d ${NAME}_forblast.fasta -i tag.fasta -o ${NAME}_taglink.blast
			cat $NAME.untwin_link.txt >> $NAME.plustag_link.txt
			
			cut -f 1,2,7,8,9,10 ${NAME}_taglink.blast >> linktemp.txt
			awk '{print $1 "\t" $3 "\t" $4 "\t" $2 "\t" $5 "\t" $6 "\tcolor=yellow_a3"}' linktemp.txt >> $NAME.plustag_link.txt
			rm tag.fasta
			rm linktemp.txt
			echo -e "chr\t-\t${NAME}_tag\t${NAME}_tag\t0\t$TAGLEN\tlyellow" >> $NAME.chromosome.txt
			##Circos plot generated
			if [ $GRAPHCHECK = true ]
				then
				echo "Generating plots."
				circos -silent -nosvg -conf $DIR/scripts/Varia.conf -param chromosome_file=$NAME.chromosome.txt -param link_file=$NAME.plustag_link.txt -param domain_file=$NAME.domains.txt -param domain_label_file=$NAME.domain_label.txt -param intracov_file=$NAME.intraclustcoverage.plot -param coverage_file=$NAME.Plot.median.coverage.plot -param axis_file=$NAME.axis_line2.txt -param axis_file2=$NAME.axis_line.txt -param axis_min=$NAME.axis_label_min.txt -param axis_min2=$NAME.axis_label_min2.txt -param axis_max=$NAME.axis_label_max.txt -param axis_max2=$NAME.axis_label_max2.txt -param max=$MAX -param range=$RANGE -param intramax=$INTRAMAX -param intrarange=$INTRARANGE -outputfile $NAME.circos.plot.png
				fi

			##Domain distribution plot scripts generated
			python $DIR/scripts/Plot_dist_bar.py $NAME.cluster_summary.txt	
			python $DIR/scripts/Plot_dist_bar.py $NAME.final_summary.txt

			##Domain distribution plots generated using scripts
			if [ $GRAPHCHECK = true ]
				then
				python Make_plot_${NAME}.cluster_summary_counts.py
				python Make_plot_${NAME}.cluster_summary_percent.py
				python Make_plot_${NAME}.final_summary_counts.py
				python Make_plot_${NAME}.final_summary_percent.py
				fi
			echo "Removing temporary files and organising files."
			##sample specific temporary files deleted
			while read p; do
				rm $p.80.blast
				rm ${p}_query_seq.fasta
				rm ${p}_db_seq.fasta
				rm ${p}_db_seq.fasta.nsq
				rm ${p}_db_seq.fasta.nsi
				rm ${p}_db_seq.fasta.nsd
				rm ${p}_db_seq.fasta.nin
				rm ${p}_db_seq.fasta.nhr
			done <$NAME.listclust.txt
			rm $NAME.listclust.txt
			rm ${NAME}_forblast.fasta.nhr
			rm ${NAME}_forblast.fasta.nin
			rm ${NAME}_forblast.fasta.nsd
			rm ${NAME}_forblast.fasta.nsi
			rm ${NAME}_forblast.fasta.nsq
			##sample specific temporary files moved to filedump directory
			mv ${NAME}_forblast.fasta $OUTDIR/filedump/$NAME.forblast.fasta
			mv $NAME.link.blast $OUTDIR/filedump/$NAME.link.blast
			mv $NAME.link.blast.length $OUTDIR/filedump/$NAME.link.blast.length
			mv $NAME.links.txt $OUTDIR/filedump/$NAME.links.txt
			mv $NAME.link.txt $OUTDIR/links/$NAME.link.txt
			mv $NAME.linked.txt $OUTDIR/filedump/$NAME.linked.txt
			mv $NAME.plotlist.txt $OUTDIR/filedump/$NAME.plotlist.txt
			
			##sample specific result files moved to appropriate directories
			mv $NAME.clusters.txt $OUTDIR/cluster_files/$NAME.clusters.txt
			mv $NAME.chromosome.txt $OUTDIR/chromosomes/$NAME.chromosome.txt
			mv $NAME.domain_label.txt $OUTDIR/labels/$NAME.domain_label.txt
			mv $NAME.domains.txt $OUTDIR/domains/$NAME.domains.txt
			mv $NAME.untwin_link.txt $OUTDIR/links/$NAME.untwin_link.txt
			mv $NAME.plustag_link.txt $OUTDIR/links/$NAME.plustag_link.txt
			mv ${NAME}_taglink.blast $OUTDIR/filedump/${NAME}_taglink.blast
			mv $NAME.axis_line.txt $OUTDIR/axis/$NAME.axis_line.txt
			mv $NAME.axis_line2.txt $OUTDIR/axis/$NAME.axis_line2.txt
			mv $NAME.axis_label_min.txt $OUTDIR/axis_label/$NAME.axis_label_min.txt
			mv $NAME.axis_label_min2.txt $OUTDIR/axis_label/$NAME.axis_label_min2.txt
			mv $NAME.axis_label_max.txt $OUTDIR/axis_label/$NAME.axis_label_max.txt
			mv $NAME.axis_label_max2.txt $OUTDIR/axis_label/$NAME.axis_label_max2.txt
			mv $NAME.Plot.median.coverage.plot $OUTDIR/coverage/$NAME.Plot.median.coverage.plot
			mv $NAME.intraclustcoverage.plot $OUTDIR/coverage/$NAME.intraclustcoverage.plot
			mv $NAME.cluster_summary.txt $OUTDIR/summaries/$NAME.cluster_summary.txt
			mv $NAME.final_summary.txt $OUTDIR/summaries/$NAME.final_summary.txt
			mv Make_plot_${NAME}.cluster_summary_counts.py $OUTDIR/Domain_Dist_configs/Make_plot_${NAME}.cluster_summary_counts.py
			mv Make_plot_${NAME}.cluster_summary_percent.py $OUTDIR/Domain_Dist_configs/Make_plot_${NAME}.cluster_summary_percent.py
			mv Make_plot_${NAME}.final_summary_counts.py $OUTDIR/Domain_Dist_configs/Make_plot_${NAME}.final_summary_counts.py
			mv Make_plot_${NAME}.final_summary_percent.py $OUTDIR/Domain_Dist_configs/Make_plot_${NAME}.final_summary_percent.py
			if [ $GRAPHCHECK = true ]
				then		
				mv $NAME.circos.plot.png $OUTDIR/plots/$NAME.circos.plot.png
				mv $NAME.cluster_summary_counts.png $OUTDIR/Domain_Dist_plots/$NAME.cluster_summary_counts.png
				mv $NAME.cluster_summary_percent.png $OUTDIR/Domain_Dist_plots/$NAME.cluster_summary_percent.png
				mv $NAME.final_summary_counts.png $OUTDIR/Domain_Dist_plots/$NAME.final_summary_counts.png
				mv $NAME.final_summary_percent.png $OUTDIR/Domain_Dist_plots/$NAME.final_summary_percent.png
				fi
		fi
		mv $NAME.fasta $OUTDIR/filedump/$NAME.fasta
		mv $NAME.blast $OUTDIR/filedump/$NAME.blast
		if [ $PROGRESS -gt 0 ]
			then
			mv $NAME.fasta.fai $OUTDIR/filedump/$NAME.fasta.fai
			mv $NAME.blast.length $OUTDIR/filedump/$NAME.blast.length
			fi
		if [ $PROGRESS -gt 1 ]
			then
			rm ${NAME}_genes.fasta.nhr
			rm ${NAME}_genes.fasta.nin
			rm ${NAME}_genes.fasta.nsd
			rm ${NAME}_genes.fasta.nsi
			rm ${NAME}_genes.fasta.nsq
			mv $NAME.formcl.txt $OUTDIR/filedump/$NAME.formcl.txt
			mv $NAME.Self.blast $OUTDIR/filedump/$NAME.Self.blast
			mv $NAME.Self.blast.length $OUTDIR/length/$NAME.Self.blast.length
			fi
		GENECHECK=$(ls -F | grep "${NAME}_genes.fasta")
				if [ "$GENECHECK" != "" ]
				then
					rm ${NAME}_genes.fasta
				fi

		GENECHECK=$(ls -F | grep "$NAME.genes.fasta")
				if [ "$GENECHECK" != "" ]
				then
					mv $NAME.genes.fasta $OUTDIR/filedump/$NAME.genes.fasta

				fi

				
		COUNT=$((COUNT +1))
	done

	##remaining temporary files removed
	mv names.txt $OUTDIR/filedump/names.txt
	rm $FILE.alt.fasta

	REMCHECK=$(ls -F | grep formatdb.log)
	if [ "$REMCHECK" != "" ]
		then
		rm formatdb.log
		fi

	##summary file moved into the Varia1_Out directory
	REMCHECK=$(ls -F | grep mcl_summary_$FILE.txt)
	if [ "$REMCHECK" != "" ]
		then
		mv mcl_summary_$FILE.txt $OUTDIR/summaries/mcl_summary_$FILE.txt
		fi
	REMCHECK=$(ls -F | grep no_hits.txt)
	if [ "$REMCHECK" != "" ]
		then
		mv no_hits.txt $OUTDIR/summaries/no_hits.txt
		fi

	if [ "$DUMPCHECK" = "true" ]
		then
		rm $OUTDIR/filedump/*
		rmdir $OUTDIR/filedump
		fi

	echo ""
	echo "Done!"
	echo ""
	echo "Circos plots are located in:"
	echo "$OUTDIR/plots/$NAME.circos.plot.png"
	echo ""
	echo "Summary files are located in:"
	echo "$OUTDIR/summaries/$NAME.cluster_summary.txt"
	echo "$OUTDIR/summaries/$NAME.final_summary.txt"

elif [ "$1" = "GEM" ]
	then
	echo "Activating GEM module."
	Blast_DB="$DIR/vardb/megavardb.fasta"	# blast database path
	Domain_database="$DIR/domains/vardb_GEM_domains.txt" 	# Domain database path
	NGS="No" # If NGS type input or single DBLa-Tag sequences, Yes/No input
	IDENT=95	# Blast identity cutoff, number between 0-100 
	THRESHOLD=66	# Threshold for when a domain is correctly determined, number between 0-100
	Cutoff=0	# Minimum cluster size cutoff, if NGS type data, positive integer
	LIMIT=0 	# Set Limit for the total number of reads needed in a run, typical around 100 reads, 0 if non-NGS data!
	INDIR=""
	OUTDIR=""


	while [ -n "$2" ]; do # while loop starts
	 
		case "$2" in

		-i)
			shift
			echo "planned location for input directory"
			INDIR=$2

			##Prevents other options from being mistaken as directory name, when -o is blank.
			if echo $INDIR | grep -q '\-[ionftclh]$';
			then
				echo "No directory name specified."
				exit
			fi
			
			##Checks -o is not blank.
			if [ "$INDIR" = "" ]
			then
				echo "No directory name specified."
				exit
			fi
			CHECK=$(ls $INDIR)
			echo $CHECK
			if [ "$CHECK" = "" ]
			then
				echo "Input directory not found or Input directory is empty"
				exit
			fi
			;;

		-o)
			echo "planned location for output directory"
			shift
			OUTDIR=$2

			##Prevents other options from being mistaken as directory name, when -o is blank.
			if echo $OUTDIR | grep -q '\-[ionftclh]$';
			then
				echo "No directory name specified."
				exit
			fi
			
			##Checks -o is not blank.
			if [ "$OUTDIR" = "" ]
			then
				echo "No directory name specified."
				exit
			fi

			if [ ! -d "$OUTDIR" ]
			then
				echo "output directory not found"
				exit
			fi
			;;

		-n)
			shift
			NGSCHECK=$2

			if [ "$NGSCHECK" = "Yes" ] || [ "$NGSCHECK" = "yes" ] || [ "$NGSCHECK" = "y" ] || [ "$NGSCHECK" = "Y" ]
			then
				NGS="Yes"
			elif [ "$NGSCHECK" = "No" ] || [ "$NGSCHECK" = "no" ] || [ "$NGSCHECK" = "n" ] || [ "$NGSCHECK" = "N" ]
			then
				NGS="No"
			else
				echo "option provided for -n must be Yes or No"
				exit
			fi
			;;

		-f) 
			shift
			IDENT=$2
	 

			##Checks -f is a numeric value. 
			if ! echo $IDENT | egrep -q '^[0-9]+\.?[0-9]*$';
			then
				echo "Identity score must be between 0 and 100"
				exit
			fi
			##Checks -f is not greater than 100. (Can't be below zero as this would require non-numeric characters, which check above prevents).
			UPCHECK=$(echo "$IDENT > 100" | bc -l)
			
			if [ "$UPCHECK" = "1" ]
			then
				echo "Identity score out of range, keep identity score between 0 and 100"
				exit
			fi 
			;;

		-t) 
			shift
			THRESHOLD=$2
	 

			##Checks -t is a numeric value. 
			if ! echo $THRESHOLD | egrep -q '^[0-9]+\.?[0-9]*$';
			then
				echo "Threshold score must be between 0 and 100"
				exit
			fi
			##Checks -t is not greater than 100. (Can't be below zero as this would require non-numeric characters, which check above prevents).
			UPCHECK=$(echo "$THRESHOLD > 100" | bc -l)
			
			if [ "$UPCHECK" = "1" ]
			then
				echo "Threshold score out of range, keep identity score between 0 and 100"
				exit
			fi
			;;

		-c) 
			shift
			Cutoff=$2
	 

			##Checks -c is a positive integer. 
			if ! echo $Cutoff | egrep -q '^[0-9]*$';
			then
				echo "Cutoff score must be a positive integer."
				exit
			fi

			if [ "$Cutoff" = "" ]
			then
				echo "no value entered for -c"
				exit
			fi
			;;

		-l) 
			shift
			LIMIT=$2
	 

			##Checks -l is a positive integer. 
			if ! echo $LIMIT | egrep -q '^[0-9]*$';
			then
				echo "Read limit must be a positive integer."
				exit
			fi

			if [ "$LIMIT" = "" ]
			then
				echo "no value entered for -l"
				exit
			fi
			;;	

		-h)
			echo ""
			echo ""
			echo ""
			cat $DIR/Readme_GEM.txt
			echo ""
			echo ""
			echo ""
			exit
			;;

		VIP)
			echo "Cannot specify both modules at the same time."
			exit
			;;
		
		GEM)
			echo "Same module Specified more than once."
			exit
			;;


		--)
		shift # The double dash makes them parameters
	 
		break
		;;
	 
		*) echo "Option $2 not recognized." ;;
	 
		esac
	 
		shift
	done

	python $DIR/VARIA_GEM.py $Blast_DB $Domain_database $NGS $IDENT $THRESHOLD $Cutoff $LIMIT

##If -v is specified, the current version of Varia is printed.
elif [ "$1" = "-v" ]
	then
	echo ""
	echo ""
	echo ""
	echo "Varia version 1_6."
	echo ""
	echo ""
	echo ""
##If -h is specified, help for general Varia usage is displayed.
elif [ "$1" = "-h" ]
	then
	echo ""
	echo ""
	echo "Varia contains two modules:"
	echo ""
	echo "Run Varia_VIP with command line:"
	echo "Varia.sh VIP [options]"
	echo "for a list of Varia VIP options use:"
	echo "Varia.sh VIP -h"
	echo ""
	echo "Run Varia_GEM with command line:"
	echo "Varia.sh GEM [options]"
	echo "for a list of Varia GEM options use:"
	echo "Varia.sh GEM -h"
	echo ""
	echo ""
else
	echo -e "No module specified, use:\nVaria.sh -h\nfor help."
	exit
fi
