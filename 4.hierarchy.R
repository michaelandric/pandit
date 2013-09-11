## get the tree levels
library(bct)
Args <- Sys.getenv("R_ARGS")
g <- noquote(strsplit(Args," ")[[1]][1])
nlevels <- as.numeric(noquote(strsplit(Args," ")[[1]][2]))

tree <- paste(g,"_lhrh_formatted.txt.bin.corr.thresh",thresh,".tree", sep = "")
for (lvl in 0:nlevels)
{
    communities = blondel_hierarchy(tree, lvl)
}

