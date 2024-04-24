import copy
import hashlib
import os
import datetime
import re
import shutil
import time
import traceback


class fuck_hack:

    def __init__(self,
                 directory: str,
                 is_delete=False,
                 exclude_dir=[],
                 reg_file='',
                 del_dir=True,
                 sleep=1,
                 log_name='hack_log.txt'):
        """

        :param directory: 检测路径
        :param is_delete: 是否删除新增文件或文件夹
        :param exclude_dir: 不检测的路径（以检测路径为基准）
        :param reg_file: 正则匹配删除文件，如为空则删除所有新增文件，如.*\.php则删除.php结尾文件
        :param del_dir: 是否删除目录
        :param sleep: 检测间隔
        :param log_name: 日志文件名称
        """

        self.__directory = os.path.realpath(directory)
        self.__files_dict_md5 = {}
        self.__files_path_dict = {}
        self.__root_file_directory = os.path.dirname(os.path.abspath(__file__))
        self.__log_name = os.path.realpath(log_name)
        self.__is_delete = is_delete
        self.__reg_file = reg_file
        self.__del_dir = del_dir
        self.__exclude_dir = []
        for d in exclude_dir:
            self.__exclude_dir.append(os.path.realpath(os.path.join(self.__directory, d)))

        scan_result = self.__get_all_files_with_path()
        self.__files_dict_md5 = scan_result['files_dict_md5']
        self.__files_path_dict = scan_result['files_path_dict']
        self.__get_files_md5()

        self.formatting_print('扫描完成')

        while True:
            self.__monitor_control()
            time.sleep(sleep)

    def __get_all_files_with_path(self) -> dict:

        files_dict_md5 = {}
        files_path_dict = {}

        # 遍历目录和子目录
        for root, dirs, files in os.walk(self.__directory):
            if root in self.__exclude_dir:
                continue

            # 遍历每个文件
            for file in files:
                # 获取文件路径
                file_path = os.path.join(root, file)
                if file_path == self.__log_name:
                    continue
                # 将文件路径作为键值添加到字典中
                files_dict_md5[file_path] = None

            files_path_dict.update({
                root: {
                    'dirs': dirs,
                    'files': files
                }
            })

        return {'files_dict_md5': files_dict_md5, 'files_path_dict': files_path_dict}

    def __get_files_md5(self):
        for file_path in self.__files_dict_md5:
            with open(file_path, 'rb') as f:
                file_content = f.read()
                md5_hash = hashlib.md5(file_content).hexdigest()

            self.__files_dict_md5[file_path] = md5_hash

    @staticmethod
    def get_file_md5(file_path: str):
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
                md5_hash = hashlib.md5(file_content).hexdigest()

            return md5_hash
        except FileNotFoundError:
            return None

    def __compare_lists(self, root, list1: list, list2: list, level=1) -> dict:
        action = {
            1: '新增',
            2: '删除'
        }

        set1 = set(list1)
        set2 = set(list2)

        # set1 - set2  # 在list1中，但不在list2中的元素
        # set2 - set1  # 在list2中，但不在list1中的元素

        difference = {1: list(set1 - set2), 2: list(set2 - set1)}

        for i in range(1, 3):
            if difference[i]:
                for _dir in difference[i]:
                    self.formatting_print(f' {action[i]} 文件: {os.path.join(root, _dir)}', level=level)

        return difference

    def __monitor_control(self):
        result_scan = self.__get_all_files_with_path()

        self.__monitor_add_or_remove_file_or_path(result_scan['files_path_dict'])

        self.__monitor_update_file(result_scan['files_dict_md5'])

        if not self.__is_delete:
            self.__files_path_dict = result_scan['files_path_dict']
        self.__files_dict_md5 = result_scan['files_dict_md5']

    def __monitor_add_or_remove_file_or_path(self, files_path_dict: dict):

        copy_files_path_dict = copy.deepcopy(self.__files_path_dict)
        for path_dict in files_path_dict:
            add_files = []
            add_dirs = []

            if path_dict in copy_files_path_dict:
                if set(files_path_dict[path_dict]['files']) != set(
                        copy_files_path_dict[path_dict]['files']):
                    difference_dir = self.__compare_lists(path_dict,
                                                          files_path_dict[path_dict]['files'],
                                                          copy_files_path_dict[path_dict]['files'],
                                                          level=3)
                    if self.__is_delete:
                        self.__del_file_or_dir(path_dict, difference_dir[1], '文件', False)

                copy_files_path_dict.pop(path_dict)

            else:

                self.formatting_print(f' 新增 目录: {path_dict}', level=2)
                add_dirs.append(path_dict)
                for add_file in files_path_dict[path_dict]['files']:
                    self.formatting_print(f' 新增 文件: {os.path.join(path_dict, add_file)}', level=3)
                    add_files.append(add_file)

            if self.__is_delete:
                self.__del_file_or_dir(path_dict, add_files, '文件', False)
                self.__del_file_or_dir(path_dict, add_dirs, '目录', True)

        if copy_files_path_dict:
            for old_path_dict in copy_files_path_dict:
                self.formatting_print(f' 删除 目录: {old_path_dict}', level=2)
                for del_file in copy_files_path_dict[old_path_dict]['files']:
                    self.formatting_print(f' 删除 文件: {os.path.join(old_path_dict, del_file)}', level=3)

    def __del_file_or_dir(self, root: str, diff: list, string: str, is_dir: bool):
        for del_diff in diff:
            try:
                if is_dir and self.__del_dir:
                    if os.path.isdir(del_diff):
                        del_diff_path = del_diff
                        shutil.rmtree(del_diff_path)
                        self.formatting_print(f' {string} {del_diff_path} 删除成功', level=1)
                else:
                    del_diff_path = os.path.join(root, del_diff)
                    if not self.__reg_file:
                        if os.path.isfile(del_diff_path) and os.path.exists(del_diff_path):
                            os.remove(del_diff_path)
                            self.formatting_print(f' {string} {del_diff_path} 删除成功', level=1)
                    else:
                        try:
                            if re.match(self.__reg_file, del_diff):
                                if os.path.isfile(del_diff_path) and os.path.exists(del_diff_path):
                                    os.remove(del_diff_path)
                                    self.formatting_print(f' {string} {del_diff_path} 删除成功', level=1)
                        except:
                            traceback.print_exc()
                            self.formatting_print(f' 删除失败 正则表达式有误！ ', level=2)

            except:
                traceback.print_exc()
                self.formatting_print(f' {string} {del_diff_path} 删除失败', level=2)

    def __monitor_update_file(self, files_dict_md5: dict):
        for file_path in files_dict_md5:
            files_dict_md5[file_path] = self.get_file_md5(file_path)
            if file_path in self.__files_dict_md5:
                if files_dict_md5[file_path] != self.__files_dict_md5[file_path]:
                    self.formatting_print(f' {file_path} 文件被修改'
                                          f'MD5: {self.__files_dict_md5[file_path]} -> {files_dict_md5[file_path]}',
                                          level=3)

    def formatting_print(self, string: str, level=1):
        level_dict = {
            1: 'info',
            2: 'warning',
            3: 'risk'
        }
        color_dict = {
            1: '\033[32m',
            2: '\033[33m',
            3: '\033[31m'
        }
        result = ''

        # 获取当前时间
        now = datetime.datetime.now()

        # 打印
        result += str(now)
        result += ' - '
        result += level_dict.get(level, 1)
        result += ' - :'
        result += string
        print(color_dict[level] +
              result
              + "\033[0m")
        with open(self.__log_name, 'a', encoding='utf-8') as f:
            f.write(result)
            f.write('\n')


# 获取当前目录的路径
current_directory = os.getcwd()
f = fuck_hack('./ttest', is_delete=True, del_dir=True, exclude_dir=[])
