## run the modularity
## RInvoke_blondel_perm executes this R script and eventually deletes it (clean up). To get the hierarchy level, there is code within this to readlines from the Rout. 
library(bct)
Args <- Sys.getenv("R_ARGS")
print(Args)
g <- noquote(strsplit(Args," ")[[1]][1])
i <- as.numeric(noquote(strsplit(Args," ")[[1]][2]))
nlevels <- as.numeric(noquote(strsplit(Args," ")[[1]][3]))
thresh <- .5

setwd("/mnt/tier2/urihas/Andric/pandit/permtrees/")

grpname <- paste(i,".grp",g, sep = "")
blondel_hierarchy(paste(grpname,".bin.corr.thresh",thresh,".tree", sep = ""), nlevels)

