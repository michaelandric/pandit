## This is to threshold the matrix, then convert format to use with blondel modularity detection
library(bct)
Args <- Sys.getenv("R_ARGS")
g <- noquote(strsplit(Args," ")[[1]][1])
thresh <- .5

setwd("/mnt/tier2/urihas/Andric/pandit")

corrmat <- paste(g,"_lhrh_formatted.txt.bin.corr", sep = "")
threshmat <- paste(g,"_lhrh_formatted.txt.bin.corr.thresh",thresh, sep = "")
blondelmat <- paste(g,"_lhrh_formatted.txt.bin.corr.thresh",thresh,".srcdst", sep = "")
print(paste("Thresholding matrix for", g, h))
fthreshold_absolute(corrmat,threshmat, thresh, 0)
print(paste("Converting to blondel format"))
blondel_convert(threshmat, blondelmat)
