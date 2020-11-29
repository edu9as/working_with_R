shinyServer(function(input, output) {
  
  output$distPlot <- renderPlot({
    x <-  data[[input$feature]]
    bins <-  seq(min(x), max(x), length.out = input$bins + 1)
    hist(x, breaks = bins, col="#75AADB", border="white",
         xlab= input$feature,
         main = "Histogram showing distribution in all numeric variables in this dataset")
  })
})