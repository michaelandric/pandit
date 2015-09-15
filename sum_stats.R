# plot node roles 
library(dplyr)
library(ggplot2)
pnd_dir <- paste('~/Documents/workspace/pandit/')
setwd(pnd_dir)
print(getwd())
group_names <- c('pandit', 'ctrl')
# thresh_dens <- c('0.1')
densities <- seq(0.1, 0.5, by=.1)

for (thresh_dens in densities)
{
    for (g in group_names)
    {
        f_name <- paste(g, 'dens', thresh_dens, sep='_')
        assign(paste(f_name), as.matrix(read.table(paste('modularity/', g, '.dens_', thresh_dens, '.Qval', sep=''))))
        rand_name <- paste('rand', g, 'dens', thresh_dens, sep='_')
        assign(paste(rand_name), as.matrix(read.table(paste('random/rand_', g, '.dens_', thresh_dens, '.Qval', sep=''))))

    print(ks.test(get(f_name), get(rand_name)))
    print(summary(get(f_name)))
    print(summary(get(rand_name)))
    }
}

print(ks.test(pandit_dens_0.1, ctrl_dens_0.1))
print(summary(pandit_dens_0.1))
print(summary(ctrl_dens_0.1))
