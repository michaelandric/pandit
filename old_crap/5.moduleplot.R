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

df.p <- data.frame(matrix(p[,2]+1,ncol=2))
colnames(df.p) <- c("lh", "rh")

pdf("pandit_moduleplot.pdf", width = 6)
heatmap(data.matrix(df.p), Rowv = NA, Colv = NA, scale = "none", labRow = nomi, col = thepal, margins = c(5, 10), main = "Pandit") ## gives upside-down (34 at the top and the 1's at the bottom)
dev.off()

df.c <- data.frame(matrix(c[,2]+1,ncol=2))
colnames(df.c) <- c("lh", "rh")

pdf("ctrl_moduleplot.pdf", width = 6)
heatmap(data.matrix(df.c), Rowv = NA, Colv = NA, scale = "none", labRow = nomi, col = thepal, margins = c(5, 10), main = "Ctrl")
dev.off()
