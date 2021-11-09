import math
import re
import os
import sys
import glob
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio.Blast import NCBIXML
from collections import Counter
import xlsxwriter
from Bio import SeqIO
import itertools
from Bio.Seq import Seq

print(sys.argv)
Blast_DB  = sys.argv[1]		# blast database path
Domain_database = sys.argv[2]   # Domain database path
NGS = sys.argv[3] 		# If NGS type input or single DBLa-Tag sequences, Yes/No input
IDENT = float(sys.argv[4])	# Blast identity cutoff, number between 0-100 
THRESHOLD = float(sys.argv[5])	# Threshold for when a domain is correctly determined, number between 0-100
Cutoff = int(sys.argv[6])			# Minimum cluster size cutoff, if NGS type data, positive integer
LIMIT = int(sys.argv[7]) 			# Set Limit for the total number of reads needed in a run, typical around 100 reads, 0 if non-NGS data!


#### Create xlsx file, add tabs and formats ####
workbook = xlsxwriter.Workbook('Result_summary.xlsx')
worksheet_all = workbook.add_worksheet("All_Samples Summary")
cell_format2, cell_format3, cell_format4, cell_format5, cell_format6, cell_format7, cell_format8, cell_format9, cell_format10,cell_format11, cell_format12, cell_format13, cell_format14, cell_format15, cell_format16, cell_format17, cell_format18 = workbook.add_format({'bg_color': '#D3D3D3'}), workbook.add_format({'bg_color': '#32ff32'}), workbook.add_format({'bg_color': '#e50000'}), workbook.add_format({'bg_color': '#32ff32'}), workbook.add_format({'bg_color': '#207068'}), workbook.add_format({'bg_color': '#40e0d0'}), workbook.add_format({'bg_color': '#cd00cd'}), workbook.add_format({'bg_color': '#696969'}),workbook.add_format({'bg_color': '#d3d3d3'}), workbook.add_format({'bg_color': '#ffa500'}), workbook.add_format({'bg_color': '#ffff00'}), workbook.add_format({'bg_color': '#4ca64c'}), workbook.add_format({'bg_color': '#cd00cd'}), workbook.add_format({'bg_color': '#0000ff'}), workbook.add_format({'bg_color': '#e50000'}), workbook.add_format({'bg_color': '#ffff00'}), workbook.add_format({'bg_color': '#8b0046'})
cell_format_new = {"Match":cell_format2,"NTSA":cell_format3, "NTSB":cell_format4,"DBLa1":cell_format5, "DBLa2":cell_format6, "DBLa0":cell_format7, "DBLpam1":cell_format8, "CIDRa1":cell_format9, "CIDRa2":cell_format10,"CIDRa3":cell_format10,"CIDRa4":cell_format10,"CIDRa5":cell_format10,"CIDRa6":cell_format10,"CIDRa2-6":cell_format10,"DBLb":cell_format11,"DBLg":cell_format12,"DBLd":cell_format13,"DBLe":cell_format14,"DBLz":cell_format15,"CIDRb":cell_format16,"CIDRg":cell_format17,"CIDRd":cell_format18}
excel_names = ['Sample_ID',"Read_count", "Blast_Cluster_sequnece","Best Blast hit","E-value","# hits in varDB","NTSA","NTSB","DBLa0","DBLa1","DBLa2","DBLpam1","CIDRa1","CIaDRa2-6","CIDRb","CIDRg","CIDRd","DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd","DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd","DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd","DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd","DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd","DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd","DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd","DBLb-DBLb","DBLg-DBLg","CIDRa1","CIDRa2","CIDRa3","CIDRa4","CIDRa5","CIDRa6","CIDRb","CIDRg","CIDRd","DBLb","DBLg","DBLd","DBLe","DBLz","CIDRa1.1","CIDRa1.2","CIDRa1.3","CIDRa1.4","CIDRa1.5","CIDRa1.6","CIDRa1.7","CIDRa1.8","CIDRa2.10","CIDRa2.11","CIDRa2.1","CIDRa2.2","CIDRa2.3","CIDRa2.4","CIDRa2.5","CIDRa2.6","CIDRa2.7","CIDRa2.8","CIDRa2.9","CIDRa3.1","CIDRa3.2","CIDRa3.3","CIDRa3.4","CIDRa3.5","CIDRa4","CIDRa5","CIDRa6","CIDRg10","CIDRg11","CIDRg12","CIDRg1","CIDRg2","CIDRg3","CIDRg4","CIDRg5","CIDRg6","CIDRg7","CIDRg8","CIDRg9","CIDRpam","DBLa0.10","DBLa0.11","DBLa0.12","DBLa0.13","DBLa0.14","DBLa0.15","DBLa0.16","DBLa0.17","DBLa0.18","DBLa0.19","DBLa0.1","DBLa0.20","DBLa0.21","DBLa0.22","DBLa0.23","DBLa0.24","DBLa0.2","DBLa0.3","DBLa0.4","DBLa0.5","DBLa0.6","DBLa0.7","DBLa0.8","DBLa0.9","DBLa1.1","DBLa1.2","DBLa1.3","DBLa1.4","DBLa1.5","DBLa1.6","DBLa1.7","DBLa1.8","DBLa2","DBLb10","DBLb11","DBLb12","DBLb13","DBLb1","DBLb2","DBLb3","DBLb4","DBLb5","DBLb6","DBLb7","DBLb8","DBLb9","DBLd1","DBLd2","DBLd3","DBLd4","DBLd5","DBLd6","DBLd7","DBLd8","DBLd9","DBLe10","DBLe11","DBLe12","DBLe13","DBLe14","DBLe1","DBLe2","DBLe3","DBLe4","DBLe5","DBLe6","DBLe7","DBLe8","DBLe9","DBLepam4","DBLepam5","DBLg10","DBLg11","DBLg12","DBLg13","DBLg14","DBLg15","DBLg16","DBLg17","DBLg18","DBLg1","DBLg2","DBLg3","DBLg4","DBLg5","DBLg6","DBLg7","DBLg8","DBLg9","DBLpam1","DBLpam2","DBLpam3","DBLz1","DBLz2","DBLz3","DBLz4","DBLz5","DBLz6"]
excel_domains = ["Position D1","Position D1", "Position D2", "Position D2", "Position D2","Position D2", "Position D3","Position D3","Position D3","Position D3","Position D3","Position D4","Position D4","Position D4","Position D4","Position D4","Position D4","Position D4","Position D4","Position D5","Position D5","Position D5","Position D5","Position D5","Position D5","Position D5","Position D5","Position D6","Position D6","Position D6","Position D6","Position D6","Position D6","Position D6","Position D6","Domain 07","Domain 07","Domain 07","Domain 07","Domain 07","Domain 07","Domain 07","Domain 07","Domain 08","Domain 08","Domain 08","Domain 08","Domain 08","Domain 08","Domain 08","Domain 08","Domain 09","Domain 09","Domain 09","Domain 09","Domain 09","Domain 09","Domain 09","Domain 09","Domain 10","Domain 10","Domain 10","Domain 10","Domain 10","Domain 10","Domain 10","Domain 10","Double Domain","Double Domain","Main Domain","Main Domain","Main Domain","Main Domain","Main Domain","Main Domain","Main Domain","Main Domain","Main Domain","Main Domain","Main Domain","Main Domain","Main Domain","Main Domain","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype","Subtype"]
excel_color = ["#FFA500","#FFA500","#EEE8AA","#EEE8AA","#EEE8AA","#EEE8AA","#6495ED","#6495ED","#6495ED","#6495ED","#6495ED","#ADD8E6","#ADD8E6","#ADD8E6","#ADD8E6","#ADD8E6","#ADD8E6","#ADD8E6","#ADD8E6","#FFA500","#FFA500","#FFA500","#FFA500","#FFA500","#FFA500","#FFA500","#FFA500","#EEE8AA","#EEE8AA","#EEE8AA","#EEE8AA","#EEE8AA","#EEE8AA","#EEE8AA","#EEE8AA","#66CDAA","#66CDAA","#66CDAA","#66CDAA","#66CDAA","#66CDAA","#66CDAA","#66CDAA","#777ACA","#777ACA","#777ACA","#777ACA","#777ACA","#777ACA","#777ACA","#777ACA","#FF7373","#FF7373","#FF7373","#FF7373","#FF7373","#FF7373","#FF7373","#FF7373","#6897BB","#6897BB","#6897BB","#6897BB","#6897BB","#6897BB","#6897BB","#6897BB","#C0C0C0","#C0C0C0","#FFFF33","#FFFF33","#FFFF33","#FFFF33","#FFFF33","#FFFF33","#FFFF33","#FFFF33","#FFFF33","#FFFF33","#FFFF33","#FFFF33","#FFFF33","#FFFF33","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F","#CD853F"]

