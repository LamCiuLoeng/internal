# -*- coding: utf-8 -*-
import os, traceback, logging, datetime
import win32com.client
import pythoncom

from win32com.client import DispatchEx
from common import *

__all__ = ["ExcelBasicGenerator", "JCPExcel", "SDWeeklyExcel", 'DBAExcel', 'TAGExcel',
           'BBYREPORTExcel', 'BBYMockupExcel', "BBYRawReportExcel",
           "SampleJobSummary", 'LemmiOrderExcel', 'CabelsOrderExcel', 'TMWExcel',
           'PrepressSummary', ]


XlBorderWeight = {
                  "xlHairline" : 1,
                  "xlThin" : 2,
                  "xlMedium" : 3,
                  "xlThick" : 4
                  }

XlBordersIndex = {
                  "xlDiagonalDown" : 5,
                  "xlDiagonalUp" : 6,
                  "xlEdgeBottom" : 9,
                  "xlEdgeLeft" : 7,
                  "xlEdgeRight" : 10,
                  "xlEdgeTop" : 8,
                  "xlInsideHorizontal" : 12,
                  "xlInsideVertical" : 11,
                  }



# http://msdn.microsoft.com/en-us/library/microsoft.office.interop.excel.xlhalign.aspx
XlHAlign = {
          "xlHAlignCenter" :-4108,  # Center
          "xlHAlignCenterAcrossSelection" : 7,  # Center across selection.
          "xlHAlignDistributed" :-4117,  # Distribute
          "xlHAlignFill" : 5,  # Fill
          "xlHAlignGeneral" : 1,  # Align according to data type.
          "xlHAlignJustify" :-4130,  # Justify
          "xlHAlignLeft" :-4130,  # Left
          "xlHAlignRight" :-4152,  # Right
          }


HorizontalAlignment = {
                       "xlCenter" :-4108,
                       "xlDistributed" :-4117,
                       "xlJustify" :-4130,
                       "xlLeft" :-4131,
                       "xlRight" :-4152,
                       }


XlUnderlineStyle = {
    "xlUnderlineStyleNone" :-4142,
    "xlUnderlineStyleSingle" : 2,
    "xlUnderlineStyleDouble" :-4119,
    "xlUnderlineStyleSingleAccounting" :4,
    "xlUnderlineStyleDoubleAccounting" : 5,
}


InteriorPattern = {
                   "xlSolid" : 1,
                   }


InteriorPatternColorIndex = {
                             "xlAutomatic" :-4105,
                             }

XlThemeColor = {
                "xlThemeColorAccent1" :    5,  # Accent1
                "xlThemeColorAccent2" :    6,  # Accent2
                "xlThemeColorAccent3" :    7,  # Accent3
                "xlThemeColorAccent4" :   8,  # Accent4
                "xlThemeColorAccent5" :   9,  # Accent5
                "xlThemeColorAccent6" :   10,  # Accent6
                "xlThemeColorDark1"   : 1,  # Dark1
                "xlThemeColorDark2"   : 3,  # Dark2
                "xlThemeColorFollowedHyperlink"  :  12,  # Followed hyperlink
                "xlThemeColorHyperlink" :    11,  # Hyperlink
                "xlThemeColorLight1"  :    2,  # Light1
                "xlThemeColorLight2"  : 4,  # Light2
                }

class ExcelBasicGenerator:
    def __init__( self, templatePath = None, destinationPath = None, overwritten = True ):
        # solve the problem when create the excel at second time ,the exception is occur.
        pythoncom.CoInitialize()

        self.excelObj = DispatchEx( 'Excel.Application' )
        self.excelObj.Visible = False

        if templatePath and os.path.exists( templatePath ):
            self.workBook = self.excelObj.Workbooks.open( templatePath )
        else:
            self.workBook = self.excelObj.Workbooks.Add()

        self.destinationPath = os.path.normpath( destinationPath ) if destinationPath else None
        self.overwritten = overwritten

    def inputData( self ): pass

    def outputData( self ):
        try:
            if not self.destinationPath : pass
            elif os.path.exists( self.destinationPath ):
                if self.overwritten:
                    os.remove( self.destinationPath )
                    self.excelObj.ActiveWorkbook.SaveAs( self.destinationPath )
            else:
                self.excelObj.ActiveWorkbook.SaveAs( self.destinationPath )
        except:
            traceback.print_exc()
        finally:
            try:
                self.workBook.Close( SaveChanges = 0 )
            except:
                traceback.print_exc()

    def clearData( self ):
        try:
            if hasattr( self, "workBook" ): self.workBook.Close( SaveChanges = 0 )
        except:
            traceback.print_exc()


    #===========================================================================
    # get the TEXT for the given ranges
    #===========================================================================
    def getRangeText( self, rang ):
        result = []
        for row in rang:
            result.append( [cell.text for cell in row] )  # use .text(), not .value() ,the .text() would get the formated value
        return result


class JCPExcel( ExcelBasicGenerator ):
    def inputData( self, additionInfo = [], header = [], data = [] ):
        excelSheet = self.workBook.Sheets( 1 )
        excelSheet.Cells( 4, 1 ).Value = "Export Time : %s" % datetime.datetime.now().strftime( "%d/%b/%Y %H:%M:%S" )
        infoStartRow = 5
        infoStartCol = 1

        for oneCriteria in additionInfo:
            excelSheet.Cells( infoStartRow, infoStartCol ).Value = oneCriteria
            infoStartRow += 1

        if not data: data = [( "", ), ]

        row = len( data )
        col = len( data[0] )
        startRow = 16
        startCol = 1

        excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( col ), startRow + row - 1 ) ).Value = data
        excelSheet.Columns( "A:AZ" ).EntireColumn.AutoFit()




#===============================================================================
# excel function for sample development
#===============================================================================
class SDWeeklyExcel( ExcelBasicGenerator ):
    def inputData( self, totalQty, totalTime, data = {} ):
        excelSheet = self.workBook.Sheets( 1 )

        startRow = 3

        for k, v in data.items():
#            print "*-"*30
#            print v
#            print "^-"*30

            startCol = 1
            endCol = len( v[0] ) if v else 0
            row = len( v )
            mg = excelSheet.Range( "%s%d:%s%d" % ( number2alphabet( startCol ), startRow, number2alphabet( endCol ), startRow ) )
            mg.Merge()
            mg.Font.Bold = True
            mg.Font.Size = 12
            mg.Interior.ColorIndex = 6
            mg.Value = k.date()
            startRow += 1
            excelSheet.Range( "%s%d:%s%d" % ( number2alphabet( startCol ), startRow, number2alphabet( endCol ), startRow + row - 1 ) ).Value = v

            startRow += row

        excelSheet.Range( "L%d" % ( startRow + 1 ) ).Value = totalQty
        excelSheet.Range( "M%d" % ( startRow + 1 ) ).Value = totalTime

        excelSheet.Range( "L%d,M%d" % ( startRow + 1, startRow + 1 ) ).Interior.ColorIndex = 6  # change the cells's background to yellow.



class DBAExcel( ExcelBasicGenerator ):
    def inputData( self, data = [], data2 = [] ):
        excelSheet = self.workBook.Sheets( 1 )
        if not data:
            data = [( "", ), ]


        startRow = 2
        row = len( data )
        col = len( data[0] )
        excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( col ), startRow + row - 1 ) ).Value = data

        startRow += len( data ) + 2
        col = len( data2[0] )
        range = excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( col ), startRow ) )
        range.Font.Bold = True
        range.Value = list( ( data2[0], ) )
        data2.remove( data2[0] )
        if not data2:
            data2 = [( "", ), ]
        startRow += 1
        row = len( data2 )
        excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( col )  , startRow + row - 1 ) ).Value = data2

