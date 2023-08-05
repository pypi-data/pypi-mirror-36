#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import
import collections
import six

import sys

class Argument(object):
    """ 項に関する情報を保持するオブジェクト 

    詳しくは下記ページの「格要素側」の記述方法を参照
    http://nlp.ist.i.kyoto-u.ac.jp/index.php?KNP%2F%E6%A0%BC%E8%A7%A3%E6%9E%90%E7%B5%90%E6%9E%9C%E6%9B%B8%E5%BC%8F

    Attributes:
        sid (str): 文ID
        tid (int): 基本句ID
        eid (int): Entity ID
        midasi (str): 表記
        flag (str): フラグ (C, N, O, D, E, U)
        sdist (int): 述語の何文前か
    """
    def __init__(self, sid=None, tid=None, eid=None, midasi='', flag=None, sdist=None):
        assert isinstance(tid, int)
        assert isinstance(midasi, six.text_type)
        self.sid = sid
        self.tid = tid
        self.eid = eid
        self.midasi = midasi
        self.flag = flag
        self.sdist = sdist 

ArgRepname = collections.namedtuple("ArgRepname", "repname,tid_list")


class Pas(object):
    """ 述語項構造を扱うクラス

    Usage:
        result = knp.result(knp_result)
        pas = Pas(5, result)

    Attributes:
        arguments (dict of (case, list of Argument)): 
                 格と項を対応付けた辞書 {case: [Argument, ..]}
                 keyは格を表す文字列, valueはArgumentオブジェクトのリスト。
                 リスト形式なのは、ガ格などは複数の項を取り得るため。
    """
    def __init__(self, tid=None, result=None, knpstyle=True):
        self.valid = True
        self.cfid = None 
        self.arguments = collections.defaultdict(list)
         
        if tid is None:
            self.valid = False
            return
            
        self.tid = tid
        self.tag_list = result.tag_list()

        pas_analysis = self.tag_list[self.tid].features.get("述語項構造") # -anaphoraの場合
        if pas_analysis is not None:
            self.__parse_case_analysis(pas_analysis, pasFlag=True)

        case_analysis = self.tag_list[self.tid].features.get("格解析結果")
        if(case_analysis is None):
            self.valid = False
            return
        self.__parse_case_analysis(case_analysis)
        return
    
    def is_valid(self):
        return self.valid
   
    def get_arguments(self,case):
        """
        指定した格の各項ごとに代表表記の配列を返す
        """
        output = []
        for arg in self.arguments[case]:
            tid = arg.tid
            rep = self.tag_list[tid].repname
            output.append(ArgRepname("+".join(rep), tid)) 
        return output
    
    def get_orig_result(self):
        return self.tag_list[self.tid].features.get("格解析結果")
     
    def __parse_case_analysis(self, analysis_result, pasFlag=False):
        assert isinstance(analysis_result, six.text_type)
        c0 = analysis_result.find(':')
        c1 = analysis_result.find(':', c0 + 1)
        self.cfid = analysis_result[:c0] + ":" + analysis_result[c0 + 1:c1]
        
        if analysis_result.count(":") < 2:  # For copula
            self.valid = False
            return
        
        for k in analysis_result[c1 + 1:].split(';'):
            items = k.split("/")
            caseflag = items[1]
            if caseflag == "U" or caseflag == "-":
                continue
            
            if pasFlag: # anaphora
                mycase = items[0]
                midasi = items[2]
                sdist = int(items[3])
                tid = int(items[4])
                eid = int(items[5])
                arg = Argument(sdist=sdist, tid=tid, eid=eid, midasi=midasi, flag=caseflag)
                self.arguments[mycase].append(arg)
            else:
                mycase = items[0]
                midasi = items[2]
                tid = int(items[3])
                sdist = int(items[4])
                sid = items[5]
               
                arg = Argument(sid=sid, tid=tid, midasi=midasi, flag=caseflag, sdist=sdist)
                self.arguments[mycase].append(arg)


