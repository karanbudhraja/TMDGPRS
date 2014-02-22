# constants

PLOT_PCH_DIAMETERS <- 0
PLOT_PCH_ITERATIONS <- 20

PLOT_COL_DIAMETER <- "black"
PLOT_COL_ITERATIONS <- "blue"
  
PLOT_TYPE <- "o"
PLOT_X_LAB <- "Number of Nodes"
PLOT_Y_LAB <- "Data Value"

# import data
randomGraphData <- read.table("Alorithm4_Haeupler_Time_Random_Graph_Diameter.txt", header=TRUE, sep=",")

# plot data
plot(randomGraphData$'nodes', log2(randomGraphData$'diameters'), pch=PLOT_PCH_DIAMETERS, col=PLOT_COL_DIAMETER, type=PLOT_TYPE, xlab=PLOT_X_LAB, ylab=PLOT_Y_LAB, ylim=c(0,5))

legend( # legend position
        'topleft',
        # no boundary
        bty='n',
#        text.width = 100,
        # legend text
        c("Diameter","lg (Iterations)"),        
        # gives the legend appropriate symbols (lines)
        lty=c(1,1),                                                         
        pch = c(PLOT_PCH_DIAMETERS,PLOT_PCH_ITERATIONS),
        # gives the legend lines the correct color and width
        lwd=c(2.5,2.5),col=c(PLOT_COL_DIAMETER,PLOT_COL_ITERATIONS)) 

#par(new=TRUE)
lines(randomGraphData$'nodes', randomGraphData$'iterations', pch=PLOT_PCH_ITERATIONS, col=PLOT_COL_ITERATIONS, type=PLOT_TYPE, xlab="", ylab="")
#par(new=TRUE)