# add by cz@2010-11-12
class TAGExcel( ExcelBasicGenerator ):
    def inputData( self, sheetName = 'Sheet1', data = [], so = '' ):
        excelSheet = self.workBook.Sheets( 1 )
        # excelSheet.Name = sheetName
        if not data:
            data = [( "", ), ]


        excelSheet.Range( "soc" ).Value = so
        startRow = 6
        row = len( data )
        col = len( data[0] )
        lastRow = startRow + row
        excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( col ), startRow + row - 1 ) ).Value = data

        alphabetCol = number2alphabet( col - 1 )
        alphabetCol2 = number2alphabet( col )


        excelSheet.Range( "%s%d:%s%d" % ( alphabetCol, startRow, alphabetCol, lastRow - 1 ) ).Interior.ColorIndex = 36  # change the cells's background to yellow.

        excelSheet.Range( "%s%d" % ( alphabetCol, lastRow ) ).Value = "=sum(%s%d:%s%d)" % ( alphabetCol, startRow, alphabetCol, lastRow - 1 )
        excelSheet.Range( "%s%d" % ( alphabetCol2, lastRow ) ).Value = "=sum(%s%d:%s%d)" % ( alphabetCol2, startRow, alphabetCol2, lastRow - 1 )

        excelSheet.Range( "A%d:%s%d" % ( startRow, alphabetCol2, startRow + row - 1 ) ).Borders( 1 ).LineStyle = 1
        excelSheet.Range( "A%d:%s%d" % ( startRow, alphabetCol2, startRow + row - 1 ) ).Borders( 2 ).LineStyle = 1
        excelSheet.Range( "A%d:%s%d" % ( startRow, alphabetCol2, startRow + row - 1 ) ).Borders( 3 ).LineStyle = 1
        excelSheet.Range( "A%d:%s%d" % ( startRow, alphabetCol2, startRow + row - 1 ) ).Borders( 4 ).LineStyle = 1

        excelSheet.Range( "%s%d:%s%d" % ( alphabetCol, lastRow, alphabetCol2, lastRow, ) ).Borders( 1 ).LineStyle = 1
        excelSheet.Range( "%s%d:%s%d" % ( alphabetCol, lastRow, alphabetCol2, lastRow, ) ).Borders( 2 ).LineStyle = 1
        excelSheet.Range( "%s%d:%s%d" % ( alphabetCol, lastRow, alphabetCol2, lastRow, ) ).Borders( 3 ).LineStyle = 1
        excelSheet.Range( "%s%d:%s%d" % ( alphabetCol, lastRow, alphabetCol2, lastRow, ) ).Borders( 4 ).LineStyle = 1
        excelSheet.Range( "%s%d:%s%d" % ( alphabetCol, lastRow, alphabetCol2, lastRow, ) ).Interior.ColorIndex = 6

        del alphabetCol, alphabetCol2

        excelSheet.Columns( "A:AZ" ).EntireColumn.AutoFit()



class BBYREPORTExcel( ExcelBasicGenerator ):
    def inputData( self, max_testings_len = 0, max_casepack_len = 0, data = [] ):
        excelSheet = self.workBook.Sheets( 1 )
        excelSheet.Range( "D2" ).Value = datetime.datetime.now()
        startRow = 4
        header = ['BestBuy Model #', 'Vendor Name', 'Option']
        excelSheet.Range( "A%d:C%d" % ( startRow, startRow ) ).Interior.ColorIndex = 49
        header_col = 4

        testing_col_index = header_col - 1

        for i in range( max_testings_len ):
            header.append( '%d Sample Express Date' % ( i + 1 ) )
            header.append( '%d Feedback Date' % ( i + 1 ) )
            excelSheet.Range( "%s%d:%s%d" % ( number2alphabet( header_col ), startRow, number2alphabet( header_col + 1 ), startRow ) ).Interior.ColorIndex = 55
            excelSheet.Range( "%s%d:%s%d" % ( number2alphabet( header_col ), startRow + 1, number2alphabet( header_col + 1 ), startRow + len( data ) ) ).NumberFormatLocal = 'yyyy-mm-dd'
            header_col += 2
            header.append( 'turn around Days' )
            excelSheet.Range( "%s%d" % ( number2alphabet( header_col ), startRow ) ).Interior.ColorIndex = 3
            excelSheet.Range( "%s%d:%s%d" % ( number2alphabet( header_col ), startRow + 1, number2alphabet( header_col ), startRow + len( data ) ) ).Font.ColorIndex = 5
            header_col += 1
        if max_testings_len > 0:
            header.append( 'Fitting Approval Date' )
            excelSheet.Range( "%s%d" % ( number2alphabet( header_col ), startRow ) ).Interior.ColorIndex = 55
            excelSheet.Range( "%s%d:%s%d" % ( number2alphabet( header_col ), startRow + 1, number2alphabet( header_col ), startRow + len( data ) ) ).NumberFormatLocal = 'yyyy-mm-dd'
            header_col += 1
            header.append( 'Total Fitting Rounds' )
            header.append( 'Fitting Lead time' )
            excelSheet.Range( "%s%d:%s%d" % ( number2alphabet( header_col ), startRow, number2alphabet( header_col + 1 ), startRow ) ).Interior.ColorIndex = 3
            excelSheet.Range( "%s%d:%s%d" % ( number2alphabet( header_col ), startRow + 1, number2alphabet( header_col + 1 ), startRow + len( data ) ) ).Font.ColorIndex = 5
            header_col += 2

        casepack_col_index = header_col - 1


        for i in range( max_casepack_len ):
            header.append( '%d Casepack Sample Express Date' % ( i + 1 ) )
            header.append( '%d Feedback Date' % ( i + 1 ) )
            excelSheet.Range( "%s%d:%s%d" % ( number2alphabet( header_col ), startRow, number2alphabet( header_col + 1 ), startRow ) ).Interior.ColorIndex = 50
            excelSheet.Range( "%s%d:%s%d" % ( number2alphabet( header_col ), startRow + 1, number2alphabet( header_col + 1 ), startRow + len( data ) ) ).NumberFormatLocal = 'yyyy-mm-dd'
            header_col += 2
            header.append( 'turn around Days' )
            excelSheet.Range( "%s%d" % ( number2alphabet( header_col ), startRow ) ).Interior.ColorIndex = 3
            excelSheet.Range( "%s%d:%s%d" % ( number2alphabet( header_col ), startRow + 1, number2alphabet( header_col ), startRow + len( data ) ) ).Font.ColorIndex = 5
            header_col += 1
        if max_casepack_len > 0:
            header.append( 'Testing Approval Date' )
            excelSheet.Range( "%s%d" % ( number2alphabet( header_col ), startRow ) ).Interior.ColorIndex = 50
            excelSheet.Range( "%s%d:%s%d" % ( number2alphabet( header_col ), startRow + 1, number2alphabet( header_col ), startRow + len( data ) ) ).NumberFormatLocal = 'yyyy-mm-dd'
            header_col += 1
            header.append( 'Total Testing Rounds' )
            header.append( 'Testing Lead Time' )
            excelSheet.Range( "%s%d:%s%d" % ( number2alphabet( header_col ), startRow, number2alphabet( header_col + 1 ), startRow ) ).Interior.ColorIndex = 3
            excelSheet.Range( "%s%d:%s%d" % ( number2alphabet( header_col ), startRow + 1, number2alphabet( header_col + 1 ), startRow + len( data ) ) ).Font.ColorIndex = 5
            header_col += 2

        status_col_index = header_col - 1

        header.append( 'Status' )
        excelSheet.Range( "%s%d" % ( number2alphabet( header_col ), startRow ) ).Font.ColorIndex = 1  # black
        header_col += 1
        header.append( 'Memo' )
        excelSheet.Range( "%s%d" % ( number2alphabet( header_col ), startRow ) ).Font.ColorIndex = 1  # black
        col = len( header )
        excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( col ), startRow ) ).Value = header

        startRow += 1
        currentRow = startRow
        content = []
        for d in data :
            tmp_data = [''] * col
            tmp_data[0:3] = [d['sku'], d['vendor'], d['option']]
            tmp_data[status_col_index] = d['status']

            testings = d.get( 'testings', [] )
            if testings:
                for index, t in enumerate( testings ):
                    if t.get( 'express_date' ) and t.get( 'feedback_date' ) :
                        compare = '=%s%d-%s%d' % ( number2alphabet( testing_col_index + index * 3 + 2 ), currentRow, number2alphabet( testing_col_index + index * 3 + 1 ), currentRow )
                    else : compare = ''
                    tmp_data[testing_col_index + index * 3:testing_col_index + index * 3 + 3] = [t.get( 'express_date' ), t.get( 'feedback_date' ), compare]
                tmp_data[testing_col_index + max_testings_len * 3:testing_col_index + max_testings_len * 3 + 3] = [testings[-1].get( 'feedback_date' ),
                                                                               len( testings ),
                                                                               '=sum(%s)' % ( ','.join( ['%s%d' % ( number2alphabet( testing_col_index + ( i + 1 ) * 3 ), currentRow ) for i in range( max_testings_len )] ) )
                                                                           ]

            casepacks = d.get( 'casepacks', [] )
            if casepacks :
                for index, c in enumerate( casepacks ):
                    if c.get( 'express_date' ) and c.get( 'feedback_date' ) :
                        compare = '=%s%d-%s%d' % ( number2alphabet( casepack_col_index + index * 3 + 2 ), currentRow, number2alphabet( casepack_col_index + index * 3 + 1 ), currentRow )
                    else : compare = ''
                    tmp_data[casepack_col_index + index * 3:casepack_col_index + index * 3 + 3] = [c.get( 'express_date' ), c.get( 'feedback_date' ), compare]

                tmp_data[casepack_col_index + max_casepack_len * 3:casepack_col_index + max_casepack_len * 3 + 3] = [casepacks[-1].get( 'feedback_date' ),
                                                                                 len( casepacks ),
                                                                                 '=sum(%s)' % ( ','.join( ['%s%d' % ( number2alphabet( casepack_col_index + ( i + 1 ) * 3 ), currentRow ) for i in range( max_casepack_len )] ) )
                                                                                 ]
            content.append( tmp_data )
            currentRow += 1
        excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( col ), currentRow - 1 ) ).Value = content

        # excelSheet.Columns("A:AZ").EntireColumn.AutoFit()


