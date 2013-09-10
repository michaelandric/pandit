## Get the modularity measure
library(bct)
Args <- Sys.getenv("R_ARGS")
print(noquote(strsplit(Args," ")[[1]]))
print(length(noquote(strsplit(Args," ")[[1]])))
g <- noquote(strsplit(Args," ")[[1]][1])
h <- as.numeric(noquote(strsplit(Args," ")[[1]][2]))
thresh <- as.numeric(noquote(strsplit(Args," ")[[1]][3]))

srcdst <- paste(g",_",h,"_formatted.txt.bin.corr.srcdst", sep = "")
tree <- paste(g",_",h,"_formatted.txt.bin.corr.thresh",thresh,".tree", sep = "")

modularity_score = blondel_community(srcdst, tree)
print(modularity_score)

write.table(modularity_score, paste("mod_score.",g,"_",h,"_thresh",thresh,".txt", sep = ""), row.names = F, col.names = F, quote = F)

