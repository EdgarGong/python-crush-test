from __future__ import division

import copy
import json
import random
import numpy as np
from goto import with_goto
import time
import sys

from crush import Crush
import utils

import csv


class Logger:
    def __init__(self, path):
        self.fo = open(path, "a")
        msg = "========== start logging at " + time.asctime( time.localtime(time.time()) ) + " =========="
        self.log(msg)

    def __del__(self):
        msg = "========== stop logging at " + time.asctime( time.localtime(time.time()) ) + " =========="
        self.log(msg)
        self.fo.close()

    def log(self, msg):
        print(msg)
        msg = str(msg)
        msg += '\n'
        self.fo.write(msg)


class Incremental:
    def __init__(self):
        self.old_pg_upmap_items = []
        self.new_pg_upmap_items = {}


class OSDMap:
    def __init__(self):
        self.pg_upmap = {}
        self.pg_upmap_items = {}


class Balancer:
    def __init__(self):
        self.crushmap = """
{"rules": {"default_rule": [["take", "default"], ["chooseleaf", "firstn", 0, "type", "host"], ["emit"]]}, "types": [{"name": "root", "type_id": 2}, {"name": "host", "type_id": 1}], "trees": [{"children": [{"children": [{"id": 0, "weight": 1, "name": "device0"}, {"id": 1, "weight": 1, "name": "device1"}, {"id": 2, "weight": 1, "name": "device2"}, {"id": 3, "weight": 1, "name": "device3"}, {"id": 4, "weight": 1, "name": "device4"}, {"id": 5, "weight": 1, "name": "device5"}, {"id": 6, "weight": 1, "name": "device6"}, {"id": 7, "weight": 1, "name": "device7"}, {"id": 8, "weight": 1, "name": "device8"}, {"id": 9, "weight": 1, "name": "device9"}, {"id": 10, "weight": 1, "name": "device10"}, {"id": 11, "weight": 1, "name": "device11"}, {"id": 12, "weight": 1, "name": "device12"}, {"id": 13, "weight": 1, "name": "device13"}, {"id": 14, "weight": 1, "name": "device14"}, {"id": 15, "weight": 1, "name": "device15"}, {"id": 16, "weight": 1, "name": "device16"}, {"id": 17, "weight": 1, "name": "device17"}, {"id": 18, "weight": 1, "name": "device18"}, {"id": 19, "weight": 1, "name": "device19"}, {"id": 20, "weight": 1, "name": "device20"}, {"id": 21, "weight": 1, "name": "device21"}, {"id": 22, "weight": 1, "name": "device22"}, {"id": 23, "weight": 1, "name": "device23"}, {"id": 24, "weight": 1, "name": "device24"}, {"id": 25, "weight": 1, "name": "device25"}, {"id": 26, "weight": 1, "name": "device26"}, {"id": 27, "weight": 1, "name": "device27"}, {"id": 28, "weight": 1, "name": "device28"}, {"id": 29, "weight": 1, "name": "device29"}, {"id": 30, "weight": 1, "name": "device30"}, {"id": 31, "weight": 1, "name": "device31"}], "type": "host", "name": "host0", "id": -2}, {"children": [{"id": 32, "weight": 1, "name": "device32"}, {"id": 33, "weight": 1, "name": "device33"}, {"id": 34, "weight": 1, "name": "device34"}, {"id": 35, "weight": 1, "name": "device35"}, {"id": 36, "weight": 1, "name": "device36"}, {"id": 37, "weight": 1, "name": "device37"}, {"id": 38, "weight": 1, "name": "device38"}, {"id": 39, "weight": 1, "name": "device39"}, {"id": 40, "weight": 1, "name": "device40"}, {"id": 41, "weight": 1, "name": "device41"}, {"id": 42, "weight": 1, "name": "device42"}, {"id": 43, "weight": 1, "name": "device43"}, {"id": 44, "weight": 1, "name": "device44"}, {"id": 45, "weight": 1, "name": "device45"}, {"id": 46, "weight": 1, "name": "device46"}, {"id": 47, "weight": 1, "name": "device47"}, {"id": 48, "weight": 1, "name": "device48"}, {"id": 49, "weight": 1, "name": "device49"}, {"id": 50, "weight": 1, "name": "device50"}, {"id": 51, "weight": 1, "name": "device51"}, {"id": 52, "weight": 1, "name": "device52"}, {"id": 53, "weight": 1, "name": "device53"}, {"id": 54, "weight": 1, "name": "device54"}, {"id": 55, "weight": 1, "name": "device55"}, {"id": 56, "weight": 1, "name": "device56"}, {"id": 57, "weight": 1, "name": "device57"}, {"id": 58, "weight": 1, "name": "device58"}, {"id": 59, "weight": 1, "name": "device59"}, {"id": 60, "weight": 1, "name": "device60"}, {"id": 61, "weight": 1, "name": "device61"}, {"id": 62, "weight": 1, "name": "device62"}, {"id": 63, "weight": 1, "name": "device63"}], "type": "host", "name": "host1", "id": -3}, {"children": [{"id": 64, "weight": 1, "name": "device64"}, {"id": 65, "weight": 1, "name": "device65"}, {"id": 66, "weight": 1, "name": "device66"}, {"id": 67, "weight": 1, "name": "device67"}, {"id": 68, "weight": 1, "name": "device68"}, {"id": 69, "weight": 1, "name": "device69"}, {"id": 70, "weight": 1, "name": "device70"}, {"id": 71, "weight": 1, "name": "device71"}, {"id": 72, "weight": 1, "name": "device72"}, {"id": 73, "weight": 1, "name": "device73"}, {"id": 74, "weight": 1, "name": "device74"}, {"id": 75, "weight": 1, "name": "device75"}, {"id": 76, "weight": 1, "name": "device76"}, {"id": 77, "weight": 1, "name": "device77"}, {"id": 78, "weight": 1, "name": "device78"}, {"id": 79, "weight": 1, "name": "device79"}, {"id": 80, "weight": 1, "name": "device80"}, {"id": 81, "weight": 1, "name": "device81"}, {"id": 82, "weight": 1, "name": "device82"}, {"id": 83, "weight": 1, "name": "device83"}, {"id": 84, "weight": 1, "name": "device84"}, {"id": 85, "weight": 1, "name": "device85"}, {"id": 86, "weight": 1, "name": "device86"}, {"id": 87, "weight": 1, "name": "device87"}, {"id": 88, "weight": 1, "name": "device88"}, {"id": 89, "weight": 1, "name": "device89"}, {"id": 90, "weight": 1, "name": "device90"}, {"id": 91, "weight": 1, "name": "device91"}, {"id": 92, "weight": 1, "name": "device92"}, {"id": 93, "weight": 1, "name": "device93"}, {"id": 94, "weight": 1, "name": "device94"}, {"id": 95, "weight": 1, "name": "device95"}], "type": "host", "name": "host2", "id": -4}, {"children": [{"id": 96, "weight": 1, "name": "device96"}, {"id": 97, "weight": 1, "name": "device97"}, {"id": 98, "weight": 1, "name": "device98"}, {"id": 99, "weight": 1, "name": "device99"}, {"id": 100, "weight": 1, "name": "device100"}, {"id": 101, "weight": 1, "name": "device101"}, {"id": 102, "weight": 1, "name": "device102"}, {"id": 103, "weight": 1, "name": "device103"}, {"id": 104, "weight": 1, "name": "device104"}, {"id": 105, "weight": 1, "name": "device105"}, {"id": 106, "weight": 1, "name": "device106"}, {"id": 107, "weight": 1, "name": "device107"}, {"id": 108, "weight": 1, "name": "device108"}, {"id": 109, "weight": 1, "name": "device109"}, {"id": 110, "weight": 1, "name": "device110"}, {"id": 111, "weight": 1, "name": "device111"}, {"id": 112, "weight": 1, "name": "device112"}, {"id": 113, "weight": 1, "name": "device113"}, {"id": 114, "weight": 1, "name": "device114"}, {"id": 115, "weight": 1, "name": "device115"}, {"id": 116, "weight": 1, "name": "device116"}, {"id": 117, "weight": 1, "name": "device117"}, {"id": 118, "weight": 1, "name": "device118"}, {"id": 119, "weight": 1, "name": "device119"}, {"id": 120, "weight": 1, "name": "device120"}, {"id": 121, "weight": 1, "name": "device121"}, {"id": 122, "weight": 1, "name": "device122"}, {"id": 123, "weight": 1, "name": "device123"}, {"id": 124, "weight": 1, "name": "device124"}, {"id": 125, "weight": 1, "name": "device125"}, {"id": 126, "weight": 1, "name": "device126"}, {"id": 127, "weight": 1, "name": "device127"}], "type": "host", "name": "host3", "id": -5}, {"children": [{"id": 128, "weight": 1, "name": "device128"}, {"id": 129, "weight": 1, "name": "device129"}, {"id": 130, "weight": 1, "name": "device130"}, {"id": 131, "weight": 1, "name": "device131"}, {"id": 132, "weight": 1, "name": "device132"}, {"id": 133, "weight": 1, "name": "device133"}, {"id": 134, "weight": 1, "name": "device134"}, {"id": 135, "weight": 1, "name": "device135"}, {"id": 136, "weight": 1, "name": "device136"}, {"id": 137, "weight": 1, "name": "device137"}, {"id": 138, "weight": 1, "name": "device138"}, {"id": 139, "weight": 1, "name": "device139"}, {"id": 140, "weight": 1, "name": "device140"}, {"id": 141, "weight": 1, "name": "device141"}, {"id": 142, "weight": 1, "name": "device142"}, {"id": 143, "weight": 1, "name": "device143"}, {"id": 144, "weight": 1, "name": "device144"}, {"id": 145, "weight": 1, "name": "device145"}, {"id": 146, "weight": 1, "name": "device146"}, {"id": 147, "weight": 1, "name": "device147"}, {"id": 148, "weight": 1, "name": "device148"}, {"id": 149, "weight": 1, "name": "device149"}, {"id": 150, "weight": 1, "name": "device150"}, {"id": 151, "weight": 1, "name": "device151"}, {"id": 152, "weight": 1, "name": "device152"}, {"id": 153, "weight": 1, "name": "device153"}, {"id": 154, "weight": 1, "name": "device154"}, {"id": 155, "weight": 1, "name": "device155"}, {"id": 156, "weight": 1, "name": "device156"}, {"id": 157, "weight": 1, "name": "device157"}, {"id": 158, "weight": 1, "name": "device158"}, {"id": 159, "weight": 1, "name": "device159"}], "type": "host", "name": "host4", "id": -6}, {"children": [{"id": 160, "weight": 1, "name": "device160"}, {"id": 161, "weight": 1, "name": "device161"}, {"id": 162, "weight": 1, "name": "device162"}, {"id": 163, "weight": 1, "name": "device163"}, {"id": 164, "weight": 1, "name": "device164"}, {"id": 165, "weight": 1, "name": "device165"}, {"id": 166, "weight": 1, "name": "device166"}, {"id": 167, "weight": 1, "name": "device167"}, {"id": 168, "weight": 1, "name": "device168"}, {"id": 169, "weight": 1, "name": "device169"}, {"id": 170, "weight": 1, "name": "device170"}, {"id": 171, "weight": 1, "name": "device171"}, {"id": 172, "weight": 1, "name": "device172"}, {"id": 173, "weight": 1, "name": "device173"}, {"id": 174, "weight": 1, "name": "device174"}, {"id": 175, "weight": 1, "name": "device175"}, {"id": 176, "weight": 1, "name": "device176"}, {"id": 177, "weight": 1, "name": "device177"}, {"id": 178, "weight": 1, "name": "device178"}, {"id": 179, "weight": 1, "name": "device179"}, {"id": 180, "weight": 1, "name": "device180"}, {"id": 181, "weight": 1, "name": "device181"}, {"id": 182, "weight": 1, "name": "device182"}, {"id": 183, "weight": 1, "name": "device183"}, {"id": 184, "weight": 1, "name": "device184"}, {"id": 185, "weight": 1, "name": "device185"}, {"id": 186, "weight": 1, "name": "device186"}, {"id": 187, "weight": 1, "name": "device187"}, {"id": 188, "weight": 1, "name": "device188"}, {"id": 189, "weight": 1, "name": "device189"}, {"id": 190, "weight": 1, "name": "device190"}, {"id": 191, "weight": 1, "name": "device191"}], "type": "host", "name": "host5", "id": -7}, {"children": [{"id": 192, "weight": 1, "name": "device192"}, {"id": 193, "weight": 1, "name": "device193"}, {"id": 194, "weight": 1, "name": "device194"}, {"id": 195, "weight": 1, "name": "device195"}, {"id": 196, "weight": 1, "name": "device196"}, {"id": 197, "weight": 1, "name": "device197"}, {"id": 198, "weight": 1, "name": "device198"}, {"id": 199, "weight": 1, "name": "device199"}, {"id": 200, "weight": 1, "name": "device200"}, {"id": 201, "weight": 1, "name": "device201"}, {"id": 202, "weight": 1, "name": "device202"}, {"id": 203, "weight": 1, "name": "device203"}, {"id": 204, "weight": 1, "name": "device204"}, {"id": 205, "weight": 1, "name": "device205"}, {"id": 206, "weight": 1, "name": "device206"}, {"id": 207, "weight": 1, "name": "device207"}, {"id": 208, "weight": 1, "name": "device208"}, {"id": 209, "weight": 1, "name": "device209"}, {"id": 210, "weight": 1, "name": "device210"}, {"id": 211, "weight": 1, "name": "device211"}, {"id": 212, "weight": 1, "name": "device212"}, {"id": 213, "weight": 1, "name": "device213"}, {"id": 214, "weight": 1, "name": "device214"}, {"id": 215, "weight": 1, "name": "device215"}, {"id": 216, "weight": 1, "name": "device216"}, {"id": 217, "weight": 1, "name": "device217"}, {"id": 218, "weight": 1, "name": "device218"}, {"id": 219, "weight": 1, "name": "device219"}, {"id": 220, "weight": 1, "name": "device220"}, {"id": 221, "weight": 1, "name": "device221"}, {"id": 222, "weight": 1, "name": "device222"}, {"id": 223, "weight": 1, "name": "device223"}], "type": "host", "name": "host6", "id": -8}, {"children": [{"id": 224, "weight": 1, "name": "device224"}, {"id": 225, "weight": 1, "name": "device225"}, {"id": 226, "weight": 1, "name": "device226"}, {"id": 227, "weight": 1, "name": "device227"}, {"id": 228, "weight": 1, "name": "device228"}, {"id": 229, "weight": 1, "name": "device229"}, {"id": 230, "weight": 1, "name": "device230"}, {"id": 231, "weight": 1, "name": "device231"}, {"id": 232, "weight": 1, "name": "device232"}, {"id": 233, "weight": 1, "name": "device233"}, {"id": 234, "weight": 1, "name": "device234"}, {"id": 235, "weight": 1, "name": "device235"}, {"id": 236, "weight": 1, "name": "device236"}, {"id": 237, "weight": 1, "name": "device237"}, {"id": 238, "weight": 1, "name": "device238"}, {"id": 239, "weight": 1, "name": "device239"}, {"id": 240, "weight": 1, "name": "device240"}, {"id": 241, "weight": 1, "name": "device241"}, {"id": 242, "weight": 1, "name": "device242"}, {"id": 243, "weight": 1, "name": "device243"}, {"id": 244, "weight": 1, "name": "device244"}, {"id": 245, "weight": 1, "name": "device245"}, {"id": 246, "weight": 1, "name": "device246"}, {"id": 247, "weight": 1, "name": "device247"}, {"id": 248, "weight": 1, "name": "device248"}, {"id": 249, "weight": 1, "name": "device249"}, {"id": 250, "weight": 1, "name": "device250"}, {"id": 251, "weight": 1, "name": "device251"}, {"id": 252, "weight": 1, "name": "device252"}, {"id": 253, "weight": 1, "name": "device253"}, {"id": 254, "weight": 1, "name": "device254"}, {"id": 255, "weight": 1, "name": "device255"}], "type": "host", "name": "host7", "id": -9}, {"children": [{"id": 256, "weight": 1, "name": "device256"}, {"id": 257, "weight": 1, "name": "device257"}, {"id": 258, "weight": 1, "name": "device258"}, {"id": 259, "weight": 1, "name": "device259"}, {"id": 260, "weight": 1, "name": "device260"}, {"id": 261, "weight": 1, "name": "device261"}, {"id": 262, "weight": 1, "name": "device262"}, {"id": 263, "weight": 1, "name": "device263"}, {"id": 264, "weight": 1, "name": "device264"}, {"id": 265, "weight": 1, "name": "device265"}, {"id": 266, "weight": 1, "name": "device266"}, {"id": 267, "weight": 1, "name": "device267"}, {"id": 268, "weight": 1, "name": "device268"}, {"id": 269, "weight": 1, "name": "device269"}, {"id": 270, "weight": 1, "name": "device270"}, {"id": 271, "weight": 1, "name": "device271"}, {"id": 272, "weight": 1, "name": "device272"}, {"id": 273, "weight": 1, "name": "device273"}, {"id": 274, "weight": 1, "name": "device274"}, {"id": 275, "weight": 1, "name": "device275"}, {"id": 276, "weight": 1, "name": "device276"}, {"id": 277, "weight": 1, "name": "device277"}, {"id": 278, "weight": 1, "name": "device278"}, {"id": 279, "weight": 1, "name": "device279"}, {"id": 280, "weight": 1, "name": "device280"}, {"id": 281, "weight": 1, "name": "device281"}, {"id": 282, "weight": 1, "name": "device282"}, {"id": 283, "weight": 1, "name": "device283"}, {"id": 284, "weight": 1, "name": "device284"}, {"id": 285, "weight": 1, "name": "device285"}, {"id": 286, "weight": 1, "name": "device286"}, {"id": 287, "weight": 1, "name": "device287"}], "type": "host", "name": "host8", "id": -10}, {"children": [{"id": 288, "weight": 1, "name": "device288"}, {"id": 289, "weight": 1, "name": "device289"}, {"id": 290, "weight": 1, "name": "device290"}, {"id": 291, "weight": 1, "name": "device291"}, {"id": 292, "weight": 1, "name": "device292"}, {"id": 293, "weight": 1, "name": "device293"}, {"id": 294, "weight": 1, "name": "device294"}, {"id": 295, "weight": 1, "name": "device295"}, {"id": 296, "weight": 1, "name": "device296"}, {"id": 297, "weight": 1, "name": "device297"}, {"id": 298, "weight": 1, "name": "device298"}, {"id": 299, "weight": 1, "name": "device299"}, {"id": 300, "weight": 1, "name": "device300"}, {"id": 301, "weight": 1, "name": "device301"}, {"id": 302, "weight": 1, "name": "device302"}, {"id": 303, "weight": 1, "name": "device303"}, {"id": 304, "weight": 1, "name": "device304"}, {"id": 305, "weight": 1, "name": "device305"}, {"id": 306, "weight": 1, "name": "device306"}, {"id": 307, "weight": 1, "name": "device307"}, {"id": 308, "weight": 1, "name": "device308"}, {"id": 309, "weight": 1, "name": "device309"}, {"id": 310, "weight": 1, "name": "device310"}, {"id": 311, "weight": 1, "name": "device311"}, {"id": 312, "weight": 1, "name": "device312"}, {"id": 313, "weight": 1, "name": "device313"}, {"id": 314, "weight": 1, "name": "device314"}, {"id": 315, "weight": 1, "name": "device315"}, {"id": 316, "weight": 1, "name": "device316"}, {"id": 317, "weight": 1, "name": "device317"}, {"id": 318, "weight": 1, "name": "device318"}, {"id": 319, "weight": 1, "name": "device319"}], "type": "host", "name": "host9", "id": -11}, {"children": [{"id": 320, "weight": 1, "name": "device320"}, {"id": 321, "weight": 1, "name": "device321"}, {"id": 322, "weight": 1, "name": "device322"}, {"id": 323, "weight": 1, "name": "device323"}, {"id": 324, "weight": 1, "name": "device324"}, {"id": 325, "weight": 1, "name": "device325"}, {"id": 326, "weight": 1, "name": "device326"}, {"id": 327, "weight": 1, "name": "device327"}, {"id": 328, "weight": 1, "name": "device328"}, {"id": 329, "weight": 1, "name": "device329"}, {"id": 330, "weight": 1, "name": "device330"}, {"id": 331, "weight": 1, "name": "device331"}, {"id": 332, "weight": 1, "name": "device332"}, {"id": 333, "weight": 1, "name": "device333"}, {"id": 334, "weight": 1, "name": "device334"}, {"id": 335, "weight": 1, "name": "device335"}, {"id": 336, "weight": 1, "name": "device336"}, {"id": 337, "weight": 1, "name": "device337"}, {"id": 338, "weight": 1, "name": "device338"}, {"id": 339, "weight": 1, "name": "device339"}, {"id": 340, "weight": 1, "name": "device340"}, {"id": 341, "weight": 1, "name": "device341"}, {"id": 342, "weight": 1, "name": "device342"}, {"id": 343, "weight": 1, "name": "device343"}, {"id": 344, "weight": 1, "name": "device344"}, {"id": 345, "weight": 1, "name": "device345"}, {"id": 346, "weight": 1, "name": "device346"}, {"id": 347, "weight": 1, "name": "device347"}, {"id": 348, "weight": 1, "name": "device348"}, {"id": 349, "weight": 1, "name": "device349"}, {"id": 350, "weight": 1, "name": "device350"}, {"id": 351, "weight": 1, "name": "device351"}], "type": "host", "name": "host10", "id": -12}, {"children": [{"id": 352, "weight": 1, "name": "device352"}, {"id": 353, "weight": 1, "name": "device353"}, {"id": 354, "weight": 1, "name": "device354"}, {"id": 355, "weight": 1, "name": "device355"}, {"id": 356, "weight": 1, "name": "device356"}, {"id": 357, "weight": 1, "name": "device357"}, {"id": 358, "weight": 1, "name": "device358"}, {"id": 359, "weight": 1, "name": "device359"}, {"id": 360, "weight": 1, "name": "device360"}, {"id": 361, "weight": 1, "name": "device361"}, {"id": 362, "weight": 1, "name": "device362"}, {"id": 363, "weight": 1, "name": "device363"}, {"id": 364, "weight": 1, "name": "device364"}, {"id": 365, "weight": 1, "name": "device365"}, {"id": 366, "weight": 1, "name": "device366"}, {"id": 367, "weight": 1, "name": "device367"}, {"id": 368, "weight": 1, "name": "device368"}, {"id": 369, "weight": 1, "name": "device369"}, {"id": 370, "weight": 1, "name": "device370"}, {"id": 371, "weight": 1, "name": "device371"}, {"id": 372, "weight": 1, "name": "device372"}, {"id": 373, "weight": 1, "name": "device373"}, {"id": 374, "weight": 1, "name": "device374"}, {"id": 375, "weight": 1, "name": "device375"}, {"id": 376, "weight": 1, "name": "device376"}, {"id": 377, "weight": 1, "name": "device377"}, {"id": 378, "weight": 1, "name": "device378"}, {"id": 379, "weight": 1, "name": "device379"}, {"id": 380, "weight": 1, "name": "device380"}, {"id": 381, "weight": 1, "name": "device381"}, {"id": 382, "weight": 1, "name": "device382"}, {"id": 383, "weight": 1, "name": "device383"}], "type": "host", "name": "host11", "id": -13}], "type": "root", "name": "default", "id": -1}]}
"""
        with open("config/engine-config.json") as f:
            config = json.load(f)
        print("config:")
        print(config)
        self.n_host = config['host_num']
        self.n_disk = config['disk_num']
        self.c = Crush()
        self.crushmap_json = json.loads(self.crushmap)
        self.c.parse(self.crushmap_json)
        self.pg_num = 8192   # Suggest PG Count = (Target PGs per OSD) x (OSD#) x (%Data) / (Size)
        self.pg_num_mask = self.pg_num - 1
        self.replication_count = 3
        self.pg_pri_in_osd = {}
        self.pg_rep_in_osd = {}
        self.obj_in_pg = {}
        # self.max_optimizations = self.pg_num
        # self.max_deviation = 1
        # self.aggressive = True
        # self.fast_aggressive = True
        # self.local_fallback_retries = 100
        # self.osdmap = OSDMap()

        self.disk_num = self.n_host * self.n_disk
        # engine_num = disk_num, Each engine corresponds to one osd.
        self.engine_num = self.disk_num
        self.engine_id = [i for i in range(self.engine_num)]
        self.obj_in_engine = {}

        self.obj_size = config['obj_size'] #MB
        self.disk_size = config['disk_size'] #GB

        self.overall_used_capacity = config['overall_used_capacity']

    def fill_engine(self, inode_num, inode_size):
        for inode_no in range(inode_num):
            # print(inode_num-inode_no)
            for block_no in range(inode_size):
                # key format: "10000000001.00000002"
                key = "100" + str('%08x' % inode_no) + '.' + str('%08x' % block_no)
                # print(key)
                hash_value = self.c.c.ceph_str_hash_rjenkins(key, len(key)) % self.engine_num
                engine_id = self.engine_id[hash_value]
                # print(engine_id)
                objs = self.obj_in_engine.get(engine_id, [])
                objs.append(key)
                self.obj_in_engine[engine_id] = objs
        # file_name = str(inode_num) + "_" + str(inode_size) + ".engine.dat"
        # file_exist = os.path.isfile(file_name)
        #
        # if file_exist:
        #     logger.log("file_exist")
        #     fo = open(file_name, "r")
        #     for inode_no in range(inode_num):
        #         for block_no in range(inode_size):
        #             key = "100" + str('%08x' % inode_no) + '.' + str('%08x' % block_no)
        #             line = fo.readline()
        #             line = line[:-1]
        #             engine_id = np.uint32(line)
        #             objs = self.obj_in_engine.get(engine_id, [])
        #             objs.append(key)
        #             self.obj_in_engine[engine_id] = objs
        #     fo.close()
        # else:
        #     logger.log("not file_exist")
        #     fo = open(file_name, "w")
        #     for inode_no in range(inode_num):
        #         for block_no in range(inode_size):
        #             key = "100" + str('%08x' % inode_no) + '.' + str('%08x' % block_no)
        #             engine_id = self.engine_id[self.c.c.ceph_str_hash_rjenkins(key, len(key)) % self.engine_num]
        #             fo.write(str(engine_id) + "\n")
        #             objs = self.obj_in_engine.get(engine_id, [])
        #             objs.append(key)
        #             self.obj_in_engine[engine_id] = objs
        #     fo.close()

    def calc_engine_deviation(self):
        s = 0
        for _, objs in self.obj_in_engine.items():
            s += len(objs)
        avg = float(s) / self.engine_num

        max_dev = 1.0
        min_dev = 1.0
        max_obj = 0
        min_obj = len(self.obj_in_engine[0])
        for _, objs in self.obj_in_engine.items():
            dev = float(len(objs)) / avg
            max_dev = max(max_dev, dev)
            min_dev = min(min_dev, dev)
            max_obj = max(max_obj, len(objs))
            min_obj = min(min_obj, len(objs))
        logger.log("Objects in Engines MIN/MAX objects number: " + str(min_obj) + "/" + str(max_obj))
        logger.log("Objects in Engines MIN/MAX deviation: " + str(min_dev) + "/" + str(max_dev))


    # CRUSH PG to OSDs
    def fill_osd_with_pg(self):
        for pg_no in range(self.pg_num):
            pps = np.int32(
                utils.crush_hash32_rjenkins1_2(utils.ceph_stable_mod(pg_no, self.pg_num, self.pg_num_mask), 3))  # 3 is pool no., not rep count
            osds = self.c.map(rule="default_rule", value=pps, replication_count=self.replication_count)
            for i in range(len(osds)):
                if i == 0:
                    pgs = self.pg_pri_in_osd.get(osds[i], [])
                    pgs.append(pg_no)
                    self.pg_pri_in_osd[osds[i]] = pgs
                else:
                    pgs = self.pg_rep_in_osd.get(osds[i], [])
                    pgs.append(pg_no)
                    self.pg_rep_in_osd[osds[i]] = pgs
        # print(self.pg_pri_in_osd)
        # print(self.pg_rep_in_osd)
                    
    def calc_pg_in_osd_deviation(self):
        max_pg = 0
        min_pg = len(self.pg_pri_in_osd.get(0, [])) + len(self.pg_rep_in_osd.get(0, []))
        pg_sum = 0
        max_pg_osdid = 0
        max_pri_pg = 0
        min_pri_pg = len(self.pg_pri_in_osd.get(0, []))
        pri_pg_sum = 0
        max_pri_pg_osdid = 0
        for osd in self.engine_id:
            pri_pg_count = len(self.pg_pri_in_osd.get(osd, []))
            pg_count = pri_pg_count + len(self.pg_rep_in_osd.get(osd, []))
            if pg_count > max_pg:
                max_pg = pg_count
                max_pg_osdid = osd
            min_pg = min(min_pg, pg_count)
            if pri_pg_count > max_pri_pg:
                max_pri_pg = pri_pg_count
                max_pri_pg_osdid = osd
            min_pri_pg = min(min_pg, pri_pg_count)
            pg_sum += pg_count
            pri_pg_sum += pri_pg_count

        avg_pg = float(pg_sum) / self.disk_num
        logger.log("PGs in OSDs MIN/MAX/AVG PGs number: " + str(min_pg) + "/" + str(max_pg) + "/" + str(avg_pg))
        
        avg_pri_pg = float(pri_pg_sum) / self.disk_num
        logger.log("pri_PGs in OSDs MIN/MAX/AVG pri_PGs number: " + str(min_pri_pg) + "/" + str(max_pri_pg) + "/" + str(avg_pri_pg))
        logger.log("PGS/pri_PGs in OSDs MAX OSD id: " + str(max_pg_osdid) + "/" + str(max_pri_pg_osdid))

    def engine_to_pg_naive_hash(self):
        for engine_id, objs in self.obj_in_engine.items():
            # the pgs that take the osd corresponding to this engine as the primary osd
            osd_id = engine_id
            pg_pri = self.pg_pri_in_osd.get(osd_id, [])
            pg_dict = {pg: False for pg in pg_pri}
            for obj in objs:
                # ?????
                # hash to one of the pgs that take the osd corresponding to this engine as the primary osd
                # hash_value = self.c.c.ceph_str_hash_rjenkins(obj, len(obj)) % len(pg_pri)
                hash_value = hash(obj) % len(pg_pri)
                
                pg_id = pg_pri[hash_value]
                pg_dict[pg_id] = True
                tmp_objs = self.obj_in_pg.get(pg_id, [])
                tmp_objs.append(obj)
                self.obj_in_pg[pg_id] = tmp_objs

            missing_pgs = [pg for pg, value in pg_dict.items() if not value]
            # logger.log("pg_pri number:" + str(len(pg_pri)) + " miss pgs number:" + str(len(missing_pgs)))
            if len(pg_pri) - len(missing_pgs) <= 3:
                logger.log("pg_pri number:" + str(len(pg_pri)) + " miss pgs number:" + str(len(missing_pgs)))
                # print("pg_pri", pg_pri)
                # print("missing pgs", missing_pgs)
                hash_values = {}
                print(objs)
                for obj in objs:
                    hash_value = self.c.c.ceph_str_hash_rjenkins(obj, len(obj)) % len(pg_pri)
                    hash_values[hash_value] = True
                print(hash_values, len(pg_pri))

            obj_counts = [len(objs) for pg_id, objs in self.obj_in_pg.items() if pg_id in pg_pri]
            max_count = max(obj_counts) if obj_counts else 0
            min_count = min(obj_counts) if obj_counts else 0
            # if len(missing_pgs) != 0:
            #     min_count = 0
            avg_count = sum(obj_counts) / len(obj_counts) if obj_counts else 0
            # logger.log("max/min/avg obj:" + str(max_count) + "/" + str(min_count) + "/" + str(avg_count))

    def gen_pg_crushmap(self, pg_pri_num):
        device_id = 0
        host_id = -2
        children = []
        for host in range(pg_pri_num):
            host_dict = {}
            host_dict["type"] = "host"
            host_dict["name"] = "host" + str(host)
            host_dict["id"] = host_id
            host_id -= 1
            host_dict_children = []
            disk_dict = {}
            disk_dict["id"] = device_id
            disk_dict["name"] = "device" + str(device_id)
            disk_dict["weight"] = 1
            device_id += 1
            host_dict_children.append(disk_dict)
            host_dict["children"] = host_dict_children
            children.append(host_dict)

        trees = []
        trees_dict = {}
        trees_dict["type"] = "root"
        trees_dict["name"] = "default"
        trees_dict["id"] = -1
        trees_dict["children"] = children
        trees.append(trees_dict)

        rules = {}
        default_rule_rep = [["take", "default"], ["chooseleaf", "firstn", 0, "type", "host"], ["emit"]]
        # default_rule_ec = [["take", "default"], ["choose", "indep", 5, "type", "host"], ["chooseleaf", "indep", 2, "type", 0], ["emit"]]
        default_rule_ec = [["take", "default"], ["chooseleaf", "indep", 0, "type", "host"], ["emit"]]

        rules["default_rule"] = default_rule_rep

        types = [{"type_id": 2, "name": "root"}, {"type_id": 1, "name": "host"}]

        crushmap = {}
        crushmap["trees"] = trees
        crushmap["rules"] = rules
        crushmap["types"] = types
        return crushmap

    def compute_pgp_num_mask(self, num):
        # Calculate the pgp_num_mask for given pgp_num
        return (1 << (num - 1).bit_length()) - 1
    
    def engine_to_pg_crush(self):
        for engine_id, objs in self.obj_in_engine.items():
            # the pgs that take the osd corresponding to this engine as the primary osd
            pg_pri = self.pg_pri_in_osd.get(engine_id, [])
            pg_pri_num = len(pg_pri)
            # pg_pri_num_mask = pg_pri_num - 1
            pg_dict = {pg: False for pg in pg_pri}
            crushmap = self.gen_pg_crushmap(pg_pri_num)
            c = Crush()
            c.parse(crushmap)
            for obj in objs:
                # hash to one of the pgs that take the osd corresponding to this engine as the primary osd
                # hash_value = self.c.c.ceph_str_hash_rjenkins(obj, len(obj)) % len(pg_pri)
                # ????
                # s_mod = hash(obj) % len(objs)
                s_mod = utils.ceph_stable_mod(hash(obj), len(objs), self.compute_pgp_num_mask(len(objs)))
                # if s_mod != s_mod2:
                #     print("!=, s_mod/s_mod2:", s_mod, s_mod2)
                pps = np.int32(
                utils.crush_hash32_rjenkins1_2(s_mod, engine_id))  # replace the pool no(original 3) with engine id
                
                osds = c.map(rule="default_rule", value=pps, replication_count=1)
                pg_id = pg_pri[osds[0]]
                pg_dict[pg_id] = True
                tmp_objs = self.obj_in_pg.get(pg_id, [])
                tmp_objs.append(obj)
                self.obj_in_pg[pg_id] = tmp_objs

            # max_objs = 0
            # min_objs = len(self.obj_in_pg[pg_pri[0]])

            # for pgid in pg_pri:
            #     len_objs = len(self.obj_in_pg[pgid])
            #     max_objs = max(max_objs, len_objs)
            #     min_objs = min(min_objs, len_objs)
            # avg_objs = float(len(objs)) / len(pg_pri)
            # logger.log("engine_to_pg_crush min/max/avg objs in pg:" + str(min_objs) + "/" + str(max_objs) + "/" + str(avg_objs))
            
            # missing_pgs = [pg for pg, value in pg_dict.items() if not value]
            # # logger.log("pg_pri number:" + str(len(pg_pri)) + " miss pgs number:" + str(len(missing_pgs)))
            # if len(missing_pgs) >= 3:
            #     logger.log("pg_pri number:" + str(len(pg_pri)) + " miss pgs number:" + str(len(missing_pgs)))
            #     # print("pg_pri", pg_pri)
            #     # print("missing pgs", missing_pgs)
            #     s_mods = {}
            #     ppss = {}
            #     pg_ids = {}
            #     # print(objs)
            #     # logger.log(pg_pri)
            #     # logger.log(engine_id)
            #     # logger.log(objs)
            #     for obj in objs:
            #         s_mod = hash(obj) % len(pg_pri)
            #         s_mods[s_mod] = True
            #         pps = np.int32(
            #         utils.crush_hash32_rjenkins1_2(s_mod, engine_id))  # replace the pool no(original 3) with engine id
            #         ppss[pps] = True
            #         osds = c.map(rule="default_rule", value=pps, replication_count=1)
            #         pg_id = pg_pri[osds[0]]   
            #         pg_ids[pg_id] = True
            #     print("pg_pri_num == len(s_mods) == len(ppss), pg_ids", pg_pri_num == len(s_mods) == len(ppss), len(pg_ids))

            # obj_counts = [len(objs) for pg_id, objs in self.obj_in_pg.items() if pg_id in pg_pri]
            # max_count = max(obj_counts) if obj_counts else 0
            # min_count = min(obj_counts) if obj_counts else 0
            # # if len(missing_pgs) != 0:
            # #     min_count = 0
            # avg_count = sum(obj_counts) / len(obj_counts) if obj_counts else 0
            # # logger.log("max/min/avg obj:" + str(max_count) + "/" + str(min_count) + "/" + str(avg_count))


    def engine_to_pg_strip(self):
        for engine_id, objs in self.obj_in_engine.items():
            # the pgs that take the osd corresponding to this engine as the primary osd
            pg_pri = self.pg_pri_in_osd.get(engine_id, [])
            current_pg_idx = 0
            for obj in objs:
                pg_id = pg_pri[current_pg_idx]
                tmp_objs = self.obj_in_pg.get(pg_id, [])
                tmp_objs.append(obj)
                self.obj_in_pg[pg_id] = tmp_objs
                current_pg_idx = (current_pg_idx + 1) % len(pg_pri)
    
    def print_pg_in_osd(self):
        max_pg_num = 0
        max_osdid = 0
        min_pg_num = sys.maxsize
        min_osdid = 0
        avg_pg_num = float(self.pg_num * self.replication_count) / self.disk_num
        for osd in range(self.disk_num):
            pg_num = len(self.pg_pri_in_osd[osd]) + len(self.pg_rep_in_osd[osd])
            if pg_num >= max_pg_num:
                max_pg_num = pg_num
                max_osdid = osd
            if pg_num <= min_pg_num:
                min_pg_num = pg_num
                min_osdid = osd
            # logger.log("(osd, pg num):" + str(osd) + "," + str(len(pgs)))
        logger.log("pg num in osd , MAX/MIN/AVG:" + str(max_pg_num) + "/" + str(min_pg_num) + "/" + str(avg_pg_num))
        logger.log("pg num in osd deviation, MAX/MIN:" + str(max_pg_num/avg_pg_num) + "/" + str(min_pg_num/avg_pg_num))
        logger.log("pg num in osd  MAX/MIN osd id:" + str(max_osdid) + "/" + str(min_osdid))
        return max_osdid, min_osdid

    def calc_obj_in_pg_deviation(self):
        max_obj = 0
        min_obj = len(self.obj_in_pg[0])
        obj_sum = 0
        for pgid, objs in self.obj_in_pg.items():
            obj_count = len(objs)
            max_obj = max(max_obj, obj_count)
            min_obj = min(min_obj, obj_count)
            obj_sum += obj_count
            # logger.log("pgid:" + str(pgid) + " object count:" + str(obj_count))
        avg_obj = float(obj_sum) / self.pg_num
        logger.log("objects in PGs MIN/MAX/AVG objects number: " + str(min_obj) + "/" + str(max_obj) + "/" + str(avg_obj))
        
        pg_counts = {pg: len(objs) for pg, objs in self.obj_in_pg.items()}
        filename = "./obj_in_pg_engine.csv"
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['PG id', 'Object Count'])
            for pgid, obj_count in pg_counts.items():
                writer.writerow([pgid, obj_count])
        # max_objects = max(pg_counts.values())
        # scale_factor = 50.0 / max_objects  # Adjust scale to fit your console width

        # for pg, num_objs in pg_counts.items():
        #     bar_length = int(num_objs * scale_factor)
        #     logger.log("PG {}: {} ({} objects)".format(pg, '*' * bar_length, num_objs))

    def calc_used_capacity_each_osd(self, max_osd_id, min_osd_id):
        obj_sum = 0
        obj_count_in_osd = {}
        for osd in self.engine_id:
            obj_count = 0
            pri_pgs = self.pg_pri_in_osd.get(osd, [])
            for pg in pri_pgs:
                objs = self.obj_in_pg.get(pg, [])
                obj_count += len(objs)
            rep_pgs = self.pg_rep_in_osd.get(osd, [])
            for pg in rep_pgs:
                objs = self.obj_in_pg.get(pg, [])
                obj_count += len(objs)

            obj_count_in_osd[osd] = obj_count
            obj_sum += obj_count
        # print("overall object sum:", obj_sum)
        overall_used_capacity = obj_sum*self.obj_size/(self.disk_num*self.disk_size*1024)
        print("overall used capacity:", overall_used_capacity)
        max_used_capacity = 0.0
        min_used_capacity = 1.0
        avg_used_capacity = float(obj_sum) / self.disk_num*self.obj_size/(self.disk_size*1024)
        
        for osd_id, obj_count in obj_count_in_osd.items():
            used_capacity = obj_count*self.obj_size/(self.disk_size*1024)
            # print("osd id:", osd_id, "used capacity:", used_capacity)
            max_used_capacity = max(max_used_capacity, used_capacity)
            min_used_capacity = min(min_used_capacity, used_capacity)
        print("max used capacity:", max_used_capacity, "min used capacity:", min_used_capacity)
        print("max used capacity deviation:", max_used_capacity/avg_used_capacity, "min used capacity deviation:", min_used_capacity/avg_used_capacity)
        
        print("max_pg_osd's used deviation:", float(obj_count_in_osd[max_osd_id]*self.obj_size/(self.disk_size*1024)) / avg_used_capacity)
        print("min_pg_osd's used deviation:", float(obj_count_in_osd[min_osd_id]*self.obj_size/(self.disk_size*1024)) / avg_used_capacity)

    def calc_obj_deviation_in_osd(self):
        obj_sum = 0
        obj_count_in_osd = {}
        for osd in self.engine_id:
            obj_count = 0
            pri_pgs = self.pg_pri_in_osd.get(osd, [])
            for pg in pri_pgs:
                objs = self.obj_in_pg.get(pg, [])
                obj_count += len(objs)
            rep_pgs = self.pg_rep_in_osd.get(osd, [])
            for pg in rep_pgs:
                objs = self.obj_in_pg.get(pg, [])
                obj_count += len(objs)

            obj_count_in_osd[osd] = obj_count
            obj_sum += obj_count

        print("overall object sum:", obj_sum)
        avg_obj = float(obj_sum) / self.engine_num

        max_dev = 1.0
        min_dev = 1.0
        for _, obj_count in obj_count_in_osd.items():
            dev = float(obj_count) / avg_obj
            max_dev = max(max_dev, dev)
            min_dev = min(min_dev, dev)
        logger.log("Objects in OSD MIN/MAX deviation: " + str(min_dev) + "/" + str(max_dev))

    def calc_obj_deviation_in_osd_with_new_rep(self, pg_rep_in_osd):
        obj_sum = 0
        obj_count_in_osd = {}
        for osd in self.engine_id:
            obj_count = 0
            pri_pgs = self.pg_pri_in_osd.get(osd, [])
            for pg in pri_pgs:
                objs = self.obj_in_pg.get(pg, [])
                obj_count += len(objs)
            rep_pgs = pg_rep_in_osd.get(osd, [])
            for pg in rep_pgs:
                objs = self.obj_in_pg.get(pg, [])
                obj_count += len(objs)

            obj_count_in_osd[osd] = obj_count
            obj_sum += obj_count

        avg_obj = float(obj_sum) / self.engine_num

        max_dev = 1.0
        min_dev = 1.0
        for _, obj_count in obj_count_in_osd.items():
            dev = float(obj_count) / avg_obj
            max_dev = max(max_dev, dev)
            min_dev = min(min_dev, dev)
        logger.log("Real Objects in OSD MIN/MAX deviation: " + str(min_dev) + "/" + str(max_dev))
        return max_dev - min_dev

    def calc_pri_obj_deviation_in_osd(self):
        obj_sum = 0
        obj_count_in_osd = {}
        for osd in self.engine_id:
            obj_count = 0
            pri_pgs = self.pg_pri_in_osd.get(osd, [])
            for pg in pri_pgs:
                objs = self.obj_in_pg.get(pg, [])
                obj_count += len(objs)

            obj_count_in_osd[osd] = obj_count
            obj_sum += obj_count

        avg_obj = float(obj_sum) / self.engine_num

        max_dev = 1.0
        min_dev = 1.0
        for _, obj_count in obj_count_in_osd.items():
            dev = float(obj_count) / avg_obj
            max_dev = max(max_dev, dev)
            min_dev = min(min_dev, dev)
        logger.log("Primary Objects in OSD MIN/MAX deviation: " + str(min_dev) + "/" + str(max_dev))

    def get_obj_count_in_osd(self):
        obj_count_in_osd = {}
        for osd, pgs in self.pg_in_osd.items():
            for pg in pgs:
                obj_count = obj_count_in_osd.get(osd, 0)
                obj_count += self.obj_count_in_pg.get(pg, 0)
                obj_count_in_osd[osd] = obj_count
        return obj_count_in_osd


