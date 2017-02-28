import os
from os.path import isfile, join
from os import walk


basepath=os.path.dirname(__file__)

label_list = []
for (dirpath, dirnames, filenames) in walk(os.path.join(basepath,"ohsumed-first-20000-docs/training")):
    label_list.extend(dirnames)


#Create dict of train labels with file number as key
train_label_dict={}
train_text_dict={}
for label in label_list:
    for (dirpath, dirnames, filenames) in walk(os.path.join(basepath,"ohsumed-first-20000-docs/training/",label)):
        for files in filenames:
            whole_text=""
            if files in train_label_dict:
                train_label_dict[files].append(label)
            else:
                train_label_dict[files] = [label]

            f = open(os.path.join(basepath,"ohsumed-first-20000-docs/training/",label, files))

            for i, line in enumerate(f):
                if i == 0:
                    line = line.rstrip("\n")[:-1] + ","

                else:
                    line = line.replace(",", ".") #comma maybe have special meaning in fasttest file format?

                whole_text= whole_text+line.rstrip("\n")

            train_text_dict[files] = whole_text

#Create dict of test labels with file number
test_label_dict={}
test_text_dict={}
for label in label_list:
    for (dirpath, dirnames, filenames) in walk(os.path.join(basepath,"ohsumed-first-20000-docs/test/",label)):
        for files in filenames:
            whole_text = ""
            if files in test_label_dict:
                test_label_dict[files].append(label)

            else:
                test_label_dict[files] = [label]
            f1 = open(os.path.join(basepath, "ohsumed-first-20000-docs/test/", label, files))

            for i, line in enumerate(f1):
                if i == 0:
                    line = line.rstrip("\n")[:-1]+","

                else:
                    line = line.replace(",", ".")  # comma maybe have special meaning in fasttest file format?

                whole_text = whole_text + line.rstrip("\n")

            test_text_dict[files] = whole_text

training_file = open(os.path.join(basepath,"fastText/data/ohsumed.train"), 'w')
for abstract_id, labels in train_label_dict.items():
    formatted_label=""
    for l in train_label_dict[abstract_id]:
        #formatted_label = formatted_label+"__label__"+l+" , "
        l = l.replace("C", "")
        if l[0]=="0":
            l=l[1:]
        formatted_label =  l + ", "

    training_file.write(formatted_label+train_text_dict[abstract_id]+"\n")

test_file = open(os.path.join(basepath,"fastText/data/ohsumed.test"), 'w')
for abstract_id, labels in test_label_dict.items():
    formatted_label=""
    for l in test_label_dict[abstract_id]:
        #formatted_label = formatted_label+"__label__"+l+" , "
        l = l.replace("C", "")
        if l[0]=="0":
            l=l[1:]

        formatted_label =   l + ", "

    test_file.write(formatted_label+test_text_dict[abstract_id]+"\n")

print(len(train_text_dict))