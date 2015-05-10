## assess normalized mutual information between two partitions
library(infotheo)
Args <- Sys.getenv("R_ARGS")
begin <- as.numeric(noquote(strsplit(Args," ")[[1]][1]))
finish <- as.numeric(noquote(strsplit(Args," ")[[1]][2]))

# This function derives the normalized mutual information
mi <- function(a, b)
{
    2*(mutinformation(a, b)) / (entropy(a) + entropy(b))
}

setwd("/mnt/tier2/urihas/Andric/pandit/permtrees/")

NMIvals <- c()   # 'NMI' is 'normalized mutual information', duh.
shortrows <- c()   # This will hold the number of entries used in each permutation. Sometimes 67 instead of 68

for (i in begin:finish)
{
    print(i)
    fileA <- as.matrix(read.table(list.files(pattern = paste("^",i,".grpA", sep = ""))[2]))[,2]
    fileB <- as.matrix(read.table(list.files(pattern = paste("^",i,".grpB", sep = ""))[2]))[,2]
    rows.to.use <- min(length(fileA), length(fileB))   # this accomodates for some having only 67 instead of 68 rows. Not entirely sure why that's the case either.
    NMIvals <- c(NMIvals, round(mi(fileA[1:rows.to.use], fileB[1:rows.to.use]), 4))
    shortrows <- c(shortrows, rows.to.use)
}

write.table(NMIvals, paste("batch.",begin,".nrmlmutI.out", sep = ""), row.names = F, col.names = F, quote = F)
write.table(shortrows, paste("batch.",begin,".used.out", sep = ""), row.names = F, col.names = F, quote = F)