def Clustering():														# Cluster sequences using Usearch11.0.667 program
	for fasta in glob.glob("*.fasta"):									# Iterate through each fasta file
		if not os.path.isdir(fasta[:-6]): os.mkdir(fasta[:-6])
		a = open(str(fasta[:-6])+"temp","w");a.close()
		with open(str(fasta[:-6])+"temp","a") as seq:
			for record in SeqIO.parse(fasta, "fasta"): 					# Remove the primer sequences before Clustering
				if NGS == "yes":
					record.seq = record.seq[23:-23]
				SeqIO.write(record, seq, 'fasta')
		seq.close()
		os.system("vsearch --cluster_fast "+str(fasta)+" -id 0.95 -uc Clusters.uc --clusters ./"+str(fasta[:-6])+"/")	 # Cluster sequences with 95% identity
		os.remove(str(fasta[:-6]+"temp"))

def Readfile(filename):								
    lines_in = [record.seq for record in SeqIO.parse(filename, "fasta") if len(record.seq) > 200]
    return lines_in

def domain_converter(domain_list):
	convert_list = ["NTSA","NTSB","DBLa0","DBLa1","DBLa2","DBLpam1","CIDRa1","CIDRa2","CIDRa3","CIDRa4","CIDRa5","CIDRa6","CIDRb","CIDRg","CIDRd","DBLb","DBLg","DBLd","DBLe","DBLz","ATSA","ATSB"]
	Ordering = [[],[],[],[],[],[],[],[],[],[]]	# First 10 doamin order list
	Double_ordering =[[],[]]
	raw_list = [[],[],[],[],[],[],[],[],[],[]]	
	double_dblb = ["DBLb","DBLb"]
	double_dbld = ["DBLg","DBLb"]
	for domain in domain_list:	
		Position_list = [["NTSA","NTSB"], ["DBLa0","DBLa1","DBLa2","DBLpam1"],["CIDRa1","CIDRa2","CIDRa3","CIDRa4","CIDRa5","CIDRa6","CIDRb","CIDRg","CIDRd"],["DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd"],["DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd"],["DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd"],["DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd"],["DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd"],["DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd"],["DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd"]]
		converted = [convert for type in domain for convert in convert_list if convert in type]
		if converted:
			position_counter = 0
			#### Identifying double DBLb/d domains ####
			double_dblb_out = ', '.join(map(str, double_dblb)) in ', '.join(map(str, converted)) 
			double_dbld_out = ', '.join(map(str, double_dbld)) in ', '.join(map(str, converted)) 
			if double_dblb_out == True:Double_ordering[0].append("DBLb")
			if double_dbld_out == True:Double_ordering[0].append("DBLd")
			#### Seperate converted and raw domains into Ordering and Raw lists ####	
			for main_domain in converted: 					
				for position in Position_list[position_counter:]: 	
					found = [found_it for found_it in position if found_it in main_domain] 
					if found:
						Ordering[position_counter].append(found[0]) 		
						raw = [raw for raw in domain if main_domain in raw]
						raw_list[position_counter].append(raw[0])
						position_counter +=1
						break
					position_counter +=1
	return Ordering, raw_list, Double_ordering

