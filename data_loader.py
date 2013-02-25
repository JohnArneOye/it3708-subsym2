#Load the training data. Returns a list of the data.

def read_training_files(data_nr):
    data_file = open('training_data/izzy-train'+str(data_nr)+'.dat', 'r')
    training_data = [float(x) for x in data_file.read().strip().split() if x]
    assert len(training_data) == 1001
    data_file.close()
    return training_data

if __name__ == '__main__':
    print read_training_files(2)
    