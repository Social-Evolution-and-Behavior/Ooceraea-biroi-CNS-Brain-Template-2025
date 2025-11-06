# setup a simple gui script to run registration

## IMPLEMETATION DETAILS
# Use PyQt5 to create a simple GUI that allows the user to enter the following:
#   - template file (Label + Textbox + Browse button) - (Row 1) Required
#   - input file (Label + Textbox + Browse button) - (Row 2) Required
#   - output directory (Label + Textbox + Browse button) - (Row 3) Required
#   - checkbox for whether to use rigid, rigid+affine, or rigid+affine+deformable (Row 4) Only one can be selected, default is rigid+affine+deformable
#   - number of threads to use (max is the number of cores on the machine) (Label + Textbox) (Row 5) Default is 1
#   - checkbox to use histogram matching (Row 5) Default is unchecked
#   - checkbox for quality_check (use the same random seed) (Row 5) Default is checked
#   - checkbox for whether to flip the brain before registration (Row 5) Default is unchecked
#   - button to run the registration (Row 6)
#   - text terminal to display the progress of the registration (Row 7)

# The GUI should be able to handle the following errors:
#   - template file or input file or output directory is not specified
#   - number of threads is not a positive integer
#   - file names or directory names have spaces in them

import glob
import json
import os
## START OF CODE
# import the necessary packages
import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets

about_message ="""
Welcome to the Kronauer Lab Ultimate Template Registration Toolkit!
===================================================================
This program uses ANTs to register a brain to a template. 
Please make sure that ANTs is installed and the ANTs executables 
are in the PATH environment variable. 
Follow the instructions at our GitHub repository to setup everything:
https://github.com/neurorishika/ant_template_builder

Version: 1.2, Jan 2025. Developed by Rishika Mohanta.
"""

