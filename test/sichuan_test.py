#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest

# Add the repo root to the Python module path.
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src import sichuan
from src.sichuan import ArithmeticExpr
from src.sichuan import LiteralExpr
from src.sichuan import BasicTokenize
from src.sichuan import CallExpr
from src.sichuan import ComparisonExpr
from src.sichuan import ConcatExpr
from src.sichuan import Keyword
from src.sichuan import ParenExpr
from src.sichuan import ParseChars
from src.sichuan import ParseExprFromStr
from src.sichuan import ParseInteger
from src.sichuan import ParseStmtFromStr
from src.sichuan import ParseToAst
from src.sichuan import Run
from src.sichuan import STMT_ASSIGN
from src.sichuan import STMT_CALL
from src.sichuan import STMT_CONDITIONAL
from src.sichuan import STMT_DEC_BY
from src.sichuan import STMT_FUNC_DEF
from src.sichuan import STMT_INC_BY
from src.sichuan import STMT_LOOP
from src.sichuan import STMT_SAY
from src.sichuan import Statement
from src.sichuan import TK_CHAR
from src.sichuan import TK_IDENTIFIER
from src.sichuan import TK_INTEGER_LITERAL
from src.sichuan import TK_STRING_LITERAL
from src.sichuan import Token
from src.sichuan import Tokenize
from src.sichuan import VariableExpr

