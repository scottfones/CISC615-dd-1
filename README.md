Familiarize yourself with the delta-debugging and the code by working through the book chapter: https://www.debuggingbook.org/html/DeltaDebugger.html

Once you have done that, you can attempt to apply delta debugging in a more realistic context.

XMLProc is a small XML parser written in Python. It has a small defect. To exhibit the defect, follow these steps:

1. Download the zip file: `dd.zip Download dd.zip`
2. In the project, the file `xpcmd.py` is a command-line interface to the XML parser.
3. To see a successful run type:

```bash
$ python3 xpcmd.py xmlproc/demo/nstest1.xml
```
4. The input file demo/urls.xml causes the parser to fail:

```bash
$ python3 xpcmd.py xmlproc/demo/urls.xml
```
Your goal is to minimize the failure-inducing file using delta debugging. main.py provides a starting point for running delta-debugging. If you run the current version, you will find that while a reduce input is created, it does not reveal the same failure.  Modify the script to address this issue. What is the reduced input that does achieve the failure?

For structured input such as XML working at the character level is less than ideal since many invalid inputs are generated.  Modify the script to work on xml tree elements (the section on Reducing Syntax Trees will be a good place to start).

Submit a copy of your code as well as a brief write-up about your experiences with using delta debugging.