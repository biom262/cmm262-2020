# Hypothesis testing intuition applet by Scott Rifkin for UCSD BIEB100 Fall 2017. 
# Creative commons license NC-SA-BY

# v2.0  Same as one from 2014, but distributions split into two rows
#v2.1   Modified so that color changes when real = null and so the null distribution is just all purple and there is no typeI except when real==null
#get rid of multicolored. 
# v2.2 Added two-sided tests
# v2.3 Allowed piNull to be changed.

if (!require("pacman")) install.packages("pacman")
pacman::p_load(shiny,pander,markdown,stringr,grDevices)


# function derived from the highlightHTMLcells() function of the highlightHTML package
colortable <- function(htmltab, css, style="table-condensed table-bordered"){
  tmp <- str_split(htmltab, "\n")[[1]] 
  CSSid <- gsub("\\{.+", "", css)
  CSSid <- gsub("^[\\s+]|\\s+$", "", CSSid)
  CSSidPaste <- gsub("#", "", CSSid)
  CSSid2 <- paste(" ", CSSid, sep = "")
  ids <- paste0("<td id='", CSSidPaste, "'")
  for (i in 1:length(CSSid)) {
    locations <- grep(CSSid[i], tmp)
    tmp[locations] <- gsub("<td", ids[i], tmp[locations])
    tmp[locations] <- gsub(CSSid2[i], "", tmp[locations], 
                           fixed = TRUE)
  }
  htmltab <- paste(tmp, collapse="\n")
  Encoding(htmltab) <- "UTF-8"
  list(
    tags$style(type="text/css", paste(css, collapse="\n")),
    tags$script(sprintf( 
      '$( "table" ).addClass( "table %s" );', style
    )),
    HTML(htmltab)
  )
}


ui <- fluidPage(
  
  title="UCSD Biostatistics.  Hypothesis Testing and Types of Error",
  h4("UCSD Biostatistics.  Hypothesis Testing and Types of Error"),
  HTML('This example tests whether a population propotion ("real parameter value") is equal to a null value specified by the user.'),
  fluidRow(
    column(9,
           plotOutput("errorPlot")
           ,          
           fluidRow(       
             column(4,
                    sliderInput("piNull",HTML("Null parameter value"),min=.28,max=.76,value=.5,animate=T,step=0.02,width="100%")
             ),
             column(6,offset=1,
                    sliderInput("piReal",HTML("Real parameter value"),min=.28,max=.76,value=.62,animate=T,step=0.02,width="100%")
             )
           ),
           fluidRow(
             column(5,
                    sliderInput("sampleSize","Sample size",min=40,max=1000,value=100,step=10,animate=T,width="100%")
             ),
             column(5,offset=2,
                    sliderInput("sigLevel","Significance level",min=0.005, max=0.2,value=0.05,width="100%",step=0.005,animate=T)
             )  
           )
    ),
    column(3,
           #h5("Reality is in the columns"),
           
           tableOutput("errorTable"),
           #h5("Your inference is in the rows")           ,
           fluidRow(
             column(12,
                    textOutput("statsSD")
             )
           ),
           br(),
           fluidRow(
             column(12,
                    textOutput("statsPRealT")
             )
           ),
           br(),
           br(),
           fluidRow(
             column(12,
                    radioButtons("tails", "Tail to use",
                                 c("Right" = "right",
                                   "Left" = "left",
                                   "Both" = "both")
                    )
             )
           )
    )
  ),
  fluidRow(
    column(9,
           uiOutput("includeHTML")
           # ),
           # column(3,
           #        radioButtons("dots",label=h5("Color scheme"),
           #                     choices=list("Multicolored"=0,"Dotted (good for colorblind)"=1),selected=1)
    )
  ),
  br(),
  br(),
  HTML('This applet by Scott Rifkin is covered by a Creative Commons NC-BY-SA license')
  
)





