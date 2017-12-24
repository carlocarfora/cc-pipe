# CC-Pipe

## Overview
CC-pipe is a general pipeline for solo/personal projects that provides a 
framework for organisation while trying not to get in the way of exploration or 
enforcing too many rules.


## Scenarios

Mr Home CG Artist wants to start a new project at home, so he fires up 
Houdini to start working and before long he's got a messy folder structure 
with files called "this_was_cool_v03" and "not_working_v05". He needs a way 
to organise his work without letting the details of where everything goes 
become too laborious. This is where he needs a pipeline so everything can be 
labelled neatly and he no longer needs to worry about what render was made from 
which file.


## Goals / Features

A list of the features it will support:

* Will not get in the way of the artist
* Houdini / Mantra / Nuke support
* Generic software support (minimal)
* Stand alone launcher
* Sets up software environment
* Standard folder structure
* Shot based pipeline
* Customisable 
* Version control
* Automate tedious things in software such as:
  * File paths
  * Render versioning
  * Folder creation
* Helper scripts to automate outputs to web, gif, etc.


## Non-Goals

Features that I am not looking to target / implement:

* Supporting other software packages in detail
* Project/task planning
* Asset management 
* Users
* Official multiple OS support 
* Publishing/dependency system (publish rigs to be used across shots etc.)

## Details

This is an overview of the pipeline, it is organic and will be updated 
accordingly as the project develops:

### Folder Structure

General folder structure is shot based then software based:

Projects
	ProjectName
		Shot
			Software (uses 3 letter acronym)
				Task
					<software folder structure>


Here is an example using named directories:

Projects
	SuperAmazingFilm
		Sh001
			Hou
				LookDev
					<houdini folder structure>
				Render
					<houdini folder structure>
			Nuke
				comp
					<nuke folder structure>
				precomp
					<nuke folder structure>

There is no hard and fast rule on shot names, but there will be a general 
guideline written up that suggests some logical workflow.

Shots can be used as general store folders, here's an example where the shot is 
called Build and assets can be created in this folder:

Projects
	ProjectName
		Build
			AssetName
				<assets go here>



#### Houdini Folder Structure

The folder structure for Houdini will be lifted from the default structure 
that they use, with an added folder for hip files. This means it's easy to 
move across somewhere without cc-pipe.

Projects
	SuperAmazingFilm
		Sh001
			Hou
				LookDev
					abc
					audio
					comp
					desk
					flip
					geo
					hda
					hip
					render
					scripts
					sim
					tex
					video


#### Nuke Folder Structure

The Nuke folder structure is created from experience working in various studios 
and tries to strike a balance between organisation and micro-management.

Projects
	SuperAmazingFilm
		Sh001
			Nuk


#### General Software Folder Structure

Using the folder structure we can adapt it to include any extra software that 
might be used on a project. It's as simple as adding a new folder under the 
shot named after the software. The pipeine will not support it any further than 
this though (version control of files, etc.).

Projects
	SuperAmazingFilm
		Sh001
			<any software here>


### Interface

cc-pipe will be launched as a GUI, it will allow the user to see all projects 
at a top level and launch the relevant software for each.

<insert some interface drawings here>


### Environments

Software will be configured so that each project folder serves as the root 
environment for scripts, etc.

### Data

There will need to be data recorded for various parts of the pipeline. This is 
a rough outline of what might be needed and there will be more added as the 
need arises. Data will be stored as yaml files throught cc-pipe for easy 
reading and parsing.

#### Data Folder Structure

One central data folder for all data files, there will be a file for each 
project and this file will hold all the data needed. Data files will be 
larger but this will avoid file bloat across the project. 

There will need to be data stored for the pipeline, per project and also per 
shot. These will be stored in folders prefixed with a . so they are not visible 
but easiliy accessed.

.data (pipeline data)
	<data files here>
Projects
	ProjectName
		.data (project data)
			<data files here>
		Shot
			Software (uses 3 letter acronym)
			.data (software data)
				<data files here>
				Task
					<software folder structure>


#### Pipeline Data

cc-pipe/.data

* Pipeline version
* Pipeline root file path 

Projects/ProjectName/.data

 * Project name
 * Resolution
 * FPS
 * Project Paths

cc-pipe/Projects/ProjectName/Shot/Software/.data

 * Software specific data


### Software Integration

#### Houdini

cc-pipe will be integrated into Houdini in the form of menu items that 
enable easy version saving. It will also automatically path, name and version 
nodes that require doing so such as cache and write nodes.

Mantra will have outputs automatically filled in with the correct path to save 
renders.


#### Nuke

Nuke will have outputs filled in with the correct paths to enable easy 
verisoning when updating shots.