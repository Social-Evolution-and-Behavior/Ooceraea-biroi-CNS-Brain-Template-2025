# setup a simple gui script to run warping using ANTs

## START OF CODE
# import the necessary packages
import sys
import os
import glob
from PyQt5 import QtWidgets, QtCore, QtGui

# check if there are no arguments or exactly 4 arguments other than the script name
if len(sys.argv) == 7:
    _output_directory = sys.argv[1] 
    _target_file = sys.argv[2] if sys.argv[2] != "MISSING" else ""
    _warp_file = sys.argv[3] if sys.argv[3] != "MISSING" else ""
    _affine_file = sys.argv[4] if sys.argv[4] != "MISSING" else ""
    _was_flipped = True if sys.argv[5] == "flipped" else False
elif len(sys.argv) == 1:
    _output_directory = ""
    _target_file = ""
    _warp_file = ""
    _affine_file = ""
    _was_flipped = False


about_message ="""
Welcome to the Kronauer Lab Warping Toolkit (To Template)!
==========================================================
This program uses ANTs to warp a file using files generated during 
warping.Please make sure that ANTs is installed and the ANTs 
executables are in the PATH environment variable. 
Follow the instructions at our GitHub repository to setup everything:
https://github.com/neurorishika/ant_template_builder

Version: 1.1, Jan 2025. Developed by Rishika Mohanta.
"""