#Define the server logic required to draw the output
server <- function(input,output){
  # Expression that generates the plot. The expression is
  # wrapped in a call to renderPlot to indicate that:
  #
  #  1) It is "reactive" and therefore should re-execute automatically
  #     when inputs change
  #  2) Its output type is a plot  
  cssNoDots <- c("#bgyellow {background-color: #FFFF99;}",
                 "#bgblue {background-color: #0099FF;}",
                 "#bgred {background-color: #FF3366;}",
                 "#bgcyan {background-color: #66FFFF;}"
  )
  cssDots <- c("#bgpurple {background-color: #7F6AFA;}",
               "#bgorange {background-color: #F49816;}",
               "#bglightpurple {background-color: #D6B7F6;}",
               "#bglightorange {background-color: #F7CF97;}"
  )
  getpiNull<-reactive({input$piNull})
  #piNull = 0.50
  xvals=seq(0,1,by=0.001)
  getpiReal<-reactive({input$piReal})
  getSigLevel<-reactive({input$sigLevel})
  getSampleSize<-reactive({input$sampleSize})
  getSENull<-reactive({sqrt(input$piNull*(1-input$piNull)/input$sampleSize)})
  getYValsNull<-reactive({dnorm(xvals,input$piNull,sqrt(input$piNull*(1-input$piNull)/input$sampleSize))})
  getYValsReal<-reactive({dnorm(xvals,input$piReal,sqrt(input$piNull*(1-input$piNull)/input$sampleSize))})
  getDots<-reactive({input$dots})
  
  getAlphaPosition<-reactive({
    switch(input$tails,
           right=qnorm(1-input$sigLevel,input$piNull,sqrt(input$piNull*(1-input$piNull)/input$sampleSize)),
           left=qnorm(input$sigLevel,input$piNull,sqrt(input$piNull*(1-input$piNull)/input$sampleSize)),
           both=c(qnorm(input$sigLevel/2,input$piNull,sqrt(input$piNull*(1-input$piNull)/input$sampleSize)),qnorm(1-input$sigLevel/2,input$piNull,sqrt(input$piNull*(1-input$piNull)/input$sampleSize)))#note this just gives left one.  need to do both later on
    )
  })
  
  
  
  getIncludeHTML<-reactive({
    if (input$piReal==input$piNull){
      return(includeHTML("includeDots_realEqnull_v2.3.html"))
    } else {
      return(includeHTML("includeDots_realNEnull_v2.3.html"))
    }
  })
  
  magenta=rgb(.4,0,1)
  darkorange=rgb(1,.7,0)
  cyan=rgb(0,1,1)
  blue=rgb(0,0,1)
  yellow=rgb(1,1,0,.7)
  red=rgb(1,0,0)
  
  output$errorPlot <- renderPlot({
    # This has been modified to make it two rows. Top is real, bottom is null
    
    #Get reactive components
    piReal=getpiReal()
    piNull=getpiNull()
    sampleSize=getSampleSize()
    seNull=getSENull()
    sigLevel=getSigLevel()
    alphaPosition=getAlphaPosition()
    realBase=.5
    yvalsNull=getYValsNull()
    yvalsNull=(realBase*0.9)*yvalsNull/max(yvalsNull)
    yvalsReal=getYValsReal()
    yvalsReal=realBase+(realBase*0.9)*yvalsReal/max(yvalsReal)
    
    #Draw distribution outlines
    plot(xvals,yvalsNull,type="l",ylim=c(0,1),xlim=c(0,1),xlab="Statistic value",yaxt='n',ylab="frequency of getting a particular statistic value",lwd=1,xaxt='n')
    axis(side=1,labels=F) 
    lines(xvals,yvalsReal)
    abline(h=.5,col='black')
    
    #New version - error regions are dots and the full distributions are shaded (or maybe just left)
    
    #Real is above, null is in bottom
    
    ###################### Right tailed #########################
    if (input$tails=='right'){
      #Draw real distribution no error
      text(-.03,.95,sprintf("Sampling distribution around the true population parameter\n(hypothetical - real one is unknowable)"),pos=4)
      
      if (piReal!=piNull){
        iL=which(xvals>=alphaPosition)[1]
        iR=length(xvals)
        xv=c(xvals[iL],xvals[iL:iR],xvals[iR],xvals[iL])
        yv=c(realBase,yvalsReal[iL:iR],realBase,realBase)
        polygon(xv,yv,col=darkorange)
      } else {
        iL=1
        iR=which(xvals>=alphaPosition)[1]
        xv=c(xvals[iL],xvals[iL:iR],xvals[iR],xvals[iL])
        yv=c(realBase,yvalsReal[iL:iR],realBase,realBase)
        polygon(xv,yv,col=magenta)
      }
      #Draw Null distribution no error
      # In v2.1, this is the entire distribution.  iR is just the length of yvalsNull
      iL=1
      iR=length(yvalsNull)#which(xvals>=alphaPosition)[1]
      xv=c(xvals[iL],xvals[iL:iR],xvals[iR],xvals[iL])
      yv=c(0,yvalsNull[iL:iR],0,0)
      polygon(xv,yv,col=magenta)
      text(-.03,.45,"Null distribution (specified by researcher)",pos=4)
      
      
      #Draw Type II error
      if (piReal!=piNull){
        iL=1
        iR=which(xvals>=alphaPosition)[1]
        xv=c(xvals[iL],xvals[iL:iR],xvals[iR],xvals[iL])
        yv=c(realBase,yvalsReal[iL:iR],realBase,realBase)
        polygon(xv,yv,col='navajowhite')
        
        text(min(alphaPosition-.05,piReal),.75,sprintf('%0.3f',pnorm(alphaPosition,piReal,seNull,lower.tail=T)),col='black',cex=1.2,vfont=c('sans serif','bold'))
        text(max(alphaPosition+.05,piReal),.75,sprintf('%0.3f',pnorm(alphaPosition,piReal,seNull,lower.tail=F)),col='black',cex=1.2,vfont=c('sans serif','bold'))
        text(min(alphaPosition,piReal-2*seNull),.6,sprintf('False negative region\n(Type II error)'),pos=2)
        text(max(alphaPosition,piReal+2*seNull),.6,sprintf('Good region\n(Test result matches reality)'),pos=4)
      }
      # #Draw Type I error
      if (piReal==piNull){
        iL=which(xvals>=alphaPosition)[1]
        iR=length(xvals)
        xv=c(xvals[iL],xvals[iL:iR],xvals[iR],xvals[iL])
        yv=c(realBase,yvalsReal[iL:iR],realBase,realBase)
        polygon(xv,yv,col='plum3')
        text(min(alphaPosition-.05,piReal),.75,sprintf('%0.3f',pnorm(alphaPosition,piReal,seNull,lower.tail=T)),col='white',cex=1.2,vfont=c('sans serif','bold'))
        text(max(alphaPosition+.05,piReal),.75,sprintf('%0.3f',pnorm(alphaPosition,piReal,seNull,lower.tail=F)),col=magenta,cex=1.2,vfont=c('sans serif','bold'))
        text(max(alphaPosition,piReal+2*seNull),.6,sprintf('False positive region\n(Type I error)'),pos=4)
        text(min(alphaPosition,piReal-2*seNull),.6,sprintf('Good region\n(Test result matches reality)'),pos=2)
      }
      abline(v=alphaPosition,lty="longdash",col="green3",lwd=3)
      
      text(piNull ,.25,sprintf('%0.3f',1-sigLevel),col='white',cex=1.2,vfont=c('sans serif','bold'))
      text(max(alphaPosition+.05,piNull +seNull*2),.25,sprintf('%0.3f',sigLevel),col=magenta,cex=1.2,vfont=c('sans serif','bold'))
      ###################### Left tailed #########################
      
    } else if (input$tails=='left'){
      #Draw real distribution no error
      text(1.03,.95,sprintf("Sampling distribution around the true population parameter\n(hypothetical - real one is unknowable)"),pos=2)
      
      if (piReal!=piNull){
        iR=which(xvals>=alphaPosition)[1]
        iL=1
        xv=c(xvals[iL],xvals[iL:iR],xvals[iR],xvals[iL])
        yv=c(realBase,yvalsReal[iL:iR],realBase,realBase)
        polygon(xv,yv,col=darkorange)
      } else {
        iL=which(xvals>=alphaPosition)[1]
        iR=length(xvals)
        xv=c(xvals[iL],xvals[iL:iR],xvals[iR],xvals[iL])
        yv=c(realBase,yvalsReal[iL:iR],realBase,realBase)
        polygon(xv,yv,col=magenta)
      }
      #Draw Null distribution no error
      # In v2.1, this is the entire distribution.  iR is just the length of yvalsNull
      iL=1
      iR=length(yvalsNull)#which(xvals>=alphaPosition)[1]
      xv=c(xvals[iL],xvals[iL:iR],xvals[iR],xvals[iL])
      yv=c(0,yvalsNull[iL:iR],0,0)
      polygon(xv,yv,col=magenta)
      text(1.03,.45,"Null distribution (specified by researcher)",pos=2)
      
      
      #Draw Type II error
      if (piReal!=piNull){
        iL=which(xvals>=alphaPosition)[1]
        iR=length(xvals)
        xv=c(xvals[iL],xvals[iL:iR],xvals[iR],xvals[iL])
        yv=c(realBase,yvalsReal[iL:iR],realBase,realBase)
        polygon(xv,yv,col='navajowhite')
        
        text(min(alphaPosition-.05,piReal),.75,sprintf('%0.3f',pnorm(alphaPosition,piReal,seNull,lower.tail=T)),col='black',cex=1.2,vfont=c('sans serif','bold'))
        text(max(alphaPosition+.05,piReal),.75,sprintf('%0.3f',pnorm(alphaPosition,piReal,seNull,lower.tail=F)),col='black',cex=1.2,vfont=c('sans serif','bold'))
        text(min(alphaPosition,piReal-2*seNull),.6,sprintf('Good region\n(Test result matches reality)'),pos=2)
        text(max(alphaPosition,piReal+2*seNull),.6,sprintf('False negative region\n(Type II error)'),pos=4)
      } 
      # #Draw Type I error
      if (piReal==piNull){
        iL=1
        iR=which(xvals>=alphaPosition)[1]
        xv=c(xvals[iL],xvals[iL:iR],xvals[iR],xvals[iL])
        yv=c(realBase,yvalsReal[iL:iR],realBase,realBase)
        polygon(xv,yv,col='plum3')
        text(min(alphaPosition-.05,piReal),.75,sprintf('%0.3f',pnorm(alphaPosition,piReal,seNull,lower.tail=T)),col=magenta,cex=1.2,vfont=c('sans serif','bold'))
        text(max(alphaPosition+.05,piReal),.75,sprintf('%0.3f',pnorm(alphaPosition,piReal,seNull,lower.tail=F)),col='white',cex=1.2,vfont=c('sans serif','bold'))
        text(max(alphaPosition,piReal+2*seNull),.6,sprintf('Good region\n(Test result matches reality)'),pos=4)
        text(min(alphaPosition,piReal-2*seNull),.6,sprintf('False positive region\n(Type I error)'),pos=2)
      }
      abline(v=alphaPosition,lty="longdash",col="green3",lwd=3)
      
      text(piNull ,.25,sprintf('%0.3f',1-sigLevel),col='white',cex=1.2,vfont=c('sans serif','bold'))
      text(min(alphaPosition-.05,piNull -seNull*2),.25,sprintf('%0.3f',sigLevel),col=magenta,cex=1.2,vfont=c('sans serif','bold'))
      
      
      ###################### Two tailed #########################
      
    } else { #both
      
      
      #Draw real distribution no error
      text(-.03,.95,sprintf("Sampling distribution around the true population parameter\n(hypothetical - real one is unknowable)"),pos=4)
      
      if (piReal!=piNull){
        iL1=1
        iR1=which(xvals>=alphaPosition[1])[1]
        iL2=which(xvals>=alphaPosition[2])[1]
        iR2=length(xvals)
        xv1=c(xvals[iL1],xvals[iL1:iR1],xvals[iR1],xvals[iL1])
        yv1=c(realBase,yvalsReal[iL1:iR1],realBase,realBase)
        xv2=c(xvals[iL2],xvals[iL2:iR2],xvals[iR2],xvals[iL2])
        yv2=c(realBase,yvalsReal[iL2:iR2],realBase,realBase)
        polygon(xv1,yv1,col=darkorange)
        polygon(xv2,yv2,col=darkorange)
        
      } else {
        iL=which(xvals>=alphaPosition[1])[1]
        iR=which(xvals>=alphaPosition[2])[1]
        xv=c(xvals[iL],xvals[iL:iR],xvals[iR],xvals[iL])
        yv=c(realBase,yvalsReal[iL:iR],realBase,realBase)
        polygon(xv,yv,col=magenta)
      }

      #Draw Null distribution no error
      # In v2.1, this is the entire distribution.  iR is just the length of yvalsNull
      iL=1
      iR=length(xvals)
      xv=c(xvals[iL],xvals[iL:iR],xvals[iR],xvals[iL])
      yv=c(0,yvalsNull[iL:iR],0,0)
      polygon(xv,yv,col=magenta)
      text(-.03,.45,"Null distribution (specified by researcher)",pos=4)
      
      
      #Draw Type II error
      if (piReal!=piNull){
        iL=which(xvals>=alphaPosition[1])[1]
        iR=which(xvals>=alphaPosition[2])[1]
        xv=c(xvals[iL],xvals[iL:iR],xvals[iR],xvals[iL])
        yv=c(realBase,yvalsReal[iL:iR],realBase,realBase)
        polygon(xv,yv,col='navajowhite')
        
        text(min(alphaPosition[1]-.05,piReal),.75,sprintf('%0.3f',pnorm(alphaPosition[1],piReal,seNull,lower.tail=T)),col='black',cex=1.2,vfont=c('sans serif','bold'))
        text(max(alphaPosition[2]+.05,piReal),.75,sprintf('%0.3f',pnorm(alphaPosition[2],piReal,seNull,lower.tail=F)),col='black',cex=1.2,vfont=c('sans serif','bold'))
        if (iL!=iR){# then there is a good false positive region
          text(.5,.75,sprintf('%0.3f',1-(pnorm(alphaPosition[1],piReal,seNull,lower.tail=T)+pnorm(alphaPosition[2],piReal,seNull,lower.tail=F))),col='black',cex=1.2,vfont=c('sans serif','bold'))
        }

        text(min(alphaPosition[1],piReal-2*seNull),.6,sprintf('Good region\n(Test result matches reality)'),pos=2)
        text(max(alphaPosition,piReal+2*seNull),.6,sprintf('Good region\n(Test result matches reality)'),pos=4)
        if (iL!=iR){# then there is a good false positive region
          text(.5,.6,sprintf('Type II\nerror)'))
        }
        
        
      } 
      # #Draw Type I error
      if (piReal==piNull){
        iL1=1
        iR1=which(xvals>=alphaPosition[1])[1]
        iL2=which(xvals>=alphaPosition[2])[1]
        iR2=length(xvals)
        xv1=c(xvals[iL1],xvals[iL1:iR1],xvals[iR1],xvals[iL1])
        yv1=c(realBase,yvalsReal[iL1:iR1],realBase,realBase)
        xv2=c(xvals[iL2],xvals[iL2:iR2],xvals[iR2],xvals[iL2])
        yv2=c(realBase,yvalsReal[iL2:iR2],realBase,realBase)
        polygon(xv1,yv1,col='plum3')
        polygon(xv2,yv2,col='plum3')
        text(min(alphaPosition[1]-.05,piReal),.75,sprintf('%0.3f',pnorm(alphaPosition[1],piReal,seNull,lower.tail=T)),col=magenta,cex=1.2,vfont=c('sans serif','bold'))
        text(max(alphaPosition[2]+.05,piReal),.75,sprintf('%0.3f',pnorm(alphaPosition[2],piReal,seNull,lower.tail=F)),col=magenta,cex=1.2,vfont=c('sans serif','bold'))
        text(.5,.75,sprintf('%0.3f',1-(pnorm(alphaPosition[1],piReal,seNull,lower.tail=T)+pnorm(alphaPosition[2],piReal,seNull,lower.tail=F))),col='white',cex=1.2,vfont=c('sans serif','bold'))
        text(min(alphaPosition[1],piReal-2*seNull),.6,sprintf('False positive region\n(Type I error)'),pos=2)
        text(max(alphaPosition[2],piReal+2*seNull),.6,sprintf('False positive region\n(Type I error)'),pos=4)
        text(piReal,.6,sprintf('Good'),col='white')
      }
      abline(v=alphaPosition[1],lty="longdash",col="green3",lwd=3)
      abline(v=alphaPosition[2],lty="longdash",col="green3",lwd=3)
      
      text(piNull ,.25,sprintf('%0.3f',1-sigLevel),col='white',cex=1.2,vfont=c('sans serif','bold'))
      text(min(alphaPosition[1]-.05,piNull -seNull*2),.25,sprintf('%0.3f',sigLevel/2),col=magenta,cex=1.2,vfont=c('sans serif','bold'))
      text(max(alphaPosition[2]+.05,piNull +seNull*2),.25,sprintf('%0.3f',sigLevel/2),col=magenta,cex=1.2,vfont=c('sans serif','bold'))
    }
    
    
  })#end render plot
  
  output$errorTable<-renderUI({
    #Get reactive components
    piReal=getpiReal()
    piNull=getpiNull()
    seNull=getSENull()
    sigLevel=getSigLevel()
    alphaPosition=getAlphaPosition()
    #Determine error table
    errorTab=array(0,dim=c(2,1))
    ###################### Right tailed #########################
    
    if (input$tails=='right'){
      if (piReal==piNull){
        #Type I
        errorTab[1,1]=sigLevel
        #Null good
        errorTab[2,1]=1-sigLevel
      } else {
        #Alt good = power
        errorTab[1,1]=pnorm(alphaPosition,piReal,seNull,lower.tail=F)
        #Type II
        errorTab[2,1]=1-errorTab[1,1]
      }
      if (piReal==piNull){
        errorTab=data.frame(Real.Is.Null=c(sprintf("%0.3f #bglightpurple",errorTab[1,1]),
                                           sprintf("%0.3f #bgpurple",errorTab[2,1])),
                            row.names=c("Reject null (Type I error)","Don't reject (good)")
        )
      } else {
        errorTab=data.frame(Real.Is.Not.Null=c(sprintf("%0.3f #bgorange",errorTab[1,1]),
                                               sprintf("%0.3f #bglightorange",errorTab[2,1])),
                            row.names=c("Reject null (good)","Don't reject (Type II error)")      )
      }
      ###################### Left tailed #########################
      
    } else if (input$tails=='left'){
      if (piReal==piNull){
        #Type I
        errorTab[1,1]=sigLevel
        #Null good
        errorTab[2,1]=1-sigLevel
      } else {
        #Alt good = power
        errorTab[1,1]=pnorm(alphaPosition,piReal,seNull,lower.tail=T)
        #Type II
        errorTab[2,1]=1-errorTab[1,1]
      }
      if (piReal==piNull){
        errorTab=data.frame(Real.Is.Null=c(sprintf("%0.3f #bglightpurple",errorTab[1,1]),
                                           sprintf("%0.3f #bgpurple",errorTab[2,1])),
                            row.names=c("Reject null (Type I error)","Don't reject (good)")
        )
      } else {
        errorTab=data.frame(Real.Is.Not.Null=c(sprintf("%0.3f #bgorange",errorTab[1,1]),
                                               sprintf("%0.3f #bglightorange",errorTab[2,1])),
                            row.names=c("Reject null (good)","Don't reject (Type II error)")      )
      }
      
      
      
      
      ###################### Two tailed #########################
      
    } else {
      
      if (piReal==piNull){
        #Type I
        errorTab[1,1]=sigLevel
        #Null good
        errorTab[2,1]=1-sigLevel
      } else {
        #Alt good = power
        errorTab[1,1]=pnorm(alphaPosition[1],piReal,seNull,lower.tail=T)+pnorm(alphaPosition[2],piReal,seNull,lower.tail=F)
        #Type II
        errorTab[2,1]=1-errorTab[1,1]
      }
      if (piReal==piNull){
        errorTab=data.frame(Real.Is.Null=c(sprintf("%0.3f #bglightpurple",errorTab[1,1]),
                                           sprintf("%0.3f #bgpurple",errorTab[2,1])),
                            row.names=c("Reject null (Type I error)","Don't reject (good)")
        )
      } else {
        errorTab=data.frame(Real.Is.Not.Null=c(sprintf("%0.3f #bgorange",errorTab[1,1]),
                                               sprintf("%0.3f #bglightorange",errorTab[2,1])),
                            row.names=c("Reject null (good)","Don't reject (Type II error)")      )
      }
      
      
      
      
      
      
      
    }
    css=cssDots
    
    htmlErrorTab=markdownToHTML(text=pandoc.table.return( errorTab, style="rmarkdown",split.tables=Inf),fragment.only=TRUE)
    colortable(htmlErrorTab,css)
  })
  
  output$statsSD<-renderText({
    seNull=getSENull()
    sprintf("SD of sampling dist (SE): %0.3f",seNull)     
  })
  output$statsPRealT<-renderText({
    alphaPosition=getAlphaPosition()
    HTML(sprintf("Statistic value for the significance level cutoff:  %0.2f",alphaPosition)  )    
  })
  
  output$includeHTML<-renderUI({
    getIncludeHTML()
    
  })
}#shinyServer

# Run the application 
shinyApp(ui = ui, server = server)