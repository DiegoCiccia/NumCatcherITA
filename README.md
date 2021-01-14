# NumCatcherITA
(ITA only) A Python Accounting Application that operates a double control between the invoice file (txt) released by an accounting program and the invoice file (csv) released by the Agenzia delle Entrate

- Be sure to place the files (txt from the accounting program, csv from Agenzia delle Entrate) in the same directory of the script;
- Start the code and input (in the Tkinter interface or directly on the Spider prompt) the name of the files (plus their extensions .txt and .csv);
- The code will output a txt file named 'Sender.txt' which contains the invoices which are missing on the basis of the cross control and other control infos;
- Some invoices may be not correctly matched by the code because of the restrictions on the number of figures in the invoice number.

