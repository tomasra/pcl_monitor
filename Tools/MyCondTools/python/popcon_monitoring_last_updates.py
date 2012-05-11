import sys,os,re,time
from xml.dom import minidom
    
try:
    import cx_Oracle
except ImportError, e: 
    print "Cannot import cx_Oracle:", e 



from xml.sax.handler import ContentHandler
from xml.sax import make_parser, SAXException
import re 

# this implements the generic parsing of the authentication file
def extract(searchTerm, authfile='./authentication.xml'):
    '''
    Obtains DB connection string from xml file

    @var searchTerm1: DB name for which connection string is constructed
    @var authfile: xml file name where stored connection data
    
    @return: tuple ('connectionString', 'user', 'schema')
    '''
    
    class conHandler(ContentHandler):
        '''        
        Overriden SAX ContentHandler for parser
        '''
        
        def __init__(self, searchTerm):
            self.searchTerm = searchTerm
            self.state = 0 # 0 - searching; 1 - DB name obtained; 2 - username obtained
            self.conDict = {}
            
        def startElement(self, name, attrs):
            # getting password
            if self.state == 2:
                self.conDict['password'] = attrs.getValue("value")
                raise SAXException() # stop parsing
            # getting username
            if self.state == 1:
                self.conDict['user'] = attrs.getValue("value")
                self.state = 2
            # getting DB name & schema
            if name == "connection" and attrs.getValue("name") == self.searchTerm:
                splitedDBConList = re.split(r'//', attrs.getValue("name"))
                splitedDBConList = re.split(r'/', splitedDBConList[1])
                self.conDict['dbName'] = splitedDBConList[0]
                if len(splitedDBConList) == 1 or splitedDBConList[1] == '':   # Checking for schema presence
                    self.conDict['schema'] = ''
                else:
                    self.conDict['schema'] = splitedDBConList[1]
                self.state = 1
            
    parser = make_parser()
    handler = conHandler(searchTerm)
    parser.setContentHandler(handler)
    try:
        parser.parse(authfile)
    except Exception, e:
        if 'password' in handler.conDict:
            connectionString = str(handler.conDict['user']+'/'+handler.conDict['password']+'@'+handler.conDict['dbName'])           
            connectionDict = {'connectionstring': connectionString, 'user':str(handler.conDict['user']), 'schema': str(handler.conDict['schema'])}
            return connectionDict
        else:
            raise Exception('Can\'t extract connection string from ' + authfile + '\n\tError code: ' + str(e))
    
    return None



    
