## resample and run fcorr procedures
library(bct)
Args <- Sys.getenv("R_ARGS")
begin <- as.numeric(noquote(strsplit(Args," ")[[1]][1]))
finish <- as.numeric(noquote(strsplit(Args," ")[[1]][2]))
thresh <- .5

setwd("/mnt/tier2/urihas/Andric/pandit/perm/")
dat <- as.matrix(read.table(paste("combo_panditctrl_formatted.txt", sep = "")))
numss = dim(dat)[2]

for (i in begin:finish)
{
    a = sample(numss, numss/2)
    b = seq(numss)[which(!seq(numss) %in% a)]
    grpA = dat[,a]
    grpB = dat[,b]
    grpAname <- paste(i,".grpA", sep = "")
    grpBname <- paste(i,".grpB", sep = "")
    write.table(grpA, grpAname, row.names = F, col.names = F, quote = F)
    write.table(grpB, grpBname, row.names = F, col.names = F, quote = F)
    fcorr(grpAname, 68, 21)
    fcorr(grpBname, 68, 21)
}
    

