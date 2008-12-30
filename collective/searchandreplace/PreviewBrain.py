from Proxy import Proxy

MAX_PRE_TEXT_LEN = 25
MAX_TEXT_LEN = 50
MAX_POST_TEXT_LEN = 25

class PreviewBrain( Proxy ):
    """ Defines the following attributes in addition to proxying the brain object:
            beginIndex: beginning character index of the match
            beforeEndIndex: ending character index of the match
            afterEndIndex: ending character index in the string after replacement
            beginPosition: (row, column) tuple of the position of the beginIndex
            beforeEndPosition: (row, column) tuple of the position of the beforeEndIndex
            afterEndPosition: (row, column) tuple of the position of the afterEndIndex
            beforeText: 5 element tuple to be used in previewing the match.  For example,
                        ('','out of the ','frying pan',' into the f','...')
            afterText: 5 element tuple to be used in previewing the replacement.  For example,
                        ('','out of the ','round metal object',' into the f','...')
    """
    
    def __init__(self, request, brain, matchIndex, matchObject, replacement, maxPreTextLen=MAX_PRE_TEXT_LEN,
        maxTextLen=MAX_TEXT_LEN, maxPostTextLen=MAX_POST_TEXT_LEN,
        beforeInContext=True, afterInContext=True):
        Proxy.__init__(self, brain)
        self.brain = brain
        self.matchIndex = matchIndex
        self.REQUEST = request
        self.maxPreTextLen = maxPreTextLen
        self.maxTextLen = maxTextLen
        self.maxPostTextLen = maxPostTextLen
        self.extractPreview(matchObject, replacement, beforeInContext, afterInContext)
        
    def extractPreview(self, matchObject, replacement, beforeInContext=True, afterInContext=True):
        (self.beginIndex, self.beforeEndIndex) = matchObject.span()
        #print "beginIndex: %d" % self.beginIndex
        beforeContent = matchObject.string
        replacement = matchObject.expand(replacement)
        afterContent = beforeContent[:self.beginIndex] + replacement + beforeContent[self.beforeEndIndex:]
        self.afterEndIndex = self.beforeEndIndex + (len(afterContent) - len(beforeContent))
        self.beginPosition = self.getLineAndColumn(beforeContent, self.beginIndex)
        self.beforeEndPosition = self.getLineAndColumn(beforeContent, self.beforeEndIndex)
        self.afterEndPosition = self.getLineAndColumn(afterContent, self.afterEndIndex)
        self.beforeText = self.extractPreviewText(beforeContent, 
            self.beginIndex, self.beforeEndIndex, self.beginPosition, self.beforeEndPosition, beforeInContext)
        self.afterText = self.extractPreviewText(afterContent, 
            self.beginIndex, self.afterEndIndex, self.beginPosition, self.afterEndPosition, afterInContext)
        #print "beforeText: %s" % str(self.beforeText)
        
    def getLineAndColumn(self, content, index):
        line = content[:index].count('\n')
        beginOfLine = content.rfind('\n', 0, index) + 1
        column = index - beginOfLine
        return (line, column)
        
    def extractPreviewText(self, content, beginIndex, endIndex, beginPosition, endPosition, inContext=True):
        if inContext:
            if (beginPosition[0] == endPosition[0]):
                # same line--only show preview text from this line
                beginOfLine = content.rfind('\n', 0, beginIndex)+1
                endOfLine = content.find('\n', endIndex)
                if endOfLine < 0:
                    endOfLine = len(content)
                content = content[beginOfLine:endOfLine]
                #print "beginIndex: %d, beginOfLine: %d" % (beginIndex, beginOfLine)
                beginIndex = beginIndex - beginOfLine
                endIndex = endIndex - beginOfLine
        
            startEllipsis = endEllipsis = '...'
            previewBeginIndex = beginIndex - self.maxPreTextLen
            if previewBeginIndex < 0: 
                previewBeginIndex = 0
                startEllipsis = ''
            previewEndIndex = endIndex + self.maxPostTextLen
            if previewEndIndex > len(content): 
                previewEndIndex = len(content)
                endEllipsis = ''
        
            preText = content[previewBeginIndex:beginIndex]
            postText = content[endIndex:previewEndIndex]
        else:
            startEllipsis = endEllipsis = preText = postText = ''

        text = content[beginIndex:endIndex]
        if len(text) > self.maxTextLen:
            halfMaxTextLen = self.maxTextLen//2
            text = text[:halfMaxTextLen] + '...' + text[(len(text)-halfMaxTextLen):]
        
        #print "beginIndex: %d, endIndex, %d, text: %s" % (beginIndex, endIndex, text)
        return (startEllipsis, preText, text, postText, endEllipsis)
        
#    def getURL(self, relative=0):
#        """Generate a URL for this record"""
#        # XXX The previous implementation attempted to eat errors coming from
#        #     REQUEST.physicalPathToURL. Unfortunately it also ate 
#        #     ConflictErrors (from getPath), which is bad. Staring at the 
#        #     relevent code in HTTPRequest.py it's unclear to me what could be 
#        #     raised by it so I'm removing the exception handling here all 
#        #     together. If undesired exceptions get raised somehow we should 
#        #     avoid bare except band-aids and find a real solution.
#        return self.REQUEST.physicalPathToURL(self.getPath(), relative)

    def getPath(self):
        return "%s[%d]" % (self.brain.getPath(), self.matchIndex)