class SichuanParseExprTest(unittest.TestCase):
  def testParseInteger(self):
    self.assertEqual(ParseExprFromStr(u'5')[0],
                     LiteralExpr(Token(TK_INTEGER_LITERAL, 5)))
    self.assertEqual(ParseExprFromStr(u'九')[0],
                     LiteralExpr(Token(TK_INTEGER_LITERAL, 9)))
    
  def testParseStringLiteral(self):
    self.assertEqual(ParseExprFromStr(u'“ 哈  哈   ”')[0],
                     LiteralExpr(Token(TK_STRING_LITERAL, u' 哈  哈   ')))

  def testParseIdentifier(self):
    self.assertEqual(ParseExprFromStr(u'老王')[0],
                     VariableExpr(Token(TK_IDENTIFIER, u'老王')))

  def testParseParens(self):
    # Wide parens.
    self.assertEqual(ParseExprFromStr(u'（老王）')[0],
                     ParenExpr(
                         VariableExpr(Token(TK_IDENTIFIER, u'老王'))))
    # Narrow parens.
    self.assertEqual(ParseExprFromStr(u'(老王)')[0],
                     ParenExpr(
                         VariableExpr(Token(TK_IDENTIFIER, u'老王'))))

  def testParseCallExpr(self):
    self.assertEqual(ParseExprFromStr(u'喊老王')[0],
                     CallExpr(Token(TK_IDENTIFIER, u'老王'), []))
    self.assertEqual(ParseExprFromStr(u'喊老王（5）')[0],
                     CallExpr(Token(TK_IDENTIFIER, u'老王'),
                              [LiteralExpr(Token(TK_INTEGER_LITERAL, 5))]))
    self.assertEqual(ParseExprFromStr(u'喊老王(6)')[0],
                     CallExpr(Token(TK_IDENTIFIER, u'老王'),
                              [LiteralExpr(Token(TK_INTEGER_LITERAL, 6))]))
    self.assertEqual(ParseExprFromStr(u'喊老王(老刘，6)')[0],
                     CallExpr(Token(TK_IDENTIFIER, u'老王'),
                              [VariableExpr(Token(TK_IDENTIFIER, u'老刘')),
                               LiteralExpr(Token(TK_INTEGER_LITERAL, 6))]))
    self.assertEqual(ParseExprFromStr(u'喊老王(“你”，老刘，6)')[0],
                     CallExpr(Token(TK_IDENTIFIER, u'老王'),
                              [LiteralExpr(Token(TK_STRING_LITERAL, u'你')),
                               VariableExpr(Token(TK_IDENTIFIER, u'老刘')),
                               LiteralExpr(Token(TK_INTEGER_LITERAL, 6))]))
    self.assertEqual(ParseExprFromStr(u'喊老王(“你”,老刘，6)')[0],
                     CallExpr(Token(TK_IDENTIFIER, u'老王'),
                              [LiteralExpr(Token(TK_STRING_LITERAL, u'你')),
                               VariableExpr(Token(TK_IDENTIFIER, u'老刘')),
                               LiteralExpr(Token(TK_INTEGER_LITERAL, 6))]))

  def testParseTermExpr(self):
    self.assertEqual(ParseExprFromStr(u'老王乘五')[0],
                     ArithmeticExpr(
                         VariableExpr(Token(TK_IDENTIFIER, u'老王')),
                         Keyword(u'乘'),
                         LiteralExpr(Token(TK_INTEGER_LITERAL, 5)))
                     )
    self.assertEqual(ParseExprFromStr(u'五除以老王')[0],
                     ArithmeticExpr(
                         LiteralExpr(Token(TK_INTEGER_LITERAL, 5)),
                         Keyword(u'除以'),
                         VariableExpr(Token(TK_IDENTIFIER, u'老王')))
                     )
    self.assertEqual(ParseExprFromStr(u'五除以老王乘老刘')[0],
                     ArithmeticExpr(
                         ArithmeticExpr(
                             LiteralExpr(Token(TK_INTEGER_LITERAL, 5)),
                             Keyword(u'除以'),
                             VariableExpr(Token(TK_IDENTIFIER, u'老王'))),
                         Keyword(u'乘'),
                         VariableExpr(Token(TK_IDENTIFIER, u'老刘'))
                     ))

  def testParseArithmeticExpr(self):
    self.assertEqual(ParseExprFromStr(u'5加六')[0],
                     ArithmeticExpr(
                         LiteralExpr(Token(TK_INTEGER_LITERAL, 5)),
                         Keyword(u'加'),
                         LiteralExpr(Token(TK_INTEGER_LITERAL, 6))
                     ))
    self.assertEqual(ParseExprFromStr(u'5加六乘3')[0],
                     ArithmeticExpr(
                         LiteralExpr(Token(TK_INTEGER_LITERAL, 5)),
                         Keyword(u'加'),
                         ArithmeticExpr(
                             LiteralExpr(Token(TK_INTEGER_LITERAL, 6)),
                             Keyword(u'乘'),
                             LiteralExpr(Token(TK_INTEGER_LITERAL, 3)))))
    self.assertEqual(ParseExprFromStr(u'5减六减老王')[0],
                     ArithmeticExpr(
                         ArithmeticExpr(
                             LiteralExpr(Token(TK_INTEGER_LITERAL, 5)),
                             Keyword(u'减'),
                             LiteralExpr(Token(TK_INTEGER_LITERAL, 6))
                         ),
                         Keyword(u'减'),
                         VariableExpr(Token(TK_IDENTIFIER, u'老王')))
                     )

  def testParseComparisonExpr(self):
    self.assertEqual(ParseExprFromStr(u'5比6大')[0],
                     ComparisonExpr(
                         LiteralExpr(Token(TK_INTEGER_LITERAL, 5)),
                         Keyword(u'大'),
                         LiteralExpr(Token(TK_INTEGER_LITERAL, 6))
                     ))
    self.assertEqual(ParseExprFromStr(u'老王加5比6小')[0],
                     ComparisonExpr(
                         ArithmeticExpr(
                             VariableExpr(Token(TK_IDENTIFIER, u'老王')),
                             Keyword(u'加'),
                             LiteralExpr(Token(TK_INTEGER_LITERAL, 5))),
                         Keyword(u'小'),
                         LiteralExpr(Token(TK_INTEGER_LITERAL, 6))
                     ))
    self.assertEqual(ParseExprFromStr(u'老王跟倒老刘一模一样呢')[0],
                     ComparisonExpr(
                         VariableExpr(Token(TK_IDENTIFIER, u'老王')),
                         Keyword(u'一模一样呢'),
                         VariableExpr(Token(TK_IDENTIFIER, u'老刘'))
                     ))
    self.assertEqual(ParseExprFromStr(u'老王加5跟倒6不一样')[0],
                     ComparisonExpr(
                         ArithmeticExpr(
                             VariableExpr(Token(TK_IDENTIFIER, u'老王')),
                             Keyword(u'加'),
                             LiteralExpr(Token(TK_INTEGER_LITERAL, 5))),
                         Keyword(u'不一样'),
                         LiteralExpr(Token(TK_INTEGER_LITERAL, 6))
                     ))

  def testParseConcatExpr(self):
    self.assertEqual(ParseExprFromStr(u'老王、2')[0],
                     ConcatExpr([
                         VariableExpr(Token(TK_IDENTIFIER, u'老王')),
                         LiteralExpr(Token(TK_INTEGER_LITERAL, 2))
                     ]))
  def testParseConcatExpr(self):
    self.assertEqual(ParseExprFromStr(u'老王加油、2、“哈”')[0],
                     ConcatExpr([
                         ArithmeticExpr(
                             VariableExpr(Token(TK_IDENTIFIER, u'老王')),
                             Keyword(u'加'),
                             VariableExpr(Token(TK_IDENTIFIER, u'油'))),
                         LiteralExpr(Token(TK_INTEGER_LITERAL, 2)),
                         LiteralExpr(Token(TK_STRING_LITERAL, u'哈'))
                     ]))