def blast(lines_in,k,filename):											# Blast first seq of each Cluster	
	result, E_VALUES, fifty_result = [], [], []
	t = open("temp","w");t.close()
	t=open("temp","a");t.write(">"+"\n"+str(lines_in[0]));t.close()
	blastn_cline = NcbiblastnCommandline(query="temp",  db=Blast_DB, evalue = 1e-2, out="my_blast.xml", outfmt=5, num_threads=4, max_target_seqs = 200)
	stdout, stderr = blastn_cline()
	for record in NCBIXML.parse(open("my_blast.xml")):
		if record.alignments:
			for hit in range(0,len(record.alignments),1):
				if hit < 50:
					fifty_result.append(str(record.alignments[hit].title))
					for hsp in record.alignments[hit].hsps:E_VALUES.append(hsp.expect) 
				id = (float(record.alignments[hit].hsps[0].identities) / float(record.alignments[hit].hsps[0].align_length))*100
				if int(record.alignments[hit].hsps[0].align_length) > 200 and id > IDENT:result.append(str(record.alignments[hit].title))
	if fifty_result: # if blast not empty return results
		return result, fifty_result, E_VALUES

def write_sheet(row,worksheet,bold,file_list,worksheet_all,sum_row,path):
	start_pred = row+8
	sum_list = ["E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","AA","AB","AC","AD","AE","AF","AG","AH","AI","AJ","AK","AL","AM","AN","AO","AP","AQ","AR","AS","AT","AU","AV","AW","AX","AY","AZ","BA","BB","BC","BD","BE","BF","BG","BH","BI","BJ","BK","BL","BM","BN","BO","BP","BQ","BR","BS","BT","BU","BV","BW","BX","BY","BZ","CA","CB","CC","CD","CE","CF","CG","CH","CI","CJ","CK","CL","CM","CN","CO","CP","CQ","CR","CS","CT","CU","CV","CW","CX","CY","CZ","DA","DB","DC","DD","DE","DF","DG","DH","DI","DJ","DK","DL","DM","DN","DO","DP","DQ","DR","DS","DT","DU","DV","DW","DX","DY","DZ","EA","EB","EC","ED","EE","EF","EG","EH","EI","EJ","EK","EL","EM","EN","EO","EP","EQ","ER","ES","ET","EU","EV","EW","EX","EY","EZ","FA","FB","FC","FD","FE","FF","FG","FH","FI","FJ","FK","FL","FM","FN","FO","FP","FQ","FR","FS","FT","FU","FV","FW","FX","FY","FZ","GA","GB","GC","GD","GE","GF","GG","GH","GI","GJ","GK","GL","GM","GN","GO","GP","GQ","GR","GS","GT","GU","GV","GW","GX","GY","GZ","HA","HB","HC","HD","HE","HF","HG","HH","HI","HJ","HK","HL","HM","HN","HO","HP","HQ","HR","HS"]
	column = 0
	row += 1 
	worksheet.write(row+1,column+4, "Sample_total:",bold);worksheet.write(row+len(file_list)+6,3,"Relative Expression Level:", bold)
	sum_column = 2
	for e,let in zip(excel_names[5:],sum_list):
		worksheet.write(row,column+5,str(e),bold)
		if let != "E":
			worksheet.write_formula(row+1,column+4, "=SUM("+let+"5:"+let+str(row-1)+")" )
		formula = "=SUMIFS("+"B"+str(start_pred)+":"+"B"+str(row+len(file_list)+6)+","+let+str(start_pred)+":"+let+str(row+len(file_list)+6)+",1)/SUM("+"B"+str(start_pred)+":"+"B"+str(row+len(file_list)+6)+")"
		if sum_column < 223:
			worksheet.write_formula(row+len(file_list)+6,column+4,formula)
			worksheet_all.write_formula(sum_row, sum_column, "="+str(path[2:-1])+"!"+str(let)+str(row+len(file_list)+7))
		column +=1
		sum_column +=1
	worksheet.write_formula(row+1,column+4, "=SUM("+"HS"+"5:"+"HS"+str(row-1)+")" )
	sum_column = 2
	worksheet_all.write_formula(sum_row,sum_column-1,"=SUM("+str(path[2:-1])+"!B"+str(start_pred)+":"+"B"+str(row+len(file_list)+6)+	")")
	column = 0
	row = 4
	worksheet.write(row+len(file_list)+5,column,"Interpreded Results",bold);worksheet.write(row+len(file_list)+6,column,"Sample_ID",bold);worksheet.write(row+len(file_list)+6,column+1,"Read_count",bold);worksheet.write(row+len(file_list)*2+8,column,"Suggested Composition",bold);worksheet.write(row+len(file_list)*2+9,column,"Sample_ID",bold);worksheet.write(row+len(file_list)*2+9,column+1,"Read_count",bold);worksheet.write(row+len(file_list)*2+9,column+2,"Position D1 (91% expected accuracy)", bold);worksheet.write(row+len(file_list)*2+9,column+3,"Position D2 (99% expected accuracy)", bold);worksheet.write(row+len(file_list)*2+9,column+4,"Position D3 (96% expected accuracy)", bold);worksheet.write(row+len(file_list)*2+9,column+5,"Position D4 (95% expected accuracy)", bold);worksheet.write(row+len(file_list)*2+9,column+6,"Position D5 (83% expected accuracy)", bold);worksheet.write(row+len(file_list)*2+9,column+7,"Position D6 (78% expected accuracy)", bold);worksheet.write(row+len(file_list)*2+9,column+8,"Position D7 (77% expected accuracy)", bold);worksheet.write(row+len(file_list)*2+9,column+9,"Position D8 (69% expected accuracy)", bold);worksheet.write(row+len(file_list)*2+9,column+10,"Position D9", bold);worksheet.write(row+len(file_list)*2+9,column+11,"Position D10", bold)
	for e_names in excel_names[6:]: 		
		try:  
			cell_format = workbook.add_format()
			cell_format.set_bg_color(str(excel_color[column]))
			worksheet.write(row+len(file_list)+5,column+4,excel_domains[column],cell_format)
		except IndexError:
			pass
		worksheet.write(row+len(file_list)+6,column+4,e_names,bold)
		column +=1
	row +=1
	for Cluster in file_list:
		column = 0
		worksheet.write(row+len(file_list)+6,column,path[2:-1]+"_Cluster_"+Cluster[0])
		worksheet.write(row+len(file_list)*2+9,column,path[2:-1]+"_Cluster_"+Cluster[0])
		row +=1
	return row

