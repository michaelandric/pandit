## Code to plot the module identities
library(RColorBrewer)
thepal = colorRampPalette(brewer.pal(8,"Accent"))(8)

setwd("/mnt/tier2/urihas/Andric/pandit/")

c = as.matrix(read.table("ctrl_lhrh_formatted.txt.bin.corr.thresh0.5.tree2"))
p = as.matrix(read.table("pandit_lhrh_formatted.txt.bin.corr.thresh0.5.tree2"))

nome <- names(read.table("lh.aparc.thickness.pandit.table", header = TRUE))[2:35]
nomi <- c()
for (n in nome)
{
    nomi <- c(nomi, paste(noquote(strsplit(n,"_"))[[1]][2]))
}

pdf("pandit_moduleplot.pdf")
heatmap(matrix(p[,2]+1,ncol=2), Rowv = NA, Colv = NA, scale = "none", labRow = nomi, col = thepal) ## gives upside-down (34 at the top and the 1's at the bottom)
dev.off()

pdf("ctrl_moduleplot.pdf")
heatmap(matrix(c[,2]+1,ncol=2), Rowv = NA, Colv = NA, scale = "none", labRow = nomi, col = thepal)
dev.off()
