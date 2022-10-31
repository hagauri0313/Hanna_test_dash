###install modules before running this script.
from Bio import SeqIO
import matplotlib.pyplot as plt
import requests

#user input
###Ask user to enter the name of fasta sequence in a local drive
fastaseq=input("Enter the name of fasta file in a local drive for sequence analysis.\n")


#report the number of sequences contained in fasta file
##by counting the number of headers containing >
def seq_numb() :
    with open(fastaseq, "r") as f:
        num = len([1 for line in f if line.startswith(">")])
        print("The number of sequences contained in the file is \n" + str(num))

seq_numb()

#parse fasta file to access header
#print headers and ask user input to select sequence
def get_head():
    headers = []
    with open(fastaseq, "r") as f:
        for record in SeqIO.parse(f, "fasta"):
            headers.append(record.description)
        print("List of sequences contained in the file \n" , headers)

get_head()

#ask for user input
##user can select the name of the sequence for analysis
###get fasta sequence of the user selected sequence
seqinput=input('\nSelect a sequence header for further analysis. \nPlease type the full header as listed above\n\n')

def get_seq():
    record_dict = SeqIO.to_dict(SeqIO.parse(fastaseq, "fasta"))
    for key in record_dict.items():
        if key[0] == seqinput:
            return str(key[1].seq)
    print('the length of ', key[0], " is ", len(key[1].seq))


#save selected sequence
selected_seq=get_seq()

#get a length of selected sequence
##ask user input for saving a file in a local drive
def get_len():
    print('the length of sequence selected is : ', len(selected_seq))
    ###ask user input
    saving=input('\nDo you want to save the length of sequence in a local folder? (Yes/No)\n')
    if saving.upper() == 'YES':
        with open('Sequence_length.txt', "w") as f:
            f.write(str(len(selected_seq)))
            f.close()
            print('File saved in a local folder as \'Sequence_length.txt\'.')
    else :
        print('The sequence length is not saved')


get_len()

#produce bar plot
##ACGT content bar graph
###Ask user input for saving a file in a local drive
def get_bar() :
    ###count occurances of AGCT
    A_count = selected_seq.count('A') ; C_count = selected_seq.count('C') ; G_count = selected_seq.count('G')
    T_count = selected_seq.count('T') ; total_count = len(selected_seq)
    A_perc = A_count / total_count * 100 ; C_perc = C_count / total_count * 100
    G_perc = G_count / total_count * 100 ; T_perc = T_count / total_count * 100

    ###bar plot style
    height = [A_perc, C_perc, G_perc, T_perc]
    bars = ('A', 'C', 'G', 'T')
    plt.bar(bars, height, color=('#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'))
    ### labels
    plt.xlabel('Nucleotide')
    plt.ylabel('Percentage of occurence (%)')
    plt.title('Distribution of nucleotides in fasta sequence')

    ### ask user input
    saving = input('\nDo you want to save the plot in a local folder? (Yes/No)\n')
    if saving.upper() == 'YES':
        plt.savefig('bar_plot.png')
        plt.show()
        print('File saved in a local folder as \'bar_plot.png\'.')

    else:
        print('The bar plot is not saved')
        plt.show()

get_bar()


## Get sequence of length 10 in sequence
def get10():
    ### empty dic var for subsequence and its GC content %
    var = {}
    ### loop through subsequence length of 10bp
    for i in range(0, len(selected_seq)):
        if i + 10 <= len(selected_seq):
            ### sub = subsequence
            sub = selected_seq[i:i + 10]
            ### GC content in percentage
            GC_content = (sub.count('G') + sub.count('C')) / len(sub) * 100
            i = i + 1
            t = {sub: GC_content}
            ### dictionaries containing all possible 10bp subsequences and its GC content
            var.update(t)
            ### find maximum GC content value
            itemMaxValue = max(var.items())
    listofseq = list()
    ###print list of sequences when its value (GC content) is equal to max(GC content)
    for key, value in var.items():
        if value == itemMaxValue[1]:
            listofseq.append(key)
    print('\nSubsequence of length 10 with the highest G+C content : ', listofseq)
    print('GC content : ', itemMaxValue[1], '%')

    ###Ask user input for saving file in a local drive
    saving = input('\nDo you want to save the list of subsequence? (Yes/No)\n')
    if saving.upper() == 'YES':
        with open('Subsequence.txt', "w") as f:
            f.write(str(listofseq))
            f.close()
            print('File saved in a local folder as \'Subsequence.txt\'.')
    else:
        print('The sequence length is not saved')


get10()

### Extra features for users who want to download fasta seuqence using url for different analysis
def import_seq():
    userin=input('\nDo you wish to download different fasta sequence from NCBI website for another analysis. (Yes/No)\n')
    if userin.upper() == 'YES':
        url=input('Provide url for fasta file.\n')
        res=requests.get(url)
        if res.status_code != 200:
            raise Exception("Could not get file")
        with open('downloaded.fasta', "w") as fh:
            fh.write(res.text)
            print('File saved in a local folder as \'downloaded.fasta\'.')
    else :
        print('Analysis Compeleted. ')

import_seq()