'''
--------------------------------------------------------------------------
Copyright (C) 2016 Lukasz Laba <lukaszlab@o2.pl>


This file is part of SeePy.
SeePy is a python script visualisation tool.
http://seepy.org/

SeePy is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

SeePy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SeePy; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
'''

import os
import re
import shutil

from PyQt4 import QtGui

class Code ():
    
    def __init__(self):
        #---
        self.script_path = ''
        self.savedir = os.path.dirname(__file__)
        #---
        self.code_oryginal = ''
        self.code_parsed = ''
        #---
        self.stamptext = ''
        #--
        self.saveLock = False
        #--

    def parse(self):
        script = self.code_oryginal
        #-------------------------------------------------------------------------
        #Here the code_oryginal is changed in to code_parsed with re.sub() replace
        #-------------------------------------------------------------------------
        
        script = re.sub(r'\r\n', r'\n', script) #new line \n (Linux) vs \r\n (windows) problem
        
        #--Variable with one line comment syntax (indentation acceptable)
        script = re.sub(    r'([ \t]*)(\w+)(.+)#!(.*)',
                            r"\1\2\3 \n\1r_comment('''```\2 = %(\2)s``` \4''' % vars_formated())",
                            script  )
                            
        #--Result EQUation  with one line comment syntax, version /a = d + 4 = 5/ (indentation acceptable)
        script = re.sub(    r'([ \t]*)(\w+)\s*=\s*(.+)#%requ(.*)',
                            r"\1\2 = \3 \n\1r_mathcomment('''```\2 = \3 = %(\2)s``` \4''' % vars_formated())",
                            script  )
                            
                            
        #--EQUation with one line comment syntax, version /a = d + 4/ (indentation acceptable)
        script = re.sub(    r'([ \t]*)(\w+)\s*=\s*(.+)#%equ(.*)',
                            r"\1\2 = \3 \n\1r_mathcomment('''```\2 = \3``` \4''' % vars_formated())",
                            script  )
                            
        #--Result EQUation with one line comment syntax, version /d + 4 = 5/ (indentation acceptable)
        script = re.sub(    r'([ \t]*)(\S[^=\^\n]+)#%requ(.*)',
                            r"\1\2 \n\1r_tmp =  \2 \n\1r_mathcomment('''```\2 = %(r_tmp)s``` \3'''.format(\2) % vars_formated()) \n\1r_tmp =  None",
                            script  )
                            
        #--EQUation with one line comment syntax, version /d + 4/  (indentation acceptable)
        script = re.sub(    r'([ \t]*)(\S[^=\^\n]+)#%equ(.*)',
                            r"\1\2 \n\1r_mathcomment('''```\2``` \3''' % vars_formated())",
                            script  )
                            
        #--One line comment syntax (indentation acceptable)
        script = re.sub(    r'#![ ]*(.+)',
                            r"r_comment('''\1''' % vars_formated())",
                            script  )
        #--Multi line comment syntax (indentation not acceptable)
        script = re.sub(    r"#!(.{1})'''(.+?)'''",
                            r"r_comment('''\2''' % vars_formated())", 
                            script, flags=re.DOTALL )
        #--One line python code showing syntax (indentation not acceptable)
        script = re.sub(    r"(.+)#%code",
                            r"\1\nr_comment('''```\1```''' )",
                            script  )
        #--Multi line python code showing syntax (indentation not acceptable)
        script = re.sub(    r"#%code(.+?)#%", 
                            r"\1r_comment('''```\1```''' )",
                            script, flags=re.DOTALL )
        #--Image showing syntax (indentation acceptable)
        script = re.sub(    r'#%img (.+)',
                            r"r_img('\1')", 
                            script  )
        #--Matplotlib plt figure syntax (indentation acceptable)
        script = re.sub(    r'([ \t]*)(\w+)(.+)#%plt',
                            r"\1\2\3 \n\1r_plt(\2)",
                            script)
        #--Pillow Image syntax (indentation acceptable)
        script = re.sub(    r'([ \t]*)(\w+)(.+)#%pil',
                            r"\1\2\3 \n\1r_pil(\2)",
                            script)
        #--One line LaTex syntax comment rendering (indentation acceptable)
        script = re.sub(    r'#%tex[ ]*(.+)',
                            r"r_tex(r'\1' % vars())", 
                            script  )
        #--Rendering LaTex syntax from python string (indentation acceptable)
        script = re.sub(    r'([ \t]*)(\w+)\s*#%stringtex',
                            r"\1\2 \n\1r_tex(\2)",
                            script)
        #--One line code rendering as LaTex syntax (indentation acceptable)
        script = re.sub(    r'([ \t]*)(\w[^\n]+)#%tex',
                            r"\1\2 \n\1r_codetex(r'\2' % vars_formated())",
                            script  )
        #--Rendering SVG syntax from python string (indentation acceptable)
        script = re.sub(    r'([ \t]*)(\w+)(.+)#%svg',
                            r"\1\2\3 \n\1r_svg(\2)",
                            script)
        #--Adjustable wariable with one line comment syntax (indentation not tested yet)
        script = re.sub(r'#(<{2,})', r"#\1_idx_", script)
        no = 1  
        while re.search(r"#<{2,}_idx_", script):
            script = script.replace(r'<_idx_', r"<_id%s_" % no, 1)
            no += 1
        script = re.sub(    r'([ \t]*)(\w+)(.+)#<<_(id\d+)_(.+)', 
                            r"\1\2\3 \n\1r_adj('''```\2 = %(\2)s```''' % vars_formated(),'\4','\5' % vars_formated(), 1, '''\2\3''')",
                            script  )
        script = re.sub(    r'([ \t]*)(\w+)(.+)#<<<_(id\d+)_(.+)', 
                            r"\1\2\3 \n\1r_adj('%(\2)s' % vars_formated(),'\4','\5' % vars_formated(), 1, '''\2\3''')",
                            script  )
        script = re.sub(    r'([ \t]*)(\w+)(.+)#<<<<_(id\d+)_(.+)', 
                            r"\1\2\3 \n\1r_adj('%(\2)s' % vars_formated(),'\4','\5' % vars_formated(), 2,  '''\2\3''')",
                            script  )
                            
        #--calling variable with val_name and var_name
        script = re.sub(r'val_(\w+)', r''' ```%(\1)s``` ''', script)
        script = re.sub(r'var_(\w+)', r''' ```\1 = %(\1)s``` ''', script)

        
        #--report end stamp
        script += "\nr_comment('>>*----- %s -----*')"%self.stamptext
        
        #--saving
        self.code_parsed = script 

    def getTimerParameters(self):
        is_active = False
        timespace = None
        #---
        script = self.code_oryginal
        timer = re.search(r"#%timer[ ]*(\d*)[ ]*ON", script)
        if timer:
            is_active = True
            timespace  = float(timer.group(1)) / 1000
            return is_active, timespace
        timer = re.search(r"#%timer[ ]*(\d*)[ ]*OFF", script)
        if timer:
            is_active = False
            timespace  = float(timer.group(1)) / 1000
            return is_active, timespace
        return None


    def editCode(self, lineID = 'id1', setvalues = None, index = None):
        if setvalues == 'None':
            setvalues = None
        #---
        script = self.code_oryginal
        #---
        script = re.sub(r'#(<{2,})', r"#\1_idx_", script)
        no = 1  
        while re.search(r"#<{2,}_idx_", script):
            script = script.replace(r'<_idx_', r"<_id%s_" % no, 1)
            no += 1 
        #---OPTION 1 Selectind one form list if list
        if setvalues :
            setvalues = re.search(r'[[](.+)[]]', setvalues).group(1)
            setvalues = setvalues.replace(" ", "")
            setvalues = setvalues.replace("'", "")
            setvalues = setvalues.split(',')
            #---
            expresion = re.search(r'(\w+)\s*=\s*(\w+)\s*[[](\d+)[]]\s*#<{2,}_%s_'%lineID, script)
            variable = expresion.group(1)
            listindex = int(expresion.group(3))
            #---asking for new value from choice list
            value_selected = QtGui.QInputDialog.getItem(None, 'Set new value', variable +'=', setvalues, listindex, False)[0]
            #---
            if value_selected:
                index_selected = setvalues.index(value_selected)
            else:
                index_selected = listindex
            #---
            script = re.sub(    r'(\w+)\s*=\s*(.+)[[]\w+[]]\s*#(<{2,})_%s_'%lineID,
                                r'\1 = \2[%s] #\3_%s_'%(index_selected, lineID),
                                script  )
        #---OPTION 2 Geting new variable value   
        else:
            expresion = re.search(r'(\w+)\s*=\s*(.+)\s*#<{2,}_%s_'%lineID, script)
            variable = expresion.group(1)
            oldvalue = expresion.group(2)
            #---asking for new value
            if ('filepath' in variable): # if variable look like filepath
                directory = '/'
                try:
                    if os.path.isdir(os.path.dirname(eval(oldvalue))):
                        directory = os.path.dirname(eval(oldvalue))
                except:
                    pass
                askmsg = "Select new filepath for '%s' variable" %variable
                filename = QtGui.QFileDialog.getOpenFileName(caption=askmsg, directory=directory)
                if filename == '':
                    newvalue = oldvalue
                else:
                    newvalue = "'%s'"%str(filename)
            elif ('dirpath' in variable): # if variable look like dirpath
                directory = '/'
                try:
                    if os.path.isdir(eval(oldvalue)):
                        directory = os.path.dirname(eval(oldvalue))
                except:
                    pass
                dirname = QtGui.QFileDialog.getExistingDirectory(caption = 'Select directory', directory = directory)
                if dirname == '':
                    newvalue = oldvalue
                else:                
                    newvalue = "'%s'"%str(dirname)
            elif (oldvalue.strip() in ['True', 'False']): # if variable has bool value
                bool_oldvalue = eval(oldvalue)
                newvalue = str(not(bool_oldvalue))
            else: # other cases
                newvalue = QtGui.QInputDialog.getText(None, 'Set new value',variable +'=', QtGui.QLineEdit.Normal,oldvalue)[0]
                newvalue = str(newvalue)
            #---
            script = re.sub(    r'(\w+)\s*=\s*(.+)\s*#(<{2,})_%s_'%lineID,
                                r'\1 = %s #\3_%s_'%(newvalue, lineID),
                                script  )
        #---
        script = re.sub(r"#(<{2,})_id(\d+)_", r'#\1', script)
        #---
        self.code_oryginal = script

    def savecode(self):
        if self.saveLock:
            QtGui.QMessageBox.information(None, 'Info', 'File open read only. Use save as option')
            return False
        else:
            file = open(self.script_path, "r+")
            file.write(self.code_oryginal)
            file.close()
            return True

    def reloadcode(self):
        file = open(self.script_path, 'r')
        self.code_oryginal = file.read()    
        file.close()  

    def openFile(self, file_path=None, saveLock = False):
        #---asking for file path if not given
        if file_path:
            filename =  file_path
        else:
            filename = QtGui.QFileDialog.getOpenFileName(caption = 'Open script',
                                                    directory = self.savedir,
                                                    filter = "Python script (*.py)")
            filename = str(filename)
        #---
        if not filename == '':
            self.savedir = os.path.dirname(filename)
            self.script_path = filename
            file = open(self.script_path, 'r')
            self.code_oryginal = file.read()    
            file.close()      
            self.parse()
            self.saveLock = saveLock
        else:
            pass
            
    def newFile(self, template_path, info='Save as', initfilename='your_script', filedirectory = None):
        #---asking for file path
        if filedirectory == None:
            filename = QtGui.QFileDialog.getSaveFileName(caption = info,
                                                    directory = self.savedir + '/' + initfilename,
                                                    filter = "Python script (*.py)")
            filename = str(filename)
        else:
            filename = filedirectory + '/' + initfilename
        #---
        if not filename == '':
            new_template = open(template_path, 'r').read()
            self.savedir = os.path.dirname(filename)
            text_file = open(filename, "w")
            text_file.write(new_template)
            text_file.close()
            self.script_path = filename
            self.reloadcode()
            self.parse()
            self.saveLock = False

    def saveAs(self, savepath = None):
        newname = 'Copy_' + os.path.basename(self.script_path)
        #---asking for file path
        initdir = self.savedir + '/' + newname
        if self.saveLock:
            initdir = '/' + newname
        if savepath:
            filename = savepath
        else:
            filename = QtGui.QFileDialog.getSaveFileName(caption = 'Save as',
                                                        directory = initdir,
                                                        filter = "Python script (*.py)")
            filename = str(filename)
        #---
        new_file = open(filename, "w")
        new_file.write(self.code_oryginal)
        new_file.close()
        #---coping files linked inside code_oryginal
        src_dir = os.path.dirname(self.script_path)
        dst_dir = os.path.dirname(filename)
        copied_dependences = []
        for fname in os.listdir(src_dir):   
            if  fname in self.code_oryginal:
                scr_file = os.path.join(src_dir, fname)
                dst_file = os.path.join(dst_dir, fname)
                if not scr_file == dst_file:
                    if os.path.isfile(scr_file) and ('.' in scr_file):
                        shutil.copyfile(scr_file, dst_file)
                        copied_dependences.append(fname)
        #---
        self.script_path = filename
        self.savedir = os.path.dirname(filename)
        self.reloadcode()
        self.parse()
        self.saveLock = False
        #---info massage
        infotext = 'Saved to '+ filename + '\n'
        if not copied_dependences == []:
            infotext += 'Copied_dependences: \n' 
            for i in copied_dependences:
                infotext += str(i) + '\n' 
        QtGui.QMessageBox.information(None, 'Info', infotext)

# Test if main
if __name__ == '__main__':
    ScriptCode = Code()
    ScriptCode.openFile('/home/lukasz/Dropbox/PYAPPS_STRUCT/SOURCE_SEEPY/seepy/pycore/test.py')
    #ScriptCode.openFile()
    ScriptCode.parse()
    print ScriptCode.code_oryginal
    print '-----'
    print ScriptCode.code_parsed
    #print ScriptCode.savedir
    #ScriptCode.openFile()
    #ScriptCode.newFile()
    #ScriptCode.editCode()
    #ScriptCode.saveAs()