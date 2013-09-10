## Get data and run fcorr
library(bct)
Args <- Sys.getenv("R_ARGS")
g <- noquote(strsplit(Args," ")[[1]][1])
h <- noquote(strsplit(Args," ")[[1]][2])

setwd("/mnt/tier2/urihas/Andric/pandit")
dat <- read.table(paste(h,".aparc.thickness.",g,".table", sep = ""), header = TRUE)
tmp_name <- paste(g,h,".txt", sep = "")
write.table(t(dat), tmp_name, row.names = F, col.names = F, quote = F)
fcorr(tmp_name, dim(t(dat))[1], dim(t(dat))[2])