# add by kevin@2011-03-30
class BBYMockupExcel( ExcelBasicGenerator ):
    def inputData( self, max_new_len = 0, max_post_len = 0, max_cancell_len = 0, data = [] ):
        excelSheet = self.workBook.Sheets( 1 )
        if not data: data = [( "", ), ]
        # print data
        now = datetime.datetime.now().strftime( "%d-%b,%y" )
        new = data.get( "new" ) if len( data.get( "new" ) ) > 0 else None
        post = data.get( "post" ) if len( data.get( "post" ) ) > 0 else None
        cancell = data.get( "cancell" ) if len( data.get( "cancell" ) ) > 0 else None

        startRow = 2
        excelSheet.Range( "A%d:%s%d" % ( 1, number2alphabet( 1 ), 1 ) ).Value = "Updated on %s" % now
        # excelSheet.Range("Chart %s:%s%d" % (1026,number2alphabet(1), 1026)).Value =  "Updated on %s" % update
        if post:
            for b in post:
                startRow += 1
                if b.get( 'confirmDate' ) and b.get( 'sendDate' ):
                    day = ( b.get( 'confirmDate' ) - b.get( 'sendDate' ) ).days
                else:
                    day = " "
                excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 5 ), startRow ) ).Borders( 1 ).LineStyle = [1, 1, 1, 1, 1]
                excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 5 ), startRow ) ).Borders( 2 ).LineStyle = [1, 1, 1, 1, 1]
                excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 5 ), startRow ) ).Borders( 3 ).LineStyle = [1, 1, 1, 1, 1]
                excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 5 ), startRow ) ).Borders( 4 ).LineStyle = [1, 1, 1, 1, 1]
                excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 1 ), startRow ) ).Font.Size = 13

                excelSheet.Range( "%s%d" % ( number2alphabet( 1 ), startRow ) ).Interior.ColorIndex = 44
                excelSheet.Range( "%s%d" % ( number2alphabet( 1 ), startRow ) ).HorizontalAlignment = -4108
                excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 5 ), startRow ) ).Value = [b.get( 'item' ), b.get( 'round' ), day, b.get( 'sendDate' ).strftime( "%d-%b,%y" ) if b.get( 'sendDate' ) else " ", b.get( 'confirmDate' ).strftime( "%d-%b,%y" ) if b.get( 'confirmDate' ) else " "]

        # chart = self.workBook.Charts('Chart1026_Click')
        chart = excelSheet.ChartObjects( 'Chart 1026' ).Chart
        chart.HasTitle = True
        chart.ChartTitle.Characters.Text = now
        chart.SetSourceData( excelSheet.Range( "='Sheet1'!$A$2:$C$%s" % startRow ) )

        startRow += 4
        excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 1 ), startRow ) ).Value = "Item under development in %s" % now
        if new:
            for a in new:
                startRow += 1
                excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 1 ), startRow ) ).Borders( 1 ).LineStyle = 1
                excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 1 ), startRow ) ).Borders( 2 ).LineStyle = 1
                excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 1 ), startRow ) ).Borders( 3 ).LineStyle = 1
                excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 1 ), startRow ) ).Borders( 4 ).LineStyle = 1
                excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 1 ), startRow ) ).Font.Size = 13
                excelSheet.Range( "%s%d" % ( number2alphabet( 1 ), startRow ) ).HorizontalAlignment = -4108
                excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 1 ), startRow ) ).Value = a.get( 'item' )

        startRow += 4

        excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 1 ), startRow ) ).Value = "Item not go forward in %s" % now
        if cancell:
            for c in cancell:
                startRow += 1
                excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 1 ), startRow ) ).Borders( 1 ).LineStyle = 1
                excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 1 ), startRow ) ).Borders( 2 ).LineStyle = 1
                excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 1 ), startRow ) ).Borders( 3 ).LineStyle = 1
                excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 1 ), startRow ) ).Borders( 4 ).LineStyle = 1
                excelSheet.Range( "%s%d" % ( number2alphabet( 1 ), startRow ) ).Interior.ColorIndex = 48
                excelSheet.Range( "%s%d" % ( number2alphabet( 1 ), startRow ) ).Font.Size = 13
                excelSheet.Range( "%s%d" % ( number2alphabet( 1 ), startRow ) ).HorizontalAlignment = -4108
                excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( 1 ), startRow ) ).Value = c.get( 'item' )



