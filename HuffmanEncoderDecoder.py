#!/usr/bin/python
# -*- coding: "windows-1252"
import ast
import struct
import collections
import heapq
import sys
import io

##File Compressor. Input path of your .txt file. 
def Compressor(path):
    with io.open(path,"rU",encoding='windows-1252') as f:
        data=f.read()
        order=list(data)
        freq=collections.Counter(data)
    heapTree=[]
    for each in freq:
        heapTree.append([freq[each],[each,""]])

    #huffman tree creator for compressor
    heapq.heapify(heapTree)
    while len(heapTree) != 1:
        lower = heapq.heappop(heapTree)
        higher = heapq.heappop(heapTree)
        for indexed in lower[1:]:
            indexed[1] = '0' + indexed[1]
        for indexed in higher[1:]:
            indexed[1] = '1' + indexed[1]
        heapq.heappush(heapTree, [lower[0] + higher[0]] + lower[1:] + higher[1:])
    print(heapTree[0][1:])
    heapTree=heapTree[0][1:]
    heapTreeDict={}

    for each in heapTree:
        heapTreeDict[each[0]]=each[1]

    indList = heapTreeDict

    print("Tree created..")

    res=""
    for each in order:
        res+=indList[each]

    real=res
    bitArr=[res[i:i+63] for i in range(0, len(res), 63)]
    for each in range(len(bitArr)):
        bitArr[each]="1"+bitArr[each]
    print("prep to be written..")

    with open(path[:-3]+"hc", "wb") as f:
        di={}
        for each in freq:
            di[each]=freq[each]
        tbw=str(di).encode("windows-1252")
        f.write(tbw+"!".encode("windows-1252"))

    with open(path[:-3]+"hc", "ab") as f:
        for each in bitArr:
            f.write(struct.pack('Q', int(each,2)))

    print("struct..")

#canonical Huffman Tree Maker. gets the tree order from the compressed file and recreates the tree again.
def resIndex(freq):
    heapTree=[]
    for each in freq:
        heapTree.append([freq[each],[each,""]])

    heapq.heapify(heapTree)
    while len(heapTree) != 1:
        lower = heapq.heappop(heapTree)
        higher = heapq.heappop(heapTree)
        for indexed in lower[1:]:
            indexed[1] = '0' + indexed[1]
        for indexed in higher[1:]:
            indexed[1] = '1' + indexed[1]
        heapq.heappush(heapTree, [lower[0] + higher[0]] + lower[1:] + higher[1:])
    heapTree=heapTree[0][1:]
    heapTreeDict={}

    for each in heapTree:
        heapTreeDict[each[1]]=each[0]

    print("Reconstructing the heap tree..")
    return heapTreeDict

#final decoder, string recreation and writing on file again.
def decoder(resStr,indexData,path):
    print(indexData)
    orderDir=resIndex(indexData)
    finishStr=""
    with open(path[:-2]+"txt", "wb") as f:
        for each in resStr:
            finishStr+=each
            if finishStr in orderDir:
                f.write(orderDir[finishStr].encode("windows-1252"))
                finishStr=""

                
##Decompressor Alg. Input the path of your file to be decompressed.                
def Decompresor(path):
    with open(path, "rb") as f:
        f.seek(0)
        start=f.read().index("}!".encode("windows-1252"))+2
        f.seek(0)
        indexData=f.read(start-1).decode("windows-1252")
    print("read")
    
    with open(path, "rb") as f:
        limit=len(f.read())
        resStr=""
        f.seek(start)
        while f.tell()!=limit:
            resStr+=bin(struct.unpack("Q",f.read(8))[0])[2:]
    print("destruct")
    resArr=[resStr[i:i+64] for i in range(0, len(resStr), 64)]

    for each in range(len(resArr)):
        resArr[each]=resArr[each][1:]

    resStr="".join(resArr)
    indexData=ast.literal_eval(indexData)
    decoder(resStr,indexData,path)

if sys.argv[1]=="compress":
    Compressor(sys.argv[2])
elif sys.argv[1]=="decompress":
    Decompresor(sys.argv[2])
else:
    print("Invalid Argument provided. Try 'python encoderDecoder.py compress textFileName.txt' or 'python encoderDecoder.py decompress textFileName.hc'")
