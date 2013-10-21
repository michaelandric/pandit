#Now threshold convert and run modularity algorithm
library(bct)
Args <- Sys.getenv("R_ARGS")
begin <- as.numeric(noquote(strsplit(Args," ")[[1]][1]))
finish <- as.numeric(noquote(strsplit(Args," ")[[1]][2]))
thresh <- .5

setwd("/mnt/tier2/urihas/Andric/pandit/perm/")
for (i in begin:finish)
{
    grpAname <- paste(i,".grpA", sep = "")
    grpBname <- paste(i,".grpB", sep = "")
    fthreshold_absolute(paste(grpAname,".bin.corr", sep = ""), paste(grpAname,".bin.corr.thresh",thresh, sep = ""), thresh, 0)
    blondel_convert(paste(grpAname,".bin.corr.thresh",thresh, sep = ""), paste(grpAname,".bin.corr.thresh",thresh,".srcdst", sep = ""))
    fthreshold_absolute(paste(grpBname,".bin.corr", sep = ""), paste(grpBname,".bin.corr.thresh",thresh, sep = ""), thresh, 0)
    blondel_convert(paste(grpBname,".bin.corr.thresh",thresh, sep = ""), paste(grpBname,".bin.corr.thresh",thresh,".srcdst", sep = ""))
}