class PopCon_Monitoring_last_updates:
    """
    This class retrieves the list of the transaction
    performed against the CMS condition databases
    using the information stored in the POPCONLOG account.
    In order to use it, pass to the constructor the time interval
    you want to check (ending now, in seconds) and the overlap,
    i.e. an additional time interval which is added to interval.
    """
 
    def __init__(self,overlap=2,interval=60):
        self.num_rows   =   0
        self.overlap    =   overlap
        self.interval   =   interval
    
    def extract(self,authfile="./auth.xml"):
        """
        This method extracts the string for the database connection
        using the ORACLE client from an xml authentication file.
        The structure of the authentication file is:
        <connectionlist>
         <connection name=\"oracle://oracle_tns_name/oracle_schema\">
          <parameter name=\"user\" value=\"user_name\"/>
          <parameter name=\"password\" value=\"user_password\"/>
         </connection>
        </connectionlist>
        """
        try:
            conn_dict               =   {}
            conn_dict = extract("oracle://cms_orcon_adg/CMS_COND_31X_POPCONLOG", authfile)
            conn_dict['account'] = 'CMS_COND_31X_POPCONLOG'
            #print conn_dict            
            return conn_dict
        except IOError, e:
            print "Authentication file not found", e
            #sys.exit()
        
    def check(self,authfile='./auth.xml'):
        records =   []
        records =   self.PopConRecentActivityRecorded(authfile)
        if (self.num_rows   !=  0):
            print time.ctime()," nums rows: ",self.num_rows
        else:
            print time.ctime()," no new payload uploads"    
            
        return records

    def PopConJobRunTime(self, authfile="./auth.xml",logFile = 'EcalLaserTimeBasedO2O.log'):
        try:
            conn_dict =   self.extract(authfile)
            #conn_string =   str(conn_dict['user']+'/'+conn_dict['password']+'@'+conn_dict['db_name'])
            conn_string = conn_dict['connectionstring']
        except Exception, e:
            print "Something went wrong with auth file", e
            sys.exit()
        
        #print conn_string
        conn =   cx_Oracle.connect(conn_string)
        try:
            start = time.time()
            curs = conn.cursor()

            # payloadtoken,

            sqlstr = """
            select 
            crontime,
            prevcrontime,
            short_tail
            FROM """+str(conn_dict['account'])+""".logtails
            WHERE
            filename = '""" + str(logFile) + """'
            """
            rows    =   curs.execute(sqlstr)
            #rows    =   curs.fetchall()
            name_of_columns =   []
            for fieldDesc in curs.description:     
                name_of_columns.append(fieldDesc[0])
            rows                        =   {}
            rows['name_of_columns']     =   name_of_columns
            rows['data']                =   {}
            rows['data']                =   curs.fetchall()
            self.num_rows   =   len(rows['data'])
            #print rows['data']
            return rows['data']
        finally:
            conn.close()

    
    def PopConRecentActivityRecorded(self,authfile="./auth.xml",account="",iovtag="",start_date="",end_date=""):
        if start_date=='':
            start_date  =   self.get_default_date('one_minute_ago')
        else:
            start_date  =   self.transform_date(start_date)
            
        if end_date=='':
            end_date  =   self.get_default_date('now')
        else:
            end_date    =   self.transform_date(end_date)
        
        time_constraints    =   """
        exectime 
        between 
        to_date('"""+start_date+"""', 'MM/DD/YYYY HH24:MI:SS') and 
        to_date('"""+end_date+"""', 'MM/DD/YYYY HH24:MI:SS') 
        """
        try:
            conn_dict =   self.extract(authfile)
            #conn_string =   str(conn_dict['user']+'/'+conn_dict['password']+'@'+conn_dict['db_name'])
            conn_string = conn_dict['connectionstring']
        except Exception, e:
            print "Something went wrong with auth file", e
            sys.exit()

        #print conn_string
        conn =   cx_Oracle.connect(conn_string)
        try:
            start = time.time()
            curs = conn.cursor()

            # payloadtoken,

            sqlstr = """
            select 
            logid,
            to_char(exectime, 'FMMonth, ddth YYYY ') || to_char(exectime, 'HH24:MI:SS') as exectime, 
            iovtag, 
            payloadname,
            payloadindex,
            destinationdb, 
            execmessage,
            usertext,
            payloadtoken
            from """+str(conn_dict['account'])+""".cond_log_view 
            where 
            """+time_constraints+"""
            and destinationdb like '%"""+account+"""%'
            and iovtag like '%"""+iovtag+"""%'
            and rownum<155
            and execmessage like '%OK%'
            order by """+str(conn_dict['account'])+""".cond_log_view.logid desc
            """
            rows    =   curs.execute(sqlstr)
            #rows    =   curs.fetchall()
            name_of_columns =   []
            for fieldDesc in curs.description:     
                name_of_columns.append(fieldDesc[0])
            rows                        =   {}
            rows['name_of_columns']     =   name_of_columns
            rows['data']                =   {}
            rows['data']                =   curs.fetchall()
            self.num_rows   =   len(rows['data'])
            #print rows['data']
            return rows
        finally:
            conn.close()
                        
    def get_default_date(self,what): 
        now_sec             =   time.time()
        now_tupla           =   time.localtime(now_sec)
        now                 =   str(now_tupla[1])+"/"+str(now_tupla[2])+"/"+str(now_tupla[0])+" "+str(now_tupla[3])+":"+str(now_tupla[4])+":"+str(now_tupla[5])
        
        one_minute_ago_sec  =   now_sec - ( self.overlap + self.interval )
        one_minute_ago_secT =   time.localtime(one_minute_ago_sec)
        one_minute_ago      =   str(one_minute_ago_secT[1])+"/"+str(one_minute_ago_secT[2])+"/"+str(one_minute_ago_secT[0])+' '+str(one_minute_ago_secT[3])+':'+str(one_minute_ago_secT[4])+':'+str(one_minute_ago_secT[5])
        
        today_sec       =   time.time()
        today_tupla     =   time.gmtime(today_sec)
        today           =   str(today_tupla[1])+"/"+str(today_tupla[2])+"/"+str(today_tupla[0])
        
        yesterday_sec   =   today_sec - 86400
        yesterday_tupla =   time.gmtime(yesterday_sec)
        yesterday       =   str(yesterday_tupla[1])+"/"+str(yesterday_tupla[2])+"/"+str(yesterday_tupla[0])
        
        one_month_ago_sec   =   today_sec - (86400*30)
        one_month_ago_tupla =   time.gmtime(one_month_ago_sec)
        one_month_ago       =   str(one_month_ago_tupla[1])+"/"+str(one_month_ago_tupla[2])+"/"+str(one_month_ago_tupla[0])
        
        if(what=='now'):
            return now
        if(what=='one_minute_ago'):
            return one_minute_ago
        if(what=='today'):
            return today
        if(what=='yesterday'):
            return yesterday
        if(what=='one_month_ago'):
            return one_month_ago

if __name__     ==  "__main__":
    authentication = "/afs/cern.ch/cms/DB/conddb/ADG/authentication.xml"

    p=PopCon_Monitoring_last_updates(interval=300)
    p.check(authentication)
    print extract("oracle://cms_orcon_adg/CMS_COND_31X_POPCONLOG", authentication)
    p.PopConJobRunTime(authentication)
