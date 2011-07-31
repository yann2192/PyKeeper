#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2011 Yann GUIBET <yannguibet@gmail.com>
#  See LICENSE for details.

import sqlite3
from base64 import b64encode
from xml.dom.minidom import Document, parseString
from tempfile import mktemp
from Config import *
from gevent import sleep

class Index:
    def __init__(self, db=''):
        if id == '':
            self.db = sqlite3.connect(mktemp())
        else:
            self.db = sqlite3.connect(db)
        try:
            self.create()
        except:
            pass
    
    def create(self):
        try:
            c = self.db.cursor()
            c.execute('CREATE TABLE datas (id INTEGER PRIMARY KEY, data TEXT, iv TEXT, hash TEXT)')
            self.db.commit()
        finally:
            c.close()

    def get_all(self):
        c = self.db.cursor()
        res = []
        try:
            c.execute('SELECT * FROM datas')
            self.db.commit()
            for i in c:
                res.append(i)
        finally:
            c.close()
            return res

    def get_data_by_id(self, id):
        c = self.db.cursor()
        res = None
        try:
            c.execute('SELECT * FROM datas WHERE id="%d"' % id)
            self.db.commit()
            res = c.fetchone()
        except:
            pass
        
        finally:
            c.close()
            return res

    def add_data(self, data, iv, hash):
        c = self.db.cursor()
        try:
            c.execute('INSERT INTO datas VALUES (NULL, "'+b64encode(data)+'", "'+b64encode(iv)+'", "'+b64encode(hash)+'")')
            self.db.commit()
        except:
            raise

        finally:
            c.close()            

    def rm_data(self, id):
        c = self.db.cursor()
        try:
            c.execute('DELETE FROM datas WHERE id=%d' % id)
            self.db.commit()
            if c.rowcount == 0:
                raise Exception, "FAIL to rm_data"
        except:
            raise

        finally:
            c.close()

    def update_data(self, id, data, iv, hash):
        c = self.db.cursor()
        try:
            c.execute('UPDATE datas SET data="%s", iv="%s", hash="%s" WHERE id=%d' % (b64encode(data), b64encode(iv), b64encode(hash), id))
            self.db.commit()
        
        except:
            raise

        finally:
            c.close()                    

    def get_xml(self):
        buff = self.get_all()
        res = Document()
        xml = res.createElement("datas")
        for i in buff:
            sleep(0)
            data = res.createElement("data")
            data.setAttribute("id", str(i[0]))
            data.setAttribute("data", i[1])
            data.setAttribute("iv", i[2])
            data.setAttribute("hash", i[3])
            xml.appendChild(data)
        res.appendChild(xml)
        return res.toxml()

    def set_xml(self, xml):
        c = self.db.cursor()
        try:
            c.execute('DELETE FROM datas WHERE 1=1')
            self.db.commit()
            xml = parseString(xml)
            index = xml.getElementsByTagName("data")
            for i in index:
                sleep(0)
                c.execute('INSERT INTO datas VALUES(%d, "%s", "%s", "%s")' % (int(i.getAttribute("id")), i.getAttribute("data"), i.getAttribute("iv"), i.getAttribute("hash")))
        except:
            raise

        finally:
            self.db.commit()
            c.close()