class BBYRawReportExcel( ExcelBasicGenerator ):
    def _addColumn( self, c, *addtion ):
        return number2alphabet( alphabet2number( c ) + sum( addtion ) )

    def inputData( self, data, component_header, max_component_count,
                  fitting_header, max_fitting_round, casepack_header, max_casepack_round ):
        sheet = self.workBook.Sheets( 1 )
        startRow = 3
        first_header_row = 1
        second_header_row = 2
        append_column = "Z"


        def _draw_header( start_column, header, times, title ):
            tmp_column = start_column
            for i in range( times ) :
                next_column = self._addColumn( tmp_column, len( header ), -1 )
                sheet.Range( "%s%s:%s%s" % ( tmp_column, second_header_row, next_column, second_header_row ) ).Value = header
                sheet.Range( "%s%s:%s%s" % ( tmp_column, first_header_row, next_column, first_header_row ) ).Merge()
                sheet.Range( "%s%s:%s%s" % ( tmp_column, first_header_row, next_column, first_header_row ) ).Value = '%s %d' % ( title, i + 1 )
                tmp_column = self._addColumn( tmp_column, len( header ) )
            return tmp_column


        column = append_column
        for h, t, title in [( component_header, max_component_count, "Component" ),
                    ( fitting_header, max_fitting_round, "Fitting Round" ), ( casepack_header, max_casepack_round, "Case Pack Round" )]:
            column = _draw_header( column, h, t, title )

        sheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( len( data[0] ) ), startRow + len( data ) - 1 ) ).Value = data

        # draw cell line
        sheet_range = "A%s:%s%d" % ( 1, number2alphabet( len( data[0] ) ), startRow + len( data ) - 1 )
        for line in ["xlInsideHorizontal", "xlInsideVertical", "xlEdgeBottom", "xlEdgeLeft", "xlEdgeRight", "xlEdgeTop"]:
            sheet.Range( sheet_range ).Borders( XlBordersIndex[line] ).Weight = XlBorderWeight["xlThin"]
            sheet.Range( sheet_range ).Borders( XlBordersIndex[line] ).LineStyle = 1

#        sheet.Range(sheet_range).WrapText = False
        sheet.Range( sheet_range ).EntireColumn.AutoFit()



class SampleJobSummary( ExcelBasicGenerator ):

    default_column_space = 2  # 3 column to seperate the two data
    default_row_space = 2

    def _addColumn( self, c, *addtion ):
        return number2alphabet( alphabet2number( c ) + sum( addtion ) )


    def _drawCellLine( self, sheet, left, top, right, bottom ):
        sheet_range = "%s%s:%s%s" % ( left, top, right, bottom )
        for line in ["xlEdgeBottom", "xlEdgeLeft", "xlEdgeRight", "xlEdgeTop"]:
            sheet.Range( sheet_range ).Borders( XlBordersIndex[line] ).Weight = XlBorderWeight["xlMedium"]
            sheet.Range( sheet_range ).Borders( XlBordersIndex[line] ).LineStyle = 1
        for line in ["xlInsideHorizontal", "xlInsideVertical"]:
            sheet.Range( sheet_range ).Borders( XlBordersIndex[line] ).Weight = XlBorderWeight["xlThin"]
            sheet.Range( sheet_range ).Borders( XlBordersIndex[line] ).LineStyle = 1


    def _drawRangLine( self, sheet, left, top, right, bottom ):
        range = "%s%s:%s%s" % ( left, top, right, bottom )
        # draw the left top cell
        sheet.Range( "%s%s:%s%s" % ( left, top, left, top + 1 ) ).Merge()
        sheet.Range( "%s%s:%s%s" % ( left, top, left, top + 1 ) ).Borders( XlBordersIndex["xlDiagonalDown"] ).LineStyle = 1
        # draw the top,left,right,bottom,inside line
        self._drawCellLine( sheet, left, top, right, bottom )



    def _drawOneTable( self, sheet, x_offest, y_offest, x_header, y_header, content, y_title ):

        x0, x1, x2 = x_offest, self._addColumn( x_offest, 1 ), self._addColumn( x_offest, len( x_header ) )
        y0, y1, y2, y3 = y_offest, y_offest + 1, y_offest + 2, y_offest + 1 + len( y_header )
        # fill in the header
        self._drawYTitle( sheet, x1, y0, x2, y0, y_title )
        sheet.Range( "%s%s:%s%s" % ( x0, y2, x0, y3 ) ).Value = map( lambda v:[v], y_header )
        sheet.Range( "%s%s:%s%s" % ( x1, y1, x2, y1 ) ).Value = x_header
        sheet.Range( "%s%s:%s%s" % ( x1, y1, x2, y1 ) ).WrapText = True
        # fill in the data
        sheet.Range( "%s%s:%s%s" % ( x1, y2, x2, y3 ) ).Value = content

        self._drawRangLine( sheet, x0, y0, x2, y3 )
        return ( x0, y0, x2, y3 )  # left,top,right,bottom


    def _drawXTitle( self, sheet, left, top, right, bottom, name ):
        range = "%s%s:%s%s" % ( left, top, right, bottom )
        sheet.Range( range ).Merge()
        sheet.Range( range ).Value = name
        sheet.Range( range ).Orientation = -90  # transfrer the text to vitical
        sheet.Range( range ).Font.Size = 22  # bold the word
        sheet.Range( range ).VerticalAlignment = XlHAlign["xlHAlignCenter"]  # set the font to middle
        sheet.Range( "%s%s" % ( left, top ) ).ColumnWidth = 4.6


    def _drawYTitle( self, sheet, left, top, right, bottom, name ):
        range = "%s%s:%s%s" % ( left, top, right, bottom )
        sheet.Range( range ).Merge()
        sheet.Range( range ).Value = name
        sheet.Range( range ).HorizontalAlignment = XlHAlign["xlHAlignCenter"]


    def _drawOneRow( self, sheet, x0, y0, data ):
        ys = []
        x, y = x0, y0
        for index, d in enumerate( data ):
            if index == 0 :
                self._drawXTitle( sheet, x, y, x, y + 1 + len( d["y_header"] ), d["x_title"] )
                x = self._addColumn( x, 1 )
            ( _, _, _, new_y ) = self._drawOneTable( sheet, x, y, d["x_header"], d["y_header"], d["content"], d["y_title"] )
            x = self._addColumn( x, len( d["x_header"] ), self.default_column_space )
            ys.append( new_y )
        return ( x0, max( ys ) )


    def _drawTotalTable( self, sheet, x, y, header, data ):
        x0, x1 = self._addColumn( x, 1 ), self._addColumn( x, len( header ) )
        y0, y1, y2 = y, y + 1, y + len( data )
        self._drawCellLine( sheet, x0, y0, x1, y2 )
        sheet.Range( "%s%s:%s%s" % ( x0, y0, x1, y0 ) ).Value = header
        sheet.Range( "%s%s:%s%s" % ( x0, y1, x1, y2 ) ).Value = data
        return x0, y0, x1, y2


    def _drawTotal( self, sheet, x, y, data ):
        x_offest, y_offest = self._addColumn( x, 1 ), y
        max_y = []
        for d in data:
            ( _, _, new_x_offest, new_y_offest ) = self._drawTotalTable( sheet, x_offest, y_offest, d["x_header"], d["content"] )
            x_offest = self._addColumn( new_x_offest, self.default_column_space )
            max_y.append( new_y_offest )
        return ( x_offest, max( max_y ) )


    def _drawCost( self, sheet, x, y, header, data ):
        x0, x1 = x, self._addColumn( x, len( header ) - 1 )
        y0, y1, y2 = y, y + 1, y + len( data )
        self._drawCellLine( sheet, x0, y0, x1, y2 )
        sheet.Range( "%s%s:%s%s" % ( x0, y0, x1, y0 ) ).Value = header
        sheet.Range( "%s%s:%s%s" % ( x0, y1, x1, y2 ) ).Value = data
        sheet.Range( "%s%s:%s%s" % ( x0, y1, x1, y2 ) ).NumberFormatLocal = "$#,##0.00;-$#,##0.00"


    def _drawOneDetailTable( self, sheet, x, y, data ):
        sub_y_header = []
        for h in data["y_header"]:
            sub_y_header.extend( h[-1] )

        x0, x1, x2, x3 = x, self._addColumn( x, 1 ), self._addColumn( x, 2 ), self._addColumn( x, 1, len( data["x_header"] ) )
        y0, y1, y2, y3, y4, y5, y6, y7, y8 = y, y + 1, y + 2, y + 3, y + 4, y + 5, y + 4 + len( sub_y_header ), y + 5 + len( sub_y_header ), y + 5 + len( sub_y_header ) + self.default_row_space

        def _fillBlack( left, top, right, bottom ):
            range = "%s%s:%s%s" % ( left, top, right, bottom )
            sheet.Range( range ).Interior.Pattern = InteriorPattern["xlSolid"]
            sheet.Range( range ).Interior.PatternColorIndex = InteriorPatternColorIndex["xlAutomatic"]
