setwd('~/Documents/workspace/pandit/similarity_measures/')
library(dplyr)
library(ggplot2)

pdf("plotting_similarity_NMI.pdf", paper="USr", width=8.5)
for (p in seq(.1, .5, .1))
{
    # Normalized Mutual Information
    pandit_nmi <- read.table(paste('withinpandit_dens_',p,'_NMI.txt', sep=''))$V1
    ctrl_nmi <- read.table(paste('withinctrl_dens_',p,'_NMI.txt', sep=''))$V1
    b_nmi <- read.table(paste('betweenpandit_ctrl_dens_',p,'_NMI.txt', sep=''))$V1
    
    repnames <- c(rep("pandit", length(pandit_nmi)), rep("ctrl", length(ctrl_nmi)), rep("btwn", length(b_nmi)))
    nm_df <- tbl_df(data.frame(c(pandit_nmi, ctrl_nmi, b_nmi), repnames))
    names(nm_df) <- c("NMI", "Group")
    print(summary(b_nmi))
    print(qplot(NMI, data = nm_df, geom="density", fill=Group, alpha=I(.66), xlim=c(0,1), main=paste("Density ",p*100,"%", sep=""), xlab="Normalized Mutual Information") + theme(panel.background = element_rect(fill="white")) + theme_bw())
}
dev.off()



# experimental
qplot(NMI, data = nm_df, geom="density", fill=Group, alpha=I(.66), xlim=c(0,1), main=paste("Density ",p*100,"%", sep=""), xlab="Normalized Mutual Information") + theme(panel.background = element_rect(fill="white")) + theme_bw()