# create the GUI class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kronauer Lab Warping Toolkit (To Template)")
        self.resize(500, 500)
        
        # create the main widget
        self.main_widget = QtWidgets.QWidget()

        # create the layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)


        # create the input file row
        self.input_row = QtWidgets.QHBoxLayout()
        self.input_label = QtWidgets.QLabel("File to Warp:")
        self.input_textbox = QtWidgets.QLineEdit()
        self.input_textbox.setReadOnly(True)
        self.input_browse = QtWidgets.QPushButton("Browse")
        self.input_browse.clicked.connect(self.browse_input)
        self.input_row.addWidget(self.input_label)
        self.input_row.addWidget(self.input_textbox)
        self.input_row.addWidget(self.input_browse)
        self.main_layout.addLayout(self.input_row)

        # create the output directory row
        self.output_row = QtWidgets.QHBoxLayout()
        self.output_label = QtWidgets.QLabel("Output Directory:")
        self.output_textbox = QtWidgets.QLineEdit()
        self.output_textbox.setText(_output_directory)
        self.output_textbox.setReadOnly(True)
        self.output_browse = QtWidgets.QPushButton("Browse")
        self.output_browse.clicked.connect(self.browse_output)
        self.output_row.addWidget(self.output_label)
        self.output_row.addWidget(self.output_textbox)
        self.output_row.addWidget(self.output_browse)
        self.main_layout.addLayout(self.output_row)

        # create the target reference row
        self.target_row = QtWidgets.QHBoxLayout()
        self.target_label = QtWidgets.QLabel("Target Reference:")
        self.target_textbox = QtWidgets.QLineEdit()
        self.target_textbox.setText(_target_file)
        self.target_textbox.setReadOnly(True)
        self.target_browse = QtWidgets.QPushButton("Browse")
        self.target_browse.clicked.connect(self.browse_target)
        self.target_textbox.textChanged.connect(self.target_changed)
        self.target_row.addWidget(self.target_label)
        self.target_row.addWidget(self.target_textbox)
        self.target_row.addWidget(self.target_browse)
        self.main_layout.addLayout(self.target_row)

        # create the Warp file row
        self.warp_row = QtWidgets.QHBoxLayout()
        self.warp_label = QtWidgets.QLabel("Warp File:")
        self.warp_textbox = QtWidgets.QLineEdit()
        self.warp_textbox.setText(_warp_file)
        self.warp_textbox.setReadOnly(True)
        self.warp_browse = QtWidgets.QPushButton("Browse")
        self.warp_browse.clicked.connect(self.browse_warp)
        self.warp_row.addWidget(self.warp_label)
        self.warp_row.addWidget(self.warp_textbox)
        self.warp_row.addWidget(self.warp_browse)
        self.main_layout.addLayout(self.warp_row)


        # create the Affine file row
        self.affine_row = QtWidgets.QHBoxLayout()
        self.affine_label = QtWidgets.QLabel("Affine File:")
        self.affine_textbox = QtWidgets.QLineEdit()
        self.affine_textbox.setText(_affine_file)
        self.affine_textbox.setReadOnly(True)
        self.affine_browse = QtWidgets.QPushButton("Browse")
        self.affine_browse.clicked.connect(self.browse_affine)
        self.affine_row.addWidget(self.affine_label)
        self.affine_row.addWidget(self.affine_textbox)
        self.affine_row.addWidget(self.affine_browse)
        self.main_layout.addLayout(self.affine_row)

        # create the Reflection file row
        self.reflection_row = QtWidgets.QHBoxLayout()
        self.reflection_label = QtWidgets.QLabel("Mat File:")
        self.reflection_textbox = QtWidgets.QLineEdit()
        self.reflection_textbox.setReadOnly(True)
        self.reflection_browse = QtWidgets.QPushButton("Browse")
        self.reflection_browse.clicked.connect(self.browse_reflection)
        self.reflection_row.addWidget(self.reflection_label)
        self.reflection_row.addWidget(self.reflection_textbox)
        self.reflection_row.addWidget(self.reflection_browse)
        self.main_layout.addLayout(self.reflection_row)

        # create the special warping row (Volume, Segmentation Label, Point Set)
        self.special_warping_row = QtWidgets.QHBoxLayout()
        self.special_warping_label = QtWidgets.QLabel("Type of Data:")
        # create a ButtonGroup
        self.special_warping_group = QtWidgets.QButtonGroup()
        # create the buttons
        self.special_warping_volume = QtWidgets.QRadioButton("Volume")
        self.special_warping_volume.setChecked(True)
        self.special_warping_volume.toggled.connect(self.set_special_warping_type)
        self.special_warping_segmentation_label = QtWidgets.QRadioButton("Segmentation Label")
        self.special_warping_segmentation_label.setChecked(False)
        self.special_warping_segmentation_label.toggled.connect(self.set_special_warping_type)
        self.special_warping_point_set = QtWidgets.QRadioButton("Point Set")
        self.special_warping_point_set.setChecked(False)
        self.special_warping_point_set.toggled.connect(self.set_special_warping_type)
        # add the buttons to the ButtonGroup
        self.special_warping_group.addButton(self.special_warping_volume)
        self.special_warping_group.addButton(self.special_warping_segmentation_label)
        self.special_warping_group.addButton(self.special_warping_point_set)
        # set the special warping type
        self.special_warping_type = "volume"
        self.special_warping_row.addWidget(self.special_warping_label)
        self.special_warping_row.addWidget(self.special_warping_volume)
        self.special_warping_row.addWidget(self.special_warping_segmentation_label)
        self.special_warping_row.addWidget(self.special_warping_point_set)
        self.main_layout.addLayout(self.special_warping_row)

        # create the row 5 layout (Affine only, Time Series, Low Memory, Mirror before warping, Debug)
        self.final_row = QtWidgets.QHBoxLayout()
        self.affine_only_checkbox = QtWidgets.QCheckBox("Affine Only")
        self.affine_only_checkbox.setChecked(False)
        self.time_series_checkbox = QtWidgets.QCheckBox("Time Series")
        self.time_series_checkbox.setChecked(False)
        self.low_memory_checkbox = QtWidgets.QCheckBox("Low Memory")
        self.low_memory_checkbox.setChecked(True)
        self.flip_brain_checkbox = QtWidgets.QCheckBox("Mirror Before Warping")
        self.flip_brain_checkbox.setChecked(_was_flipped)
        self.debug_mode_checkbox = QtWidgets.QCheckBox("Debug Mode")
        self.debug_mode_checkbox.setChecked(False)
        self.final_row.addWidget(self.affine_only_checkbox)
        self.final_row.addWidget(self.time_series_checkbox)
        self.final_row.addWidget(self.low_memory_checkbox)
        self.final_row.addWidget(self.flip_brain_checkbox)
        self.final_row.addWidget(self.debug_mode_checkbox)
        self.main_layout.addLayout(self.final_row)

        # create the run button
        self.run_button = QtWidgets.QPushButton("Run Warping")
        self.run_button.clicked.connect(self.run_warping)
        self.main_layout.addWidget(self.run_button)

        # create the terminal
        self.terminal = QtWidgets.QTextEdit()
        self.terminal.setReadOnly(True)
        self.main_layout.addWidget(self.terminal)

        # set the main widget
        self.setCentralWidget(self.main_widget)

        # show the window
        self.show()

        # as the program starts, show a message to the user about the program using QtMessageBox
        QtWidgets.QMessageBox.information(self, "About", about_message)

    # function to verify no spaces in the file names or directory names
    def verify_no_spaces(self, filename):
        # check if there are spaces in the filename
        if " " in filename:
            QtWidgets.QMessageBox.warning(self, "Warning", "File name or directory name cannot contain spaces. Please change the file name or directory name.")
            return False
        else:
            return True
        
    # function to browse for the input file (can be Image Files, or csv files)
    def browse_input(self):
        # open a file dialog
        open_folder = os.getcwd() if self.input_textbox.text() == "" else os.path.dirname(self.input_textbox.text())
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Input File', open_folder, 'Image Files (*.nii.gz *.nrrd) ;; CSV Files (*.csv)')[0]
        # make sure there are no spaces in the filename and alert the user to change it if there are
        if self.verify_no_spaces(filename) is False:
            return
        # set the textbox to the filename
        self.input_textbox.setText(filename)

    # function to browse for the target reference file
    def browse_target(self):
        # open a file dialog
        open_folder = os.getcwd() if self.target_textbox.text() == "" else os.path.dirname(self.target_textbox.text())
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Target Reference File', open_folder, 'Image Files (*.nii.gz *.nrrd)')[0]
        # make sure there are no spaces in the filename and alert the user to change it if there are
        if self.verify_no_spaces(filename) is False:
            return
        # set the textbox to the filename
        self.target_textbox.setText(filename)

    # function to ask if the user wants to autofill the files
    def target_changed(self):
        # ask the user if they want to autofill the files
        reply = QtWidgets.QMessageBox.question(self, "Autofill", "Do you want to autofill the files?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            # get the target file
            target_file = self.target_textbox.text()
            # make sure the target file has "deformed.nii.gz" at the end
            if not target_file.endswith("deformed.nii.gz"):
                QtWidgets.QMessageBox.warning(self, "Warning", "Target file must be a deformed file. Please change the target file for autofill.")
                return
            # change deformed.nii.gz to Warp.nii.gz
            warp_file = target_file.replace("deformed.nii.gz", "Warp.nii.gz")
            # check if the warp file exists
            if not os.path.exists(warp_file):
                QtWidgets.QMessageBox.warning(self, "Warning", "Warp file does not exist. Please change the target file for autofill or add the warp file manually.")
            else:
                self.warp_textbox.setText(warp_file)
            # change deformed.nii.gz to Affine.txt
            affine_file = target_file.replace("deformed.nii.gz", "Affine.txt")
            # check if the affine file exists
            if not os.path.exists(affine_file):
                QtWidgets.QMessageBox.warning(self, "Warning", "Affine file does not exist. Please change the target file for autofill or add the affine file manually.")
            else:
                self.affine_textbox.setText(affine_file)
            # change deformed.nii.gz to .mat
            reflection_file = target_file.replace("_deformed.nii.gz", ".mat")
            # check if the mat file exists
            if not os.path.exists(reflection_file):
                QtWidgets.QMessageBox.warning(self, "Warning", "Reflection file does not exist. Please change the target file for autofill or add the mat file manually.")
            else:
                self.reflection_textbox.setText(reflection_file)


    # function to browse for the output directory
    def browse_output(self):
        # open a file dialog
        open_folder = os.getcwd() if self.output_textbox.text() == "" else self.output_textbox.text()
        filename = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open Output Directory', open_folder)
        # make sure there are no spaces in the filename and alert the user to change it if there are
        if self.verify_no_spaces(filename) is False:
            return
        # set the textbox to the filename
        self.output_textbox.setText(filename)

    # function to browse for the warp file
    def browse_warp(self):
        # open a file dialog
        open_folder = os.getcwd() if self.warp_textbox.text() == "" else os.path.dirname(self.warp_textbox.text())
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Warp File', open_folder, 'Image Files (*.nii.gz)')[0]
        # make sure there are no spaces in the filename and alert the user to change it if there are
        if self.verify_no_spaces(filename) is False:
            return
        # set the textbox to the filename
        self.warp_textbox.setText(filename)

    # function to browse for the affine file (can be mat files or txt files)
    def browse_affine(self):
        # open a file dialog
        open_folder = os.getcwd() if self.affine_textbox.text() == "" else os.path.dirname(self.affine_textbox.text())
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Affine File', open_folder, 'MAT Files (*.mat) ;; TXT Files (*.txt)')[0]
        # make sure there are no spaces in the filename and alert the user to change it if there are
        if self.verify_no_spaces(filename) is False:
            return
        # set the textbox to the filename
        self.affine_textbox.setText(filename)

    # function to browse for the mat file
    def browse_reflection(self):
        # open a file dialog
        open_folder = os.getcwd() if self.reflection_textbox.text() == "" else os.path.dirname(self.reflection_textbox.text())
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Mat File', open_folder, 'MAT Files (*.mat)')[0]
        # make sure there are no spaces in the filename and alert the user to change it if there are
        if self.verify_no_spaces(filename) is False:
            return
        # set the textbox to the filename
        self.reflection_textbox.setText(filename)
    
    # function to set the special warping type
    def set_special_warping_type(self):
        # get the sender
        sender = self.sender()

        # check which button was clicked
        if sender.text() == "Volume":
            self.special_warping_type = "volume"
        elif sender.text() == "Segmentation Label":
            self.special_warping_type = "segmentation_label"
        elif sender.text() == "Point Set":
            self.special_warping_type = "point_set"


    # function to run the warping using ANTs
    def run_warping(self):
        # get the all files
        input_file = self.input_textbox.text()
        target_file = self.target_textbox.text()
        output_directory = self.output_textbox.text()
        warp_file = self.warp_textbox.text()
        affine_file = self.affine_textbox.text()
        affine_only = self.affine_only_checkbox.isChecked()

        # make sure none of the files are empty
        if input_file == "" or target_file == "" or output_directory == "" or affine_file == "":
            QtWidgets.QMessageBox.warning(self, "Warning", "All files must be specified.")
            return
        
        if affine_only == False and warp_file == "":
            QtWidgets.QMessageBox.warning(self, "Warning", "Warp file must be specified for to_template warping.")
            return
        
        # if the output directory does not have a / at the end, add it
        if not output_directory.endswith("/"):
            output_directory += "/"
        
        # setup output directory
        input_filename = os.path.basename(input_file)
        output_prefix = os.path.splitext(input_filename)[0]+"_warped_"
        output_prefix = os.path.join(output_directory, output_prefix)

        # make sure no files with the same prefix already exist (use glob)
        if len(glob.glob(output_prefix+"*")) > 0:
            QtWidgets.QMessageBox.warning(self, "Warning", "Files with the same prefix already exist. Please change the output directory or the input file.")
            return

        special_warping_type = self.special_warping_type
        time_series = self.time_series_checkbox.isChecked()
        low_memory = "1" if self.low_memory_checkbox.isChecked() else "0"
        flip_brain = self.flip_brain_checkbox.isChecked()
        debug_mode = self.debug_mode_checkbox.isChecked()

        intermediate_files = []
        flip_brain_commands = []

        if flip_brain:

            flipped_input_file = output_directory + os.path.splitext(input_filename)[0]+"_flipped"+os.path.splitext(input_filename)[1]
            mirror_file = self.reflection_textbox.text()
            flip_brain_commands.append("antsApplyTransforms -d 3 -i {} -o {} -t {} -r {} --float {} >{}_out.log 2>{}_err.log".format(input_file, flipped_input_file, mirror_file, input_file, low_memory, flipped_input_file[:-5], flipped_input_file[:-5]))
            input_file = flipped_input_file

            # intermediate files
            intermediate_files.append(flipped_input_file)
            intermediate_files.append(mirror_file[:-4]+"_out.log")
            intermediate_files.append(mirror_file[:-4]+"_err.log")
            intermediate_files.append(flipped_input_file[:-5]+"_out.log")
            intermediate_files.append(flipped_input_file[:-5]+"_err.log")

        # create the command
        warping_command = "antsApplyTransforms" # base command
        warping_command += " -d 4 -e 3" if time_series else " -d 3"
        warping_command += " -i "+input_file
        warping_command += " -o "+output_prefix[:-1]+".nrrd" if not special_warping_type == "point_set" else " -o "+output_prefix[:-1]+".csv"
        warping_command += " -r "+target_file

        if not affine_only:
            warping_command += " -t "+warp_file
        warping_command += " -t "+affine_file

        if special_warping_type == "segmentation_label":
            warping_command += " -n GenericLabel"

        if low_memory:
            warping_command += " --float 1"

        # add logging
        warping_command += " >{}_out.log 2>{}_err.log".format(output_prefix[:-1], output_prefix[:-1])

        # intermediate files
        intermediate_files.append(output_prefix[:-1]+"_out.log")
        intermediate_files.append(output_prefix[:-1]+"_err.log")

        # output file
        out_file = output_prefix[:-1]+".nrrd" if not special_warping_type == "point_set" else output_prefix[:-1]+".csv"
        
        # save the output file
        self.out_file = out_file
        
        if debug_mode:
            intermediate_files = []

        # disable all the buttons
        self.run_button.setEnabled(False)
        self.input_browse.setEnabled(False)
        self.target_browse.setEnabled(False)
        self.output_browse.setEnabled(False)
        self.warp_browse.setEnabled(False)
        self.affine_browse.setEnabled(False)
        self.special_warping_volume.setEnabled(False)
        self.special_warping_segmentation_label.setEnabled(False)
        self.special_warping_point_set.setEnabled(False)
        self.affine_only_checkbox.setEnabled(False)
        self.time_series_checkbox.setEnabled(False)
        self.low_memory_checkbox.setEnabled(False)
        self.flip_brain_checkbox.setEnabled(False)
        self.debug_mode_checkbox.setEnabled(False)


        # create a new thread to run the warping command
        self.warping_thread = QtCore.QThread()
        self.warping_worker = WarpingWorker(warping_command, flip_brain_commands, intermediate_files)
        self.warping_worker.moveToThread(self.warping_thread)
        self.warping_thread.started.connect(self.warping_worker.run_warping)
        self.warping_worker.finished.connect(self.warping_thread.quit)
        self.warping_worker.finished.connect(self.warping_worker.deleteLater)
        self.warping_thread.finished.connect(self.warping_thread.deleteLater)
        self.warping_worker.progress.connect(self.update_terminal)
        self.warping_thread.start()

        # when the thread is finished, print a message and enable the run button
        self.warping_thread.finished.connect(self.warping_finished)

    # function to print a message when the warping is finished
    def warping_finished(self):
        # enable all the buttons
        self.run_button.setEnabled(True)
        self.input_browse.setEnabled(True)
        self.target_browse.setEnabled(True)
        self.output_browse.setEnabled(True)
        self.warp_browse.setEnabled(True)
        self.affine_browse.setEnabled(True)
        self.special_warping_volume.setEnabled(True)
        self.special_warping_segmentation_label.setEnabled(True)
        self.special_warping_point_set.setEnabled(True)
        self.affine_only_checkbox.setEnabled(True)
        self.time_series_checkbox.setEnabled(True)
        self.low_memory_checkbox.setEnabled(True)
        self.flip_brain_checkbox.setEnabled(True)
        self.debug_mode_checkbox.setEnabled(True)

        # pop up a message box
        QtWidgets.QMessageBox.information(self, "Warping Finished", "Warping finished check the output directory for the registered file: {}".format(self.out_file))

    # function to update the terminal
    def update_terminal(self, text):
        self.terminal.append(text)

# create a worker class to run the warping command
class WarpingWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(str)

    def __init__(self, warping_command, flip_brain_commands, intermediate_files):
        super().__init__()
        self.warping_command = warping_command
        self.flip_brain_commands = flip_brain_commands
        self.intermediate_files = intermediate_files

    def run_warping(self):
        if len(self.flip_brain_commands) > 0:
            self.progress.emit("Flipping brain...")
            self.progress.emit("")
            # run the flip brain command
            for command in self.flip_brain_commands:
                self.progress.emit(command)
                os.system(command)
                self.progress.emit("")

        # run the warping command
        self.progress.emit("Running warping...")
        self.progress.emit("")
        self.progress.emit(self.warping_command)
        os.system(self.warping_command)

        # remove all empty log/error files
        if len(self.intermediate_files) > 0:
            self.progress.emit("Removing intermediate files...")
            for file in self.intermediate_files:
                # check if log or error file
                if file.endswith("_out.log") or file.endswith("_err.log"):
                    # check if file exists, if not, continue
                    if not os.path.exists(file):
                        continue
                    # convert to error file
                    error_file = file[:-8]+"_err.log"
                    # check if error file exists, if not, continue
                    if not os.path.exists(error_file):
                        continue
                    # check if empty
                    if os.stat(error_file).st_size == 0:
                        # remove the log file and the error file
                        if os.path.exists(file[:-8]+"_out.log"):
                            self.progress.emit("Removing "+file[:-8]+"_out.log")
                            os.remove(file[:-8]+"_out.log")
                            self.progress.emit("")
                        self.progress.emit("Removing "+error_file)
                        os.remove(error_file)
                        self.progress.emit("")
                else:
                    # remove the file (if it exists)
                    if not os.path.exists(file):
                        continue
                    self.progress.emit("Removing "+file)
                    os.remove(file)
                    self.progress.emit("")

        self.progress.emit("")
        self.progress.emit("Warping finished.")
        # emit the finished signal
        self.finished.emit()

# create the main function
def main():
    # create the application
    app = QtWidgets.QApplication(sys.argv)

    # create the main window
    main_window = MainWindow()

    # exit the application
    sys.exit(app.exec_())

# check if the script is being run directly
if __name__ == "__main__":
    main()

## END OF CODE