#            sheet.Range(range).Interior.ThemeColor = XlThemeColor["xlThemeColorLight1"]  #problem in 2003, but OK in 2007
            sheet.Range( range ).Interior.ColorIndex = 1

        sheet.Range( "%s%s:%s%s" % ( x0, y0, x3, y0 ) ).Merge()
        _fillBlack( x0, y0, x3, y0 )
        sheet.Range( "%s%s:%s%s" % ( x0, y2, x3, y2 ) ).Merge()
        _fillBlack( x0, y2, x3, y2 )
        sheet.Range( "%s%s:%s%s" % ( x0, y7, x3, y7 ) ).Merge()
        _fillBlack( x0, y7, x3, y7 )
        sheet.Range( "%s%s:%s%s" % ( x0, y1, x3, y1 ) ).Merge()
        # draw title
        sheet.Range( "%s%s:%s%s" % ( x0, y1, x3, y1 ) ).Value = data["title"]
        sheet.Range( "%s%s:%s%s" % ( x0, y1, x3, y1 ) ).HorizontalAlignment = XlHAlign["xlHAlignCenter"]
        # draw y_header
        y_offest = y5
        for ( h, sub ) in data["y_header"]:
            range = "%s%s:%s%s" % ( x0, y_offest, x0, y_offest + len( sub ) - 1 )
            sheet.Range( range ).Merge()
            sheet.Range( range ).Value = h
            y_offest += len( sub )
        sheet.Range( "%s%s:%s%s" % ( x1, y5, x1, y6 ) ).Value = map( lambda v:[v], sub_y_header )

        # draw x_header
        header_x1 = "%s%s:%s%s" % ( x0, y3, x1, y3 )
        sheet.Range( header_x1 ).Merge()
        sheet.Range( header_x1 ).Value = "Program Details"
        header_x2 = "%s%s:%s%s" % ( self._addColumn( x1, 1 ), y3, self._addColumn( x1, 3 ), y3 )
        sheet.Range( header_x2 ).Merge()
        sheet.Range( header_x2 ).Value = "Designs"
        header_x3 = "%s%s:%s%s" % ( self._addColumn( x1, 4 ), y3, self._addColumn( x1, 5 ), y3 )
        sheet.Range( header_x3 ).Merge()
        sheet.Range( header_x3 ).Value = "Outputs"
        sheet.Range( "%s%s:%s%s" % ( self._addColumn( x1, 6 ), y3, self._addColumn( x1, 6 ), y3 ) ).Value = "Remarks"
        sheet.Range( "%s%s:%s%s" % ( x0, y3, x3, y3 ) ).HorizontalAlignment = XlHAlign["xlHAlignCenter"]
        # sheet.Range("%s%s:%s%s" %(x0,y3,x3,y3)).Font.Color = -4165632  #set the word to be blue
        sheet.Range( "%s%s:%s%s" % ( x0, y3, x3, y3 ) ).Font.ColorIndex = 23  # set the word to be blue

        sheet.Range( "%s%s:%s%s" % ( x0, y4, x3, y4 ) ).Value = ["Retailer Company", "Project Name"] + data["x_header"]
        sheet.Range( "%s%s:%s%s" % ( x0, y4, x3, y4 ) ).WrapText = True
        # fill the content
        sheet.Range( "%s%s:%s%s" % ( x2, y5, x3, y6 ) ).Value = data["content"]
        # draw the cell line
        self._drawCellLine( sheet, x0, y0, x3, y7 )

        sheet.Range( "%s%s:%s%s" % ( x1, y8, x3, y8 ) ).Value = ["Total", ] + data["total"]
        sheet.Range( "%s%s:%s%s" % ( x2, y8, x3, y8 ) ).Interior.ColorIndex = 36  # yellow
        return x3, y8



    def _drawOneDetailTable2( self, sheet, x, y, data ):
        sub_y_header = []
        for h in data["hk_y_header"]:  sub_y_header.extend( h[-1] )  # add the hk project
        for h in data["sz_y_header"]:  sub_y_header.extend( h[-1] )  # add the sz project
        x0, x1, x2, x3 = x, self._addColumn( x, 1 ), self._addColumn( x, 2 ), self._addColumn( x, 1, len( data["x_header"] ) )
        y0, y1, y2, y3, y4, y5, y6, y7, y8 = y, y + 1, y + 2, y + 3, y + 4, y + 5, y + 4 + len( sub_y_header ), y + 5 + len( sub_y_header ), y + 5 + len( sub_y_header ) + self.default_row_space

        def _fillBlack( left, top, right, bottom ):
            range = "%s%s:%s%s" % ( left, top, right, bottom )
            sheet.Range( range ).Interior.Pattern = InteriorPattern["xlSolid"]
            sheet.Range( range ).Interior.PatternColorIndex = InteriorPatternColorIndex["xlAutomatic"]
