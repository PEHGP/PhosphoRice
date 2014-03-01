#PhosphoRice
[PhosphoRice](http://www.plantmethods.com/content/8/1/5),a meta-predictor of rice-specific phosphorylation site, was constructed by integrating the newly phosphorylation sites predictors, NetPhos2.0, NetPhosK, Kinasephos, Scansite, Disphos and Predphosphos with parameters selected by restricted grid search and random search. It archieve an increase in MCC of 7.1%, and an increase in ACC of 4.6% than that of the best element predictor (Disphos_default), respectively.
 
***Attention:Because Scansite and Predphosphos have not been used for a long time. We have to choice another weight for our tool.***
##Get Started
###Requires
- [python](http://www.python.org/downloads/)>=2.6(not support python3.0)
- python module:[poster](https://pypi.python.org/pypi/poster/0.4)

###Install
```
git clone git@github.com:PEHGP/PhosphoRice.git
```
if you don't install git.You can download PhosphoRice [here](https://github.com/PEHGP/PhosphoRice/archive/master.zip).
###How to use   
```
python PhosphoRice.py <InputFile> <OutputFile>
```
###Input File
The input file must be a protein sequence and format in FASTA.  
A FASTA sequence seems like below:  
```
>kuan  
MGSGPRGALSLLLLLLAPPSRPAAGCPAPCSCAGTLVDCGRRGLTWASLPTAFPVDTTELVLT
GNNLTALPPGLLDALPALRTAHLGANPWRCDCRLVPLRAWLAGRPERAPYRDLRCVAPPALRG
RLLPYLAEDELRAACTDES 
```
***Attention:Disphos can't update files now. So our programs only predict a sequence at a time.***
###Output File
 The firs line is sequence name.The result from the second line.  
 The output file seems like below:
```
kuan
10	6	S  
23	12	T
45	7	Y
```
- The first column is the amino acid position.
- The second column is the score.The higher the score is, the more possible the position is a phosphorylation site.
- The third column is the phosphorylation amino acid.

***Attention:Our programs rely on the third party web tools.If the third party web tools can't be used,our programs can not predict results.***
##How to cite
 Que S, Li K, Chen M, et al. PhosphoRice: a meta-predictor of rice-specific phosphorylation sites[J]. Plant methods, 2012, 8(1): 1-9.
