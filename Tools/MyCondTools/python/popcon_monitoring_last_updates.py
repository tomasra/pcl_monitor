import sys,os,re,time
from xml.dom import minidom
    
try:
    import cx_Oracle
except ImportError, e: 
    print "Cannot import cx_Oracle:", e 
    
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
            xmldoc = minidom.parse(authfile)
            
            reflist     =   xmldoc.getElementsByTagName('connection')
            bitref      =   reflist[0]
            db_name     =   bitref.attributes["name"]
            
            reflist     =   xmldoc.getElementsByTagName('parameter')
            bitref      =   reflist[0]
            user        =   bitref.attributes["value"]
            bitref      =   reflist[1]
            password    =   bitref.attributes["value"]
            
            
            lista = re.split(r'//', db_name.value)
            lista = re.split(r'/', lista[1])
            db_name.value   =   lista[0]
            #user.value      =   lista[1]
            conn_dict               =   {}
            conn_dict['account']    =   lista[1]  
            conn_dict['user']       =   user.value
            conn_dict['password']   =   password.value
            conn_dict['db_name']    =   db_name.value
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
            conn_string =   str(conn_dict['user']+'/'+conn_dict['password']+'@'+conn_dict['db_name'])
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
    p=PopCon_Monitoring_last_updates(interval=300)
    p.check()
