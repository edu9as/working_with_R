library(shiny)
library(shinyWidgets)
library(tidyverse)

data <- read.csv("nba2k20.csv")
ui <- fluidPage(
  titlePanel("Hello Shiny!"),
  sidebarLayout(
    sidebarPanel(sliderTextInput(inputId = "feature", 
                             label = "Feature:",
                             choices = colnames(data)[unlist(lapply(data, is.numeric))]), 
                 sliderInput(inputId = "bins", 
                             label = "Number of bins:",
                             min=1,
                             max=50,
                             value=30)),
    mainPanel(plotOutput(outputId = "distPlot"))
  )
)

server <- function(input, output) {
  output$distPlot <- renderPlot({
    x <-  data[[input$feature]]
    bins <-  seq(min(x), max(x), length.out = input$bins + 1)
    hist(x, breaks = bins, col="#75AADB", border="white",
         xlab= input$feature,
         main = "Histogram showing distribution in all numeric variables in this dataset")
  })
}

shinyApp(ui, server)
