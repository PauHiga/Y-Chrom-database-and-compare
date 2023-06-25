# Y Chrom Database & Compare
#### Video Demo:  https://youtu.be/_K4S9UMBBnE
#### Description: This is a program designed to extract data (Y Chromosome markers patterns) from tables in .docx files, and save the information as .csv file. Then, the user can input an Y Chromosome pattern and the program checks if it matches any pattern in the .csv file created.

</br>
</br>

### Considerations:
To be able to extract the data from the tables in .docx file, I needed to consider how the data was presented in such tables. 

I made this program thinking in a real life case we had at my former job. 
The tables with the information were presented in two formats (with the information contained in two or three rows, this was because were files used for printing and the whole pattern was too wide to be visualized in a single row). 


![table format](https://github.com/PauHiga/Y-Chrom-database-and-compare/blob/main/images/table-examples.png)


I designed my program to be able to extract the information from that formats. 
It can also extract the information if the Y chromosome pattern is displayed in more or less rows, or if the markers are in different order. But for the comparison part to work, the table's headers should be (case insensitive): 'MUESTRA', 'DYS576','DYS389I', 'DYS448', 'DYS389II', 'DYS19', 'DYS391', 'DYS481', 'DYS549', 'DYS533', 'DYS438', 'DYS437', 'DYS570', 'DYS635', 'DYS390', 'DYS439', 'DYS392', 'DYS643', 'DYS393', 'DYS458', 'DYS385A/B', 'DYS456' and'Y-GATA-H4'.
Once the data is normalized in .csv files, it can be saved in a database in a further step of this project
