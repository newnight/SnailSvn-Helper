# coding=utf8

import sublime,sublime_plugin,subprocess, platform,os

class SnailSvnCommand(sublime_plugin.WindowCommand):
    __path=''
    __svncmd ='snailsvn' if os.path.exists('/Applications/SnailSVN.app') else ('snailsvnfree' if os.path.exists('/Applications/SnailSVNLite.app') else '')
    __simple_actions=["checkout","cleanup","commit","blame","export","import","log","merge","relocate","revert","switch","update","add-working-copy"]
    __complex_actions=["add","delete","info","ignore","lock","unlock"]

    def get_path(self, paths):
        try:
            return paths[0]
        except IndexError:
            return self.window.active_view().file_name()

    def set_path(self,paths,is_folder=False):
        if is_folder:
            self.__path=os.path.dirname(self.get_path(paths))
        else:
            self.__path=self.get_path(paths)

    def runSnailCmd(self,action,paths):
        self.set_path(paths)
        if action in self.__simple_actions or action in self.__complex_actions:
            import subprocess
            cmd = self.__svncmd+'://svn-'+action+self.__path
            print(cmd)
            subprocess.Popen(['open',cmd])

    def has_install_snail(self):
        return (self.__svncmd in ["snailsvnfree","snailsvn"]) 
    
    def is_visible(self,paths=[]):
        return self.has_install_snail() and sublime.platform() == "osx"

class SnailsvnHelperCommand(SnailSvnCommand):
    def run(self,action,paths=[]):
        self.runSnailCmd(action,paths)

    def is_visible(self, paths=[]):
        return super().is_visible(paths) and os.path.isfile(self.get_path(paths)) 
    
    def is_enabled(self, paths=[]):
        return os.path.isfile(self.get_path(paths))

class SnailSvnFolderCommand(SnailSvnCommand):
    def set_path(self, paths=[]):
        super().set_path(paths,is_folder=True);

class SnailsvnFolderHelperCommand(SnailSvnFolderCommand):
    def run(self,action,paths=[]):
        self.runSnailCmd(action,paths)



