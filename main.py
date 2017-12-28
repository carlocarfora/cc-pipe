import sys
import os
import yaml
import shutil
import subprocess
from PyQt5.QtCore import QUrl
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (QApplication, QWidget, QFileSystemModel, 
    QMessageBox, QVBoxLayout)
from PyQt5.QtWebEngineWidgets import QWebEngineView

class CcPipeMainWindow(QWidget):
    def __init__(self):
        super(CcPipeMainWindow, self).__init__()

        # Init variables
        self.repo_path = None
        self.version = None

        # Init UI
        self.init_ui()

        # Init methods
        self.load_settings('data/settings.yml')
        self.list_projects(self.repo_path)
        self.set_ui_text(self.version)

    def init_ui(self):

        # Load Ui
        self.ui = loadUi('ui/MainWindow.ui')
        self.ui.show()

        # Set up UI connections
        self.ui.NewProjBtn.clicked.connect(self.open_new_project)
        self.ui.NewShotBtn.clicked.connect(self.open_new_shot)
        self.ui.NewTaskBtn.clicked.connect(self.open_new_task)
        self.ui.DeleteShotTaskBtn.clicked.connect(self.delete_shot_task)
        self.ui.SettingsBtn.clicked.connect(self.open_settings)
        self.ui.HelpBtn.clicked.connect(self.open_help)
        self.ui.HouBtn.clicked.connect(self.open_hou)
        self.ui.NukBtn.clicked.connect(self.open_nuk)

        self.ui.ProjectView.clicked.connect(lambda: self.load_proj_info(
            self.ui.ProjectView.currentItem().text()))
        self.ui.ProjectView.clicked.connect(lambda: self.populate_shot_view(
            self.ui.ProjectView.currentItem().text()))
        self.ui.ProjectView.itemDoubleClicked.connect(lambda: self.browse_proj(
            self.ui.ProjectView.currentItem().text()))
        self.ui.DeleteProjBtn.clicked.connect(lambda: self.delete_proj(
            self.ui.ProjectView.currentItem().text()))

    def open_new_project(self):
        self.window = CcPipeNewProject()
        self.window.init_ui()

    def open_new_shot(self):
        self.window = CcPipeNewShot()
        self.window.init_ui()

    def open_new_task(self):
        if len(self.ui.ShotTaskView.selectedIndexes()) == 0:
            print('Select a shot first!')
        else:
            self.window = CcPipeNewTask()
            self.window.init_ui()

    def open_settings(self):
        settings = 'data/settings.yml'

        try:
            os.system('xdg-open ' + settings)
        except:
            print('Could not open settings file in text editor')

    def open_help(self):
        self.window = CcPipeHelp()
        self.window.init_ui()

    def open_hou(self):
        try:
            index = self.ui.ShotTaskView.selectedIndexes()[0]
            current_path = self.model.filePath(index)
            subprocess.Popen(['shou'], cwd=current_path, shell=True)
        except:
            print('You must launch software from a task')        

    def open_nuk(self):
        try:
            index = self.ui.ShotTaskView.selectedIndexes()[0]
            current_path = self.model.filePath(index)
            subprocess.Popen(['optirun nuke'], cwd=current_path, shell=True)
        except:
            print('You must launch software from a task')

    def load_settings(self, filePath):
        """ opens settings.yml and loads values into class variables """
        
        with open(filePath, 'r') as file:
            data = yaml.load(file)

        settings = data.get('settings')
        self.repo_path = settings['repo']
        self.version = settings['version']

    def set_ui_text(self, ver):
        self.ui.VersionLbl.setText('cc-pipe version ' + str(ver))
        self.ui.RepoLocationLbl.setText(self.repo_path)

    def list_projects(self, rootDir):
        sortedDir = sorted(os.listdir(rootDir))
        for item in sortedDir:
            self.ui.ProjectView.addItem(item)

    def load_proj_info(self, projName):
        filepath = 'data/projects/' + projName + '.yml'

        # load yaml file
        with open(filepath, 'r') as file:
            data = yaml.load(file)

        # update ui labels
        proj_ui = 'Project: ' + data['projectname']
        res_ui = 'Resolution: ' + data['width'] + 'x' + data['height']
        fps_ui = 'FPS: ' + data['fps']

        self.ui.ProjNameLbl.setText(proj_ui)
        self.ui.ResLbl.setText(res_ui)
        self.ui.FPSLbl.setText(fps_ui)

    def browse_proj(self, projName):
        proj_path = os.path.join(self.repo_path, projName)

        try:
            subprocess.Popen((['xdg-open', proj_path]))
        except:
            os.startfile(projName)

    def delete_proj(self, projName):
        try:
            proj_path = os.path.join(self.repo_path, projName)
            yaml_path = 'data/projects'
            
            delete_msg = 'Delete ' + projName + '? This cannot be undone!'
            reply = QMessageBox.question(self, 'Message', 
                     delete_msg, QMessageBox.Yes | QMessageBox.No, 
                     QMessageBox.No)

            if reply == QMessageBox.Yes:
                try:
                    if os.path.exists(proj_path):
                        yaml_file = (os.path.join(yaml_path, projName) + '.yml')
                        print('Deleted project folder ' + proj_path)
                        print('Deleted' + yaml_file)                     
                        shutil.rmtree(
                            proj_path, ignore_errors=False, onerror=None)
                        os.remove(yaml_file)
                        self.ui.ProjectView.clear()   
                        self.list_projects(self.repo_path)
                    else:
                        print('Project does not exist!')
                except:
                    print("Unable to delete selected")
            else: 
                print('Delete project cancelled')
        except:
            print("Error, need to select a folder to delete!") 

    def populate_shot_view(self, projName):
        """ Create and attach a QFileSystemModel() to the tree view """

        proj_path = os.path.join(self.repo_path, projName)

        self.model = QFileSystemModel()
        self.model.setRootPath(self.repo_path)

        self.view = self.ui.ShotTaskView
        self.view.setModel(self.model)
        self.view.setRootIndex(self.model.index(proj_path))
        self.view.header().hide()
        self.view.hideColumn(1)
        self.view.hideColumn(2)
        self.view.hideColumn(3)

    def delete_shot_task(self):
        try:
            index = self.ui.ShotTaskView.selectedIndexes()[0]
            item = self.model.filePath(index)
            tail = os.path.split(item)

            delete_msg = 'Delete ' + tail[1] + '?'

            reply = QMessageBox.question(self, 'Message', 
                     delete_msg, QMessageBox.Yes | QMessageBox.No, 
                     QMessageBox.No)

            if reply == QMessageBox.Yes:
                try:
                    print('Deleted ' + tail[1])
                    shutil.rmtree(item, ignore_errors=False, onerror=None)
                except:
                    print("Could not delete selected")
            else:
                print('Not deleting')
        except:
            print("Error, need to select a folder to delete!")