#            sheet.Range(range).Interior.ThemeColor = XlThemeColor["xlThemeColorLight1"]  #problem in 2003, but OK in 2007
            sheet.Range( range ).Interior.ColorIndex = 1

        sheet.Range( "%s%s:%s%s" % ( x0, y0, x3, y0 ) ).Merge()
        _fillBlack( x0, y0, x3, y0 )
        sheet.Range( "%s%s:%s%s" % ( x0, y2, x3, y2 ) ).Merge()
        _fillBlack( x0, y2, x3, y2 )
        sheet.Range( "%s%s:%s%s" % ( x0, y7, x3, y7 ) ).Merge()
        _fillBlack( x0, y7, x3, y7 )
        sheet.Range( "%s%s:%s%s" % ( x0, y1, x3, y1 ) ).Merge()
        # draw title
        sheet.Range( "%s%s:%s%s" % ( x0, y1, x3, y1 ) ).Value = data["title"]
        sheet.Range( "%s%s:%s%s" % ( x0, y1, x3, y1 ) ).HorizontalAlignment = XlHAlign["xlHAlignCenter"]

        # draw y_header
        hk_y_offset = y_offest = y5
        for ( h, sub ) in data["hk_y_header"]:
            range = "%s%s:%s%s" % ( x0, y_offest, x0, y_offest + len( sub ) - 1 )
            sheet.Range( range ).Merge()
            sheet.Range( range ).Value = h
            y_offest += len( sub )

        if hk_y_offset != y_offest :
            sheet.Range( "%s%s:%s%s" % ( self._addColumn( x0, -1 ), hk_y_offset, self._addColumn( x0, -1 ), hk_y_offset ) ).Value = "HKO"  # draw hko title

        sz_y_offset = y_offest
        for ( h, sub ) in data["sz_y_header"]:
            range = "%s%s:%s%s" % ( x0, y_offest, x0, y_offest + len( sub ) - 1 )
            sheet.Range( range ).Merge()
            sheet.Range( range ).Value = h
            y_offest += len( sub )

        if sz_y_offset != y_offest :
            sheet.Range( "%s%s:%s%s" % ( x0, sz_y_offset, x3, y_offest - 1 ) ).Interior.ColorIndex = 40  # draw the szo rows to be orange
            sheet.Range( "%s%s:%s%s" % ( self._addColumn( x0, -1 ), sz_y_offset, self._addColumn( x0, -1 ), sz_y_offset ) ).Value = "SZO"  # draw szo title

        sheet.Range( "%s%s:%s%s" % ( x1, y5, x1, y6 ) ).Value = map( lambda v:[v], sub_y_header )
        # draw x_header
        header_x1 = "%s%s:%s%s" % ( x0, y3, x1, y3 )
        sheet.Range( header_x1 ).Merge()
        sheet.Range( header_x1 ).Value = "Program Details"
        header_x2 = "%s%s:%s%s" % ( self._addColumn( x1, 1 ), y3, self._addColumn( x1, 3 ), y3 )
        sheet.Range( header_x2 ).Merge()
        sheet.Range( header_x2 ).Value = "Designs"
        header_x3 = "%s%s:%s%s" % ( self._addColumn( x1, 4 ), y3, self._addColumn( x1, 6 ), y3 )
        sheet.Range( header_x3 ).Merge()
        sheet.Range( header_x3 ).Value = "Outputs"
        sheet.Range( "%s%s:%s%s" % ( self._addColumn( x1, 7 ), y3, self._addColumn( x1, 7 ), y3 ) ).Value = "Remarks"
        sheet.Range( "%s%s:%s%s" % ( x0, y3, x3, y3 ) ).HorizontalAlignment = XlHAlign["xlHAlignCenter"]
        # sheet.Range("%s%s:%s%s" %(x0,y3,x3,y3)).Font.Color = -4165632  #set the word to be blue
        sheet.Range( "%s%s:%s%s" % ( x0, y3, x3, y3 ) ).Font.ColorIndex = 23  # set the word to be blue

        sheet.Range( "%s%s:%s%s" % ( x0, y4, x3, y4 ) ).Value = ["Retailer Company", "Project Name"] + data["x_header"]
        sheet.Range( "%s%s:%s%s" % ( x0, y4, x3, y4 ) ).WrapText = True

        # fill the content
        data['hk_content'].extend( data['sz_content'] )
        sheet.Range( "%s%s:%s%s" % ( x2, y5, x3, y6 ) ).Value = data['hk_content']
        # draw the cell line
        self._drawCellLine( sheet, x0, y0, x3, y7 )

        sheet.Range( "%s%s:%s%s" % ( x1, y8, x3, y8 ) ).Value = ["Total", ] + data["total"]
        sheet.Range( "%s%s:%s%s" % ( x2, y8, x3, y8 ) ).Interior.ColorIndex = 36  # yellow
        return x3, y8


    def inputData( self, monthData, monthTotalData, monthCost, teamData, teamTotalData, teamCost, baseYear , kw):
        both  = kw.get( "designers", "BOTH" ) == "BOTH"
        start_x = "B"
        start_y = 3

        monthSheet = self.workBook.Sheets( 1 )
        monthSheet.Range( "A1:AB1" ).Value = "%s Job Summary" % baseYear
        x, y = start_x, start_y
        for row in monthData:
            ( newX, newY ) = self._drawOneRow( monthSheet, x, y, row )
            y = newY + self.default_row_space

        new_x, new_y = self._drawTotal( monthSheet, x, y, monthTotalData )
        # add the material front title
        monthSheet.Range( "%s%s" % ( self._addColumn( new_x, -len( monthTotalData[-1]["x_header"] ), -2 ), new_y - 1 ) ).Value = "Total used material:"
        monthSheet.Range( "%s%s" % ( self._addColumn( new_x, -len( monthTotalData[-1]["x_header"] ), -2 ), new_y ) ).Value = "Cost for each paper(HKD):"

        new_x = self._addColumn( new_x, 1, -self.default_column_space, -len( monthCost["x_header"] ) )
        new_y += self.default_row_space
        self._drawCost( monthSheet, new_x, new_y, monthCost["x_header"], monthCost["content"] )
        # add the total cost front title
        monthSheet.Range( "%s%s" % ( self._addColumn( new_x, -1 ), new_y ) ).Value = "Estimate spent on paper stock:"
        monthSheet.Range( "%s%s" % ( self._addColumn( new_x, -1 ), new_y + 1 ) ).Value = "(HKD)"
        monthSheet.Columns(3).ColumnWidth = 10
        monthSheet.Range("L:L").ColumnWidth = 10
        if both: monthSheet.Range("U:U").ColumnWidth = 10



        teamSheet = self.workBook.Sheets( 2 )
        teamSheet.Range( "A1" ).Value = "%s Job Summary" % baseYear
        x, y = start_x, start_y
        for row in teamData:
            ( newX, newY ) = self._drawOneRow( teamSheet, x, y, row )
            y = newY + self.default_row_space
        new_x, new_y = self._drawTotal( teamSheet, x, y, teamTotalData )
        # add the material front title
        teamSheet.Range( "%s%s" % ( self._addColumn( new_x, -len( teamTotalData[-1]["x_header"] ), -2 ), new_y - 1 ) ).Value = "Total used material:"
        teamSheet.Range( "%s%s" % ( self._addColumn( new_x, -len( teamTotalData[-1]["x_header"] ), -2 ), new_y ) ).Value = "Cost for each paper(HKD):"

        new_x = self._addColumn( new_x, 1, -self.default_column_space, -len( teamCost["x_header"] ) )
        new_y += self.default_row_space
        self._drawCost( teamSheet, new_x, new_y, teamCost["x_header"], teamCost["content"] )
        # add the total cost front title
        teamSheet.Range( "%s%s" % ( self._addColumn( new_x, -1 ), new_y ) ).Value = "Estimate spent on paper stock:"
        teamSheet.Range( "%s%s" % ( self._addColumn( new_x, -1 ), new_y + 1 ) ).Value = "(HKD)"


    def inputData2( self, allTeamData, baseYear ):
        start_x = "B"
        start_y = 3

        self.workBook.Sheets["template"].Range( "A1:AI1" ).Value = "%s Job Summary" % baseYear

        for oneTeam in allTeamData:
            # create sheet
            templateSheet = self.workBook.Sheets["template"]
            templateSheet.Copy( templateSheet )
            updateSheet = self.workBook.ActiveSheet
            updateSheet.name = oneTeam["name"]

            x, y = start_x, start_y

            _, y = self._drawOneRow( updateSheet, x, y, oneTeam["data"] )
            y += self.default_row_space
            x, y = self._drawTotal( updateSheet, x, y, oneTeam["total"] )


            # add the material front header
            updateSheet.Range( "%s%s" % ( self._addColumn( x, -len( oneTeam["total"][-1]["x_header"] ), -2 ), y - 1 ) ).Value = "Total used material:"
            updateSheet.Range( "%s%s" % ( self._addColumn( x, -len( oneTeam["total"][-1]["x_header"] ), -2 ), y ) ).Value = "Cost for each paper(HKD):"


            y += self.default_row_space
            range = "%s%s:%s%s" % ( "M", y, self._addColumn( "M", 8 ), y )
            updateSheet.Range( range ).Merge()
            updateSheet.Range( range ).Value = "Estimate spent on paper stock: HKD %.2f" % oneTeam["totalSpend"]
            updateSheet.Range( range ).Font.Bold = True
            updateSheet.Range( range ).Font.Size = 16
            updateSheet.Range( range ).Font.Underline = XlUnderlineStyle["xlUnderlineStyleDouble"]
            updateSheet.Range( range ).HorizontalAlignment = HorizontalAlignment["xlCenter"]

        self.workBook.Sheets["template"].Visible = False
        self.workBook.Sheets( 1 ).Select()


    def inputData3( self, allTeamData, baseYear ):
        start_x = "B"
        start_y = 3

