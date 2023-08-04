OpenDSS Scientific Visualization Project
--------------------
This Python package contains a collection of functions for analysis and visualization of data produced by the [OpenDSS](https://sourceforge.net/p/electricdss/wiki/Home) software application. OpenDSS is an electric power Distribution System Simulator (DSS) designed to support distributed energy resource (DER) grid integration and grid modernization. It enables engineers to perform complex analyses using a flexible, customization, and easy to use platform intended specifically to meet current and future distribution system challenges and provides a foundation for understanding and integrating new technologies and resources. More information on OpenDSS can be found in the Reference Guide (Dugan & Montenegro, 2020). OpenDSS (the Delphi version) that runs on a Windows operating system is available (Electric Power Research Institute, 2022) along with a PowerPoint tutorial (Fu, 2019). 

This package written in the Python computer language provides a set of functions for conveniently accessing and plotting the data in the Comma-Separated Value (CSV) files output by OpenDSS. 

Features
---------------------
- Remains to be listed.

Installation
---------------------
To install the package simply use the pip3 command: (REMAINS TO BE DONE)

`% pip3 install OpenDSS_SciVis`

If you are upgrading the package then include the upgrade option:

`% pip3 install OpenDSS_SciVis --upgrade`

Note that the OpenDSS_SciVis package now only supports Python 3. 

Example Scripts
---------------------
Refer to the "Examples" folder for a collection of example Python scripts showing how to produce plots in a variety of formats from the OpenDSS CSV files as described in the [Wiki Home page](https://github.com/kevinwuw/OpenDSS_SciVis/wiki). There are multiple examples of time series that progress from very simple to more customized figures. These series of examples provide an easy tutorial on how to use the various options of the plotting functions. They also provide a quick reference in future for how to produce the plots with specific features. 

Example Plots
---------------------
The plots produced by the example scripts are in Portable Network Graphics (PNG) format and have the same file name as the script with a `.png` suffix. The PNG files created can be viewed by following the links shown below. This is a useful starting point for users looking to identify the best example from which to begin creating a diagram for their specific need by modifying the accompanying Python script.

[Time Series Plots](http://github.com/kevinwu/OpenDSS_SciVis/wiki/Time-Series-Examples)

Here is a sample of the plots you'll find in the above examples: (REMAINS TO BE DONE)

FAQ
---------------------
A list of Frequently Asked Questions ([FAQ](https://github.com/kevinwuw/OpenDSS_SciVis/wiki/FAQ)) is maintained on the Wiki. Users are encouraged to look there for solutions to problems they may encounter when using the package. 

How to cite OpenDSS_SciVis
---------------------
Kevin Wu and Peter A. Rochford (2023) OpenDSS_SciVis: A Python package for scientific visualization of results from the OpenDSS electric power Distribution System Simulator (DSS), http://github.com/kevinwuw/OpenDSS_SciVis

```
  @misc{wuskillmetrics, 
    title={OpenDSS_SciVis: A Python package for scientific visualization of results from the OpenDSS electric power Distribution System Simulator (DSS)}, 
    author={Levin Wu, Peter A. Rochford}, 
    year={2023}, 
    url={http://github.com/kevinwuw/OpenDSS_SciVis}, 
```

Guidelines to contribute
---------------------
1. In the description of your Pull Request (PR) explain clearly what it implements/fixes and your changes. Possibly give an example in the description of the PR. 
2. Give your pull request a helpful title that summarises what your contribution does. 
3. Write unit tests for your code and make sure the existing [backward compatibility tests](http://github.com/kevinwu/OpenDSS_SciVis/wiki/Backward-Compatibility-Testing) pass. 
4. Make sure your code is properly commented and documented. Each public method needs to be documented as the existing ones.

References
---------------------
Dugan, R. C., & Montenegro, D. (2020). The Open Distribution System Simulator (OpenDSS) Reference Guide. Electric Power Research Institute. Washington, DC: Electric Power Research Institute. Retrieved from https://sourceforge.net/p/electricdss/code/HEAD/tree/trunk/Distrib/Doc/OpenDSSManual.pdf

Electric Power Research Institute. (2022, April 2). OpenDSS. Retrieved from EPRI: https://www.epri.com/pages/sa/opendss

Fu, F. (2019). OpenDSS Tutorial and Cases. Iowa State University, Department of Electrical and Computer Engineering. Ames, Iowa: Iowa State University. Retrieved from https://www.coursehero.com/file/87693420/EE653-OpenDSS-Tutorial-and-Casespptx