logger = Logger("log-new.txt")

b = Balancer()
# disk_load = 12288  # GB
# inode_size = 4096
inode_size = 4096
# inode_num = int(b.disk_num * disk_load / inode_size / b.replication_count * 256)
disk_capacity = b.disk_num*b.disk_size #GB
overall_utilization = b.overall_used_capacity
obj_load_num = int(disk_capacity*overall_utilization*1024/b.replication_count/b.obj_size)
print("object load number:", obj_load_num)
inode_num = int(obj_load_num/inode_size)
print("inode number:", inode_num)
# each inode has {inode_size} blocks
# each block is a object
b.fill_engine(inode_num, inode_size)
# b.calc_engine_deviation()
b.fill_osd_with_pg()
print("start engine to pg crush")
b.engine_to_pg_naive_hash()
# b.engine_to_pg_crush()
# b.engine_to_pg_strip()

max_osdid, min_osd_id = b.print_pg_in_osd()
b.calc_engine_deviation()
b.calc_pg_in_osd_deviation()
b.calc_obj_in_pg_deviation()
b.calc_used_capacity_each_osd(max_osdid, min_osd_id)
# b.calc_obj_deviation_in_osd()
# b.calc_pri_obj_deviation_in_osd()

# pg_did, obj_dev, _ = b.do_upmap_by_pg()
# logger.log("pg upmap total_did:{}, obj_dev:{}".format(pg_did, obj_dev))

# total_did, _ = b.do_upmap_by_obj(0, 1.0)
# logger.log("obj upmap total_did:{}".format(total_did))


 