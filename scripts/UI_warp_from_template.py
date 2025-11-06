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
    _warp_deformed_file = sys.argv[3] if sys.argv[3] != "MISSING" else ""
    _inverse_warp_file = sys.argv[4] if sys.argv[4] != "MISSING" else ""
    _affine_file = sys.argv[5] if sys.argv[5] != "MISSING" else ""
    _was_flipped = True if sys.argv[6] == "flipped" else False
elif len(sys.argv) == 1:
    _output_directory = ""
    _target_file = ""
    _warp_deformed_file = ""
    _inverse_warp_file = ""
    _affine_file = ""
    _was_flipped = False


about_message ="""
Welcome to the Kronauer Lab Warping Toolkit (From Template)!
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
        self.setWindowTitle("Kronauer Lab  Warping Toolkit (From Template)")
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
        self.target_row.addWidget(self.target_label)
        self.target_row.addWidget(self.target_textbox)
        self.target_row.addWidget(self.target_browse)
        self.main_layout.addLayout(self.target_row)

        # create the deformation reference row
        self.warp_deformed_row = QtWidgets.QHBoxLayout()
        self.warp_deformed_label = QtWidgets.QLabel("Warp Deformation:")
        self.warp_deformed_textbox = QtWidgets.QLineEdit()
        self.warp_deformed_textbox.setText(_warp_deformed_file)
        self.warp_deformed_textbox.setReadOnly(True)
        self.warp_deformed_browse = QtWidgets.QPushButton("Browse")
        self.warp_deformed_browse.clicked.connect(self.browse_warp_deformed)
        self.warp_deformed_textbox.textChanged.connect(self.warp_deformed_changed)
        self.warp_deformed_row.addWidget(self.warp_deformed_label)
        self.warp_deformed_row.addWidget(self.warp_deformed_textbox)
        self.warp_deformed_row.addWidget(self.warp_deformed_browse)
        self.main_layout.addLayout(self.warp_deformed_row)

        # create the Inverse Warp file row
        self.inverse_warp_row = QtWidgets.QHBoxLayout()
        self.inverse_warp_label = QtWidgets.QLabel("Inverse Warp File:")
        self.inverse_warp_textbox = QtWidgets.QLineEdit()
        self.inverse_warp_textbox.setText(_inverse_warp_file)
        self.inverse_warp_textbox.setReadOnly(True)
        self.inverse_warp_browse = QtWidgets.QPushButton("Browse")
        self.inverse_warp_browse.clicked.connect(self.browse_inverse_warp)
        self.inverse_warp_row.addWidget(self.inverse_warp_label)
        self.inverse_warp_row.addWidget(self.inverse_warp_textbox)
        self.inverse_warp_row.addWidget(self.inverse_warp_browse)
        self.main_layout.addLayout(self.inverse_warp_row)

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

        # create the row 5 layout (Affine only, Time Series, Low Memory, Mirror after warping, Debug)
        self.final_row = QtWidgets.QHBoxLayout()
        self.affine_only_checkbox = QtWidgets.QCheckBox("Affine Only")
        self.affine_only_checkbox.setChecked(False)
        self.time_series_checkbox = QtWidgets.QCheckBox("Time Series")
        self.time_series_checkbox.setChecked(False)
        self.low_memory_checkbox = QtWidgets.QCheckBox("Low Memory")
        self.low_memory_checkbox.setChecked(True)
        self.flip_brain_checkbox = QtWidgets.QCheckBox("Mirror After Warping")
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

        if not os.path.exists(_affine_file):
            self.flip_brain_checkbox.setEnabled(False)


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

    # function to browse for the target reference file
    def browse_warp_deformed(self):
        # open a file dialog
        open_folder = os.getcwd() if self.warp_deformed_textbox.text() == "" else os.path.dirname(self.warp_deformed_textbox.text())
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Target Reference File', open_folder, 'Image Files (*.nii.gz *.nrrd)')[0]
        # make sure there are no spaces in the filename and alert the user to change it if there are
        if self.verify_no_spaces(filename) is False:
            return
        # set the textbox to the filename
        self.warp_deformed_textbox.setText(filename)

    # function to ask if the user wants to autofill the files
    def warp_deformed_changed(self):
        # ask the user if they want to autofill the files
        reply = QtWidgets.QMessageBox.question(self, "Autofill", "Do you want to autofill the files?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            # get the warp_deformed file
            warp_deformed_file = self.warp_deformed_textbox.text()
            # make sure the warp_deformed file has "deformed.nii.gz" at the end
            if not warp_deformed_file.endswith("deformed.nii.gz"):
                QtWidgets.QMessageBox.warning(self, "Warning", "Target file must be a deformed file. Please change the warp_deformed file for autofill.")
                return
            # change deformed.nii.gz to InverseWarp.nii.gz
            inverse_warp_file = warp_deformed_file.replace("deformed.nii.gz", "InverseWarp.nii.gz")
            # check if the inverse warp file exists
            if not os.path.exists(inverse_warp_file):
                QtWidgets.QMessageBox.warning(self, "Warning", "Inverse Warp file does not exist. Please change the warp_deformed file for autofill or add the inverse warp file manually.")
            else:
                self.inverse_warp_textbox.setText(inverse_warp_file)
            # change deformed.nii.gz to Affine.txt
            affine_file = warp_deformed_file.replace("deformed.nii.gz", "Affine.txt")
            # check if the affine file exists
            if not os.path.exists(affine_file):
                QtWidgets.QMessageBox.warning(self, "Warning", "Affine file does not exist. Please change the warp_deformed file for autofill or add the affine file manually.")
            else:
                self.affine_textbox.setText(affine_file)
            # change deformed.nii.gz to .mat
            reflection_file = warp_deformed_file.replace("_deformed.nii.gz", ".mat")
            if os.path.exists(reflection_file):
                self.reflection_textbox.setText(reflection_file)
                self.flip_brain_checkbox.setEnabled(True)
            else:
                self.reflection_textbox.setText("")
                self.flip_brain_checkbox.setEnabled(False)
                QtWidgets.QMessageBox.warning(self, "Warning", "Reflection file does not exist. Mirror After Warping option will be disabled.")



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


    # function to browse for the inverse warp file
    def browse_inverse_warp(self):
        # open a file dialog
        open_folder = os.getcwd() if self.inverse_warp_textbox.text() == "" else os.path.dirname(self.inverse_warp_textbox.text())
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Inverse Warp File', open_folder, 'Image Files (*.nii.gz)')[0]
        # make sure there are no spaces in the filename and alert the user to change it if there are
        if self.verify_no_spaces(filename) is False:
            return
        # set the textbox to the filename
        self.inverse_warp_textbox.setText(filename)

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

        # Enable or disable the Mirror After Warping checkbox based on file availability
        self.flip_brain_checkbox.setEnabled(bool(filename))
    
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
        # Get all files
        input_file = self.input_textbox.text()
        target_file = self.target_textbox.text()
        output_directory = self.output_textbox.text()
        inverse_warp_file = self.inverse_warp_textbox.text()
        affine_file = self.affine_textbox.text()

        affine_only = self.affine_only_checkbox.isChecked()

        # Ensure required fields are filled
        if input_file == "" or target_file == "" or output_directory == "" or affine_file == "":
            QtWidgets.QMessageBox.warning(self, "Warning", "All files must be specified.")
            return
        
        if not affine_only and inverse_warp_file == "":
            QtWidgets.QMessageBox.warning(self, "Warning", "Inverse Warp file must be specified for from_template warping.")
            return
        
        if self.flip_brain_checkbox.isChecked() and self.reflection_textbox.text() == "":
            QtWidgets.QMessageBox.warning(self, "Warning", "Reflection file must be specified for mirroring.")
            return

        # Ensure output directory ends with "/"
        if not output_directory.endswith("/"):
            output_directory += "/"

        # Prepare output file prefix
        input_filename = os.path.basename(input_file)
        output_prefix = os.path.splitext(input_filename)[0] + "_warped_"
        output_prefix = os.path.join(output_directory, output_prefix)

        # Check for existing output files
        if len(glob.glob(output_prefix + "*")) > 0:
            QtWidgets.QMessageBox.warning(self, "Warning", "Files with the same prefix already exist. Please change the output directory or input file.")
            return

        # Prepare the warping command
        special_warping_type = self.special_warping_type
        time_series = self.time_series_checkbox.isChecked()
        low_memory = "1" if self.low_memory_checkbox.isChecked() else "0"
        debug_mode = self.debug_mode_checkbox.isChecked()

        warping_command = f"antsApplyTransforms -d {'4 -e 3' if time_series else '3'}"
        warping_command += f" -i {input_file} -o {output_prefix[:-1]}.nrrd" if special_warping_type != "point_set" else f" -o {output_prefix[:-1]}.csv"
        warping_command += f" -r {target_file}"
        warping_command += f" -t [{affine_file}, 1]"
        if not affine_only:
            warping_command += f" -t {inverse_warp_file}"
        if special_warping_type == "segmentation_label":
            warping_command += " -n GenericLabel"
        if low_memory:
            warping_command += " --float 1"

        warping_command += f" >{output_prefix[:-1]}_out.log 2>{output_prefix[:-1]}_err.log"

        # Prepare mirroring commands for after warping
        flip_brain_commands = []
        intermediate_files = [output_prefix[:-1] + "_out.log", output_prefix[:-1] + "_err.log"]

        if self.flip_brain_checkbox.isChecked():
            mirrored_output_file = output_prefix[:-1] + "_mirrored.nrrd" if special_warping_type != "point_set" else output_prefix[:-1] + "_mirrored.csv"
            mirror_file = self.reflection_textbox.text()
            flip_brain_commands.append(
                f"antsApplyTransforms -d 3 -i {output_prefix[:-1]}.nrrd -o {mirrored_output_file} "
                f"-t {mirror_file} -r {output_prefix[:-1]}.nrrd --float {low_memory} "
                f">{mirrored_output_file[:-5]}_out.log 2>{mirrored_output_file[:-5]}_err.log"
            )
            out_file = mirrored_output_file

            # Intermediate files from mirroring
            intermediate_files.append(mirrored_output_file)
            intermediate_files.append(mirror_file[:-4] + "_out.log")
            intermediate_files.append(mirror_file[:-4] + "_err.log")
            intermediate_files.append(mirrored_output_file[:-5] + "_out.log")
            intermediate_files.append(mirrored_output_file[:-5] + "_err.log")

        # output file
        else:
            out_file = output_prefix[:-1] + ".nrrd" if special_warping_type != "point_set" else output_prefix[:-1] + ".csv"
        
        # save the output file
        self.out_file = out_file

        if debug_mode:
            intermediate_files = []

        # Disable the UI during processing
        self.run_button.setEnabled(False)
        self.input_browse.setEnabled(False)
        self.warp_deformed_browse.setEnabled(False)
        self.target_browse.setEnabled(False)
        self.output_browse.setEnabled(False)
        self.inverse_warp_browse.setEnabled(False)
        self.affine_browse.setEnabled(False)
        self.special_warping_volume.setEnabled(False)
        self.special_warping_segmentation_label.setEnabled(False)
        self.special_warping_point_set.setEnabled(False)
        self.affine_only_checkbox.setEnabled(False)
        self.time_series_checkbox.setEnabled(False)
        self.low_memory_checkbox.setEnabled(False)
        self.flip_brain_checkbox.setEnabled(False)
        self.debug_mode_checkbox.setEnabled(False)

        # Run warping and mirroring commands in sequence
        self.warping_thread = QtCore.QThread()
        self.warping_worker = WarpingWorker(warping_command, flip_brain_commands, intermediate_files)
        self.warping_worker.moveToThread(self.warping_thread)
        self.warping_thread.started.connect(self.warping_worker.run_warping)
        self.warping_worker.finished.connect(self.warping_thread.quit)
        self.warping_worker.finished.connect(self.warping_worker.deleteLater)
        self.warping_thread.finished.connect(self.warping_thread.deleteLater)
        self.warping_worker.progress.connect(self.update_terminal)
        self.warping_thread.start()

        # When finished, re-enable the UI
        self.warping_thread.finished.connect(self.warping_finished)


    # function to print a message when the warping is finished
    def warping_finished(self):
        # enable all the buttons
        self.run_button.setEnabled(True)
        self.input_browse.setEnabled(True)
        self.target_browse.setEnabled(True)
        self.warp_deformed_browse.setEnabled(True)
        self.output_browse.setEnabled(True)
        self.inverse_warp_browse.setEnabled(True)
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

        # run the warping command
        self.progress.emit("Running warping...")
        self.progress.emit("")
        self.progress.emit(self.warping_command)
        os.system(self.warping_command)

        # Run the flip brain commands after warping
        if len(self.flip_brain_commands) > 0:
            self.progress.emit("Starting post-warp mirroring...")
            for command in self.flip_brain_commands:
                self.progress.emit(command)
                os.system(command)
                self.progress.emit("")
            self.progress.emit("Post-warp mirroring completed.")

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