class CcPipeNewProject(QWidget):
    def __init__(self):
        super(CcPipeNewProject, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.ui = loadUi('ui/NewProject.ui')
        self.ui.show()

        self.ui.NewProjectBtn.clicked.connect(self.create_project)

    def create_project(self):
        """ Writes a project settings yaml file and creates a project folder """
        
        d = dict()
        d['projectname'] = self.ui.NameEdit.text()
        d['width'] = self.ui.WidthEdit.text()
        d['height'] = self.ui.HeightEdit.text()
        d['fps'] = self.ui.FPSEdit.text()

        values = all([value for key, value in d.items() if value ==''])

        if not values:
            print('One or more fields are blank')
        else:
            # save yaml file to data/projects
            file_path = 'data/projects/'
            file_name = file_path + d['projectname'] + '.yml'

            with open(file_name,'w') as f:
                f.write(yaml.dump(d, default_flow_style=False))

            # create folder in projects repo
            proj = os.path.join(
                CcPipeMainWindow.repo_path, d['projectname'])
            if not os.path.exists(proj):
                os.mkdir(proj)
                CcPipeMainWindow.ui.ProjectView.clear()
                CcPipeMainWindow.list_projects(CcPipeMainWindow.repo_path)
            else:
                print('Project already exists!')


class CcPipeNewShot(QWidget):
    def __init__(self):
        super(CcPipeNewShot, self).__init__()

        self.project = CcPipeMainWindow.ui.ProjectView.currentItem().text()
        self.init_ui()

    def init_ui(self):
        self.ui = loadUi('ui/NewShot.ui')
        self.ui.show()

        self.ui.ProjNameLbl.setText(self.project)        
        self.ui.NewShotBtn.clicked.connect(self.create_shot)

    def create_shot(self):
        if self.ui.ShotNameEdit.text() == '':
            print('Shot name empty!')
        else:
            path_head = os.path.join(CcPipeMainWindow.repo_path, self.project)
            path_tail = self.ui.ShotNameEdit.text()
            path = os.path.join(path_head, path_tail)

            if not os.path.exists(path):
                os.mkdir(path)
                print('Shot created in ' + path)
            else:
                print('Shot already exists!')


class CcPipeNewTask(QWidget):
    def __init__(self):
        super(CcPipeNewTask, self).__init__()

        self.project = CcPipeMainWindow.ui.ProjectView.currentItem().text()
        self.index = CcPipeMainWindow.ui.ShotTaskView.selectedIndexes()[0]
        self.item = CcPipeMainWindow.model.filePath(self.index)

        self.init_ui()

    def init_ui(self):
        self.ui = loadUi('ui/NewTask.ui')
        self.ui.show()

        self.proj_shot_path = self.split_path(self.item)
        self.ui.ProjShotDirLbl.setText(self.proj_shot_path) 
       
        self.ui.NewTaskBtn.clicked.connect(lambda:self.create_task(
            self.ui.TaskNameEdit.text(),
            self.ui.TaskSoftwareCmb.currentText()))
        self.ui.TaskSoftwareCmb.currentIndexChanged.connect(lambda:
            self.check_text(self.ui.TaskSoftwareCmb.currentText()))
        self.ui.OtherSoftwareEdit.setEnabled(0)

    def split_path(self, path):

        shot = os.path.split(path)
        proj = os.path.split(shot[0])
        repo = CcPipeMainWindow.repo_path
        concat = os.path.join(proj[1], shot[1])
        concat_path = os.path.join(repo, concat)    
        
        return concat_path

    def check_text(self, text):
        if text == 'Other':
            self.ui.OtherSoftwareEdit.setEnabled(1)
        else:
            self.ui.OtherSoftwareEdit.setEnabled(0)

    def create_task(self, name, software):
        """ Creates directories for task and software """

        other_software = self.ui.OtherSoftwareEdit.text()

        hou_dirs = ['abc',
                    'audio',
                    'comp',
                    'desk',
                    'flip',
                    'geo',
                    'hda',
                    'hip',
                    'render',
                    'scripts',
                    'sim',
                    'tex',
                    'video']

        nuk_dirs = ['comp',
                    'scripts',
                    'elements',
                    'ref']

        make_dirs = {'hou': hou_dirs, 
                     'nuk': nuk_dirs,}

        software_path = os.path.join(self.proj_shot_path, software.lower())

        if name == '':
            print('Task Name is empty!')
        else:
            if software == 'Houdini':
                task_path = os.path.join(software_path, name)
                if not os.path.exists(task_path):
                    for path in hou_dirs:
                        os.makedirs(os.path.join(task_path, path))
                else:
                    print('Task already exists!')
            elif software == 'Nuke':
                task_path = os.path.join(software_path, name)
                if not os.path.exists(task_path):                       
                    for path in nuk_dirs:
                        os.makedirs(os.path.join(task_path, path))
                else:
                    print('Task already exists!')
            else:
                if other_software == '':
                    print('Other Software is empty!')
                else:
                    other_path = os.path.join(self.proj_shot_path, 
                        other_software.lower())
                    task_path = os.path.join(other_path, name)
                    if not os.path.exists(task_path):
                        os.makedirs(task_path)
                    else:
                        print('Task already exists!')


class CcPipeHelp(QWidget):
    def __init__(self):
        super(CcPipeHelp, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.wv = QWebEngineView()
        abs_path = os.path.abspath("help/help.html")
        local_url = QUrl.fromLocalFile(abs_path)
        print(abs_path)
        self.wv.load(local_url)
        self.wv.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    CcPipeMainWindow = CcPipeMainWindow()
    sys.exit(app.exec_())