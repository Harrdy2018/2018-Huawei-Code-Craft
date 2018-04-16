# coding=utf-8
import sys
import os
import predictor

def main():
    print 'main function begin.'
    # Read the input files
    ecsDataPath = "TrainData.txt"
    inputFilePath = "input.txt"
    resultFilePath='output.txt'
    ecs_infor_array = read_lines(ecsDataPath)
    #print(ecs_infor_array)
    input_file_array = read_lines(inputFilePath)
    predic_result = predictor.predict_vm(ecs_infor_array, input_file_array)
    print predic_result
    if len(predic_result) != 0:
        write_result(predic_result, resultFilePath)
    else:
        predic_result.append("NA")
        write_result(predic_result, resultFilePath)
    print 'main function end.'
def read_lines(file_path):
        array = []
        with open(file_path, 'r') as lines:
            for line in lines:
                array.append(line)
        return array
def write_result(array, outpuFilePath):
    with open(outpuFilePath, 'w') as output_file:
        for item in array:
            output_file.write("%s\n" % item)

if __name__ == "__main__":
    main()
