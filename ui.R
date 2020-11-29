shinyUI(fluidPage(
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
))