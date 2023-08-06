import os
import glob


class Autodesk3dsmax(object):

    def __init__(self):
        super(Autodesk3dsmax, self).__init__()

        self.exe_filename = None
        self.max_root = None
        self.version = None
        self.version_str = None
        self.icon = None
        self.bit = None

        self.startup_script_path = None
        self.local_startup_script_path = None

    def __repr__(self):
        return '[{}_{}]'.format(self.version_str, self.bit)

    def mxs_base64(self, code):
        import base64
        base_64_data = base64.b64encode(code.encode('gbk')).decode('utf-8')
        data = '''
base64data = "{}"
dotnet_encoding = dotnetclass "System.Text.Encoding"
ascii_object = dotnet_encoding.ASCII
dotnet_convert = dotnetclass "Convert"
bytes_data = dotnet_convert.FromBase64String(base64data)
real_data = ascii_object.Default.GetString(bytes_data);
execute(real_data);
        '''.format(base_64_data)
        data = data
        return data

    def filein_script_code(self, script_filename):
        """
        生成filein脚本的mxs代码
        :param script_filename:
        """
        code = 'try(filein @"{}";)catch(print ("error_filein:"+@"{}"))'.format(script_filename, script_filename)
        code = 'try(if (maxversion())[1] >= 21000 then(filein @"{}";)else({});)catch(print "error_kjk")'.format(
            script_filename,
            self.mxs_base64(code))
        return code

    def ready_data_from_finder(self, data):
        self.exe_filename = data['path']
        self.version = data['version']
        self.version_str = data['version_string']
        self.icon = data['icon']
        self.bit = data['bit']

        self.max_root = os.path.dirname(self.exe_filename)

        self.startup_script_path = os.path.join(self.max_root, 'scripts\Startup')
        self.local_startup_script_path = data['local_path']

    def install_startup_script(self, filename, data):
        """
        安装启动脚本
        :param data:
        """

        lang_lst = glob.glob(self.local_startup_script_path + "\\*\\scripts\\startup")

        is_sucess = False

        for lang_folder in lang_lst:
            full_script_filename = os.path.join(lang_folder, filename)

            try:
                with open(full_script_filename, 'wb') as f:
                    f.write(data.encode())
                    is_sucess = True
            except:
                pass

        if not is_sucess:
            # 尝试安装到主目录
            full_script_filename = os.path.join(self.startup_script_path, filename)

            try:
                with open(full_script_filename, 'wb') as f:
                    f.write(data.encode())
                    return True
            except:
                pass

        return True

    def uninstall_startup_script(self, filename):
        """
        卸载启动脚本
        """

        lang_lst = glob.glob(self.local_startup_script_path + "\\*\\scripts\\startup")

        for lang_folder in lang_lst:
            full_script_filename = os.path.join(lang_folder, filename)
            if os.path.exists(full_script_filename):
                os.remove(full_script_filename)

        full_script_filename = os.path.join(self.startup_script_path, filename)
        if os.path.exists(full_script_filename):
            os.remove(full_script_filename)

    def is_install_startup_script(self, filename, code=None):
        """
        是否安装过启动脚本
        data = 脚本内容
        :rtype: object
        """

        lang_lst = glob.glob(self.local_startup_script_path + "\\*\\scripts\\startup")

        is_installed = False

        for lang_folder in lang_lst:
            full_script_filename = os.path.join(lang_folder, filename)

            if os.path.exists(full_script_filename):
                with open(full_script_filename, 'rb') as f:
                    old_code = f.read()
                    if old_code == code.encode():
                        is_installed = True

        if is_installed == False:
            full_script_filename = os.path.join(self.startup_script_path, filename)

            if os.path.exists(full_script_filename):
                with open(full_script_filename, 'rb') as f:
                    old_code = f.read()
                    if old_code == code.encode():
                        is_installed = True

        return is_installed


if __name__ == '__main__':
    data = {'bit': '64',
            'local_path': r'C:\Users\Administrator\AppData\Local\Autodesk\3dsMax\2012 - 64bit',
            'icon': {'large': 'C:\\Program Files\\Autodesk\\3ds Max '
                              '2014\\UI_ln/Icons/ATS/ATSScene.ico',
                     'small': 'C:\\Program Files\\Autodesk\\3ds Max '
                              '2014\\UI_ln/Icons/ATS/ATSScene.ico'},
            'path': 'C:\\Program Files\\Autodesk\\3ds Max 2014\\3dsmax.exe',
            'version': 1604200000,
            'version_string': '3dsmax 2014'}

    a = Autodesk3dsmax()
    a.ready_data_from_finder(data)

    file_in_code = a.filein_script_code(r"E:\XDL_MANAGER3\plug-ins\3dsmax\xdl_init.ms")
    file_in_name = 'kjj_init_test.ms'

    print(file_in_code)

    # print(a.is_install_startup_script(file_in_name, file_in_code))
    print(a.install_startup_script(file_in_name, file_in_code))
