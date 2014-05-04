#!/usr/bin/env python
from predict import PhosphoRice
import sys,re
def ReadFasta(FastaFile):
	FastaDirectory={}
	FileLines=open(FastaFile).readlines()
	m=re.search("^>",FileLines[0])
	if not m:
		print "Input file is not a fasta file."
		sys.exit(1)
	for x in FileLines:
		x=x.rstrip()
		m=re.search("^>(.*)",x)
		if m:
			p=m.group(1)
			FastaDirectory[p]=""
			continue
		FastaDirectory[p]+=x
	return FastaDirectory
if __name__=="__main__":
	if len(sys.argv)!=3:
		print "\nPhosphoRice.py <FastaFile> <OutPutFile>\n"
		sys.exit(1)
	FastaFile=sys.argv[1]
	Results=sys.argv[2]
	FD=ReadFasta(FastaFile)
	name=FD.keys()[0]
	seq=FD[name]
	p=PhosphoRice(SeqName=name,Seq=seq)
	r1={}
	r1[name]=[]
	#r1=p.NetPhosk(0.5)#id=1,w=0
	#print "Netphosk(0.5) OK."
	r2=p.NetPhosk2()#id=2,w=1.23
	print "NetPhosk2 OK."
	r3=p.Disphos(0)#id=3,w=4.25 need change
	print "Disphos(0) OK."
	r4=p.Disphos(1,genome=6)#id=4,w=1.65 need change
	print "Disphos(1,genome=6) OK."
	r5=p.Kinsephos(90)#id=5,w=2.76
	print "Kinsephos(90) OK."
	r6=p.Kinsephos(95)#id=6,w=0.79
	print "Kinsephos(95) OK."
	r7=p.Kinsephos(100)#id=7,w=2.75
	print "Kinsephos(100) OK."
	r8=p.Kinsephos2(2)#id=8,w=0.71
	print "Kinsephos2(2) OK."
	r9=p.ScanSite("High")#id=9,w=2.57
	print "ScanSite(\"High\") OK."
	r10=p.ScanSite("Low")#id=10,w=3.90
	print "ScanSite(\"Low\") OK."
	r11=p.ScanSite("Medium")#id=11,w=1.60
	print "ScanSite(\"Medium\") OK."
	r={1:r1,2:r2,3:r3,4:r4,5:r5,6:r6,7:r7,8:r8,9:r9,10:r10,11:r11}
	#need change below
	d={}
	for i in range(1,12):
		#print r[i]
		if i!=3 and i!=4 and i!=9 and i!=10 and i!=11:
			if not name in r[i]:
				ps=list(set(r[i][name.upper()]))
			else:
				ps=list(set(r[i][name]))
			for s in ps:
				#print s
				if not s in d:
					d[s]=[0,0,0,0,0,0,0,0,0,0,0,0]
					d[s][i]=1
				else:
					d[s][i]=1
		else:
			for s in r[i]:
				if not s in d:
						d[s]=[0,0,0,0,0,0,0,0,0,0,0,0]
						d[s][i]=1
				else:
					d[s][i]=1
	#print d
	fr=open(Results,"w")
	fr.write(name+"\n")
	for s in d:
		score=d[s][1]*0+d[s][2]*1.23+d[s][3]*4.25+d[s][4]*1.65+d[s][5]*2.76+d[s][6]*0.79+d[s][7]*2.75+d[s][8]*0.71+d[s][9]*2.57+d[s][10]*3.90+d[s][11]*1.60#calculate score
		if score>=11.47:
			fr.write(s+"\t"+str(score)+"\t"+seq[int(s)-1]+"\n")
	#need change up
	fr.close()
	print "Finish."
#if scansite does not work:NetPhosk(0.5) w=1,NetPhosk2() w=1,Disphos(0) w=3,Disphos(1,genome=6) w=3,Kinsephos(90) w=1,Kinsephos(95) w=1,Kinsephos(100) w=1,Kinsephos2(2) w=1; score>=6