def Interpreter(Ordering,raw_list,worksheet,row,file_list):
	Position_list = [["NTSA","NTSB"], ["DBLa0","DBLa1","DBLa2","DBLpam1"],["CIDRa1","CIDRa2","CIDRa3","CIDRa4","CIDRa5","CIDRa6","CIDRb","CIDRg","CIDRd"],["DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd"],["DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd"],["DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd"],["DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd"],["DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd"],["DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd"],["DBLb","DBLg","DBLd","DBLe","DBLz","CIDRb","CIDRg","CIDRd"]]		
	column, CIDRa_total, position_counter, BREAK = 0, 0, 0, 1
	for domains, raw_domains in zip(Ordering, raw_list):
		if domains:
			BREAK -=1
			domain_total = sum(Counter(domains).values())
			for position in Position_list[position_counter]:
				for domain, raw in zip(Counter(domains).most_common(100),Counter(raw_domains).most_common(100)):
					if position in domain[0]:
						output = domain[1]
						if "CIDRa2" in domain[0] or "CIDRa3" in domain[0] or "CIDRa4" in domain[0] or "CIDRa5" in domain[0] or "CIDRa6" in domain[0] and (domains.count("CIDRa2")+domains.count("CIDRa3")+domains.count("CIDRa4")+domains.count("CIDRa5")+domains.count("CIDRa6")) > 0:
							column = 7
							worksheet.write(row,column+6,int(domains.count("CIDRa2")+domains.count("CIDRa3")+domains.count("CIDRa4")+domains.count("CIDRa5")+domains.count("CIDRa6")),cell_format2)
							if float(domain[1])/(domains.count("CIDRa2")+domains.count("CIDRa3")+domains.count("CIDRa4")+domains.count("CIDRa5")+domains.count("CIDRa6")) >= float(THRESHOLD)/100:
								output = domains.count("CIDRa2")+domains.count("CIDRa3")+domains.count("CIDRa4")+domains.count("CIDRa5")+domains.count("CIDRa6")
						else:
							worksheet.write(row,column+6,int(output),cell_format2)
						if (float(output)/domain_total >= float(THRESHOLD)/100 or domain_total == 1) and BREAK == 0:
							BREAK +=1
							worksheet.write(row+len(file_list)+7,column+4,1,cell_format_new["Match"])
							if float(raw[1])/domain[1] >= float(THRESHOLD)/100: # Write subtype
								if raw[0] in excel_names[89:]:
									if domain[0] in excel_names[75:89]:worksheet.write(row+len(file_list)+7,73+excel_names[75:89].index(domain[0]),1,cell_format2)
									worksheet.write(row+len(file_list)+7,87+excel_names[89:].index(raw[0]),1,cell_format2)
								worksheet.write(row+len(file_list)*2+10,position_counter+2,str(raw[0]),cell_format_new[domain[0]])
							else:  									# Write Maintype
								if domain[0] in excel_names[75:89]:
									worksheet.write(row+len(file_list)+7,73+excel_names[75:89].index(domain[0]),1,cell_format2)
								worksheet.write(row+len(file_list)*2+10,position_counter+2,str(domain[0]),cell_format_new[domain[0]])
				if "CIDRa2" in position or "CIDRa3" in position or "CIDRa4" in position or "CIDRa5" in position: column -=1
				column +=1
		else:
			if position_counter > 0:
				BREAK -=1
			for position in Position_list[position_counter]:
				if "CIDRa2" in position or "CIDRa3" in position or "CIDRa4" in position or "CIDRa5" in position: column -=1
				column +=1
		position_counter += 1
	return column

