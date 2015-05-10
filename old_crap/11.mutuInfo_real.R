## assess normalized mutual information between two partitions
library(infotheo)

# This function derives the normalized mutual information
mi <- function(a, b)
{
    2*(mutinformation(a, b)) / (entropy(a) + entropy(b))
}

setwd("/mnt/tier2/urihas/Andric/pandit/")

NMIvals <- c()   # 'NMI' is 'normalized mutual information', duh.
shortrows <- c()   # This will hold the number of entries used in each permutation. Sometimes 67 instead of 68

pn <- as.matrix(read.table("pandit_lhrh_formatted.txt.bin.corr.thresh0.5.tree2"))[,2]
ct <- as.matrix(read.table("ctrl_lhrh_formatted.txt.bin.corr.thresh0.5.tree2"))[,2]

print(mi(pn, ct))

setwd("/mnt/tier2/urihas/Andric/pandit/permtrees/")
nrml <- as.matrix(read.table("batch.total.nrmlmutI.out"))  # the 1000 permutations
used <- as.matrix(read.table("batch.total.used.out"))   # this can be used to filter whether to include only those permutations that use 68 or also include less (which is only a small portion of the 1000 total)
#print(length(sort(nrml[which(used == 68)])))
#print(sort(nrml[which(used == 68)])[length(sort(nrml[which(used == 68)])) * .95])

print(sort(nrml)[950])   # all 1000 permutations

