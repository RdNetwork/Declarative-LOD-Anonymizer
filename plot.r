library(plyr)
write_stats <- function(p_size, u_size) {
    # Load data
    data = read.csv(sprintf("exp/stats_%d_%d.csv", p_size, u_size))
    data_comp = data[data$Incompatibility == 'False',]
    data_incomp = data[data$Incompatibility == 'True',]
    data_util9 = data[data$UtilitySize == '9',]
    data_priv9 = data[data$PrivacySize == '9',]
    data_comp_util9 = data_comp[data_comp$UtilitySize == '9',]
    data_comp_priv9 = data_comp[data_comp$PrivacySize == '9',]

    ### PLOT 1 : Candidate sets over overlapping ###
    data_comp$Overlap <- as.numeric(sub("%", "", data_comp$Overlap,fixed=TRUE))/100
    data_incomp$Overlap <- as.numeric(sub("%", "", data_incomp$Overlap,fixed=TRUE))/100
    data_comp$Overlap <- cut(data_comp$Overlap, breaks = seq(0,1,0.10))
    data_incomp$Overlap <- cut(data_incomp$Overlap, breaks = seq(0,1,0.10))

    x <- quantile(data_comp$Length,0.99)
    png(sprintf('exp/cand_overlap_%d_%d.png', p_size, u_size))
        boxplot(Length~Overlap, data_comp,
            xlab="Overlapping measurement", 
            ylab="# of candidate sets",
            ylim=range(c(data_comp$Length[data_comp$Length<=x],0)),
            outline=FALSE)
        # Best fit regression lines
        # abline(lm(data_comp$Length ~ as.numeric(data_comp$Overlap)))
        # Local regression line
        # lines(lowess(as.numeric(data_comp$Overlap), data_comp$Length), col="blue")
    dev.off()

    # Load data
    data = read.csv(sprintf("exp/stats_hist_u9_%d_%d.csv", p_size, u_size))
    data_comp = data[data$Incompatibility == 'False',]
    data_incomp = data[data$Incompatibility == 'True',]
    data_util9 = data[data$UtilitySize == '9',]
    data_priv9 = data[data$PrivacySize == '9',]
    data_comp_util9 = data_comp[data_comp$UtilitySize == '9',]
    data_comp_priv9 = data_comp[data_comp$PrivacySize == '9',]
    data_comp$Overlap <- as.numeric(sub("%", "", data_comp$Overlap,fixed=TRUE))/100
    data_incomp$Overlap <- as.numeric(sub("%", "", data_incomp$Overlap,fixed=TRUE))/100
    data_comp$Overlap <- cut(data_comp$Overlap, breaks = seq(0,1,0.10))
    data_incomp$Overlap <- cut(data_incomp$Overlap, breaks = seq(0,1,0.10))

    x_u9 <- quantile(data_comp_util9$Length,0.95)
    x_p9 <- quantile(data_comp_priv9$Length,0.95)
    ### PLOT : Candidate sets over privacy size (Utility fixed at 9) ###
    png(sprintf('exp/cand_size_priv_%d_%d.png', p_size, u_size))
        boxplot(Length~PrivacySize, data_comp_util9,
            xlab="Privacy total size",
            ylab="# of candidate sets", pch=19, col="indianred"
        )
        # Best fit regression lines
        #try(abline(lm(data_comp_util9$Length ~ data_comp_util9$PrivacySize), col="red", lwd=3))
        #try(lines(smooth.spline(data_comp_util9$PrivacySize, data_comp_util9$Length), col="red", lty=5))
    dev.off()


    ### PLOT : Compatibility frequency over privacy size ###
    png(sprintf('exp/incomp_size_priv_%d_%d.png', p_size, u_size))
        table <- rbind.fill.matrix(
                    head(table(data_util9$Incompatibility, data_util9$PrivacySize),2)
                )
        table <- table[, order(as.integer(colnames(table)))]
        barplot(table,
                #xlim=range(c(data_comp_util9$PrivacySize,data_comp_priv9$UtilitySize),na.rm=TRUE),
                col=c("red","indianred"),
                #width=0.3,
                xlab="Privacy size (# of triples)",
                ylab="# of executions")
        legend("topright", legend=c("Compatible cases", "Incompatible cases"),
            fill=c("red", "indianred"),
        )
    dev.off()

    # Load data
    data = read.csv(sprintf("exp/stats_hist_p9_%d_%d.csv", p_size, u_size))
    data_comp = data[data$Incompatibility == 'False',]
    data_incomp = data[data$Incompatibility == 'True',]
    data_util9 = data[data$UtilitySize == '9',]
    data_priv9 = data[data$PrivacySize == '9',]
    data_comp_util9 = data_comp[data_comp$UtilitySize == '9',]
    data_comp_priv9 = data_comp[data_comp$PrivacySize == '9',]
    data_comp$Overlap <- as.numeric(sub("%", "", data_comp$Overlap,fixed=TRUE))/100
    data_incomp$Overlap <- as.numeric(sub("%", "", data_incomp$Overlap,fixed=TRUE))/100
    data_comp$Overlap <- cut(data_comp$Overlap, breaks = seq(0,1,0.10))
    data_incomp$Overlap <- cut(data_incomp$Overlap, breaks = seq(0,1,0.10))

    x_u9 <- quantile(data_comp_util9$Length,0.95)
    x_p9 <- quantile(data_comp_priv9$Length,0.95)
    ### PLOT : Candidate sets over utility size (privacy fixed at 9) ###
    png(sprintf('exp/cand_size_util_%d_%d.png', p_size, u_size))
        boxplot(Length~UtilitySize, data_comp_priv9,
            xlab="Utility total size",
            ylab="# of candidate sets", pch=19, col="lightgreen"
        )
        #title(main = "Number of candidate sets depending on privacy total size 
        #    (red; utility size fixed at 9) and utility total size (green; 
        #    privacy size set at 9).")
        # Best fit regression lines
        #try(abline(lm(data_comp_priv9$Length ~ data_comp_priv9$UtilitySize), col="green", lwd=3))
        #try(lines(smooth.spline(data_comp_priv9$UtilitySize, data_comp_priv9$Length), col="green", lty=5))
    dev.off()

    ### PLOT : Incompatiblity over utility size (privacy fixed at 9) ###
    png(sprintf('exp/incomp_size_util_%d_%d.png', p_size, u_size))
        table <- rbind.fill.matrix(
                    head(table(data_priv9$Incompatibility, data_priv9$UtilitySize),2)
                )
        table <- table[, order(as.integer(colnames(table)))]
        barplot(table,
                #xlim=range(c(data_comp_util9$PrivacySize,data_comp_priv9$UtilitySize),na.rm=TRUE),
                col=c("green","lightgreen"),
                #width=0.3,
                xlab="Utility size (# of triples)",
                ylab="# of executions")
        #title(main = "Compatibility rate depending on privacy total size
        #   (red; utility size fixed at 9) and utility total size 
        #   (green; privacy size set at 9).")
        legend("topright", legend=c("Compatible cases", "Incompatible cases"),
            fill=c("green", "lightgreen"),
        )
    dev.off()

}

write_stats(3, 3)

graphics.off()
