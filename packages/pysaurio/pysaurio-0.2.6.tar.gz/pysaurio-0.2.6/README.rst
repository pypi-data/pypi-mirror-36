Pysaurio
========

This package contains two tools: Raptor & Reptar

Raptor
------

**Raptor** for extracting and displaying information from a set of files of the same type; and creating a single file with all the selected information.
    
The information in the files may be in multiple rows::
    
    PC01.txt:
    User=ms123
    Name=Mayra Sanz
    OS=GNU/Linux
    IP=10.226.140.1
    
But, also, the information may be in several columns. It is possible to read data from multiple fields in a single line::
    
    PC01.log:
    User: ms123     Name: Mayra Sanz
    OS: GNU/Linux   IP: 10.226.140.1        

**Example:** data from the following files::

    PC01.txt:
    User=ms123
    Name=Mayra Sanz
    OS=GNU/Linux
    IP=10.226.140.1

    PC02.txt:
    User=lt001
    Name=Luis Toribio
    OS=GNU/Linux
    IP=10.226.140.2

    PC03.txt:
    User=co205
    Name=Clara Osto
    OS=Win
    IP=10.226.140.3

... You can create a CSV file with the following information::

    users.csv:
    User,Name,OS,IP
    MS123,Mayra Sanz,GNU/linux,10.226.140.1
    LT001,Luis Toribio,GNU/linux,10.226.140.2
    CO205,Clara Osto,Win,10.226.140.3

To achieve this you need to create a template (.rap) with Raptor, which is similar to an INI file with the following information::

    users.rap:
    [General]
    description = Get list of users
    extension = txt
    prefix = PC
    output_folder = txt
    input_folder = txt
    output_file = users.csv
    delimiter = ,
    quotechar = "
    include_header = 1
    include_file = 0
    include_record_num = 0
    include_empty_record = 0    
    search_multiple = 0
    alternate_header =
    search_multiple = 0
    
    [Fields]
    user = User=
    name = Name=
    os = OS=
    ip = IP=
    
    [Rules]
    rule1 = ('user', 'UPPER')                                       

To create .rap template (If the .rap template exists it is not saved). (Caution: field names must be lowercase)::

    from pysaurio import Raptor  
    rap1 = Raptor()       
    rap1.description = 'Get list of users'
    rap1.extension = 'txt'
    rap1.prefix = 'PC'
    rap1.input_folder = 'txt'
    rap1.output_folder = 'txt'
    rap1.output_file = 'users.csv'
    rap1.delimiter = ','
    rap1.quotechar = '"'
    rap1.include_header = '1'
    rap1.include_file = '1'
    rap1.include_record_num = '1'
    rap1.include_empty_record = '0'
    rap1.search_multiple = '0'
    rap1.alternate_header = ''
    rap1.fields['user'] = 'User='
    rap1.fields['name'] = 'Name='
    rap1.fields['os'] = 'OS='
    rap1.fields['ip'] = 'IP='
    rap1.rules.append(('user', 'UPPER'))
    rap1.rules.append(('name', 'REMOVEFROM', ' '))     
    rap1.Save("users.rap")  
    del rap1
    

**Attribute List:**

- description: short descripton of .rap template
- extension: extension of the files to read
- prefix: files must begin with this string
- input_folder: folder of files to read
- output_folder: output folder to save file with result
- output_file: output filename
- delimiter: delimiter character
- quotechar: quote character
- include_header: '0' or '1'
- include_file: '0' or '1'
- inclide_file_datetime: '0' or '1' (file creation & modification date/time)
- include_record_num: '0' or '1'
- include_empty_record: '0' or '1'
- search_multiple: '0' or '1'
- alternate_header: alternative text of the report header
- fields: dictionary with fieldnames and search string (read template)
- record: dictionary with fieldnames and values (read template)
- rules: list of rules (read template)
- list_files: list of filenames to read (auto)
- record_counter: number of records (auto) 
- errors: list of errors (auto)
- number_errors: number of errors after you open or save a template                 

**Functions available for rules:**
        
- rule1 = (fieldname, 'SUBSTR', postion_initial, lenght)
- rule1 = (fieldname, 'REPLACE', 'search_string', 'replace_string')
- rule1 = (fieldname, 'REPLACEALL', 'search_string', 'replace_string')
- rule1 = (fieldname, 'UPPER')
- rule1 = (fieldname, 'LOWER')
- rule1 = (fieldname, 'REVERSE')
- rule1 = (fieldname, 'REMOVE')
- rule1 = (fieldname, 'FIELDISDATA')
- rule1 = (fieldname, 'REMOVEFROM', 'string')
- rule1 = (fieldname, 'REMOVETO', 'string')

