## Introduction
- This is a python calculator that I have built for the purpose of stock valuation, using the __discounted free cash flow method__ using the *yfinance* and *pandas* libraries.  
 *(For information about discounted free cash flow, check out :point_right: https://www.investopedia.com/terms/d/dcf.asp)*
 
 - The steps are based on this Youtube video by [Learn to invest](https://www.youtube.com/channel/UCSglJMvX-zSgv3PEJIE_inw) in this link :point_right: https://www.youtube.com/watch?v=fd_emLLzJnk
 
 ## How it works
 - Basically, it will ask the user to input a ticker symbol that is available on Yahoo! Finance. Then it will perform all the calculations required and return the intrinsic/fair value
 of the stock based on the discounted free cash flow analysis.  
 
 *For specific features :point_down:*
 
 ## Features
 - This calculator can:  
 1. Grab all the financial statement data available on Yahoo! Finance automatically for the user using Yahoo! Finance's API.
 2. Calculate all the financial rates by itself, or ask the user for their preferred rates, including cost of debt, cost of equity (CAPM), cost of capital (WACC), etc.
 3. Handle any invalid input from the user without breaking or requiring the restarting the program 
 
 ## Some limitations of this calculator...
 __1. It will not work on some tickers__
 #### Why?
 - Out of the [many ways to find free cash flow](https://www.investopedia.com/ask/answers/033015/what-formula-calculating-free-cash-flow.asp), and thus to forecast it, this calculator 
 uses the __Operating Cash Flow method__, which requires *Net operating cash flow* and *Capital expenditure*. 
 The thing is, some tickers, like JPM, *does not have 'Capital expenditure' as a line item in their financial statement as presented on Yahoo! Finance*. Therefore, that line item 
 wouldn't exist when using *yfinance* as well. Thus, making any further calculation useless. 
 
 __2. Some tickers will require manual inputs from the user__
  #### Why?
  - As a feature, this calculate not only can do all the calculations by itself based on the API data, but it also allows manual number inputs from the users. Other than being a feature, 
  this is to tackle the problem that *some ticker's API data does not have the required line items to calculate the cost of debt or cost of equity and cost of equity, properly*. 
  This is due to how much information the Yahoo! Finance's API provide, which means some items could be missing for some companies, and the users would have to manually search for 
  the comapany's financial data from the company's site or other financial websites.. 
  
  ## Important reminder about the jupyter notebook file vs the actual python file
  1. The jupyter notebook file is better to use if you are trying to understand how the code works and the steps to the mathematical calculations, since it contains markdown cells
  that explains break down the steps and make them clearer. 
  2. The python file has been cleaned up in terms of the comments, but the codes (variable names, functions, etc.) are the same as the jupyter notebook version
  3. __HOWEVER__, the the __first two cells__ in the jupyter notebook version are __wrapped together in a while loop__ in the python version. This is purely for handling the the 1st issue mentioned
  in the limitations of the calculator. The rest is the same. 
  
  ## How to try the program
  The best way to try the program without needing to have an IDE is to download the DFCF Stock Valuation Calculator.**ipynb** file and run it with [Google Colab]  (https://research.google.com/colaboratory/)
