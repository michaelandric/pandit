# below is data from split (9 v. 9 within groups) and from split between groups
setwd('~/Documents/workspace/pandit/similarity_measures')
library(dplyr)

# ks tests
for (p in seq(.1, .5, .1))
{
    # Normalized Mutual Information
    ctrl_nmi <- read.table(paste('withinctrl_dens_',p,'_NMI.txt', sep=''))$V1
    pandit_nmi <- read.table(paste('withinpandit_dens_',p,'_NMI.txt', sep=''))$V1
    b_nmi <- read.table(paste('betweenpandit_ctrl_dens_',p,'_NMI.txt', sep=''))$V1
    
    repnames <- c(rep("ctrl", length(ctrl_nmi)), rep("pandit", length(pandit_nmi)), rep("btwn", length(b_nmi)))
    nm_df <- tbl_df(data.frame(c(ctrl_nmi, pandit_nmi, b_nmi), repnames))
    names(nm_df) <- c("NMI", "Group")
    print(paste("Density is",p))
    print(paste("ctrl and pandit :"))
    print(ks.test(filter(nm_df, Group=='ctrl')$NMI, filter(nm_df, Group=='pandit')$NMI))
    print(paste("ctrl and btwn"))
    print(ks.test(filter(nm_df, Group=='ctrl')$NMI, filter(nm_df, Group=='btwn')$NMI))
    print(paste("pandit and btwn"))
    print(ks.test(filter(nm_df, Group=='pandit')$NMI, filter(nm_df, Group=='btwn')$NMI))
    print(paste("  ------------------------------------------  "))
}

# means and std dev
for (p in seq(.1, .5, .1))
{
    # Normalized Mutual Information
    ctrl_nmi <- read.table(paste('withinctrl_dens_',p,'_NMI.txt', sep=''))$V1
    pandit_nmi <- read.table(paste('withinpandit_dens_',p,'_NMI.txt', sep=''))$V1
    b_nmi <- read.table(paste('betweenpandit_ctrl_dens_',p,'_NMI.txt', sep=''))$V1
    
    repnames <- c(rep("ctrl", length(ctrl_nmi)), rep("pandit", length(pandit_nmi)), rep("btwn", length(b_nmi)))
    nm_df <- tbl_df(data.frame(c(ctrl_nmi, pandit_nmi, b_nmi), repnames))
    names(nm_df) <- c("NMI", "Group")
    print(paste("Density is",p))
    print(paste("Means: "))
    print(tapply(nm_df$NMI, nm_df$Group, mean))
    print(paste("STD: "))
    print(tapply(nm_df$NMI, nm_df$Group, sd))
    print(paste("  ------------------------------------------  "))
}