Opens template (.rap) and creates (.csv) file from the data read from multiple text files::

    from pysaurio import Raptor
    import csv

    rap2 = Raptor()
    rap2.Open('users.rap')
    if rap2.number_errors == 0:         
        file_csv = open(rap2.output_file, 'w', newline='')
        csv_output = csv.writer(file_csv, 
                                delimiter=rap2.delimiter,
                                quotechar=rap2.quotechar, 
                                quoting=csv.QUOTE_MINIMAL)
        if rap2.include_header == '1':
            fields_list = rap2.BuildHeader()
            print(fields_list)
            csv_output.writerow(fields_list)
                            
        for row in rap2.list_files:
            valid_record, new_record = rap2.BuildRow(row)
            new_record = rap2.ApplyRules(new_record)
            if valid_record:
                new_record = list(new_record.values())
                print(new_record)
                csv_output.writerow(new_record)         
        file_csv.close()            
    else:
        print(rap2.ShowError())
    del rap2


Reptar
------
    
**Reptar** allows merge files, including only the necessary lines.

**Example:** data from the following files::

    PCS01.txt:
    User,Name,OS,IP
    ms123,Mayra Sanz,GNU/Linux,10.226.140.1
    lt001,Luis Toribio,GNU/Linux,10.226.140.2
    co205,Clara Osto,Win,10.226.140.3

    PCS02.txt:
    User,Name,OS,IP
    nn345,Nadia Pacheco,Win,10.226.140.4
    jm401,Juan Madrid,GNU/Linux,10.226.140.5

... You can create a file with the following information::

    Linux.csv:
    User,Name,OS,IP
    MS124,MAYRA SANZ,GNU/LINUX,10.226.140.1
    LT001,LUIS TORIBIO,GNU/LINUX,10.226.140.2
    CO205,CLARA OSTO,WIN,10.226.140.3
    JM401,JUAN MADRID,GNU/LINUX,10.226.140.5
    
In this example, lines that contain the text "Linux" or beginning with the text "co205" are included::

    from pysaurio import Reptar
    rep1 = Reptar()       
    rep1.description = 'Get list of Linux users'
    rep1.extension = 'txt'
    rep1.prefix = 'PCS'
    rep1.input_folder = 'txt'
    rep1.output_folder = 'txt'
    rep1.output_file = 'Linux.csv'
    rep1.include_header = '1'
    rep1.include_file = '0'
    rep1.include_record_num = '0'
    rep1.alternate_header = ''
    rep1.lines.append(('INCLUDE', 'Linux'))
    rep1.lines.append(('INCLUDRE', '^co205'))
    rep1.rules.append(('line', 'UPPER'))            
    rep1.Save("linux.rep")
    del rep1

    # Opens .rep template and create file with output information
    
    rep2 = Reptar()
    rep2.Open('linux.rep')
    if rep2.number_errors == 0:         
        file_csv = open(rep2.output_file, 'w')
        if rep2.include_header == '1':
            header = rep2.BuildHeader(rep2.list_files[0])
            print(header)
            file_csv.write(header + '\n')
                                    
        for row in rep2.list_files:
            current_file = open(rep2.input_folder + row, 'rb')
            while True:
                new_record = current_file.readline()
                new_record = new_record.decode("utf-8", "ignore")
                if not new_record: break
                valid_record, new_record = rep2.BuildRow(new_record, row)
                if valid_record:
                    new_record = rep2.ApplyRules(new_record)
                    print(new_record)
                    file_csv.write(new_record + '\n')
            current_file.close()
        file_csv.close()            
    else:
        print(rep2.ShowError())
    del rep2


**Functions available for including and excluding lines:**
        
- line1 = ('EXCLUDE', 'string')
- line1 = ('INCLUDE', 'string')
- line1 = ('EXCLUDEND', 'string')
- line1 = ('INCLUDEND', 'string')
- line1 = ('EXCLUDRE', 'regex', '0'|'1')  # '1' not case sensitive
- line1 = ('INCLUDRE', 'regex', '0'|'1')  # (See module re)

The package contains more examples and data files to test.

Changelog
---------

- Pysaurio 0.2.6 - 2018-09-14 - Corrected error in function REMOVECOL
- Pysaurio 0.2.5 - 2016-09-09 - new attribute: include_file_datetime = '0' or '1'
- Pysaurio 0.2.4 - Reptar include new rule: 'REMOVECOL', remove column
- Pysaurio 0.2.3 - New functions: 'INCLUDEND' and 'EXCLUDEND'
- Pysaurio 0.2.2 - New argument in the 'INCLUDRE' and 'EXCLUDRE' functions
- Pysaurio 0.2.1 - Reptar includes rules and the section 'Lines' you can use regular expressions.
- Pysaurio 0.2.0 - Initial release (continued "Pyraptor").
