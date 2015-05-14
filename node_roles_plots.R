# plot node roles 
library(dplyr)
library(ggplot2)
pnd_dir <- paste('~/Documents/workspace/pandit/')
setwd(paste(pnd_dir, 'node_roles/', sep=''))
print(getwd())
group_names <- c('pandit', 'ctrl')
regions_labels <- tbl_df(
    read.csv(paste(pnd_dir, 'region_names_labels_p.csv', sep='')))
pandit_incl <- tbl_df(
    read.csv(paste(pnd_dir, 'pandit.inclusionlist.dens_0.1.csv', sep='')))[,c(2,3)]
ctrl_incl <- tbl_df(
    read.csv(paste(pnd_dir, 'ctrl.inclusionlist.dens_0.1.csv', sep='')))[,c(2,3)]
l_indices <- which(regions_labels$label=='L')
v_indices <- which(regions_labels$label=='V')
part_coefs <- c()
part_coefs_l <- c()
part_coefs_v <- c()
part_coefs_lv <- c()
within_mod_z <- c()
within_mod_z_l <- c()
within_mod_z_v <- c()
within_mod_z_lv <- c()

group <- c()
for (g in group_names)
{
    pc <- paste(g, 'p', sep='_')
    assign(paste(pc),
           tbl_df(read.table(paste(g, '.dens_0.1_part_coef.txt', sep=''))))
    withinz <- paste(g, 'wz', sep='_')
    assign(paste(withinz),
           tbl_df(read.table(paste(g, '.dens_0.1_within_mod_Z.txt', sep=''))))
    assign('part_coefs', c(part_coefs, get(pc)$V1))
    assign('within_mod_z', c(within_mod_z, get(withinz)$V1))
    assign('group', c(group, rep(g, length(get(pc)$V1))))
    for (t in c('l', 'v'))
    {
        sub_pc_vec <- paste(g, 'p', t, sep='_')
        sub_wz_vec <- paste(g, 'wz', t, sep='_')
        indic <- paste(t, 'indices', sep='_')
        assign(paste(sub_pc_vec), get(pc)[get(indic), ])
        assign(paste(sub_wz_vec), get(withinz)[get(indic), ])
        pc_vec <- paste('part_coefs', t, sep='_')
        assign(paste(pc_vec), c(get(pc_vec), get(sub_pc_vec)$V1))
        wz_vec <- paste('within_mod_z', t, sep='_')
        assign(paste(wz_vec), c(get(wz_vec), get(sub_wz_vec)$V1))
    }
}

roles_df <- tbl_df(data.frame(part_coefs, within_mod_z, group))


part_coefs_lv <- c(part_coefs_l, part_coefs_v)
within_mod_z_lv <- c(within_mod_z_l, within_mod_z_v)
group_l <- c(rep('pandit', length(l_indices)), rep('ctrl', length(l_indices)))
group_v <- c(rep('pandit', length(v_indices)), rep('ctrl', length(v_indices)))
group_lv <- c(group_l, group_v)
region_type <- c(rep('Language', length(l_indices)*2), rep('Visual', length(v_indices)*2))
roles_df_lv <- tbl_df(data.frame(part_coefs_lv, within_mod_z_lv, group_lv, region_type))


pdf('node_roles_plots.pdf')
gp = ggplot(roles_df, 
       aes(x=part_coefs, y=within_mod_z, color=group)) +
    geom_point() +
    scale_x_continuous(breaks=c(.05, .62, .8)) +
    scale_y_continuous(breaks=c(-2, 2.5), minor_breaks=c(-2, 2.5)) +
    expand_limits(x=c(0, 1), y=c(-2, 3)) +
    xlab('Participation Coef') +
    ylab('Within-module degree Z') +
    ggtitle('All regions') +
    theme_bw() +
    theme(panel.grid.major= element_line(size=.5, color='gray25'),
          panel.grid.minor.y = element_line(size=.2, linetype='dashed', color='gray25')) +
    scale_shape_manual(values=c(15, 17)) +
    scale_color_manual(values=c('#6EEDCE','#ECA15F'))
plot(gp)

gp = ggplot(roles_df_lv,
       aes(x=part_coefs_lv, y=within_mod_z_lv, color=group_lv, shape=region_type)) +
    geom_point() +
    scale_x_continuous(breaks=c(.05, .62, .8)) +
    scale_y_continuous(breaks=c(-2, 2.5), minor_breaks=c(-2, 2.5)) +
    expand_limits(x=c(0, 1), y=c(-2, 3)) +
    xlab('Participation Coef') +
    ylab('Within-module degree Z') +
    ggtitle('Language & Visual regions') +
    theme_bw() +
    theme(panel.grid.major = element_line(size=.5, color='gray25'),
          panel.grid.minor.y = element_line(size=.2, linetype='dashed', color='gray25')) +
    scale_shape_manual(values=c(15, 17)) +
    scale_color_manual(values=c('#6EEDCE','#ECA15F'))
plot(gp)
dev.off()

tmp <- filter(roles_df_lv, part_coefs_lv <= .05)
print(aggregate(tmp$part_coefs_lv, list(tmp$group_lv, tmp$region_type), length))

tmp <- filter(roles_df_lv, part_coefs_lv > .05 & part_coefs_lv <= .62)
print(aggregate(tmp$part_coefs_lv, list(tmp$group_lv, tmp$region_type), length))

tmp <- filter(roles_df_lv, part_coefs_lv > .62 & part_coefs_lv <= .8)
print(aggregate(tmp$part_coefs_lv, list(tmp$group_lv, tmp$region_type), length))

tmp <- filter(roles_df_lv, part_coefs_lv > .8)
print(aggregate(tmp$part_coefs_lv, list(tmp$group_lv, tmp$region_type), length))
