# blsh001
This repository holds various investment algorithms followign the BUY Low Sell High approach to market. It holds fully working algorithms that has been tested on the liquid US equities.

The files here are to be used with the MarkSignAlgo education videos on YouTube, where thorough explanations and examples for variables are being/will be provided.

It has two main functions:
1. get_data_api(ticker) that getst the ticker data from IEX CLOUD. You need to provide your own token to make it work. Alaternatively, if you are using a different source, make sure the output DataFrame has the columns seen inside the function.
2. trading_flattish(). The actual investment algorithm, that takes a series of inputs and then identifies the investment timings, BUY and SELL.


