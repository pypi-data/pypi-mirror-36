cimport numpy as np
from libc.stdlib import size_t
from libc.stdio cimport FILE


cdef extern from "common.h":
    ctypedef np.int32_t boolean
    ctypedef np.uint16_t bits16
    ctypedef np.uint32_t bits32
    ctypedef np.uint64_t bits64

    int sameString(char *a, char *b)
    FILE *mustOpen(char *fileName, char *mode)
    void carefulClose(FILE **pFile)


cdef extern from "localmem.h":
    cdef struct lm:
        size_t blockSize
        size_t allignMask
        size_t allignAdd

    lm *lmInit(int blockSize)
    void lmCleanup(lm **pLm)


cdef extern from "bbiFile.h":
    cdef struct bbiInterval:
        bbiInterval *next
        bits32 start, end
        double val

    cdef struct bbiChromInfo:
        bbiChromInfo *next
        char *name
        bits32 id, size

    cdef struct bbiFile:
        bbiFile *next
        char *fileName
        #udcFile *udc
        #bptFile *chromBpt
        #cirTreeFile *unzoomedCir
        #bbiZoomLevel *levelList
        boolean isSwapped
        bits32 typeSig
        bits16 version
        bits16 zoomLevels
        bits64 chromTreeOffset
        bits64 unzoomedDataOffset
        bits64 unzoomedIndexOffset
        bits16 fieldCount
        bits16 definedFieldCount
        bits64 asOffset
        bits64 totalSummaryOffset
        bits32 uncompressBufSize
        bits64 extensionOffset
        bits16 extensionSize
        bits16 extraIndexCount
        bits64 extraIndexListOffset
    
    bbiChromInfo *bbiChromList(bbiFile *bbi)
    void bbiFileClose(bbiFile **pBwf)
    void bbiChromInfoFreeList(bbiChromInfo **pList)
    

cdef extern from "bigWig.h":
    bbiFile *bigWigFileOpen(char *fileName)
    bbiInterval *bigWigIntervalQuery(bbiFile *bwf, char *chrom, bits32 start, bits32 end, lm *lm)