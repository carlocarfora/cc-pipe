import sys
import os
import yaml
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QWidget, QFileSystemModel


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
        self.ui.ProjectView.clicked.connect(lambda: self.load_proj_info(
            self.ui.ProjectView.currentItem().text()))
        self.ui.ProjectView.clicked.connect(lambda: self.populate_shot_view(
            self.ui.ProjectView.currentItem().text()))
        self.ui.BrowseProjBtn.clicked.connect(lambda: self.browse_proj(
            self.ui.ProjectView.currentItem().text()))


    def open_new_project(self):
        self.window = CcPipeNewProject()
        self.window.init_ui()

    def open_new_shot(self):
        self.window = CcPipeNewShot()
        self.window.init_ui()

    def open_new_task(self):
        self.window = CcPipeNewTask()
        self.window.init_ui()

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
            os.system('xdg-open ' + proj_path)
        except:
            os.startfile(projName)

    def populate_shot_view(self, projName):
        """ Create and attach a QFileSystemModel() to the tree view """

        proj_path = os.path.join(self.repo_path, projName)

        self.model = QFileSystemModel()
        self.model.setRootPath(self.repo_path)

        self.view = self.ui.ShotTaskView
        self.view.setModel(self.model)
        self.view.setRootIndex(self.model.index(proj_path))
        self.view.hideColumn(1)
        self.view.hideColumn(2)
        self.view.resizeColumnToContents(1)

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
        self.shot = None
        self.init_ui()

    def init_ui(self):
        self.ui = loadUi('ui/NewTask.ui')
        self.ui.show()

        self.ui.NewTaskBtn.clicked.connect(self.create_task)

    def create_task(self):
        pass
        # check if name is empty

        # check if software is other

        # if software is not other then make relevant folders

        # if software is other then ungrey field and check if empty

        # 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    CcPipeMainWindow = CcPipeMainWindow()
    sys.exit(app.exec_())
