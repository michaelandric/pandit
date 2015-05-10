## Get the modularity measure
library(bct)
Args <- Sys.getenv("R_ARGS")
print(noquote(strsplit(Args," ")[[1]]))
print(length(noquote(strsplit(Args," ")[[1]])))
g <- noquote(strsplit(Args," ")[[1]][1])
thresh <- as.numeric(noquote(strsplit(Args," ")[[1]][2]))

srcdst <- paste(g,"_lhrh_formatted.txt.bin.corr.thresh",thresh,".srcdst", sep = "")
tree <- paste(g,"_lhrh_formatted.txt.bin.corr.thresh",thresh,".tree", sep = "")

modularity_score = blondel_community(srcdst, tree)
print(modularity_score)

write.table(modularity_score, paste("mod_score.",g,"_lhrh_thresh",thresh,".txt", sep = ""), row.names = F, col.names = F, quote = F)

