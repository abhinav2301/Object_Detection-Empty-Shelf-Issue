import PySimpleGUI as sg      
import os
#from object_detection.ssd2 import cropped
from shutil import copyfile
#from train import train_func
import shutil
#from main import main_func
directory = os.getcwd()
direc=os.getcwd()


layout = [[sg.Text('Product Training!', size=(30, 1), font=("Helvetica", 25), text_color='black')],      
    #[sg.Text('Training Section ', font=("Helvetica", 18), text_color='black')],
    [sg.Text('_'  * 100, size=(70, 1))],
    [sg.Text('Add Single SKU',font=("Helvetica", 15), text_color='black')],
    [sg.Text('SKU Name : '),sg.InputText(do_not_clear=False)],  
    [sg.Text('Select Image path: '),sg.InputText(do_not_clear=False), sg.FolderBrowse()],
    [sg.Button('Add SKU',button_color=('white', 'green'))],
    [sg.Text('_'  * 100, size=(70, 1))],
    [sg.Text("Add Multiple SKU's", font=("Helvetica", 15), text_color='black')],    
    [sg.Text("Select SKU's path: "),sg.InputText(do_not_clear=False),sg.FolderBrowse()],
    [sg.Button("Add Multiple SKU's",button_color=('white', 'green'))],
    [sg.Text('_'  * 100, size=(70, 1))],
    [sg.Text("Add CSV file", font=("Helvetica", 15), text_color='black')],    
    [sg.Text("Select csv path: "),sg.InputText(do_not_clear=False),sg.FileBrowse()],
    [sg.Button('Add CSV', button_color=('white', 'green'))],
    [sg.Text('_'  * 100, size=(70, 1))],      
    [sg.Button('Train', button_color=('white', 'green')), sg.Button('Detect', button_color=('white', 'green')), sg.Button('Exit', button_color=('white', 'green'))]]
window = sg.Window('UST-Global', layout, auto_size_text=True, default_element_size=(40, 1))    
directory = directory + '/Dataset'
count_class = 0

def Add_SKU(value0,value1):  
    
    os.mkdir(directory + '/train/' + value0)
    os.mkdir(directory + '/test/' + value0)
    counter = 0
    for filename in os.listdir(value1):
        counter = counter + 1
    n = 0    
    for filename in os.listdir(value1):
        n = n + 1
        
        if n!= counter and n!= counter-1 :
            copyfile(value1 +'/'+ filename, directory +'/train/' + value0 + '/' + str(n) + '.jpg')
            #cropped(directory +'/train/' + value0 + '/' + str(n) + '.jpg')

            for i in range(10):
                shutil.copy2(directory +'/train/' + value0 + '/' + str(n) + '.jpg' , directory +'/train/' + value0 + '/' + str(n) + '{}.jpg'.format(i))
    
        else :
            copyfile(value1 +'/'+ filename, directory +'/test/' + value0 + '/' +str(counter-n+1)+'.jpg' )
            #cropped(directory +'/test/' + value0 + '/'+ str(counter-n+1)+'.jpg')


def add_csv(value3):
    copyfile(value3,direc+'/SKU.csv')

 
def Add_Multiple_SKU(value):
    for clname in os.listdir(value):
        os.mkdir(directory + '/train/' + str(clname))
        os.mkdir(directory + '/test/' + str(clname))
        counter=0
        for filename in os.listdir(value+'/'+str(clname)):
            counter = counter + 1
        n = 0    
        for filename in os.listdir(value+'/'+str(clname)):
            n = n + 1
        
            if n!= counter and n!= counter-1 :
                copyfile(value + '/' + str(clname) +'/'+ filename, directory +'/train/' + str(clname) + '/' + str(n) + '.jpg')
                #cropped(directory +'/train/' + str(clname) + '/' + str(n) + '.jpg')

                for i in range(10):
                    shutil.copy2(directory +'/train/' + str(clname) + '/' + str(n) + '.jpg' , directory +'/train/' + str(clname) + '/' + str(n) + '{}.jpg'.format(i))
    
            else :
                copyfile(value + '/' + str(clname) +'/'+ filename, directory +'/test/' + str(clname) + '/' +str(counter-n+1)+'.jpg' )
                #cropped(directory +'/test/' + str(clname) + '/'+ str(counter-n+1)+'.jpg')
   

while True:                 # Event Loop
    event, value = window.Read()
    if event is None or event == 'Exit':
        break
    if event == "Add SKU":
        Add_SKU(value[0],value[1])    
    if event == "Add Multiple SKU's":
        Add_Multiple_SKU(value[2])    
    for j in os.listdir(directory + '/train/'):
        count_class = count_class + 1 
    if event == 'Train':
        train_func(count_class)
    if event == 'Add CSV':
        add_csv(value[3]) 
    if event == 'Detect':
        window.Close() 
        import main

window.Close()




