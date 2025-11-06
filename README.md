# Kronauer Lab - Ooceraea biroi CNS Brain Template 2025

![ants](https://www.rockefeller.edu/research/uploads/www.rockefeller.edu/sites/8/2017/12/clonal_ants7-2400x800.png)

This repository contains the protocol to generate a 3D template of the brain of the ant *Ooceraea biroi* (Clonal Raider Ant) from anti-Synapsin1 stained confocal stacks of the ant brain (α-SYN A647 marker) imaged at the [Kronauer Lab](https://www.rockefeller.edu/research/2280-kronauer-laboratory/) at the [Rockefeller University](https://www.rockefeller.edu/). The brains were imaged at 0.13 μm x 0.13 μm x 0.29 μm.

## Protocol for generating the template

### 1. Install ANTs Software for image registration

The ANTs software can be downloaded from [here](https://github.com/ANTsX/ANTs), you will need to use [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install) to run the ANTs software on [Windows](https://github.com/ANTsX/ANTs/wiki/Compiling-ANTs-on-Windows-10). The ANTs software is also available on [Mac and Linux](https://github.com/ANTsX/ANTs/wiki/Compiling-ANTs-on-Linux-and-Mac-OS).

### 2. Clone this repository

Make sure you have [git](https://git-scm.com/) installed on your computer. Then clone this repository by running the following command in your terminal:

```
git clone https://github.com/neurorishika/ant_template_builder.git 
```

### 3. Place the pre-processed images in the `cleaned_data/whole_brain` folder

The pre-processed images should be in the `.nrrd` format. NRRD stands for Nearly Raw Raster Data, and is a file format designed to store and visualize medical image data. The images should be in the same orientation. Please use [Fiji](https://imagej.net/Fiji/Downloads) to reorient the images if they are not in the same orientation. Also preferably the images should be 8-bit. This is not necessary but recommended.

### 4. Install poetry and build the environment

[Poetry](https://python-poetry.org/) is a tool for dependency management and packaging in Python. To install poetry, follow the instructions [here](https://python-poetry.org/docs/#installation). Once poetry is installed, open a linux terminal (wsl for windows and bash for Mac/Linux) and navigate to the `ant_template_builder` folder. Then run the following command to build the environment:

```
poetry install
```

### 5. Install PyQT5

To run the GUI for Registration, you will need to install the PyQT5 library. First, make sure all the dependencies are installed by running the following command:

```
sudo apt-get update
sudo apt-get install '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev libfontconfig1-dev 
sudo apt-get install ffmpeg libsm6 libxext6
```

Next open the environment by running the following command:

```
poetry shell
```

Install the PyQT5 library by running the following command:

```
pip install pyqt5
```

### Run the mirroring script

If you want to generate mirrored images to include in the template, you can run the mirroring script. To run the mirroring script, run the following command in the terminal (make sure you are in the `ant_template_builder` folder).

```
poetry run python scripts/mirror.py
```

By default, the script will look for data (*.nrrd files) in the `cleaned_data/whole_brain` folder and generate mirrored images in the same folder. You can use "--help" to see the options for the script, including the option to change the input and output folders. Also it will replace any mirrored images that already exist in the output folder unless the -skip flag is set as True.

```
poetry run python scripts/mirror.py --help
```

### 5. Run the resampling script

To run the resampling script, run the following command in the terminal (make sure you are in the `ant_template_builder` folder).

```
poetry run python scripts/resample.py
```

By default, the target resolution is an isotropic resolution of 0.8 μm. You can use "--help" to see the options for the script, including the option to change the target resolution to a different value (potentially anisotropic). The script will generate the resampled images in the `resampled_data/whole_brain` folder by default. You can use "--help" to see the options for the script, including the option to change the input and output folders. 

```
poetry run python scripts/resample.py --help
```

### 6. Run the asymmetrize script

The ant brain has a notable asymmetry in the medial lobe of the mushroom body. Therefore, it is recommended to use only the brains that are oriented in one direction and use the mirror reflections for the others. You can do this by having a whole_brain_metadata.csv (as in this repository) file. The metadata file must have two columns: `Clean Name` and `Egocentric Leaning` where the first is name of the file, and the second has values of `left` or `right` (or `sym` (symmetric) if a determination cannot be made). The script will only mirror the brains that have `left` or `right` in the `Egocentric Leaning` column depending on the -lr flag. Ideally, mirror and resample ALL the brains (unless disk space is an issue) and then use the asymmetrize.py script to filter it down to the brains that are oriented in one direction.

To run the asymmetrize script, run the following command in the terminal (make sure you are in the `ant_template_builder` folder).

```
poetry run python scripts/asymmetrize.py
```

By default, the script will look for data (*.nrrd files) in the `resampled_data/whole_brain` folder and generate asymmetrized images in the same folder. It will also backup the original images in the backup folder. You can use "--help" to see the options for the script, including the option to change the input, output and backup folders. This requires the whole_brain_metadata.csv file described above to be present and linked using the -m flag.

```
poetry run python scripts/asymmetrize.py --help
```

OPTIONAL LEGACY FEATURE: By default, the asymmetrize script will keep the symmetric brains in their original orientation. However this can reduce the final template quality. We therefore have an additional flag -q or --quality_affine that will copy all the symmetric brains into a diff_folder which will NOT be used for creating the initial affine template, but used for the final template. This may improve the quality of the final template. If quality affine is set to True, the metadata file must also include a column called 'Skip Affine' with values of 0 or 1. If the value is 1, the brain will be skipped for affine registration. This is useful for brains that of a poor quality and should not be used for affine registration (this is excluding the symmetric brains which are automatically skipped for affine registration).

ADDITIONAL NOTE: You can also reset the folder to the original state by running the following command:

```
poetry run python scripts/reset_symmetry.py
```

By default, this will fix the `resampled_data/whole_brain` folder. You can use "--help" to see the options for the script, including the option to change the input folder.

```
poetry run python scripts/reset_symmetry.py --help
```

### 6. Run the registration script

The bash script for running the registration is in the `group_registration` folder. To run the script, navigate to the `group_registration` folder and run the following command:

```
./run_whole_brain_registration_mtc.sh
```

for using the more updated antsMultivariateTemplateConstruction.sh script from ANTs. Alternatively, you can run:

```
./run_whole_brain_registration_btp.sh
```
to use the legacy buildtemplateparallel.sh which is now quasi-deprecated (see:[https://github.com/ANTsX/ANTs/issues/791](https://github.com/ANTsX/ANTs/issues/791)).

As of right now, both codes generate are set up to generate virtually identical results.

Once the registration is complete, the final results will be in the 'results/obiroi_cns_<mtc/btp>_YYYYMMDD_HHMM' folder, all intermediate information will be inside the 'affine' and  'syn' subfolders. The final template will be in the 'results/obiroi_cns_<mtc/btp>_YYYYMMDD_HHMM/complete_template<0>.nrrd' file. Note that this template will be in the same orientation and resolution as the input images. To generate videos or a higher resolution template, please see the next section.


## Generate a different resolution template from a generated template

To generate a different resolution template from a generated template, you can use the `template_resample.py` script. To run the script, navigate to the `ant_template_builder` folder and run the following command:

```
poetry run python scripts/template_resample.py
```

By default, the script will look for the latest obiroi_brain_YYYYMMDD_HHMM folder in the `results` folder and generate a template at 0.8 μm x 0.8 μm x 0.8 μm resolution in the 'final_templates' folder. You can use "--help" to see the options for the script, including the option to change the input and output folders and the target resolution.

```
poetry run python scripts/template_resample.py --help

```

## Using the generated template

A tutorial for registration and warping is available on [YouTube](https://www.youtube.com/watch?v=u3zFSthJ0VI).

[![Watch the video](https://img.youtube.com/vi/u3zFSthJ0VI/maxresdefault.jpg)](https://youtu.be/u3zFSthJ0VI)


### Register a new brain to the template

To register a new brain, we have provided a GUI that can be used to register a new brain to the template. To run the GUI, navigate to the `ant_template_builder` folder and run the following command:

```
./run_registration_gui.sh
```

### Warp a Segmentation Label / Point Set / Different Channel to the Template

To warp a segmentation label, point set or a different channel to the template, we have provided a GUI that can be used to warp the segmentation label, point set or a different channel to the template. To run the GUI, navigate to the `ant_template_builder` folder and run the following command:

```
./run_warping_gui.sh
```

### (Optional) Generate a video of the final template

The best way to generate a video of the final template is to use [Fiji](https://imagej.net/Fiji/Downloads). Open the final template in Fiji and then go to Save As > Save as AVI or Save as Animated GIF.

## Setup on RU HPC Cluster

### 1. Get an account on the HPC cluster

Contact the [HPC team](https://hpc.rockefeller.edu/contact) to get an account on the HPC cluster. They will give you the instructions to connect to the cluster via ssh.

### 2. Access the HPC cluster via ssh and setup Spack, ANTs and Conda

Once you have an account on the HPC cluster, you can access the cluster via ssh. You can use the following command to access the cluster:

```
ssh -l <username> login<node>-hpc.rockefeller.edu
```

Once you are logged in, you can setup Spack by adding the following lines to your `.bashrc` file:

```
# Spack
SPACK_RELEASE=spack_2020b
source /ru-auth/local/home/ruitsoft/soft/spackrc/spackrc.sh
```

Latest instructions for setting up Spack can be found [here](https://hpcguide.rockefeller.edu/guides/spack.html)

Restart your terminal and run the following command to initialize Spack:

```
lmodinit
```

Load the modules needed for building ANTs:

```
module load gcc/10.2.0-h4gobj
module load cmake/3.17.3-3rjy3k
```

Note: You can cross-reference the modules available on the HPC cluster using ```module avail gcc``` and ```module avail cmake``` with the suggested versions for compiling ANTs as mentioned [here](https://github.com/ANTsX/ANTs/wiki/Compiling-ANTs-on-Linux-and-Mac-OS), and choose the most appropriate version.

Install ANTs using the instructions [here](https://github.com/ANTsX/ANTs/wiki/Compiling-ANTs-on-Linux-and-Mac-OS). When configuring using CMake, make sure to have BUILD_ALL_ANTS_APPS as ON.

Then follow the instructions [here](https://hpcguide.rockefeller.edu/guides/conda.html) to setup Conda. Once you have setup Conda, you can create a new environment for running the ANTs software by running the following command:

```
conda create -n ants python
conda activate ants
```

Then you can install poetry by running the following command:

```
curl -sSL https://install.python-poetry.org | python3 -
```

Newer instructions for installing poetry can be found [here](https://python-poetry.org/docs/#installation).

### 3. Setup the Pipeline

Follow the instructions from step 2 in the previous section to complete the setup. It is preferred to setup the repository in the scratch folder on the HPC cluster for the lab. For the Kronauer lab, the scratch folder is located at `/rugpfs/fs0/kron_lab/scratch/<username>`.

An easy way to deal with scratch is to use a symlink to the scratch folder from your home directory. To do this, run the following command:

```
ln -s /rugpfs/fs0/kron_lab/scratch/<username> ~/scratch
```

Then you can navigate to the scratch folder by using the following command:

```
cd ~/scratch
```

Then you can clone the repository by running the following command:

```
git clone https://github.com/neurorishika/ant_template_builder.git 
```

Go inside the `ant_template_builder` folder and run the following command to build the environment:

```
poetry install
```

### 4. Run the template generation pipeline

At this point, you should have the ANTs software installed and the environment setup. You can now run the template generation pipeline as described in the previous section. The only difference is that you will have to requisition a node on the HPC cluster to run the registration. 

RECOMMENDED PARTITIONS ON RU HPC CLUSTER(AS OF DEC 2023):
1. bigmem (for running the template generation pipeline with a massive dataset with maximum parallelization)
2. hpc_a10 (for running the template generation pipeline with a small dataset with maximum parallelization or a medium dataset with moderate parallelization (recommended for most cases))

#### TIPS for running the python scripts on the HPC cluster

##### Copying data to and from the HPC cluster

Copy data from your local computer to the HPC cluster using `scp` or `rsync`. For example, to copy the data from your local computer to the HPC cluster, run the following command:

```
rsync -avz <local_folder> <username>@login04-hpc.rockefeller.edu:/rugpfs/fs0/kron_lab/scratch/<username>/<remote_folder>
``` 

Copy data from the HPC cluster to your local computer using `scp` or `rsync`. For example, to copy the data from the HPC cluster to your local computer, run the following command:

```
rsync -avz <username>@login04-hpc.rockefeller.edu:/rugpfs/fs0/kron_lab/scratch/<username>/<remote_folder> <local_folder>
```
In most cases you will either need to copy the cleaned data to the HPC cluster or copy the final template from the HPC cluster to your local computer.

##### Running the python scripts on the HPC cluster

Use `screen` to run the python scripts on the HPC cluster using interactive mode. This will allow you to run the scripts in the background and disconnect from the HPC cluster without interrupting the scripts. First connect to the HPC cluster using ssh and then run the following command:

```
screen -S <screen_name>
```

Check which partitions have nodes that are idle by running the following command:

```
sinfo | grep idle
```

If you find a hpc_a10 or bigmem partition that has idle nodes, start a new interactive session on the HPC cluster on an exclusive node by running the following command:

```
srun -p <hpc_a10 or bigmem> --time=<however long you need in DD-HH:MM:SS format> --exclusive --pty -i /bin/bash
```

Once you are on the node, navigate to the scratch folder and start the python scripts of your choice as described in the previous section. Once the scripts are running, you can disconnect from the HPC cluster by pressing `Ctrl + A + D`. To reconnect to the screen, run the following command:

```
screen -r <screen_name>
```

Regularly check the status of the scripts by reconnecting to the screen and checking the status of the scripts. Once the scripts are complete, you can exit the screen by pressing `Ctrl + D`.

## Guidelines for cleaning data

### For template generation

These guidelines are for cleaning the data for template generation. The data should be cleaned in the following order:

1. Open the raw confocal stacks (*.czi file) exported from Zen in Fiji.

2. Check the mounting orientation of the brain. The preferred mounting orientation is the anterior side up, such that as you move from Z=0 to Z=Max, you move from the anterior to the posterior side of the brain. Sometimes, the mounting orientation is incorrect, so you will need to rearrange the stacks in the reverse order. You can do this by going to Image > Stacks > Tools > Reverse. If you do so, remember to get the correct left-right orientation; the brain needs to be left-right flipped. DO NOT FLIP THE BRAIN USING THE FLIP COMMAND IN FIJI. This is incompatible with ANTs.  KEEP A NOTE OF THESE FILES, I.E., WHICH NEED TO BE FLIPPED.

3. Make sure the brain is in the correct orientation, i.e., the dorsal side to the top and the ventral side to the bottom in each stack. If the brain is not in the proper orientation, you can rotate the brain by going to Image > Transform > Rotate. Make sure to rotate the brain in the correct direction. If you turn the brain in the wrong direction, you will need to rotate the brain in the opposite direction to get the proper orientation.

4. Normalize the intensity of the image by going to Process > Enhance Contrast. Check the Normalize option, Use stack histogram, Process all slices, and set the saturated pixels to 0.0.

5. To save data, you can change the type of the image to 8-bit by going to Image > Type > 8-bit. This is optional but recommended.

6. If there are multiple channels, you can split the channels by going to Image > Color > Split Channels. Then you can save the channels as separate files. The SynA647 (Synapsin1) channel is used for registration. The other channels warped to the template can be used for visualization, but only the SynA647 channel is used for template generation.

7. Save the image as an NRRD file by going to File > Save As > NRRD. The files should be saved under `cleaned_data/whole_brain`. The preferred naming convention is as follows:  <Channel Type>_<Author Initials>_<Brain ID>_<Date>. The channel type for the template construction pipeline should be `synA647`. For example, if the brain ID is `OB-1`, the date is `2024-01-01`, and the author is Rishika Mohanta, the file name should be `synA647_RM_OB-1_20240101.nrrd`. The date should be in the YYYYMMDD format. Try to keep the file names as short as possible. Files that need to be flipped to account for mounting orientation should be kept in a subfolder named `to_flip` inside the `cleaned_data/whole_brain` folder.

8. Run the mirror.py script to generate the mirrored images. Navigate to the `ant_template_builder` folder and run the following command:

```
poetry run python scripts/mirror.py -i cleaned_data/whole_brain/to_flip -o cleaned_data/whole_brain
```

The new files will have `_mirror` appended to the file name. For example, if the original file name was `synA647_RM_OB-1_20240101.nrrd`, the new file name will be `synA647_RM_OB-1_20240101_mirror.nrrd`. You can remove the `_mirror` from the file name. Also, feel free to remove the files in the `to_flip` folder once you are done.

9. The last step is to reopen the files in Fiji and to note the type of the brain by looking at the medial lobe of the mushroom body. Take a look at the section titled "Determining the Asymmetry of the Brain" for more details. Keep track of the filename and the egocentric leaning in a .csv file under `Clean Name` and `Egocentric Leaning` and save them as whole_brain_metadata.csv at the root of this repository.

### For Segmentation

For Segmentation, first follow the same steps for cleaning the data as for template construction except the last step which is not needed. Further, don't save the files in the cleaned data folder; create a new folder to keep all the data, lets call it the "segmentation_folder" and place the cleaned data under a subfolder called "cleaned_data"

1. Resample the brains using the resample.py script. Determine a reasonable isometric resolution to segment at since unnecessarily higher resolutions can lead to instability for manual segmentation using Amira. A good target resolution is 0.8x0.8x0.8 um (i.e., the template resolution). Navigate to the `ant_template_builder` folder and run the following command:

```
poetry run python scripts/resample.py -i /path/to/segmentation_folder/cleaned_data -o /path/to/segmentation_folder/ -v 0.8x0.8x0.8
```

2. Open the image in Amira and setup the following textures:

FOR TEMPLATE EVALUATION:

| Texture Name | Texture Value | How to setup     |
| ------------ | ------------- | ---------------- |
| Outside      | 0             | Default          |
| Inside Brain | 1             | Lindsey's Recipe |
| AL (Left)    | 2             | Manual           |
| AL (Right)   | 3             | Manual           |
| MB (Left)    | 4             | Manual           |
| MB (Right)   | 5             | Manual           |
| Central Body | 6             | Manual           |

FOR TEMPLATE SEGMENTATION:

| Texture Name           | Texture Value | How to setup    |
| ---------------------- | ------------- | --------------- |
| Outside                | 0             | Default         |
| Inside Brain           | 1             | Lindsey's Recipe|
| AL (L)                 | 2             | Manual          |
| AL (R)                 | 3             | Manual          |
| Medial MB Calyx (L)    | 4             | Manual          |
| Medial MB Calyx (R)    | 5             | Manual          |
| Lateral MB Calyx (L)   | 6             | Manual          |
| Lateral MB Calyx (R)   | 7             | Manual          |
| MB Peduncle + Lobes (L)| 8             | Manual          |
| MB Peduncle + Lobes (R)| 9             | Manual          |
| Medulla (L)            | 10            | Manual          |
| Medulla (R)            | 11            | Manual          |
| Lobula (L)             | 12            | Manual          |
| Lobula (R)             | 13            | Manual          |
| Protocerebral Bridge   | 14            | Manual          |
| Nodule (L)             | 15            | Manual          |
| Nodule (R)             | 16            | Manual          |
| Central Body Upper     | 17            | Manual          |
| Central Body Lower     | 18            | Manual          |

3. Use the paintbrush tool to manually segment the brain. Use the textures to keep track of the different regions. The textures are used to keep track of the different regions and are not used for segmentation. The segmentation is done using the paintbrush tool and the wand tool. Save the project and the segmentation at regular intervals.

4. Once segmentation is complete, export the segmentation as a TIFF file. Sometimes the voxel information is lost in the process of exporting the segmentation. To fix this, open the segmentation in Fiji and go to Image > Properties and set the voxel size to the correct value. Then save the segmentation as a NRRD file by going to File > Save As > NRRD. The files should be saved under `segmentation_folder/segmentation`. The preferred naming convention is as follows:  <Channel Type>_<Author Initials>_<Brain ID>_<Date>_segmented. The channel type for the template construction pipeline should be `synA647`. For example, if the brain ID is `OB-1`, the date is `2024-01-01`, and the author is Rishika Mohanta, the file name should be `synA647_RM_OB-1_20240101_segmented.nrrd`. The date should be in the YYYYMMDD format. Try to keep the file names as short as possible.

## Determining the Asymmetry of the Brain

### When it is clearly Asymmetric

![Clearly Asymmetric](https://raw.githubusercontent.com/neurorishika/ant_template_builder/main/tutorial/clearly_asymmetric.png)
 
Look at the point where the two hemispheres of the mushroom body meet. If there is an apparent tilt towards the left/right (from your viewpoint in the stack) due to one hemisphere of the Medial Lobe being larger and more dorsal to the other, mark them as egocentric right/left accordingly (since we are looking from the front of the animal, anterior to posterior, the egocentric leaning is the opposite of what we see). 

![Clearly Asymmetric Labelled](https://raw.githubusercontent.com/neurorishika/ant_template_builder/main/tutorial/clearly_asymmetric_labelled.png)

### When it is hard to identify the Asymmetry

![Barely Asymmetric](https://raw.githubusercontent.com/neurorishika/ant_template_builder/main/tutorial/barely_asymmetric.png)

Sometimes, the leaning/dominance of the hemisphere is a little unclear; at that point, you can adjust the brightness using the Fiji brightness/contrast tool to see if the tilt is more evident. Focus on the area slightly posterior to the first point of contact when going from anterior to posterior. Two sub-lobe-like structures can be seen at this point. Note that the one that is higher up at the dorsal edge of the mushroom body's medial lobe, right under the central body, is likely the dominant lobe. Another way to look at it is the boundary of the sub-lobes on the less dominant side meets the other hemisphere on the L/R boundary. If the left side is more prominent and higher up from your viewpoint, the effective leaning is right-leaning, and therefore, the brain is egocentric left-leaning and vice versa.

![Barely Asymmetric Labelled](https://raw.githubusercontent.com/neurorishika/ant_template_builder/main/tutorial/barely_asymmetric_labelled.png)