#        self.workBook.Sheets["template"].Range("A1:AB1").Value = "%s Job Summary" %baseYear

        for oneTeam in allTeamData:
            templateSheet = self.workBook.Sheets["template"]
            templateSheet.Copy( templateSheet )
            updateSheet = self.workBook.ActiveSheet
            updateSheet.name = oneTeam["name"]
            x, y = start_x, start_y
            for d in oneTeam["data"]:
                _, y = self._drawOneDetailTable( updateSheet, x, y, d )
                y += self.default_row_space

        self.workBook.Sheets["template"].Visible = False
        self.workBook.Sheets( 1 ).Select()



    def inputData4( self, oneTeamData, baseYear ):
        start_x = "C"
        start_y = 3

        for oneMonth in oneTeamData['data']:
            templateSheet = self.workBook.Sheets["template"]
            templateSheet.Copy( templateSheet )
            updateSheet = self.workBook.ActiveSheet
            updateSheet.name = oneMonth["month"]
            x, y = start_x, start_y
            self._drawOneDetailTable2( updateSheet, x, y, oneMonth )

        self.workBook.Sheets["template"].Visible = False
        self.workBook.Sheets( 1 ).Select()




# add by cz@20120105
class LemmiOrderExcel( ExcelBasicGenerator ):
    def inputData( self, data = None ):
        excelSheet = self.workBook.Sheets( 1 )
        if not data:
            data = [( "", ), ]
        col = len( data[0] )
        startRow = 2
#        sheet.Range("A%d:%s%d" %(startRow, number2alphabet(col),
#                                 startRow+row-1)).Value = data
        for d in data:
            excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( col ),
                                     startRow ) ).Value = [d]
            startRow += 1

class CabelsOrderExcel( ExcelBasicGenerator ):
    def inputData( self, additionInfo = [], header = [], data = [] ):
        excelSheet = self.workBook.Sheets( 1 )
        excelSheet.Name = additionInfo[1]

        if not data: data = [( "", ), ]

        row = len( data )

        col = len( data[0] )
        startRow = 12
        lastRow = startRow + row
        startCol = 1
        '''
        excelSheet.Range("supplier_name").Value=additionInfo[0] if len(additionInfo)>1 else ''
        excelSheet.Range("A%d:%s%d"%(startRow, number2alphabet(col), lastRow)).Borders.LineStyle=1
        excelSheet.Range("A%d:%s%d"%(startRow, number2alphabet(col), lastRow)).Borders.Weight=2
        excelSheet.Range("A%d:%s%d"%(startRow, number2alphabet(col), lastRow)).Font.Name="Trebuchet MS"
        excelSheet.Range("A%d:%s%d"%(startRow, number2alphabet(col), lastRow)).Font.Size=12 
        '''
        excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( col ), lastRow - 1 ) ).Value = data


class TMWExcel( ExcelBasicGenerator ):
    def inputData( self, file = '', data = None ):
        if not data:
            data = [( "", ), ]
        excelSheet = self.workBook.Sheets( 1 )

        startRow = 2
        row = len( data )
        col = len( data[0] )
        excelSheet.Range( "A%d:%s%d" % ( startRow, number2alphabet( col ), startRow + row - 1 ) ).Value = data

class MglobalDailyExcel( ExcelBasicGenerator ):
    def inputData( self, data = None ):
        excelSheet = self.workBook.Sheets( 1 )
        if data:
            row = len( data )
            col = len( data[0] )
            startRow = 5
            lastRow = startRow + row
            startCol = 2
            for i in data:
                for index in range( col ):
                    # print "A%d:%s%d" % (startRow, number2alphabet(startCol+index), startRow + row - 1), i[index]
                    excelSheet.Cells( startRow, number2alphabet( startCol + index ) ).Value = i[index]
                startRow += 1





'''
class PrepressSummary(ExcelBasicGenerator):

    default_column_space = 2  # 3 column to seperate the two data
    default_row_space = 2

    def _addColumn(self, c, *addtion):
        return number2alphabet(alphabet2number(c) + sum(addtion))


    def _drawCellLine(self, sheet, left, top, right, bottom):
        sheet_range = "%s%s:%s%s" % (left, top, right, bottom)
        for line in ["xlEdgeBottom", "xlEdgeLeft", "xlEdgeRight", "xlEdgeTop"]:
            sheet.Range(sheet_range).Borders(XlBordersIndex[line]).Weight = XlBorderWeight["xlMedium"]
            sheet.Range(sheet_range).Borders(XlBordersIndex[line]).LineStyle = 1
        for line in ["xlInsideHorizontal", "xlInsideVertical"]:
            sheet.Range(sheet_range).Borders(XlBordersIndex[line]).Weight = XlBorderWeight["xlThin"]
            sheet.Range(sheet_range).Borders(XlBordersIndex[line]).LineStyle = 1


    def _drawRangLine(self, sheet, left, top, right, bottom):
        range = "%s%s:%s%s" % (left, top, right, bottom)
        # draw the left top cell
        sheet.Range("%s%s:%s%s" % (left, top, left, top + 1)).Merge()
        sheet.Range("%s%s:%s%s" % (left, top, left, top + 1)).Borders(XlBordersIndex["xlDiagonalDown"]).LineStyle = 1
        # draw the top,left,right,bottom,inside line
        self._drawCellLine(sheet, left, top, right, bottom)



    def _drawOneTable(self, sheet, x_offest, y_offest, x_header, y_header, content, y_title):

        x0, x1, x2 = x_offest, self._addColumn(x_offest, 1), self._addColumn(x_offest, len(x_header))
        y0, y1, y2, y3 = y_offest, y_offest + 1, y_offest + 2, y_offest + 1 + len(y_header)
        # fill in the header
        self._drawYTitle(sheet, x1, y0, x2, y0, y_title)
        sheet.Range("%s%s:%s%s" % (x0, y2, x0, y3)).Value = map(lambda v:[v], y_header)
        sheet.Range("%s%s:%s%s" % (x1, y1, x2, y1)).Value = x_header
        sheet.Range("%s%s:%s%s" % (x1, y1, x2, y1)).WrapText = True
        # fill in the data
        sheet.Range("%s%s:%s%s" % (x1, y2, x2, y3)).Value = content

        self._drawRangLine(sheet, x0, y0, x2, y3)
        return (x0, y0, x2, y3)  # left,top,right,bottom


    def _drawXTitle(self, sheet, left, top, right, bottom, name):
        range = "%s%s:%s%s" % (left, top, right, bottom)
        sheet.Range(range).Merge()
        sheet.Range(range).Value = name
        sheet.Range(range).Orientation = -90  # transfrer the text to vitical
        sheet.Range(range).Font.Size = 22  # bold the word
        sheet.Range(range).VerticalAlignment = XlHAlign["xlHAlignCenter"]  # set the font to middle
        sheet.Range("%s%s" % (left, top)).ColumnWidth = 4.6


    def _drawYTitle(self, sheet, left, top, right, bottom, name):
        range = "%s%s:%s%s" % (left, top, right, bottom)
        sheet.Range(range).Merge()
        sheet.Range(range).Value = name
        sheet.Range(range).HorizontalAlignment = XlHAlign["xlHAlignCenter"]


    def _drawOneRow(self, sheet, x0, y0, data):
        ys = []
        x, y = x0, y0
        for index, d in enumerate(data):
            if index == 0 :
                self._drawXTitle(sheet, x, y, x, y + 1 + len(d["y_header"]), d["x_title"])
                x = self._addColumn(x, 1)
            (_, _, _, new_y) = self._drawOneTable(sheet, x, y, d["x_header"], d["y_header"], d["content"], d["y_title"])
            x = self._addColumn(x, len(d["x_header"]), self.default_column_space)
            ys.append(new_y)
        return (x0, max(ys))


    def _drawTotalTable(self, sheet, x, y, header, data):
        x0, x1 = self._addColumn(x, 1), self._addColumn(x, len(header))
        y0, y1, y2 = y, y + 1, y + len(data)
        self._drawCellLine(sheet, x0, y0, x1, y2)
        sheet.Range("%s%s:%s%s" % (x0, y0, x1, y0)).Value = header
        sheet.Range("%s%s:%s%s" % (x0, y1, x1, y2)).Value = data
        return x0, y0, x1, y2


    def _drawTotal(self, sheet, x, y, data):
        x_offest, y_offest = self._addColumn(x, 1), y
        max_y = []
        for d in data:
            (_, _, new_x_offest, new_y_offest) = self._drawTotalTable(sheet, x_offest, y_offest, d["x_header"], d["content"])
            x_offest = self._addColumn(new_x_offest, self.default_column_space)
            max_y.append(new_y_offest)
        return (x_offest, max(max_y))


    def inputData(self, monthData, monthTotalData, teamData, teamTotalData, baseYear):
        start_x = "B"
        start_y = 3

        monthSheet = self.workBook.Sheets(1)
        monthSheet.Range("A1:AB1").Value = "%s Job Summary" % baseYear
        x, y = start_x, start_y
        for row in monthData:
            (newX, newY) = self._drawOneRow(monthSheet, x, y, row)
            y = newY + self.default_row_space

        new_x, new_y = self._drawTotal(monthSheet, x, y, monthTotalData)
        monthSheet.Columns("A:AZ").EntireColumn.AutoFit()

        teamSheet = self.workBook.Sheets(2)
        teamSheet.Range("A1").Value = "%s Job Summary" % baseYear
        x, y = start_x, start_y
        for row in teamData:
            (newX, newY) = self._drawOneRow(teamSheet, x, y, row)
            y = newY + self.default_row_space
        new_x, new_y = self._drawTotal(teamSheet, x, y, teamTotalData)
        teamSheet.Columns("A:AZ").EntireColumn.AutoFit()
'''




