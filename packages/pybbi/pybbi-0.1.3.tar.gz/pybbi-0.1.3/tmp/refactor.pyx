def listChroms():
    pass


def listZooms():
    pass


cdef bigWigSummaryQuery(bwf, chromName, start, end, nbins):
    if start >= end:
        return result
    cdef bits32 baseSize = end - start ## converts start to uint32!!!
    cdef int fullReduction = baseSize//nbins

    # Get the closest zoom level less than what we're looking for
    cdef int zoomLevel = fullReduction//2
    if zoomLevel < 0:
        zoomLevel = 0
    cdef bbiZoomLevel *zoomObj = bbiBestZoom(bbi.levelList, zoomLevel)

    # Create summary elements
    cdef bbiSummaryElement *elements
    AllocArray(elements, nbins)

    # Populate summary elements
    cdef boolean result = False
    if zoomObj != NULL:
        result = _summarizeFromZoom(zoomObj, bbi, chrom, start, end, nbins, elements)
    else
        result = _summarizeFromFull(bbi, chrom, start, end, bigWigIntervalQuery, nbins, elements)

    return elements


cdef boolean _summarizeFromZoom(
    bbiZoomLevel *zoom,
    bbiFile *bbi, 
    char *chrom, 
    bits32 start, 
    bits32 end,
    int nbins, 
    bbiSummaryElement *elements):
    # Look up region in index and get data at given zoom level.
    # Summarize this data in the summary array.

    cdef boolean result = False
    cdef int chromId = bbiChromId(bbi, chrom)
    if chromId < 0:
        return False

    # Find appropriate summary elements
    bbiSummary *sum, *sumList = bbiSummariesInRegion(zoom, bbi, chromId, start, end)

    if sumList != NULL:
        cdef int i
        cdef bits32 baseStart = start, baseEnd
        cdef bits32 baseCount = end - start
        cdef sum = sumList
        for i in range(nbins):
            # Calculate end of this part of summary
            baseEnd = start + (bits64)baseCount*(i+1) // nbins

            # Advance sum to skip over parts we are no longer interested in.
            while sum != NULL and sum.end <= baseStart:
                sum = sum.next

            # Update element[i]
            if bbiSummarySlice(bbi, baseStart, baseEnd, sum, &elements[i]):
                result = True

            # Next time round start where we left off.
            baseStart = baseEnd

    slFreeList(&sumList)

    return result


cdef boolean _summarizeFromFull(
    bbiFile *bbi, 
    char *chrom, 
    bits32 start, 
    bits32 end, 
    BbiFetchIntervals fetchIntervals,
    int nbins, 
    struct bbiSummaryElement *elements):
    # Summarize data, not using zoom. Updates the summary elements.

    boolean result = False

    # Find appropriate interval elements
    lm *lm = lmInit(0)
    
    bbiInterval *intervalList = NULL
    bbiInterval *interval
    intervalList = (*fetchIntervals)(bbi, chrom, start, end, lm)
    if intervalList != NULL:
        int i
        cdef bits32 baseStart = start, baseEnd
        cdef bits32 baseCount = end - start
        interval = intervalList
        for i in range(nbins):
            # Calculate end of this part of summary
            baseEnd = start + (bits64)baseCount*(i+1) // nbins
            int end1 = baseEnd
            if end1 == baseStart:
                end1 = baseStart+1

            # Advance interval to skip over parts we are no longer interested in.
            while interval != NULL  and interval.end <= baseStart:
                interval = interval.next

            # Update element[i]
            if bbiIntervalSlice(bbi, baseStart, end1, interval, &elements[i]):
                result = True

            # Next time round start where we left off.
            baseStart = baseEnd
        
    lmCleanup(&lm)

    return result


