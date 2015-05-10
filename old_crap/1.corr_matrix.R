## Get data and run fcorr
library(bct)
Args <- Sys.getenv("R_ARGS")
g <- noquote(strsplit(Args," ")[[1]][1])
h <- noquote(strsplit(Args," ")[[1]][2])

setwd("/mnt/tier2/urihas/Andric/pandit")
tmp_name <- paste(g,"_",h,"_formatted.txt", sep = "") ## data have already been hand formatted with 34 regions (rows) by 21 participants (cols)
fcorr(tmp_name, 34, 21)
