# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 15:07:11 2020

@author: 39380
"""


import pandas as pd
import tkinter as tk

window=tk.Tk()
window.geometry("400x100")
window.title("NumCatcher")
window.configure(background='#49A')

tk.Label(window, text="Inserisci txt:").grid(row=0)
tk.Label(window, text="Inserisci csv:").grid(row=1)

tx=tk.Entry(window)
cs=tk.Entry(window)

tx.grid(row=0, column=1)
cs.grid(row=1, column=1)

      

def control():
    txt=str(tx.get())
    csv=str(cs.get())

    try:
        imp=open(txt)  
    except:
        print('File non trovato')
    
    sender=open("sender.txt", "w")
    
    
    num=[]
    nnum=0
    nsum=0.0

    
    for line in imp:
        if line.startswith(" 01"):
            lines=line.split()
            pnum=str(lines[4])           
                        
            if lines[-4]=='VENDITA' or lines[-4]=='PRESTAZIONE' or lines[-3]=='VENDITA' or lines[-3]=='PRESTAZIONE':
               
                if pnum.startswith('000000'):
                    vnum=pnum[-1:]
                elif pnum.startswith('00000'):
                    vnum=pnum[-2:]
                elif pnum.startswith('0000'):
                    vnum=pnum[-3:]
                elif pnum.startswith('000'):
                    vnum=pnum[-4:]
                elif pnum.startswith('00'):
                    vnum=pnum[-5:]
                else:
                    vnum=pnum
            else:
                vnum=pnum
                
                                   
            num.append(vnum) 
            nnum=nnum+1
            
            
        elif line.startswith("                                                        TOTALE FATTURA"):
            sep=line.split()
            tot=sep[3]
            
            if "-" in tot:
                totn=tot.replace("-", "")
                totc=totn[-3:].replace(",",".")
                tots=totn[:-3].replace(".", "")
                unv=float(tots+totc)
                nsum=nsum-unv
                
            else: 
                totr=tot                
                totc=totr[-3:].replace(",",".")
                tots=totr[:-3].replace(".", "")
                unv=float(tots+totc)
                nsum=nsum+unv
                
        if 'BROGLIACCIO  I.V.A.' in line:
            ditta=line.split()
            nam=''
            for u in ditta:
                nam=nam+" "+u
            
          
    try:
        file=pd.read_csv(csv, sep=';')
    except:
        print('File non trovato')
    
    
    
    
    sender.write(nam)
    sender.write(" \n")
    sender.write(" \n")
    
       
    rep={}
    for x in num:
        if x not in rep:
            rep[x]=1
        else:
            rep[x]=rep[x]+1
    
    for ind,val in rep.items():
        if val != 1:
            repc='Si ripete in contabilità:'+' '+ str(ind) +','+' '+ str(val)+' '+'volte'
            print(repc)
            sender.write(repc)
            sender.write(" \n")
            sender.write(" \n")
            
            
            
            
    print("")
    print("")
            
            
        
    ade=[]
    dict={}
    forn={}
    tsum={}
    nade=0
    adesum=0
    
    for i in file.index:
        val=file.iloc[i, 2]
        date=file.iloc[i,3]
        tipo=file.iloc[i,1]
        impon=file.iloc[i,6]
        tax=file.iloc[i,7]
        fornitore=file.iloc[i,5]
        
        vas=val.replace("'", "")
        impons=impon.replace("'", "")
        taxs=tax.replace("'", "")
        
        if impons.startswith('0000000'):
            impon=impons[-8:]
        elif impons.startswith('00000000'):
            impon=impons[-7:]
        elif impons.startswith('000000000'):
            impon=impons[-6:]
        elif impons.startswith('0000000000'):
            impon=impons[-5:]
        elif impons.startswith('00000000000'):
            impon=impons[-4:]
        else:
            impon=impons
        
        imponc=impon.replace(".","")
        imponr=imponc.replace(",", ".")
        imponibile=float(imponr)
        
        if taxs.startswith('0000000'):
            tax=taxs[-8:]
        elif taxs.startswith('00000000'):
            tax=taxs[-7:]
        elif taxs.startswith('000000000'):
            tax=taxs[-6:]
        elif taxs.startswith('0000000000'):
            tax=taxs[-5:]
        elif taxs.startswith('00000000000'):
            tax=taxs[-4:]
        else:
            impon=impons
        
        
        taxc=tax.replace(".","")
        taxr=taxc.replace(",", ".")
        imposta=float(taxr)
        
        totale_ft=imponibile+imposta
        
        if tipo=='Fattura':
            adesum=adesum+totale_ft
        elif tipo=='Nota di credito':
            adesum=adesum-totale_ft
            
        
        
        if vas[-5:-2]=="/A/":
            vai=vas[:-3]
            
        elif vas[-5:-2]=='/20':
            vai=vas[:-5]
            
        elif len(vas)>7:
            vai=vas[-7:]
        
        else:
            vai=vas
            
        ade.append(vai)
        
        dict[vai]=date
        forn[vai]=fornitore
        tsum[vai]=totale_ft
        nade=nade+1
        
    repade={}
    for y in ade:
        if y not in repade:
            repade[y]=1
        else:
            repade[y]=repade[y]+1
    
    for ind,val in repade.items():
        if val != 1:
            repa='Si ripete in AdE:'+' '+ str(ind)+','+ ' '+ str(val)+ ' ' + 'volte'
            print(repa)
            sender.write(repa)
            sender.write("\n")
            
            
       
    print("")
    print("") 
    
    sender.write(" \n")
    sender.write(" \n")
    
    print('Da controllare:')
    print('N.B.: se le fatture si ripetono in AdE, allora i dati si riferiscono alla prima fattura controllata')
    print("")
    
    sender.write('Da controllare:')
    sender.write("\n")
    sender.write('N.B.: se le fatture si ripetono in AdE, allora i dati si riferiscono all\'ultima fattura controllata')
    sender.write(" \n")
        
            
    count=0    
    for x in ade:
        
        if x in num:
            num.remove(x)
        
        elif x not in num:
            count=count+1
            fpr=str(x)+' '+str(dict[x])+' '+str(forn[x])+' '+str(tsum[x])
            print(fpr)
            sender.write(fpr)
            sender.write("\n")
            
    print('')
    print('')
    
    sender.write(" \n")
    sender.write(" \n")
    
    
            
    outone='Ci sono'+' '+ str(count)+' '+'fatture da controllare'
    outtwo=str(nade)+' '+'Fatture presenti in AdE'
    outthree=str(nnum)+' '+'Fatture acquisite in contabilità'
    outfour='Totale Imponibile+Iva ft. acquisite:'+' '+ str(nsum)
    outfive='Totale Imponibile+Iva da AdE:'+ ' '+str(adesum)
    
    print(outone)
    print(outtwo)
    print(outthree)
    print(outfour)
    print(outfive)
    
    sender.write(outone)
    sender.write("\n")
    sender.write(outtwo)
    sender.write("\n")
    sender.write(outthree)
    sender.write("\n")
    sender.write(outfour)
    sender.write("\n")
    sender.write(outfive)
    sender.write("\n")
   
    sender.close()
    
    text="File txt creato in output"
    text_ou=tk.Label(window, text=text,fg="red")
    text_ou.grid(row=0, column=2)
    

tk.Button(window, text='Esegui Controllo', command=control).grid(row=3,column=0,sticky=tk.W, pady=4) 



if __name__ == '__main__':
    window.mainloop()

           