cdef inline fetch_summarized(
        np.ndarray[np.double_t, ndim=1] out,
        bbiFile *bbi,
        char *chromName,
        int start,
        int end,
        int nbins,
        double missing,
        double oob):
    
    # Create summary elements array
    cdef bbiSummaryElement *elements = bigWigSummaryQuery(bwf, chromName, start, end, nbins)

    # Fill array
    out = np.zeros(length, dtype=float)
    if result:
        cdef int i
        cdef double covFactor = (double)summarySize / (end - start)
        for i in range(nbins):
            cdef bbiSummaryElement *el = &elements[i]
            if el.validCount > 0:
                cdef double val
                if summaryType == bbiSumMean:
                    val = el.sumData / el.validCount
                elif summaryType == bbiSumMax:
                    val = el.maxVal
                elif summaryType == bbiSumMin:
                    val = el.minVal
                elif summaryType == bbiSumCoverage:
                    val = covFactor * el.validCount
                elif summaryType == bbiSumStandardDeviation:
                    val = calcStdFromSums(el.sumData, el.sumSquares, el.validCount)
                else:
                    raise RuntimeError()
            out[i] = val

    # deal with boundary conditions?
    # ...

    # Delete summary elements
    freeMem(elements)


cdef inline fetch_full(
        np.ndarray[np.double_t, ndim=1] out, 
        bbiFile *bwf, 
        char *chromName, 
        int start, 
        int end,
        int refStart, 
        int chromSize, 
        double missing, 
        double oob):

    cdef lm *lm = lmInit(0)

    cdef bbiInterval *interval = bigWigIntervalQuery(bwf, chromName, start, end, lm)
    cdef boolean firstTime = True
    cdef int saveStart = -1, prevEnd = -1
    cdef double saveVal = -1.0

    while interval != NULL:
        if firstTime:
            saveStart = interval.start
            saveVal = interval.val
            firstTime = False
        elif not ( (interval.start == prevEnd) and (interval.val == saveVal) ):
            out[saveStart-refStart:prevEnd-refStart] = saveVal
            saveStart = interval.start
            saveVal = interval.val
        prevEnd = interval.end
        interval = interval.next

    if not firstTime:
       out[saveStart-refStart:prevEnd-refStart] = saveVal

    if refStart < start:
        out[:(start-refStart)] = oob
    if end >= chromSize:
        out[(chromSize - refStart):] = oob

    lmCleanup(&lm)


def query(
        str inFile,
        str chrom,
        int start,
        int end,
        int nbins,
        double missing=0.0,
        double oob=np.nan):
    """
    """
    cdef bytes bInFile = inFile.encode('utf-8')
    cdef char *cInFile = bInFile
    cdef bbiFile *bwf = bigWigFileOpen(cInFile)

    cdef bytes bChrom = chrom.encode('utf-8')
    cdef char *cChrom = bChrom
    if bbiChromId(bwf, cChrom) == -1:
        raise KeyError("Chromosome not found: {}".format(chrom))

    cdef int refStart, length
    refStart = start
    if start < 0:
        start = 0
    if end < 0:
        end = chromInfo.size
    length = end - refStart
    if length < 0:
        raise ValueError(
            "Interval cannot have negative length:"
            " start = {}, end = {}.".format(start, end))
    
    out = fetcher(bwf, chromObj.name, start, end, missing, oob)

    bbiChromInfoFreeList(&chromInfo)
    bbiFileClose(&bwf)

    return out


def multiquery(
        str inFile, 
        np.ndarray[object, ndim=1] chroms,
        np.ndarray[np.int_t, ndim=1] starts,
        np.ndarray[np.int_t, ndim=1] ends,
        double missing=0.0,
        double oob=np.nan):
    """
    Vertically stack equal-length bigwig intervals.

    """
    cdef bytes bInFile = inFile.encode('utf-8')
    cdef char *cInFile = bInFile
    cdef bbiFile *bwf = bigWigFileOpen(cInFile)
    
    cdef int n = chroms.shape[0]
    cdef length = ends[0] - starts[0]
    if not len(np.unique(ends - starts)) == 1:
        raise ValueError("Windows must have equal size")

    cdef bytes bChrom
    cdef char *cChrom
    for chrom in np.unique(chroms):
        bChrom = chrom.encode('utf-8')
        cChrom = bChrom
        if bbiChromId(bwf, cChrom) == -1:
            raise KeyError("Chromosome not found: {}".format(chrom))

    out = fetcher(bwf, chromLookup, starts, ends, missing, oob)

    bbiChromInfoFreeList(&chromList)
    bbiFileClose(&bwf)

    return out