# create the GUI class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kronauer Lab Ultimate Template Registration Toolkit")
        self.resize(500, 500)

        # add a registration chain
        self.registration_chain = []  # Dynamic list of registration steps
        
        # create the main widget
        self.main_widget = QtWidgets.QWidget()

        # create the layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        # create the template file row
        self.template_row = QtWidgets.QHBoxLayout()

        self.template_label = QtWidgets.QLabel("Template File:")
        self.template_textbox = QtWidgets.QLineEdit()
        self.template_textbox.setReadOnly(True)
        self.template_browse = QtWidgets.QPushButton("Browse")
        self.template_browse.clicked.connect(self.browse_template)
        self.template_row.addWidget(self.template_label)
        self.template_row.addWidget(self.template_textbox)
        self.template_row.addWidget(self.template_browse)
        self.main_layout.addLayout(self.template_row)

        # create the input file row
        self.input_row = QtWidgets.QHBoxLayout()
        # add a checkbox for enabling or disabling batch mode
        self.batch_mode_checkbox = QtWidgets.QCheckBox("Batch Mode")
        self.batch_mode_checkbox.setChecked(False)
        self.batch_mode_checkbox.stateChanged.connect(self.toggle_batch_mode)
        self.selected_input_files = []  # List of selected input files
        self.input_label = QtWidgets.QLabel("Input File:")
        self.input_textbox = QtWidgets.QLineEdit()
        self.input_textbox.setReadOnly(True)
        self.input_browse = QtWidgets.QPushButton("Browse")
        self.input_browse.clicked.connect(self.browse_input)
        self.input_row.addWidget(self.batch_mode_checkbox)
        self.input_row.addWidget(self.input_label)
        self.input_row.addWidget(self.input_textbox)
        self.input_row.addWidget(self.input_browse)
        self.main_layout.addLayout(self.input_row)

        # create the output directory row
        self.output_row = QtWidgets.QHBoxLayout()
        self.output_label = QtWidgets.QLabel("Output Directory:")
        self.output_textbox = QtWidgets.QLineEdit()
        self.output_textbox.setReadOnly(True)
        self.output_browse = QtWidgets.QPushButton("Browse")
        self.output_browse.clicked.connect(self.browse_output)
        self.output_row.addWidget(self.output_label)
        self.output_row.addWidget(self.output_textbox)
        self.output_row.addWidget(self.output_browse)
        self.main_layout.addLayout(self.output_row)

        # Registration Chain Section
        self.chain_label = QtWidgets.QLabel("Registration Chain:")
        self.chain_list = QtWidgets.QListWidget()  # List to display selected steps
        self.add_step_button = QtWidgets.QPushButton("Add Step")
        self.add_step_button.clicked.connect(self.add_registration_step)
        self.remove_step_button = QtWidgets.QPushButton("Remove Last Step")
        self.remove_step_button.clicked.connect(self.remove_last_registration_step)
        # Add Save and Load buttons for the chain
        self.save_chain_button = QtWidgets.QPushButton("Save Chain")
        self.save_chain_button.clicked.connect(self.save_chain)
        self.load_chain_button = QtWidgets.QPushButton("Load Chain")
        self.load_chain_button.clicked.connect(self.load_chain)


        # Layout for chain management
        self.chain_layout = QtWidgets.QVBoxLayout()
        self.chain_layout.addWidget(self.chain_label)
        self.chain_layout.addWidget(self.chain_list)
        # Add the buttons to the chain layout
        self.chain_layout.addWidget(self.add_step_button)
        self.chain_layout.addWidget(self.remove_step_button)
        self.chain_layout.addWidget(self.save_chain_button)
        self.chain_layout.addWidget(self.load_chain_button)

        # Add to main layout
        self.main_layout.addLayout(self.chain_layout)

        # create the last row layout (quality_check, low_memory, flip_brain, debug_mode)
        self.last_row = QtWidgets.QHBoxLayout()

        self.quality_check_checkbox = QtWidgets.QCheckBox("Quality Check")
        self.quality_check_checkbox.setChecked(False)
        self.last_row.addWidget(self.quality_check_checkbox)

        self.low_memory_checkbox = QtWidgets.QCheckBox("Low Memory")
        self.low_memory_checkbox.setChecked(False)
        self.last_row.addWidget(self.low_memory_checkbox)

        self.flip_brain_checkbox = QtWidgets.QCheckBox("Mirror before Registration")
        self.flip_brain_checkbox.setChecked(False)
        self.last_row.addWidget(self.flip_brain_checkbox)

        self.debug_mode_checkbox = QtWidgets.QCheckBox("Debug Mode")
        self.debug_mode_checkbox.setChecked(False)
        self.last_row.addWidget(self.debug_mode_checkbox)

        self.main_layout.addLayout(self.last_row)

        # create the run button
        self.run_button = QtWidgets.QPushButton("Run Registration")
        self.run_button.clicked.connect(self.run_registration)
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
    
    def save_chain(self):
        # Open a file dialog to select the save location
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Chain", "", "JSON Files (*.json)")
        if not file_path:
            return  # User canceled the save dialog

        # Ensure the file has a .json extension
        if not file_path.endswith(".json"):
            file_path += ".json"

        try:
            # Save the registration chain to the file
            with open(file_path, 'w') as file:
                json.dump(self.registration_chain, file, indent=4)
            QtWidgets.QMessageBox.information(self, "Success", f"Chain saved successfully to {file_path}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save chain: {str(e)}")

    def load_chain(self):
        # Open a file dialog to select the JSON file
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load Chain", "", "JSON Files (*.json)")
        if not file_path:
            return  # User canceled the load dialog

        try:
            # Load the registration chain from the file
            with open(file_path, 'r') as file:
                loaded_chain = json.load(file)

            # Validate the loaded chain
            if not isinstance(loaded_chain, list) or not all(
                isinstance(step, dict) and "step" in step and "num_iterations" in step and "similarity_metric" in step and "n4_bias_field" in step
                for step in loaded_chain
            ):
                raise ValueError("Invalid chain format")

            # Update the registration chain and the UI
            self.registration_chain = loaded_chain
            self.chain_list.clear()
            for step in self.registration_chain:
                self.chain_list.addItem(
                    f"{step['step']} - Iter: {step['num_iterations']}, Sim: {step['similarity_metric']} + N4: {step['n4_bias_field']}"
                )

            QtWidgets.QMessageBox.information(self, "Success", f"Chain loaded successfully from {file_path}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load chain: {str(e)}")



    # function to verify no spaces in the file names or directory names
    def verify_no_spaces(self, filename):
        # check if there are spaces in the filename
        if " " in filename:
            QtWidgets.QMessageBox.warning(self, "Warning", "File name or directory name cannot contain spaces. Please change the file name or directory name.")
            return False
        else:
            return True

    # function to browse for the template file
    def browse_template(self):
        # open a file dialog
        open_folder = os.getcwd() if self.template_textbox.text() == "" else os.path.dirname(self.template_textbox.text())
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Template File', open_folder, 'Image Files (*.nii.gz *.nrrd)')[0]
        # make sure there are no spaces in the filename and alert the user to change it if there are
        if self.verify_no_spaces(filename) is False:
            return
        # set the textbox to the filename
        self.template_textbox.setText(filename)

    # function to browse for the input file
    def browse_input(self):
        # open a file dialog
        open_folder = os.getcwd() if self.input_textbox.text() == "" else os.path.dirname(self.input_textbox.text())
        if not self.batch_mode_checkbox.isChecked():
            print('Single Mode')
            filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Input File', open_folder, 'Image Files (*.nii.gz *.nrrd)')[0]
            # make sure there are no spaces in the filename and alert the user to change it if there are
            if self.verify_no_spaces(filename) is False:
                return
            # set the textbox to the filename
            self.input_textbox.setText(filename)
            self.selected_input_files = [filename]  # Single file mode
        else:
            print('Batch Mode')
            # get multiple files
            filenames, _ = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open Input Files', open_folder, 'Image Files (*.nii.gz *.nrrd)')
            # make sure there are no spaces in the filename and alert the user to change it if there are
            for filename in filenames:
                if self.verify_no_spaces(filename) is False:
                    return
            # set the textbox to the filename
            self.input_textbox.setText(", ".join(filenames))
            self.selected_input_files = filenames # Batch mode

    def toggle_batch_mode(self):
        if not self.batch_mode_checkbox.isChecked() and len(self.selected_input_files) > 1:
            reply = QtWidgets.QMessageBox.question(
                self, "Confirm Action",
                "Disabling batch mode will clear the current file selection. Proceed?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.No:
                self.batch_mode_checkbox.setChecked(True)
                return
        self.input_textbox.clear()
        self.selected_input_files = []



    # function to browse for the output directory
    def browse_output(self):
        # open a file dialog
        open_folder = os.getcwd() if self.output_textbox.text() == "" else os.path.dirname(self.output_textbox.text())
        filename = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open Output Directory', open_folder)
        # make sure there are no spaces in the filename and alert the user to change it if there are
        if self.verify_no_spaces(filename) is False:
            return
        # set the textbox to the filename
        self.output_textbox.setText(filename)


    def add_registration_step(self):
        # Define available steps and default parameters
        steps = ["Purely Rigid", "Affine + Rigid", "Elastic Registration", "SyN with arbitrary time", "SyN with 2 time points", "Greedy SyN", "Exponential SyN", "Diffeomorphic Demons"]
        step_map = {
            "Purely Rigid": "RI",
            "Affine + Rigid": "RA",
            "Elastic Registration": "EL",
            "SyN with arbitrary time": "SY",
            "SyN with 2 time points": "S2",
            "Greedy SyN": "GR",
            "Exponential SyN": "EX",
            "Diffeomorphic Demons": "DD"
        }
        similarity_metrics = ["Cross Correlation", "Mutual Information", "Mean Squared Difference", "Probability Mapping"]
        similarity_metric_map = {
            "Cross Correlation": "CC",
            "Mutual Information": "MI",
            "Mean Squared Difference": "MSQ",
            "Probability Mapping": "PR"
        }

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Add Registration Step")
        dialog_layout = QtWidgets.QFormLayout(dialog)

        # Step selection dropdown
        step_dropdown = QtWidgets.QComboBox()
        step_dropdown.addItems(steps)
        dialog_layout.addRow("Step:", step_dropdown)

        # Number of iterations
        num_iterations_input = QtWidgets.QLineEdit("30x30x30x90x20x8")
        dialog_layout.addRow("Number of Iterations:", num_iterations_input)
        # check if the number of iterations is valid
        num_iterations_input.textChanged.connect(self.check_num_iterations)

        # Similarity metric
        similarity_dropdown = QtWidgets.QComboBox()
        similarity_dropdown.addItems(similarity_metrics)
        dialog_layout.addRow("Similarity Metric:", similarity_dropdown)

        # Checkbox for histogram matching
        n4_bias_field_checkbox = QtWidgets.QCheckBox()
        n4_bias_field_checkbox.setChecked(True)
        dialog_layout.addRow("Histogram Matching:", n4_bias_field_checkbox)

        # Buttons for dialog
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        dialog_layout.addWidget(buttons)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Get user inputs
            step = step_map[step_dropdown.currentText()]
            num_iterations = num_iterations_input.text()
            similarity_metric = similarity_metric_map[similarity_dropdown.currentText()]
            n4_bias_field = "1" if n4_bias_field_checkbox.isChecked() else "0"

            # Add step with parameters to the chain
            self.registration_chain.append({
                "step": step,
                "num_iterations": num_iterations,
                "similarity_metric": similarity_metric,
                "n4_bias_field": n4_bias_field
            })
            self.chain_list.addItem(f"{step_dropdown.currentText()} - Iter: {num_iterations}, Sim: {similarity_metric} + N4: {n4_bias_field}")

    
    def remove_last_registration_step(self):
        if len(self.registration_chain) > 0:
            self.registration_chain.pop()
            self.chain_list.takeItem(self.chain_list.count() - 1)


    # function to check the number of iterations
    def check_num_iterations(self):
        # get the number of iterations
        num_iterations = self.num_iterations_textbox.text()

        # make sure its a series of positive integers separated by x
        try:
            num_iterations = [int(i) for i in num_iterations.split("x")]
            assert all(i > 0 for i in num_iterations)
        except:
            QtWidgets.QMessageBox.warning(self, "Warning", "Number of iterations must be a series of positive integers separated by x.")
            return
    
    def validate_input_files(self, input_files):
        for file in input_files:
            if not os.path.exists(file):
                QtWidgets.QMessageBox.warning(
                    self, "Error",
                    f"Input file does not exist: {file}"
                )
                return False
            if " " in file:
                QtWidgets.QMessageBox.warning(
                    self, "Error",
                    f"Input file contains spaces: {file}"
                )
                return False
        return True


    # function to run the registration using ANTs
    def run_registration(self):

        if not self.registration_chain:
            QtWidgets.QMessageBox.warning(self, "Warning", "No registration steps defined in the chain.")
            return

        # get the template file
        template_file = self.template_textbox.text()

        # get the input files
        input_files = self.input_textbox.text()

        # get the output directory
        output_directory = self.output_textbox.text()

        # check if the template file, input file, or output directory is not specified
        if template_file == "" or output_directory == "" or input_files == "":
            QtWidgets.QMessageBox.warning(self, "Warning", "Template file, input file, and output directory must be specified.")
            return
        
        # if the output directory does not end with a slash, add a slash
        if not output_directory.endswith("/"):
            output_directory += "/"
        
        # validate input files
        if not self.validate_input_files(self.selected_input_files):
            return


        # loop through the files
        for input_file in self.selected_input_files:
            # update terminal
            self.terminal.append(f"Running registration for {input_file}...")
        
            # setup output directory
            input_filename = os.path.basename(input_file)
            output_prefix = os.path.splitext(input_filename)[0]+"_"
            output_prefix = os.path.join(output_directory, output_prefix)

            # run the registration
            self._run_single_registration(template_file, input_file, output_prefix)
        
    
    def _run_single_registration(self, template_file, input_file, output_prefix):
        # Registration parameters
        quality_check = "1" if self.quality_check_checkbox.isChecked() else "0"
        flip_brain = self.flip_brain_checkbox.isChecked()
        low_memory_flip = "1" if self.low_memory_checkbox.isChecked() else "0"
        intermediate_files = []
        flip_brain_commands = []

        # Prepare flip brain commands (if needed)
        if flip_brain:
            # Define flipped command
            flipped_input_file = output_prefix + "_flipped.nii.gz"
            mirror_file = output_prefix + "_mirror.mat"
            flip_brain_commands.append(
                f"ImageMath 3 {mirror_file} ReflectionMatrix {input_file} 0 >{output_prefix}out.log 2>{output_prefix}err.log"
            )
            flip_brain_commands.append(
                f"antsApplyTransforms -d 3 -i {input_file} -o {flipped_input_file} -t {mirror_file} -r {input_file} --float {low_memory_flip} >{output_prefix}out.log 2>{output_prefix}err.log"
            )

            # Add intermediate files to the list
            intermediate_files.append(flipped_input_file)
            intermediate_files.append(f"{output_prefix}_mirror_out.log")
            intermediate_files.append(f"{output_prefix}_mirror_err.log")
            intermediate_files.append(f"{flipped_input_file[:-7]}_out.log")
            intermediate_files.append(f"{flipped_input_file[:-7]}_err.log")

            # Update input file for the next step
            input_file = flipped_input_file

        # Build registration commands for the chain
        commands = []
        for step_config in self.registration_chain:
            step = step_config["step"]
            num_iterations = step_config["num_iterations"]
            similarity_metric = step_config["similarity_metric"]
            n4_bias_field = step_config["n4_bias_field"]

            registration_command = (
                f"antsIntroduction.sh -d 3 -r {template_file} -i {input_file} -o {output_prefix} "
                f"-m {num_iterations} -t {step} -n {n4_bias_field} -q {quality_check} -s {similarity_metric}"
            )
            commands.append(registration_command)
            
            # Add intermediate files to the list
            intermediate_files.append(f"{output_prefix}out.log")
            intermediate_files.append(f"{output_prefix}err.log")

            # Update input file for the next step
            input_file = f"{output_prefix}deformed.nii.gz"

            # Update output prefix for the next step
            output_prefix += "deformed_"


        # Create and start the registration worker
        self._start_registration_worker(commands, flip_brain_commands, output_prefix, intermediate_files)
    
    def _start_registration_worker(self, commands, flip_brain_commands, output_prefix, intermediate_files):

        # check if debug mode is enabled
        if self.debug_mode_checkbox.isChecked():
            intermediate_files = []

        # Disable UI elements
        self.run_button.setEnabled(False)
        self.template_browse.setEnabled(False)
        self.input_browse.setEnabled(False)
        self.output_browse.setEnabled(False)
        self.quality_check_checkbox.setEnabled(False)
        self.flip_brain_checkbox.setEnabled(False)
        self.low_memory_checkbox.setEnabled(False)

        # Start the registration worker thread
        self.registration_thread = QtCore.QThread()
        self.registration_worker = RegistrationWorker(commands, flip_brain_commands, output_prefix, intermediate_files)
        self.registration_worker.moveToThread(self.registration_thread)
        self.registration_thread.started.connect(self.registration_worker.run_registration)
        self.registration_worker.finished.connect(self.registration_thread.quit)
        self.registration_worker.finished.connect(self.registration_worker.deleteLater)
        self.registration_thread.finished.connect(self.registration_thread.deleteLater)
        self.registration_worker.progress.connect(self.update_terminal)
        self.registration_thread.start()
        self.registration_thread.finished.connect(self.registration_finished)

    # function to print a message when the registration is finished
    def registration_finished(self):
        # enable all the buttons
        self.run_button.setEnabled(True)
        self.template_browse.setEnabled(True)
        self.input_browse.setEnabled(True)
        self.output_browse.setEnabled(True)
        self.quality_check_checkbox.setEnabled(True)
        self.flip_brain_checkbox.setEnabled(True)
        self.low_memory_checkbox.setEnabled(True)

        # check if batch mode is not enabled
        if not self.batch_mode_checkbox.isChecked():
            
            # pop up a message box
            QtWidgets.QMessageBox.information(self, "Registration Finished", "Registration finished check the output directory for the registered file: {}_deformed.nii.gz".format(os.path.splitext(os.path.basename(self.input_textbox.text()))[0]))

            # ask the user if they want to warp other channels
            reply = QtWidgets.QMessageBox.question(self, "Warp Other Channels", "Do you want to warp other channels?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
            if reply == QtWidgets.QMessageBox.Yes:
                # create a list with the files to send to warping gui
                output_directory = os.path.dirname(self.output_textbox.text()+"/")
                target_file = os.path.join(output_directory, os.path.splitext(os.path.basename(self.input_textbox.text()))[0]+"_deformed.nii.gz")
                warp_file = os.path.join(output_directory, os.path.splitext(os.path.basename(self.input_textbox.text()))[0]+"_Warp.nii.gz")
                inverse_warp_file = os.path.join(output_directory, os.path.splitext(os.path.basename(self.input_textbox.text()))[0]+"_InverseWarp.nii.gz")
                affine_file = os.path.join(output_directory, os.path.splitext(os.path.basename(self.input_textbox.text()))[0]+"_Affine.txt")
                was_flipped = "flipped" if self.flip_brain_checkbox.isChecked() else "not_flipped"
                print(output_directory, target_file, warp_file, inverse_warp_file, affine_file, was_flipped)
                # make sure the files exist
                if not os.path.exists(target_file) or not os.path.exists(warp_file) or not os.path.exists(inverse_warp_file) or not os.path.exists(affine_file):
                    QtWidgets.QMessageBox.warning(self, "Warning", "Some files are missing. Please check the output directory.")
                    target_file = "MISSING" if not os.path.exists(target_file) else target_file
                    warp_file = "MISSING" if not os.path.exists(warp_file) else warp_file
                    inverse_warp_file = "MISSING" if not os.path.exists(inverse_warp_file) else inverse_warp_file
                    affine_file = "MISSING" if not os.path.exists(affine_file) else affine_file
                # use os.system to run the warping gui
                os.system("poetry run python scripts/UI_warp.py "+output_directory+" "+target_file+" "+warp_file+" "+inverse_warp_file+" "+affine_file+" "+was_flipped)
            else:
                return
        
        
    # function to update the terminal
    def update_terminal(self, text):
        self.terminal.append(text)

class RegistrationWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(str)

    def __init__(self, registration_commands, flip_brain_commands, output_directory, intermediate_files):
        super().__init__()
        self.registration_commands = registration_commands  # Support multiple commands
        self.flip_brain_commands = flip_brain_commands
        self.output_directory = output_directory
        self.intermediate_files = intermediate_files

    def run_registration(self):
        # Flip the brain if required
        if len(self.flip_brain_commands) > 0:
            self.progress.emit("Flipping the brain...")
            self.progress.emit("")
            for command in self.flip_brain_commands:
                self.progress.emit(command)
                os.system(command)
                self.progress.emit("")

        # Execute each registration command
        for idx, command in enumerate(self.registration_commands):
            self.progress.emit(f"Running registration step {idx + 1}/{len(self.registration_commands)}...")
            self.progress.emit("")
            self.progress.emit(command)
            os.system(command)
            self.progress.emit("")

        # Move temporary files
        self.progress.emit("Move temporary files...")
        cwd = os.getcwd()
        current_time = time.time()
        tmp_folder = filter(lambda x: os.path.isdir(x) and x.startswith("tmp"), os.listdir(cwd))
        tmp_folder = filter(lambda x: os.stat(x).st_ctime > current_time, tmp_folder)
        tmp_folder = sorted(tmp_folder, key=lambda x: os.stat(x).st_ctime)
        if len(tmp_folder) > 0:
            tmp_folder = tmp_folder[0]
            self.progress.emit("mv " + tmp_folder + " " + self.output_directory)
            os.system("mv " + tmp_folder + " " + self.output_directory)
            if len(self.intermediate_files) > 0:
                self.intermediate_files.append(os.path.join(self.output_directory, tmp_folder))
            self.progress.emit("")

        # Move additional output files
        self.progress.emit("Moving additional output files...")
        cwd = os.getcwd()
        cfg_files = filter(lambda x: os.path.isfile(x) and x.endswith(".cfg"), os.listdir(cwd))
        nii_files = filter(lambda x: os.path.isfile(x) and x.endswith(".nii.gz"), os.listdir(cwd))
        cfg_files = filter(lambda x: os.stat(x).st_ctime > current_time, cfg_files)
        cfg_files = sorted(cfg_files, key=lambda x: os.stat(x).st_ctime)
        nii_files = filter(lambda x: os.stat(x).st_ctime > current_time, nii_files)
        nii_files = sorted(nii_files, key=lambda x: os.stat(x).st_ctime)
        if len(cfg_files) > 0:
            cfg_files = cfg_files[0]
            self.progress.emit("mv " + cfg_files + " " + self.output_directory)
            os.system("mv " + cfg_files + " " + self.output_directory)
            if len(self.intermediate_files) > 0:
                self.intermediate_files.append(os.path.join(self.output_directory, cfg_files))
            self.progress.emit("")
        if len(nii_files) > 0:
            nii_files = nii_files[0]
            self.progress.emit("mv " + nii_files + " " + self.output_directory)
            os.system("mv " + nii_files + " " + self.output_directory)
            if len(self.intermediate_files) > 0:
                self.intermediate_files.append(os.path.join(self.output_directory, nii_files))
            self.progress.emit("")

        # Remove intermediate files
        if len(self.intermediate_files) > 0:
            self.progress.emit("Removing intermediate files...")
            for file in self.intermediate_files:
                if file.endswith("_out.log") or file.endswith("_err.log"):
                    if not os.path.exists(file):
                        continue
                    error_file = file[:-8] + "_err.log"
                    if not os.path.exists(error_file):
                        continue
                    if os.stat(error_file).st_size == 0:
                        if os.path.exists(file[:-8] + "_out.log"):
                            self.progress.emit("Removing " + file[:-8] + "_out.log")
                            os.remove(file[:-8] + "_out.log")
                            self.progress.emit("")
                        self.progress.emit("Removing " + error_file)
                        os.remove(error_file)
                        self.progress.emit("")
                else:
                    if os.path.isdir(file):
                        self.progress.emit("Removing " + file)
                        os.system("rm -rf " + file)
                        self.progress.emit("")
                    else:
                        self.progress.emit("Removing " + file)
                        os.remove(file)
                        self.progress.emit("")

        self.progress.emit("Registration finished.")
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



