# get joint counts for module to type of region
setwd('~/Documents/workspace/pandit/')
library(dplyr)
library(hexbin)
library(ggplot2)

pandit_dat <- tbl_df(read.csv('pandit_data.csv'))
regions_labels <- tbl_df(read.csv('region_names_labels_p.csv'))
groups <- c('pandit', 'ctrl')
lregions <- filter(regions_labels, label=='L')$region
vregions <- filter(regions_labels, label=='V')$region
xregions <- filter(regions_labels, label=='X')$region

for (g in groups)
{
    in_file <- paste(g, '.inclusionlist.dens_0.1.csv', sep='')
    assign(paste(g, 'incl', sep='_'),
           tbl_df(read.csv(in_file))[, c(2, 3)])
    for (t in c('l', 'v', 'x'))
    {
        filt_name <- paste(g, t, 'filt', sep='_')
        incl_name <- paste(g, 'incl', sep='_')
        assign(paste(filt_name),
               filter(get(incl_name),
                      region %in% get(paste(t,'regions', sep=''))))
        for (wo in c('within', 'outside', 'other'))
        {
            assign(paste(wo, t, g, sep='_'), c())
        }
    }
}


for (g in groups)
{
    for (t in c('l', 'v'))
    {
        filt_name <- paste(g, t, 'filt', sep='_')
        for (reg in get(paste(filt_name))$region)
        {
            assign("reg_com",
                   get(filt_name)$community[get(filt_name)$region==reg])
            set_name_within <- paste('within', t, g, sep='_')
            set_name_outside <- paste('outside', t, g, sep='_')
            assign(paste(set_name_within), 
                   c(get(set_name_within),
                     length(which(get(filt_name)$community == reg_com))))
            if (t == 'l'){
                fname <- paste(g, 'v', 'filt', sep='_')
            }
            if (t == 'v'){
                fname <- paste(g, 'l', 'filt', sep='_')
            }
            assign(paste(set_name_outside), 
                   c(get(set_name_outside),
                     length(which(get(fname)$community == reg_com))))
        }
        mod_df_name <- paste(g, t, 'mod', sep='_')
        assign(paste(mod_df_name),
               data.frame(get(filt_name)$region,
                          get(set_name_within),
                          get(set_name_outside)))
    }
}

# now set up final df
for (t in c('l', 'v'))
{
    within_dat_vec <- c()
    outside_dat_vec <- c()
    group_name_vec <- c()
    for (g in groups)
    {
        mod_df_name <- paste(g, t, 'mod', sep='_')
        assign('within_dat_vec',
               c(within_dat_vec, get(mod_df_name)$get.set_name_within.))
        assign('outside_dat_vec',
                c(outside_dat_vec, get(mod_df_name)$get.set_name_outside.))
        assign('group_name_vec',
               c(group_name_vec, c(rep(g, dim(get(mod_df_name))[1]))))
    }
    df_name <- paste(t, 'dat', sep='_')
    assign(paste(df_name),
           tbl_df(data.frame(within_dat_vec,
                             outside_dat_vec,
                             group_name_vec)))
}

colnames(l_dat) <- c('within', 'outside', 'gr')
colnames(v_dat) <- c('within', 'outside', 'gr')

# Plotting
axlim = 15
pdf(paste('Cross_combo_pandit_ctrl_separategroups.pdf'))
for (t in c('l', 'v'))
{
    dat <- paste(t, 'dat', sep='_')
    if (t == 'l'){
        axlabels <- c('Connect within Language Regions', 'Connect to Visual Regions')
        titl <- 'Language'
    }
    if (t == 'v'){
        axlabels <- c('Connect to Visual Regions', 'Connect within Language Regions')
        titl <- 'Visual'
    }
    for (g in groups)
    {
        ll = filter(get(dat), gr==g)
        aa = aggregate(ll$within, list(ll$gr, ll$outside, ll$within), length)
        if (g == groups[1]){
            sh = 16
        }
        if (g == groups[2]){
            sh = 17
        }
        gp = ggplot(aa, 
               aes(x=aa$Group.3, y=aa$Group.2, size=aa$x, shape=aa$Group.1, label=aa$x)) +
            geom_point(shape=sh) +
            expand_limits(x=c(0,axlim), y=c(0,axlim)) +
            scale_x_continuous(minor_breaks=seq(0,axlim,1), breaks=seq(0,axlim,5)) +
            scale_y_continuous(minor_breaks=seq(0,axlim,1), breaks=seq(0,axlim,5)) +
            scale_size_continuous(range=c(2,10)) +
            xlab(axlabels[1]) +
            ylab(axlabels[2]) +
            ggtitle(paste(g, titl, sep=' ')) +
            theme_bw() +
            theme(panel.grid.minor = element_line(size=.2, linetype='dashed', color='gray25'),
                  panel.grid.major= element_line(size=.5, color='gray25')) +
            geom_text(aes(x=aa$Group.3, y=aa$Group.2, label=aa$x, size=5),
                      hjust=1.75, vjust=-1.5)
        plot(gp)
    }
}
dev.off()
