import time

def format_result(s, up_bytes, app, port):
    """format my output"""
    x = time.localtime(s)
    text = '%s,%s,%s,%s\n' % (time.strftime('%Y%m%d %H:%M:%S', x), up_bytes, app, port)
    return text

f_out = open("d:\\yl_us_20131003_imei_0128480018959912.txt", 'w')

f_in = open("d:\\yl_us_20131003_imei_0128480018959912.csv")
line = f_in.readline() #skip header

# get first sample time
line = f_in.readline()
strlist = line.split(',')
str_tmp = strlist[0].split('.')[0]
str_sample_time = str_tmp[0:10] + " " + str_tmp[10:18]
sample_start_time = time.mktime(time.strptime(str_sample_time,'%Y-%m-%d %H:%M:%S') )
sample_end_time = sample_start_time + 24*60*60
sample_time = sample_start_time
sample_value = strlist[20]
         
# read first tuple
str_tmp = strlist[0].split('.')[0]
str_first_time = str_tmp[0:10] + " " + str_tmp[10:18]
str_tmp = strlist[1].split('.', 1)[0]
str_end_time = str_tmp[0:10] + " " + str_tmp[10:18]
   
first_time = time.mktime(time.strptime(str_first_time,'%Y-%m-%d %H:%M:%S') )
end_time = time.mktime(time.strptime(str_end_time,'%Y-%m-%d %H:%M:%S') )

while (sample_time <= sample_end_time):
    
    while sample_time > end_time:
        line=f_in.readline()
        if line:
            strlist = line.split(',')
            str_tmp = strlist[0].split('.')[0]
            str_first_time = str_tmp[0:10] + " " + str_tmp[10:18]
          
            str_tmp = strlist[1].split('.')[0]
            str_end_time = str_tmp[0:10] + " " + str_tmp[10:18]
            
            first_time = time.mktime(time.strptime(str_first_time,'%Y-%m-%d %H:%M:%S') )
            end_time = time.mktime(time.strptime(str_end_time,'%Y-%m-%d %H:%M:%S') )
        else:
            break
    
    if (sample_time >= first_time and sample_time <= end_time):
#         text = '%d,%s\n' % (sample_time, strlist[20])
        text = format_result(sample_time, strlist[20], strlist[16], strlist[27])
        f_out.write(text)
    else:
#         text = '%d,%s\n' % (sample_time, 0)
        text = format_result(sample_time, 0, strlist[16], strlist[27])
        f_out.write(text)
    
    sample_time += 60;
    
f_in.close()
f_out.close()

print "--finished--"