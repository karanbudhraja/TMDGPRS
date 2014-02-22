# constants

PLOT_PCH_COMPLETE_GRAPH <- 0
PLOT_PCH_I_TREE <- 1
PLOT_PCH_LINEAR_GRAPH <- 2
PLOT_PCH_RANDOM_GRAPH <- 3
PLOT_PCH_STAR_GRAPH <- 18

PLOT_COL_COMPLETE_GRAPH <- "black"
PLOT_COL_I_TREE <- "blue"
PLOT_COL_LINEAR_GRAPH <- "red"
PLOT_COL_RANDOM_GRAPH <- "limegreen"
PLOT_COL_STAR_GRAPH <- "black"
  
PLOT_TYPE <- "o"
PLOT_X_LAB <- "Number of Nodes"
PLOT_Y_LAB <- "Rounds"

# import data
completeGraphData <- read.table("Alorithm4_Haeupler_Time_2_complete_graph.txt", header=TRUE, sep=",")
iTreeData <- read.table("Alorithm4_Haeupler_Time_2_i_tree.txt", header=TRUE, sep=",")
linearGraphData <- read.table("Alorithm4_Haeupler_Time_2_linear_graph.txt", header=TRUE, sep=",")
randomGraphData <- read.table("Alorithm4_Haeupler_Time_2_random_graph.txt", header=TRUE, sep=",")
starGraphData <- read.table("Alorithm4_Haeupler_Time_2_star_graph.txt", header=TRUE, sep=",")

# plot rounds
plot(completeGraphData$'nodes', completeGraphData$'rounds', pch=PLOT_PCH_COMPLETE_GRAPH, col=PLOT_COL_COMPLETE_GRAPH, type=PLOT_TYPE, xlab=PLOT_X_LAB, ylab=PLOT_Y_LAB, ylim=c(0,12))

legend( # legend position
        'topleft',
        # no boundary
        bty='n',
        #font size
        cex=0.75,
#        text.width = 100,
        # legend text
        c("Complete Graph","I Tree","Linear Graph","Random Graph","Star Graph"),        
        # gives the legend appropriate symbols (lines)
        lty=c(1,1,1,1,1),                                                         
        pch = c(PLOT_PCH_COMPLETE_GRAPH,PLOT_PCH_I_TREE,PLOT_PCH_LINEAR_GRAPH,PLOT_PCH_RANDOM_GRAPH,PLOT_PCH_STAR_GRAPH),
        # gives the legend lines the correct color and width
        lwd=c(2.5,2.5),col=c(PLOT_COL_COMPLETE_GRAPH,PLOT_COL_I_TREE,PLOT_COL_LINEAR_GRAPH,PLOT_COL_RANDOM_GRAPH,PLOT_COL_STAR_GRAPH)) 

#par(new=TRUE)
lines(iTreeData$'nodes', iTreeData$'rounds', pch=PLOT_PCH_I_TREE, col=PLOT_COL_I_TREE, type=PLOT_TYPE, xlab="", ylab="")
#par(new=TRUE)
lines(linearGraphData$'nodes', linearGraphData$'rounds', pch=PLOT_PCH_LINEAR_GRAPH, col=PLOT_COL_LINEAR_GRAPH, type=PLOT_TYPE, xlab="", ylab="")
#par(new=TRUE)
lines(randomGraphData$'nodes', randomGraphData$'rounds', pch=PLOT_PCH_RANDOM_GRAPH, col=PLOT_COL_RANDOM_GRAPH, type=PLOT_TYPE, xlab="", ylab="")
#par(new=TRUE)
lines(starGraphData$'nodes', starGraphData$'rounds', pch=PLOT_PCH_STAR_GRAPH, col=PLOT_COL_STAR_GRAPH, type=PLOT_TYPE, xlab="", ylab="")
#par(new=TRUE)
