## run the modularity
## RInvoke_blondel_perm executes this R script and eventually deletes it (clean up). To get the hierarchy, there is code within this to readlines from the Rout. 
library(bct)
Args <- Sys.getenv("R_ARGS")
print(Args)
g <- noquote(strsplit(Args," ")[[1]][1])
i <- as.numeric(noquote(strsplit(Args," ")[[1]][2]))
thresh <- .5

setwd("/mnt/tier2/urihas/Andric/pandit/perm/")

grpname <- paste(i,".grp",g, sep = "")
modularity_score = blondel_community(paste(grpname,".bin.corr.thresh",thresh,".srcdst", sep = ""), paste("/mnt/tier2/urihas/Andric/pandit/permtrees/",grpname,".bin.corr.thresh",thresh,".tree", sep = ""))
print(modularity_score)

