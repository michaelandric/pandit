## This is to threshold the matrix, then convert format to use with blondel modularity detection
library(bct)
Args <- Sys.getenv("R_ARGS")
g <- noquote(strsplit(Args," ")[[1]][1])
h <- noquote(strsplit(Args," ")[[1]][2])

setwd("/mnt/tier2/urihas/Andric/pandit")

corrmat <- paste(g,"_",h,"_formatted.txt.bin.corr", sep = "")
threshmat <- paste(g,"_",h,"_formatted.txt.bin.corr.thresh", sep = "")
blondelmat <- paste(g,"_",h,"_formatted.txt.bin.corr.srcdst", sep = "")
print(paste("Thresholding matrix for",g,h))
fthreshold_absolute(corrmat,threshmat, .5, 0)
print(paste("Converting to blondel format"))
blondel_convert(threshmat, blondelmat)
