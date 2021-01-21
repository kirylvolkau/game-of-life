import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Dense

from data_prep import neighbourhood as nb
from data_prep import train_parser as tp

from cone_models import layer3_1 as lr
import time

full_data = tp.read_file("data/train.csv")

delta1_matrices = [m for m in full_data if int(m.delta) == 1]

train_set = [];
target_set = [];
test_setX = [];
test_setY = [];

print(len(delta1_matrices))

# we don't need that much training data
# the following loop will use the first SAMPLE SIZE matrices
# each matrix provides for 625 data points
#
#TEST VALS
#epochs, SampleSize: val
#100, 10: 0.17952583730220795
#100, 20: 0.15150538086891174
#100, 25: 0.17131944000720978
#100, 100: 0.14687006175518036 
#100, 250: 0.1660555601119995 
#100, 500: 0.14054317772388458 <----
#100, 1000: 0.15636806190013885
#HUBER LOSS:
#100, 100: 0.050485122948884964
#10, 10: 0.0606510154902935 
#COSINE SIMILARITY:
#10, 10: -0.1925347000360489
#100, 100: -0.19253471493721008
#CROSSENTROPY,SGD
#100, 500: 0.30233538150787354
#10, 10: 0.4226294159889221 
#100, 10: 0.3861066997051239
#100, 1000: 0.3020850121974945
SAMPLE_SIZE = 1000
c = 1
flag = True
for m in delta1_matrices:
    if c == SAMPLE_SIZE:
        flag = False;
    if flag:
        for i in range(0,24):
            for j in range(0, 24):
                train_set.append(nb.return_neighbourhood_matrix(m.stopmatrix, 3, i, j, 25))
                target_set.append(m.startmatrix[i][j])
        c = c + 1
    else:
        for i in range(0,24):
            for j in range(0, 24):
                test_setX.append(nb.return_neighbourhood_matrix(m.stopmatrix, 3, i, j, 25))
                test_setY.append(m.startmatrix[i][j])
        c = c + 1
        if c == 2 * SAMPLE_SIZE:
            break

model = lr.get3_1Model()
print("Starting Training...")
start_time = time.time()
(history, trained) = lr.trainModel(model, np.asarray(train_set), np.asarray(target_set))
print("Training took:", time.time() - start_time)
lr.testModel(trained, np.asarray(test_setX), np.asarray(test_setY))

model_path = 'saved_models/model_crossentropy_1000_1000.model'

trained.save(model_path)

