#!/usr/bin/python
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
	r1=p.NetPhosk(0.5)#id=1,w=1
	if not r1:
		print "NetPhosk(0.5) has no results."
		sys.exit(1)
	else:
		print "Netphosk(0.5) OK."
	r2=p.NetPhosk2()#id=2,w=1
	if not r2:
		print "NetPhosk2 has no results."
		sys.exit(1)
	else:
		print "NetPhosk2 OK."
	r3=p.Disphos(0)#id=3,w=3 need change
	if not r3:
		print "Disphos(0) has no results."
		sys.exit(1)
	else:
		print "Disphos(0) OK."
	r4=p.Disphos(1,genome=6)#id=4,w=3 need change
	if not r4:
		print "Disphos(1,genome=6) has no results"
		sys.exit(1)
	else:
		print "Disphos(1,genome=6) OK."
	r5=p.Kinsephos(90)#id=5,w=1
	if not r5:
		print "Kinsephos(90) has no results."
		sys.exit(1)
	else:
		print "Kinsephos(90) OK."
	r6=p.Kinsephos(95)#id=6,w=1
	if not r6:
		print "Kinsephos(95) has no results."
		sys.exit(1)
	else:
		print "Kinsephos(95) OK."
	r7=p.Kinsephos(100)#id=7,w=1
	if not r7:
		print "Kinsephos(100) has no results."
		sys.exit(1)
	else:
		print "Kinsephos(100) OK."
	r8=p.Kinsephos2(2)#id=8,w=1
	if not r8:
		print "Kinsephos2(2) has no results."
		sys.exit(1)
	else:
		print "Kinsephos2(2) OK."
	r={1:r1,2:r2,3:r3,4:r4,5:r5,6:r6,7:r7,8:r8}
	#need change
	da={}
	for i in range(1,9):
		if i!=3 and i!=4: 
			for p in r[i]:
				d={}
				for s in r[i][p]:
					if not s in d:
						d[s]=[0,0,0,0,0,0,0,0,0]
						d[s][i]=1
					else:
						d[s][i]=1
				da[p]=d.copy()
	#print d
	fr=open(Results,"w")
	for p in da:
		print p
		fr.write(p+"\n")
		for s in da[p]:
			score=da[p][s][1]+da[p][s][2]+da[p][s][3]*3+da[p][s][4]*3+da[p][s][5]+da[p][s][6]+da[p][s][7]+da[p][s][8]#calculate score
			if score>=6:
				fr.write(s+"\t"+str(score)+"\t"+seq[int(s)-1]+"\n")
	fr.close()
	print "Finish."
