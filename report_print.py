import os
import json
import subprocess

from functions import get_answer_files


class ReportPrint:
    def __init__(self, s_id: int, 
                 hw_name: str,
                 prob_name: list,
                 case_num: list,
                 class_num: list,
                 is_submitted=True):
        
        self.s_id = s_id
        self.hw_name = hw_name
        self.prob_names = prob_name
        self.case_nums = case_num
        self.class_num = class_num
        self.is_submitted = is_submitted

        if is_submitted: 
            if not os.path.isdir(f"./reports/submitted/{self.s_id}"): 
                os.mkdir(f"./reports/submitted/{self.s_id}")
        else: 
            if not os.path.isdir(f"./reports/not_submitted/{self.s_id}"): 
                os.mkdir(f"./reports/not_submitted/{self.s_id}")


        self.report_file_summary = f"./reports/submitted/{self.s_id}/{self.s_id}_summary.md" if self.is_submitted else \
                                   f"./reports/not_submitted/{self.s_id}/{self.s_id}_summary.md"
        self.report_file_submit_compile = f"./reports/submitted/{self.s_id}/{self.s_id}_submit_compile.md" if self.is_submitted else \
                                          f"./reports/not_submitted/{self.s_id}/{self.s_id}_submit_compile.md"
        self.report_file_output_diff = f"./reports/submitted/{self.s_id}/{self.s_id}_output_diff.md" if self.is_submitted else \
                                       f"./reports/not_submitted/{self.s_id}/{self.s_id}_output_diff.md"
        
        self.summary_f = open(self.report_file_summary, "w")
        self.submit_compile_f = open(self.report_file_submit_compile, "w")
        self.output_diff_f = open(self.report_file_output_diff, "w")

    
    def __del__(self):
        self.summary_f.close()
        self.submit_compile_f.close()
        self.output_diff_f.close()

        
    def __print_result(self):
        result_json_file = f"./outputs/{self.s_id}/{self.s_id}_result.json"
        with open(result_json_file, "r") as f: result_dict: dict = json.load(f)
        
        write_str = "\n## Result\n```\n"
        for key in result_dict.keys():
            write_str += f"{key} : {result_dict[key]}\n"
        write_str += "```\n"

        return write_str


    def __print_zip_ls(self):
        zip_command = ['unzip', '-l', f'./student_submission/{self.hw_name}_*_{self.s_id}.zip']
        subprocess_result = subprocess.run(zip_command, capture_output=True, text=True)

        write_str = "\n## Inside .zip\n```"
        write_str += subprocess_result.stdout
        write_str += "\n```\n"

        return write_str


    def __print_source_code(self, prob_name):
        sourcecode_file = f"./student_submission/{self.s_id}/{self.hw_name}_{prob_name}_{self.s_id}.cpp"
        
        write_str = f"\n### submitted problem-{prob_name} source code\n"
        
        if os.path.isfile(sourcecode_file):
            with open(sourcecode_file, "r", errors="replace") as f: source_code = f.read()
            write_str += f"\n```c++\n{source_code}\n```\n"
        else:
            write_str += f"no submitted problem-{prob_name} source code.\n"

        return write_str


    def __print_compile_code(self, prob_name, case_num):
        compiled_code_file = f"./outputs/{self.s_id}/{self.hw_name}_{prob_name}_case_{case_num}_{self.s_id}.cpp"

        write_str = ""

        write_str += f"\n### compiled problem-{prob_name}-case-{case_num} code\n"
        if os.path.isfile(compiled_code_file):
            with open(compiled_code_file, "r") as f: compiled_code = f.read()
            write_str += f"\n```c++\n{compiled_code}\n```\n"
        else:
            write_str += f"no compiled problem-{prob_name}-case-{case_num} code"

        return write_str


    def __print_compile_result(self, prob_name, case_num):
        compiled_result_file = f"./outputs/{self.s_id}/{self.hw_name}_{prob_name}_case_{case_num}_{self.s_id}_compile_result.txt"

        write_str = f"\n### compiled problem-{prob_name}-case-{case_num} result\n"
        if os.path.isfile(compiled_result_file):
            with open(compiled_result_file, "r", errors="replace") as f: compiled_result = f.read()
            write_str += f"\n```\n{compiled_result}\n```\n"
        else:
            write_str += f"no compiled problem-{prob_name}-case-{case_num} result"

        return write_str


    def __print_output_result(self, prob_name, case_num):
        output_result_file = f"./outputs/{self.s_id}/{self.hw_name}_{prob_name}_case_{case_num}_{self.s_id}_output.txt"

        write_str = f"\n### problem-{prob_name}-case-{case_num} output result\n"
        if os.path.isfile(output_result_file):
            with open(output_result_file, "r", errors="replace") as f: output_result = f.read()
            write_str += f"\n```\n{output_result}\n```\n"
        else:
            write_str += f"no problem-{prob_name}-case-{case_num} output result"

        return write_str

    
    def __print_output_diff_result(self, prob_name, case_num):
        answer_files = get_answer_files(self.hw_name, prob_name, case_num)
        write_str = ""
        flexible_destructor_marker = (
            f"./grading_cases/{self.hw_name}_{prob_name}_case_{case_num}"
            "_allow_all_destructor_orders"
        )
        if os.path.isfile(flexible_destructor_marker):
            write_str += ("\n> All six relative orders of the OrderProcessing, Tables, "
                          "and CoffeeShop destructor groups are accepted. The internal "
                          "reverse order of the Table array is still required.\n")
        for answer_index, answer_file in enumerate(answer_files, start=1):
            with open(answer_file, "r") as f:
                output_answer = f.read()
            answer_label = "output answer" if len(answer_files) == 1 else f"accepted output answer {answer_index}"
            write_str += (f"\n### problem-{prob_name}-case-{case_num} {answer_label}"
                          f"\n```\n{output_answer}\n```\n")
        
        output_diff_result_file = f"./outputs/{self.s_id}/{self.hw_name}_{prob_name}_case_{case_num}_{self.s_id}_output_diff.txt"
        write_str += f"\n### problem-{prob_name}-case-{case_num} output diff result\n"
        if os.path.isfile(output_diff_result_file):
            with open(output_diff_result_file, "r", errors="replace") as f: output_diff_result = f.read()
            write_str += f"\n```c++\n{output_diff_result}\n```\n"
        else:
            write_str += f"no problem-{prob_name}-case-{case_num} output diff result"

        return write_str

    
    def print_report(self):
        write_str_summary = f"# {self.s_id} {self.hw_name} scoring report - summary\n\n"
        write_str_submit_compile = f"{self.s_id} {self.hw_name} scoring report - submit_compile\n\n"
        write_str_output_diff = f"{self.s_id} {self.hw_name} scoring report - output_diff\n\n"

        if not self.is_submitted:
            write_str_summary += f"{self.s_id} did not submitted .zip file\n"
            write_str_submit_compile += f"{self.s_id} did not submitted .zip file\n"
            write_str_output_diff += f"{self.s_id} did not submitted .zip file\n"
        else:
            write_str_summary += self.__print_result()
            write_str_summary += self.__print_zip_ls()

            write_str_submit_compile += "\n## Submitted Source Code\n"
            for i, prob_name in enumerate(self.prob_names):
                write_str_submit_compile += self.__print_source_code(prob_name)
            
            write_str_submit_compile += "\n## Compiled code & compiled result\n" 
            for i, prob_name in enumerate(self.prob_names):
                for j in range(self.case_nums[i]):
                    write_str_submit_compile += self.__print_compile_code(prob_name, j+1)
                    write_str_submit_compile += self.__print_compile_result(prob_name, j+1)

            write_str_output_diff += "\n## Output result & diff result\n"
            for i, prob_name in enumerate(self.prob_names):
                for j in range(self.case_nums[i]):
                    write_str_output_diff += self.__print_output_result(prob_name, j+1)
                    write_str_output_diff += self.__print_output_diff_result(prob_name, j+1)

        self.summary_f.write(write_str_summary)
        self.submit_compile_f.write(write_str_submit_compile)
        self.output_diff_f.write(write_str_output_diff)