class PrepressSummary( ExcelBasicGenerator ):
    def _addColumn( self, c, *addtion ):
        return number2alphabet( alphabet2number( c ) + sum( addtion ) )


    def _drawCellLine( self, sheet, sheet_range ):
        for line in ["xlEdgeBottom", "xlEdgeLeft", "xlEdgeRight", "xlEdgeTop"]:
            sheet.Range( sheet_range ).Borders( XlBordersIndex[line] ).Weight = XlBorderWeight["xlMedium"]
            sheet.Range( sheet_range ).Borders( XlBordersIndex[line] ).LineStyle = 1
        for line in ["xlInsideHorizontal", "xlInsideVertical"]:
            sheet.Range( sheet_range ).Borders( XlBordersIndex[line] ).Weight = XlBorderWeight["xlThin"]
            sheet.Range( sheet_range ).Borders( XlBordersIndex[line] ).LineStyle = 1


    def _drawPieChart( self , title = None ):
        if title : self.workBook.ActiveChart.ChartTitle.Text = title
        self.workBook.ActiveChart.SetElement( 2 )  # msoElementChartTitleAboveChart 2 Display title above chart.
        self.workBook.ActiveChart.ChartArea.Select()
        self.workBook.ActiveChart.SeriesCollection( 1 ).ApplyDataLabels()
        self.workBook.ActiveChart.SeriesCollection( 1 ).DataLabels().Select()
        self.excelObj.Selection.POsition = 2  # xlLabelPositionOutsideEnd
        self.excelObj.Selection.ShowPercentage = True  # show the percentage
        self.excelObj.Selection.ShowSeriesName = False
        self.excelObj.Selection.ShowCategoryName = True  # show the catory name
        self.excelObj.Selection.ShowValue = False  # don't show the value


    def inputData( self, teamTotal, taskTotal, summary, jobsummary ):
        sheet = self.workBook.Sheets( 1 )
        startRow = 2
        startCol, teamCol, jobCol = 'A', 'A', 'D'

        #=======================================================================
        # draw team chart
        #=======================================================================
        if not teamTotal : teamTotal = [( '', '' )]
        team_range = "%s%s:%s%s" % ( teamCol, startRow, self._addColumn( teamCol, len( teamTotal[0] ), -1 ), len( teamTotal ) + startRow - 1 )
        sheet.Range( team_range ).Value = teamTotal
        self._drawCellLine( sheet, team_range )

        #=======================================================================
        # draw task chart
        #=======================================================================
        if not taskTotal : taskTotal = [( '', '' )]
        task_range = "%s%s:%s%s" % ( jobCol, startRow, self._addColumn( jobCol, len( taskTotal[0] ), -1 ), len( taskTotal ) + startRow - 1 )
        sheet.Range( task_range ).Value = taskTotal
        self._drawCellLine( sheet, task_range )

        rows = max( [len( teamTotal ), len( taskTotal )] )

        #=======================================================================
        # draw job detail chart
        #=======================================================================
        curRow = startRow + rows + 2
        tmpCol = startCol
        for data in summary:
            tmp_range = "%s%s:%s%s" % ( tmpCol, curRow, self._addColumn( tmpCol, len( data[0] ), -1 ), len( data ) + curRow - 1 )
            sheet.Range( tmp_range ).Value = data
            self._drawCellLine( sheet, tmp_range )
            tmpCol = self._addColumn( tmpCol, len( data[0] ), 1 )

        sheet.Columns( "A:AZ" ).EntireColumn.AutoFit()
        # draw graphic
        sheet.ChartObjects()[0].Activate()

        self.workBook.ActiveChart.SetSourceData( sheet.Range( team_range ) )
        self._drawPieChart( "Monthly Utilization for\n(Pre-Flight & Artwork Adaption)" )

        _chartSpace = 3
        # move the chart down
        sheet.Shapes( "graphic1" ).IncrementTop( 12 * ( len( summary[0] ) + _chartSpace ) )


        # draw the job type summary graphic
        datasheet = self.workBook.Sheets( 2 )
        _scolumn = 'A'
        _chartcol = 'H'
        curRow += len( summary[0] )

        for i, k in enumerate( sorted( jobsummary.keys() ) ):
            v = jobsummary[k]
            _c = [( k2, v2 ) for k2, v2 in v['jobs'].items()]
            _range = '%s%s:%s%s' % ( self._addColumn( _scolumn, i * 2 ), 1 , self._addColumn( _scolumn, i * 2, 1 ) , len( _c ) )
            datasheet.Range( _range ).Value = _c
            sheet.ChartObjects( 'graphic1' ).Activate()
            self.workBook.ActiveChart.ChartArea.Copy()
            sheet.Range( "%s%s" % ( _chartcol, curRow + _chartSpace ) ).Select()
            sheet.Paste()
            self.workBook.ActiveChart.SetSourceData( datasheet.Range( _range ) )
            self._drawPieChart( v['label'] )
            _chartcol = self._addColumn( _chartcol, 8 )

#             sheet.Shapes( "graphic_%s" % k1 ).IncrementTop( 20 * ( curRow - startRow + len( summary[0] ) ) )
        sheet.Range( "%s%s" % ( startCol, startRow ) ).select
        datasheet.Select()
        self.excelObj.ActiveWindow.SelectedSheets.Visible = False



'''
class PrepressDesigner( PrepressSummary ):

    def inputData( self, designData, params ):
        startRow = 5
        nameCol, startCol, endCol = 'A', 'B', 'D'
        sheet = self.workBook.Sheets( 1 )

        allData, currentRow = [], startRow
        for v in designData.values():
            name, data = v['name'], v['data']
            allData.extend( data )
            r = "%s%s:%s%s" % ( nameCol, currentRow, nameCol, currentRow + len( data ) - 1 )
            sheet.Range( r ).Merge()
            sheet.Range( r ).VerticalAlignment = XlHAlign["xlHAlignCenter"]    # set the font to middle
            sheet.Range( r ).Value = name
            currentRow += len( data )

        valRange = "%s%s:%s%s" % ( startCol, startRow, endCol, startRow + len( allData ) - 1 )
        sheet.Range( valRange ).Value = allData
        self._drawCellLine( sheet, '%s%s:%s%s' % ( nameCol, startRow, endCol, currentRow - 1 ) )

        sheet.Range( 'from' ).Value = params.get( 'from', '' )
        sheet.Range( 'to' ).Value = params.get( 'to', '' )

'''