class sichuanParseStatementTest(unittest.TestCase):
  def testParseConditional(self):
    self.assertEqual(
        ParseStmtFromStr(u'看哈儿：老王比五大啵？要是呢话摆哈儿：老王。')[0],
        Statement(STMT_CONDITIONAL,
                  (ComparisonExpr(
                      VariableExpr(Token(TK_IDENTIFIER, u'老王')),
                      Keyword(u'大'),
                      LiteralExpr(Token(TK_INTEGER_LITERAL, 5))),
                   # then-branch
                   Statement(STMT_SAY,
                             VariableExpr(Token(TK_IDENTIFIER, u'老王'))),
                   # else-branch
                   None
                  )))
  
class sichuanTest(unittest.TestCase):
  def testRunEmptyProgram(self):
    self.assertEqual(Run(''), '')

  def testRunHelloWorld(self):
    self.assertEqual(
        Run(u'摆哈儿：“这踏踏儿巴适得板！”。'),
        u'这踏踏儿巴适得板！\n')

  def testRunHelloWorld2(self):
    self.assertEqual(
        Run(u'摆哈儿：“你那踏踏儿也巴适得板！”。'),
        u'你那踏踏儿也巴适得板！\n')

  def testVarDecl(self):
    self.assertEqual(
        Run(u'老张凶得很。'), '')

  def testVarAssignment(self):
    self.assertEqual(
        Run(u'老张凶得很。\n老张巴倒250。\n摆哈儿：老张。'), '250\n')

  def testTokenize(self):
    self.assertEqual(
        list(BasicTokenize(u'【阶乘】')),
        [Token(TK_IDENTIFIER, u'阶乘'),])
    self.assertEqual(
        list(BasicTokenize(u'【 阶  乘   】')),
        [Token(TK_IDENTIFIER, u'阶乘'),])
    self.assertEqual(
        list(BasicTokenize(u'【阶乘】（好多）')),
        [Token(TK_IDENTIFIER, u'阶乘'),
         Keyword(u'（'),
         Token(TK_CHAR, u'好'),
         Token(TK_CHAR, u'多'),
         Keyword(u'）'),])
    self.assertEqual(
        list(BasicTokenize(u'“ ”')),
        [Keyword(u'“'),
         Token(TK_STRING_LITERAL, u' '),
         Keyword(u'”'),])
    self.assertEqual(
        list(BasicTokenize(u'“”')),
        [Keyword(u'“'),
         Token(TK_STRING_LITERAL, u''),
         Keyword(u'”'),])
    self.assertEqual(
        list(BasicTokenize(u'“ A B ”')),
        [Keyword(u'“'),
         Token(TK_STRING_LITERAL, u' A B '),
         Keyword(u'”'),])
    self.assertEqual(
        list(BasicTokenize(u'老张')),
        [Token(TK_CHAR, u'老'),
         Token(TK_CHAR, u'张'),])
    self.assertEqual(
        list(BasicTokenize(u'  老 张   ')),
        [Token(TK_CHAR, u'老'),
         Token(TK_CHAR, u'张'),])
    self.assertEqual(
        list(Tokenize(u'# 123456\n老张')),
        [Token(TK_IDENTIFIER, u'老张')])
    self.assertEqual(
        list(Tokenize(u'老张')),
        [Token(TK_IDENTIFIER, u'老张')])
    self.assertEqual(
        ParseInteger(u'老张'),
        (None, u'老张'))
    self.assertEqual(
        list(ParseChars(u'老张')),
        [Token(TK_IDENTIFIER, u'老张')])
    self.assertEqual(
        list(Tokenize(u'老张凶得很')),
        [Token(TK_IDENTIFIER, u'老张'),
         Keyword(u'凶得很')])
    self.assertEqual(
        list(Tokenize(u'老张 凶\n得很 。 ')),
        [Token(TK_IDENTIFIER, u'老张'),
         Keyword(u'凶得很'),
         Keyword(u'。'),
        ])
    self.assertEqual(
        list(Tokenize(u'老张凶得很。\n老王凶得很。\n')),
        [Token(TK_IDENTIFIER, u'老张'),
         Keyword(u'凶得很'),
         Keyword(u'。'),
         Token(TK_IDENTIFIER, u'老王'),
         Keyword(u'凶得很'),
         Keyword(u'。'),
        ])
    self.assertEqual(
        list(Tokenize(u'老张巴倒250。\n老王巴倒老张。\n')),
        [Token(TK_IDENTIFIER, u'老张'),
         Keyword(u'巴倒'),
         Token(TK_INTEGER_LITERAL, 250),
         Keyword(u'。'),
         Token(TK_IDENTIFIER, u'老王'),
         Keyword(u'巴倒'),
         Token(TK_IDENTIFIER, u'老张'),
         Keyword(u'。')])
    self.assertEqual(
        list(Tokenize(u'摆哈儿：“你好”。')),
        [Keyword(u'摆哈儿'),
         Keyword(u'：'),
         Keyword(u'“'),
         Token(TK_STRING_LITERAL, u'你好'),
         Keyword(u'”'),
         Keyword(u'。')])

  def testTokenizeArithmetic(self):
    self.assertEqual(
        list(Tokenize(u'250加13减二乘五除以九')),
        [Token(TK_INTEGER_LITERAL, 250),
         Keyword(u'加'),
         Token(TK_INTEGER_LITERAL, 13),
         Keyword(u'减'),
         Token(TK_INTEGER_LITERAL, 2),
         Keyword(u'乘'),
         Token(TK_INTEGER_LITERAL, 5),
         Keyword(u'除以'),
         Token(TK_INTEGER_LITERAL, 9),
        ])
    
  def testTokenizeLoop(self):
    self.assertEqual(
        list(Tokenize(u'老王从1拢9打转转儿：转完了。')),
        [Token(TK_IDENTIFIER, u'老王'),
         Keyword(u'从'),
         Token(TK_INTEGER_LITERAL, 1),
         Keyword(u'拢'),
         Token(TK_INTEGER_LITERAL, 9),
         Keyword(u'打转转儿：'),
         Keyword(u'转完了'),
         Keyword(u'。'),
        ])

  def testTokenizeCompound(self):
    self.assertEqual(
        list(Tokenize(u'开始：\n  摆哈儿：老王。\n刹脚。')),
        [Keyword(u'开始：'),
         Keyword(u'摆哈儿'),
         Keyword(u'：'),
         Token(TK_IDENTIFIER, u'老王'),
         Keyword(u'。'),
         Keyword(u'刹脚'),
         Keyword(u'。'),])

  def testTokenizingIncrements(self):
    self.assertEqual(
        list(Tokenize(u'老王走哈儿')),
        [Token(TK_IDENTIFIER, u'老王'),
         Keyword(u'走哈儿'),])
    self.assertEqual(
        list(Tokenize(u'老王走两步')),
        [Token(TK_IDENTIFIER, u'老王'),
         Keyword(u'走'),
         Token(TK_INTEGER_LITERAL, 2),
         Keyword(u'步'),
        ])

  def testTokenizingDecrements(self):
    self.assertEqual(
        list(Tokenize(u'老王倒起走哈儿')),
        [Token(TK_IDENTIFIER, u'老王'),
         Keyword(u'倒起走哈儿'),])
    self.assertEqual(
        list(Tokenize(u'老王倒起走三步')),
        [Token(TK_IDENTIFIER, u'老王'),
         Keyword(u'倒起走'),
         Token(TK_INTEGER_LITERAL, 3),
         Keyword(u'步'),
        ])

  def testTokenizingConcat(self):
    self.assertEqual(
        list(Tokenize(u'老刘、二')),
        [Token(TK_IDENTIFIER, u'老刘'),
         Keyword(u'、'),
         Token(TK_INTEGER_LITERAL, 2),])

  def testTokenizingFuncDef(self):
    self.assertEqual(
        list(Tokenize(u'写九九表啷个办：刹脚。')),
        [Token(TK_IDENTIFIER, u'写九九表'),
         Keyword(u'啷个办：'),
         Keyword(u'刹脚'),
         Keyword(u'。'),])

  def testTokenizingFuncCall(self):
    self.assertEqual(
        list(Tokenize(u'喊写九九表')),
        [Keyword(u'喊'),
         Token(TK_IDENTIFIER, u'写九九表'),])
    
  def testParsingIncrements(self):
    self.assertEqual(
        ParseToAst(u'老王走哈儿。'),
        [Statement(
            STMT_INC_BY,
            (Token(TK_IDENTIFIER, u'老王'),
             LiteralExpr(Token(TK_INTEGER_LITERAL, 1))))])
    self.assertEqual(
        ParseToAst(u'老王走两步。'),
        [Statement(
            STMT_INC_BY,
            (Token(TK_IDENTIFIER, u'老王'),
             LiteralExpr(Token(TK_INTEGER_LITERAL, 2))))])

  def testParsingDecrements(self):
    self.assertEqual(
        ParseToAst(u'老王倒起走哈儿。'),
        [Statement(
            STMT_DEC_BY,
            (Token(TK_IDENTIFIER, u'老王'),
             LiteralExpr(Token(TK_INTEGER_LITERAL, 1))))])
    self.assertEqual(
        ParseToAst(u'老王倒起走三步。'),
        [Statement(
            STMT_DEC_BY,
            (Token(TK_IDENTIFIER, u'老王'),
             LiteralExpr(Token(TK_INTEGER_LITERAL, 3))))])

  def testParsingLoop(self):
    self.assertEqual(
        ParseToAst(u'老王从1拢9打转转儿：转完了。'),
        [Statement(
            STMT_LOOP,
            (Token(TK_IDENTIFIER, u'老王'),
             LiteralExpr(Token(TK_INTEGER_LITERAL, 1)),
             LiteralExpr(Token(TK_INTEGER_LITERAL, 9)),
             []))])

  def DisabledTestParsingComparison(self):
    self.assertEquals(
        ParseToAst(u'摆哈儿：2比5大。'),
        [Statement(
            STMT_SAY,
            ComparisonExpr(2, 'GT', 5)
        )])

  def testParsingFuncDef(self):
    self.assertEqual(
        ParseToAst(u'写九九表啷个办：刹脚。'),
        [Statement(STMT_FUNC_DEF,
                   (Token(TK_IDENTIFIER, u'写九九表'),
                    [],  # Formal parameters.
                    []  # Function body.
                   ))])
    self.assertEqual(
        ParseToAst(u'写九九表啷个办：摆哈儿：1。刹脚。'),
        [Statement(STMT_FUNC_DEF,
                   (Token(TK_IDENTIFIER, u'写九九表'),
                    [],  # Formal parameters.
                    # Function body.
                    [Statement(STMT_SAY,
                               LiteralExpr(Token(
                                   TK_INTEGER_LITERAL, 1)))]
                   ))])
    
  def testParsingFuncDefWithParam(self):
    self.assertEqual(
        ParseToAst(u'【阶乘】（好多）啷个办：刹脚。'),
        [Statement(STMT_FUNC_DEF,
                   (Token(TK_IDENTIFIER, u'阶乘'),
                    [Token(TK_IDENTIFIER, u'好多')],  # Formal parameters.
                    []  # Function body.
                   ))])
    
  def testParsingFuncCallWithParam(self):
    self.assertEqual(
        ParseToAst(u'喊【阶乘】（五）。'),
        [Statement(STMT_CALL,
                   CallExpr(Token(TK_IDENTIFIER, u'阶乘'),
                            [LiteralExpr(Token(TK_INTEGER_LITERAL, 5))]))])

  def testVarAssignmentFromVar(self):
    self.assertEqual(
        Run(u'老张凶得很。\n老王凶得很。\n'
                    u'老张巴倒250。\n老王巴倒老张。\n摆哈儿：老王。'), '250\n')

  def testIncrements(self):
    self.assertEqual(
        Run(u'老张凶得很。老张巴倒二。老张走哈儿。摆哈儿：老张。'),
        '3\n')
    self.assertEqual(
        Run(u'老张凶得很。老张巴倒三。老张走五步。摆哈儿：老张。'),
        '8\n')

  def testDecrements(self):
    self.assertEqual(
        Run(u'老张凶得很。老张巴倒二。老张倒起走哈儿。摆哈儿：老张。'),
        '1\n')
    self.assertEqual(
        Run(u'老张凶得很。老张巴倒三。老张倒起走五步。摆哈儿：老张。'),
        '-2\n')

  def testLoop(self):
    self.assertEqual(
        Run(u'老张从1拢3打转转儿：摆哈儿：老张。转完了。'),
        '1\n2\n3\n')

  def testLoopWithNoStatement(self):
    self.assertEqual(
        Run(u'老张从1拢2打转转儿：转完了。'),
        '')

  def testLoopWithMultipleStatements(self):
    self.assertEqual(
        Run(u'老张从1拢2打转转儿：摆哈儿：老张。摆哈儿：老张加一。转完了。'),
        '1\n2\n2\n3\n')

  def testPrintBool(self):
    self.assertEqual(
        Run(u'摆哈儿：五比二大。'),
        u'对\n')
    self.assertEqual(
        Run(u'摆哈儿：五比二大、五比二小、一跟倒2一模一样呢、1跟倒二不一样。'),
        u'对错错对\n')

  def testArithmetic(self):
    self.assertEqual(
      Run(u'摆哈儿：五加二。'),
      u'7\n')
    self.assertEqual(
      Run(u'摆哈儿：五减二。'),
      u'3\n')
    self.assertEqual(
      Run(u'摆哈儿：五乘二。'),
      u'10\n')
    self.assertEqual(
      Run(u'摆哈儿：十除以二。'),
      u'5.0\n')
    self.assertEqual(
      Run(u'摆哈儿：五加七乘二。'),
      u'19\n')
    self.assertEqual(
      Run(u'摆哈儿：（五加七）乘二。'),
      u'24\n')
    self.assertEqual(
      Run(u'摆哈儿：(五加七)乘二。'),
      u'24\n')
    self.assertEqual(
      Run(u'摆哈儿：(五减（四减三）)乘二。'),
      u'8\n')

  def testConcat(self):
    self.assertEqual(
        Run(u'摆哈儿：“牛”、二。'),
        u'牛2\n')
    self.assertEqual(
        Run(u'摆哈儿：“老王”、665加一。'),
        u'老王666\n')

  def testCompound(self):
    self.assertEqual(
        Run(u'开始：刹脚。'),
        u'')
    self.assertEqual(
        Run(u'开始：摆哈儿：1。刹脚。'),
        u'1\n')
    self.assertEqual(
        Run(u'开始：摆哈儿：1。摆哈儿：2。刹脚。'),
        u'1\n2\n')

  def testRunConditional(self):
    self.assertEqual(
        Run(u'看哈儿：5比2大啵？要是呢话摆哈儿：“OK”。'),
        u'OK\n')
    self.assertEqual(
        Run(u'看哈儿：5比2大啵？要是呢话开始：\n'
            u'刹脚。'),
        u'')
    self.assertEqual(
        Run(u'看哈儿：5比2大啵？\n'
            u'要是呢话开始：\n'
            u'    摆哈儿：5。\n'
            u'刹脚。'),
        u'5\n')
    self.assertEqual(
        Run(u'看哈儿：5比6大啵？要是呢话摆哈儿：“OK”。\n'
            u'不是呢话摆哈儿：“不OK”。'),
        u'不OK\n')
    self.assertEqual(
        Run(u'看哈儿：5比6大啵？\n'
            u'要是呢话摆哈儿：“OK”。\n'
            u'不是呢话开始：\n'
            u'  摆哈儿：“不OK”。\n'
            u'  摆哈儿：“还是不OK”。\n'
            u'刹脚。'),
        u'不OK\n还是不OK\n')
    # Else should match the last If.
    self.assertEqual(
        Run(u'''
          看哈儿：2比1大啵？   # condition 1: True
          要是呢话看哈儿：2比3大啵？  # condition 2: False
              要是呢话摆哈儿：“A”。  # for condition 2
              不是呢话摆哈儿：“B”。# for condition 2
          '''),
        u'B\n')

  def testRunFunc(self):
    self.assertEqual(
        Run(u'埋汰啷个办：摆哈儿：“你虎了吧唧”。刹脚。'),
        u'')
    self.assertEqual(
        Run(u'埋汰啷个办：摆哈儿：“你虎了吧唧”。刹脚。喊埋汰。'),
        u'你虎了吧唧\n')

  def testFuncCallWithParam(self):
    self.assertEqual(
        Run(u'【加一】（好多）啷个办：摆哈儿：好多加一。刹脚。\n'
                    u'喊【加一】（五）。'),
        u'6\n')

  def testFuncWithReturnValue(self):
    self.assertEqual(
        Run(u'【加一】（好多）啷个办：爬远点好多加一。刹脚。\n'
                    u'摆哈儿：喊【加一】（二）。'),
        u'3\n')

  def testRecursiveFunc(self):
    self.assertEqual(
        Run(u'''
【阶乘】（好多）啷个办：
看哈儿：好多比一小啵？
要是呢话爬远点一。
爬远点好多乘整【阶乘】（好多减一）。
刹脚。

摆哈儿：喊【阶乘】（五）。
        '''),
        u'120\n')

  def testMultiArgFunc(self):
    self.assertEqual(
        Run(u'''
求和（甲，乙）啷个办：
  爬远点 甲加乙。
刹脚。

摆哈儿：喊求和（五，七）。
        '''),
        u'12\n')
    self.assertEqual(
        Run(u'''
求和（甲，乙）啷个办：
  摆哈儿：甲加乙。
刹脚。

喊求和（五，七）。
        '''),
        u'12\n')

  def testNormalizingBang(self):
    self.assertEqual(
        Run(u'【加一】（好多）啷个办：摆哈儿：好多加一！刹脚！\n'
                    u'喊【加一】（五）！'),
        u'6\n')
    
if __name__ == '__main__':
  unittest.main()
