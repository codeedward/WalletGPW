def FilterExcel(listOfExcelRows, accountType):
    return filter(lambda x: filterExcel(x, accountType), listOfExcelRows)


def filterExcel(excelEntryRow, accountType):
    vowels = ['a', 'e', 'i', 'o', 'u']

    if(excelEntryRow.accountType != accountType and accountType != ''):
        return False


    return True