def main():
	os.chdir('./GEM/')	
	#### Cluster all sample fasta files found ####
	Clustering()														
	print("CLUSTERING COMPLETE")
	sum_row = 4
	#### Iterate across all sample folders ####
	for path in glob.glob("./*/"):
		bold, sum_column = workbook.add_format({'bold': True}), 0
		worksheet = workbook.add_worksheet(path[2:-1]);worksheet_all.set_column(0, 0, 35);worksheet_all.write("A4","Sample_ID",bold);worksheet_all.write("B4","Read_count",bold);worksheet_all.write(sum_row,sum_column,str(path[2:-1]))
		cell_format = workbook.add_format()
		worksheet.set_column(0, 0, 35);worksheet.set_column(1, 88, 20);worksheet_all.set_column(1, 88, 20)
		os.chdir(path)
		Cluster_dict, total, singletons, row, column = {}, 0 , 0, 4, 0
		#### Determine Total and Singleton reads ####
		for filename in glob.glob("*[0-9]*"):								
			lines_in = Readfile(filename)
			if len(lines_in) > 1:total +=len(lines_in)
			else:singletons +=1												
			Cluster_dict.update({filename : len(lines_in)})
		#### Add Domain names, color to sheet ####
		worksheet.write("B1", "Total reads",bold);worksheet.write("B2",int(total+singletons));worksheet.write("C1", "Singletons",bold);worksheet.write("C2",int(singletons))
		file_list = sorted(Cluster_dict.items(), key=lambda x: x[1], reverse=True)	 	
		if total < LIMIT:continue
		for e_names in excel_names: 			
			try:
				cell_format = workbook.add_format()
				cell_format.set_bg_color(str(excel_color[column]))
				worksheet.write(row-2,column+6,excel_domains[column],cell_format)
				worksheet_all.write(row-2,column+2,excel_domains[column],cell_format)
			except IndexError:pass
			worksheet.write(row-1,column,e_names,bold)
			if column > 5:worksheet_all.write(row-1,column-4,e_names,bold)
			column +=1
		print(path[2:-1])
		#### Iterate across all Cluster files, performing blast and domain annotation ####
		for Cluster in file_list:
			column, top_hits, domain_list, lines_in = 0, [], [], Readfile(Cluster[0])
			worksheet.write(row,column,path[2:-1]+"_Cluster_"+Cluster[0]) 						
			for names in excel_names[6:]:
				worksheet.write(row,column+6,0);worksheet.write(row+len(file_list)+7,column+4, 0)
				column +=1
			if len(lines_in) > Cutoff:															
				if blast(lines_in,path,filename):
					blast_result, blast_top, e_values = blast(lines_in,path,Cluster)					
					worksheet.write(row,column-220,int(Cluster[1]));worksheet.write(row,column-219,str(lines_in[0]));worksheet.write(row,column-216,int(len(blast_result)));worksheet.write(row+len(file_list)+7,column-221,path[2:-1]+"_Cluster_"+Cluster[0]);worksheet.write(row+len(file_list)+7,column-220,int(Cluster[1]));worksheet.write(row+len(file_list)*2+10,column-220,int(Cluster[1]))					
					for blast_hit in blast_result:
						with open(Domain_database,'r') as file:domains = [(line.split( ))[1][:-1].split("-") for line in file for domain in line.split( ) if domain in blast_hit]
						if domains:
							for doms in domains:
								if doms[0] != "":
									domain_list.append(doms)
									break
					for top_hit in blast_top:
						with open(Domain_database,'r') as file:top_domains = [(line.split( ))[1][:-1].split("-") for line in file for domain in line.split( ) if domain in top_hit]
						if len(top_domains) == 0: continue  
						if filter(lambda x: 'DBLa' in x, top_domains[0]): top_hits.append(filter(lambda x: 'DBLa' in x, top_domains[0]))
					dbla_list = [item for sublist in top_hits for item in sublist]
					if len(dbla_list) != 0: top_dbla = max(set(dbla_list), key = dbla_list.count)
					else: dbla_list = ["None"]; top_dbla = "None"
					worksheet.write(row,column-218,str(top_dbla));worksheet.write(row,column-217,e_values[dbla_list.index(top_dbla)])							
				#### Convert domains to appropriate Main-types and Subtypes, seperatoing into position list####
				Ordering, raw_list, Double_ordering = domain_converter(domain_list)[0], domain_converter(domain_list)[1], domain_converter(domain_list)[2]
				#### Write double DBLb/d to sheet ####
				for dbl in Double_ordering:
					if dbl.count("DBLb") > 0: worksheet.write(row,column-148,int(dbl.count("DBLb")),cell_format_new["Match"])
					if dbl.count("DBLd") > 0: worksheet.write(row,column-147,int(dbl.count("DBLd")),cell_format_new["Match"])
				#### Write Main domains and subdomains to sheet ####
				main_domains = [dom for domain in Ordering for dom in domain ]
				sub_domains = [subtype for types in raw_list for subtype in types]
				for name in excel_names[75:89]:
					if main_domains.count(name) > 0:worksheet.write(row,column-146, int(main_domains.count(name)),cell_format_new["Match"]); 
					column +=1
				for name in excel_names[89:]:
					if sub_domains.count(name) > 0:worksheet.write(row,column-146, int(sub_domains.count(name)),cell_format_new["Match"]); 
					column +=1
				#### Write Domain postion D1-D10, interpretations and suggested compositions ####
				Interpreter(Ordering,raw_list,worksheet,row,file_list)
			row += 1
		#### Write sum of columns, interpredet columns, interpreded colors and names ####
		row = write_sheet(row,worksheet,bold,file_list,worksheet_all,sum_row,path)
		sum_row +=1
		os.chdir("..")
	workbook.close()
	print("The resulting Excel file has been created in the GEM folder")

if __name__ == "__main__":
	try:
		main()
	except Exception:
		print(" Error: Please remember to create GEM folder and place all fasta files within")











