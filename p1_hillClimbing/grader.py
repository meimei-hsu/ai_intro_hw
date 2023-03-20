import json
import subprocess
import sys
import graderUtil

total_score = 0

for i in range(4):
    task_file_base = "task_" + str(i) + "_"
    for j in range(2):
        if (i >= 2) & (j == 0):
            continue
        task_file = task_file_base + str(j) + ".txt"
        cmd = [graderUtil.py_command, graderUtil.py_code, task_file]
        cmd = " ".join(cmd)
        print(cmd)
        
        # Run the submmision.py by tasks
        try:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except:
            print("Unexpected error:", sys.exc_info())
        (output, err) = p.communicate()     
        result = output.decode("utf-8")
        result = [x for x in result.split("\n") if x]
        result = result[-1]

        # Check the result format
        is_pass = graderUtil.check_format(i, j, result)
        if not is_pass:
            print("\tYour result format is not correct!")
            continue
        
        # Verify the result
        result = json.loads(result)
        answers = graderUtil.load_answer_file("answer.txt")
        #if i <= 3:
        if i <= 1:
            is_pass, total_score = graderUtil.verify_result(task_file, answers[task_file], i, j, result, total_score)
            if is_pass:
                print(task_file + " -- pass! current score: " + str(total_score))
            print()
        else:
            print("\ton-line testing ... ", result)

print("Totla Score: ", total_score)
