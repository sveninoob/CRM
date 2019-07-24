# coding: utf8
import urllib.request
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import os
global resolver
global master_dict
global current
current=""
array_quality=['Ancestral','Legendaire','Ultime']
def parse(frame,path):
    global resolver
    global master_dict
    global current

    print("launch")
    resolver={}
    opener = urllib.request.FancyURLopener({})
    typed=7
    url='https://aioncodex.com/fr/item/{}/'
    master_dict={} #pseudo as key and then dict that contain item id as key and quantity as value
    file=open(path,'r')
    for line in file.readlines():
        if 'a gagné' in line or 'Vous avez gagné [@item' in line or "a obtenu [item" in line:
                pseudo=line.split(' ')[3]
                result=line.split(':')[4]
                if 'Vous avez gagné [@item' in line:
                    result=result.split(';')[0]
                else:
                    result=result.split(']')[0]
                if not resolver.get(result) is None:
                    item=resolver.get(result)
                    r=item.split("|")[0]
                    item=item.split("|")[1]
                else:
                    f=opener.open(url.format(result))
                    content=f.readlines()
                    for dbline in content:
                        if '<span class="item_title' in dbline.decode('utf-8'):
                            quality=dbline.decode('utf-8').split('<span class="item_title item_grade_')[1]
                            quality=quality.split('"')[0]
                            item=dbline.decode('utf-8').split('<b>')[1]
                            item=item.split('</b>')[0]
                            r=int(quality)-int(typed)
                            qu='osef'
                            resolver[result]=str(r) +"|" + item
                if int(r) > -1 and int(r) < 4 :#we should care what the personn is getting
                            qu=array_quality[int(r)]
                            if not master_dict.get(pseudo) is None:
                                            print("pseudo  in " + pseudo)
                                            loaded_dict= master_dict.get(pseudo)
                                            if not loaded_dict.get(result) is None:
                                                quantity=loaded_dict.get(result)
                                                quantity=quantity+1
                                                loaded_dict[result]=quantity
                                            else :
                                                loaded_dict[result]=1
                                            master_dict[pseudo]=loaded_dict
                            else:
                                            loaded_dict={}
                                            loaded_dict[result]=1
                                            master_dict[pseudo]=loaded_dict
    #                    print(str(pseudo) + ' a ninja ' + str(item) + 'de qualite ' + qu)
    i=0
    liste.delete(0,'end')
    for client in master_dict.keys():
        liste.insert(i,client)
        i=i+1
    liste.bind("<<ListboxSelect>>",display)
    liste.pack()
    
def addToClipBoard(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)
def display(event):
    global liste
    global resolver
    global master_dict
    i=0
    pseudo=""
    for client in master_dict.keys():
        if i == liste.curselection()[0]:
            pseudo=client
            break
        else:
            i=i+1
    print(pseudo)
    texter=json_to_str(master_dict.get(pseudo),pseudo)
    label.config(text=texter)
    label.pack()
def json_to_str(dicto,pseudo):
    output=''
    name={}
    chaine=pseudo
    global current
    for item in dicto.keys():
        dictinfo=get_name(item,resolver)
        if not dictinfo is None:
            name=dictinfo.get("n")
            r=dictinfo.get("r")
            print(dictinfo)
            quantity=dicto.get(item)
            if not "Kébé" in name and not 'Lot de cubulus' in name:
                output =output+ name.replace("&#39;","'") +" X"+ str(quantity)+ "   " + array_quality[int(r)] +  "\n"
                chaine= chaine +" [@item:"+item+"] X"+str(quantity) 
    print(chaine)
    current=chaine
    return output 
def get_name(ide,resolver):
    if not resolver.get(ide) is None:
        return  {"n" : resolver.get(ide).split("|")[1],"r" : resolver.get(ide).split("|")[0]}
    else:
        return None
fenetre=Tk()
fenetre.style = Style()
s=Style()
print(s.theme_names())
#('clam', 'alt', 'default', 'classic')
fenetre.style.theme_use("vista")
fenetre.title("Communism Roll Meter (CRM)")
fenetre.attributes('-alpha', 0.98)
fenetre.iconbitmap("cbau2-rc1y0-001.ico")
failed=0
while(True):
    path=filedialog.askopenfilename(initialdir = os.getcwd(),title='Ou est ton Chat.log poutine???',)
    if os.path.basename(path) == "Chat.log":
        if not failed == 0:
            print("wess cotorep")
        break
    else:
        failed = failed +1
        if failed > 3:
            exit(0)
fenetre.update()
#fenetre.iconbitmap('s-l300')
#fenetre.withdraw()
le = LabelFrame(fenetre, text="Wess selectionne le noob de ton choix :")
le.pack(fill="both", expand="yes")
liste=Listbox(le)
liste.pack(side=TOP)
l = LabelFrame(fenetre, text="Wess ici le loot :")
l.pack(fill="both", expand="yes")
label = Label(l, text="",width=70)
label.pack(side=RIGHT)
bouton=Button(fenetre,text="PRESS ME FIRST",command=lambda: parse(fenetre,path))
bouton.pack(side=RIGHT)
bouton2=Button(fenetre,text="Copy to clipboard",command=lambda: addToClipBoard(current))
bouton2.pack(side=RIGHT)

fenetre.mainloop()
