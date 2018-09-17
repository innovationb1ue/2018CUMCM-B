import xlrd
import csv
import codecs

workbook = xlrd.open_workbook('./0302.xlsx')
booksheet = workbook.sheet_by_index(0)


CNCs = booksheet.col_values(1)
times = booksheet.col_values(2)

f = codecs.open('./Boom-0302.csv', 'a+', 'gbk')
writer  = csv.writer(f)

for cnc in enumerate(CNCs):
    for cnc2 in enumerate(CNCs[cnc[0]+1:]):
        times2 = times[cnc[0]+1:]
        if cnc2[1] == cnc[1]:
            writer.writerow([cnc[1], times[cnc[0]], times2[cnc2[0]]])
            break
