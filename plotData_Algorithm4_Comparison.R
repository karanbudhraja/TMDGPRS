# constants

PLOT_PCH_RANDOM_GRAPH_ITERATIONS <- 0
PLOT_PCH_RANDOM_GRAPH_ROUNDS <- 1
PLOT_PCH_RANDOM_GRAPH_IMPROVED_ITERATIONS <- 2
PLOT_PCH_RANDOM_GRAPH_IMPROVED_ROUNDS <- 3

PLOT_COL_RANDOM_GRAPH_ITERATIONS <- "black"
PLOT_COL_RANDOM_GRAPH_ROUNDS <- "blue"
PLOT_COL_RANDOM_GRAPH_IMPROVED_ITERATIONS <- "red"
PLOT_COL_RANDOM_GRAPH_IMPROVED_ROUNDS <- "limegreen"

PLOT_TYPE <- "o"
PLOT_X_LAB <- "Number of Nodes"
PLOT_Y_LAB <- "Time Steps"

# import data
randomGraphData <- read.table("Alorithm4_Haeupler_Time_random_graph.txt", header=TRUE, sep=",")
randomGraphData_Improved <- read.table("Alorithm4_Haeupler_Time_2_random_graph.txt", header=TRUE, sep=",")

# plot iterations
plot(randomGraphData$'nodes', randomGraphData$'iterations', pch=PLOT_PCH_RANDOM_GRAPH_ITERATIONS, col=PLOT_COL_RANDOM_GRAPH_ITERATIONS, type=PLOT_TYPE, xlab=PLOT_X_LAB, ylab=PLOT_Y_LAB, , ylim=c(0,17))

legend( # legend position
        'topleft',
        # no boundary
        bty='n',
        #font size
        cex=0.75,
#        text.width = 100,
        # legend text
        c("Base Iterations","Improved Iterations"),        
        # gives the legend appropriate symbols (lines)
        lty=c(1,1),                                                         
        pch = c(PLOT_PCH_RANDOM_GRAPH_ITERATIONS,PLOT_PCH_RANDOM_GRAPH_IMPROVED_ITERATIONS),
        # gives the legend lines the correct color and width
        lwd=c(2.5,2.5),col=c(PLOT_COL_RANDOM_GRAPH_ITERATIONS,PLOT_COL_RANDOM_GRAPH_IMPROVED_ITERATIONS)) 
#par(new=TRUE)
lines(randomGraphData_Improved$'nodes', randomGraphData_Improved$'iterations', pch=PLOT_PCH_RANDOM_GRAPH_IMPROVED_ITERATIONS, col=PLOT_COL_RANDOM_GRAPH_IMPROVED_ITERATIONS, type=PLOT_TYPE, xlab="", ylab="")

# plot(randomGraphData$'nodes', randomGraphData$'rounds', pch=PLOT_PCH_RANDOM_GRAPH_ROUNDS, col=PLOT_COL_RANDOM_GRAPH_ROUNDS, type=PLOT_TYPE, xlab=PLOT_X_LAB, ylab=PLOT_Y_LAB, , ylim=c(0,17))
# legend( # legend position
        # 'topleft',
        # bty='n',
        # cex=0.75,
        # c("Base Rounds","Improved Rounds"),        
        # lty=c(1,1),                                                         
        # pch = c(PLOT_PCH_RANDOM_GRAPH_ROUNDS,PLOT_PCH_RANDOM_GRAPH_IMPROVED_ROUNDS),
        # lwd=c(2.5,2.5),col=c(PLOT_COL_RANDOM_GRAPH_ROUNDS,PLOT_COL_RANDOM_GRAPH_IMPROVED_ROUNDS)) 
# lines(randomGraphData_Improved$'nodes', randomGraphData_Improved$'rounds', pch=PLOT_PCH_RANDOM_GRAPH_IMPROVED_ROUNDS, col=PLOT_COL_RANDOM_GRAPH_IMPROVED_ROUNDS, type=PLOT_TYPE, xlab="", ylab="")
