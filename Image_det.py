from imageai.Prediction.Custom import CustomImagePrediction
import os
import PySimpleGUI as sg
import csv
import glob
import datetime


def detection(num):
    bound = []
    index = []
    main_index = []
    ls = []
    img = []
    res = []
    item = ''
    classes = []
    count = 0
    counter = []
    execution_path = os.getcwd()
    model_name = os.listdir('Dataset/models/')
    model_name.sort()
    a = model_name[len(model_name)-1]

    prediction = CustomImagePrediction()
    prediction.setModelTypeAsResNet()

    prediction.setModelPath(os.path.join(
        execution_path, 'Dataset/models/'+str(a)))
    prediction.setJsonPath(os.path.join(
        execution_path, 'Dataset/json/model_class.json'))
    prediction.loadModel(num_objects=num)

    for i in os.listdir(execution_path + '/Dataset/train'):
        classes.append(i)
        count = count+1

    os.chdir(os.getcwd() + '/images/crop')
    exec_path = os.getcwd()

    counter = [0] * count
    try:
        duck = os.listdir('.')
        duck.sort()
        res = prediction.predictMultipleImages(duck, result_count_per_image=1)
        for each_result in res:
            predictions, percentage_probabilities = each_result[
                "predictions"], each_result["percentage_probabilities"]
            img.append(predictions)

        for j in range(0, len(img)):
            for k in range(0, count):
                if "['"+str(classes[k])+"']" == str(img[j]) or '["'+str(classes[k])+'"]' == str(img[j]):
                    counter[k] = counter[k]+1

        for j in range(0, count):
            for k in range(0, len(img)):
                if "['"+str(classes[j])+"']" == str(img[k]):
                    index.append(k)

            main_index.append(index)
            index = []
        for i in range(0, count):
            for j in range(0, counter[i]-1):
                if main_index[i][j]+1 != main_index[i][j+1]:
                    bound.append(str(classes[i]))

        os.chdir(execution_path)
        counter.insert(0, str(datetime.datetime.now())[:-10])

        try:

            if bound != []:
                with open('Bound_Error.csv', 'w') as csv_file:
                    writer = csv.writer(csv_file, delimiter=',')
                    writer.writerow(bound)
            else:
                os.remove('Bound_Error.csv')

        except:
            print('No error in placement ')

        with open("Results.csv", "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(counter)

    except Exception as e:
        print(e)
        print('Unknown object detected')


detection(0, 8)
