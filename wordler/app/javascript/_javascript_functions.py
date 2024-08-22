"""JavaScript functions used in clientside callbacks"""

boxIds = """
    /**
     * Element IDs for letter inputs in initial guess row.
     */
    const boxIds = [
        '{"index":"11","type":"letter"}',
        '{"index":"12","type":"letter"}',
        '{"index":"13","type":"letter"}',
        '{"index":"14","type":"letter"}',
        '{"index":"15","type":"letter"}',
    ];
"""

getCurrentIndex = """
    /**
     * Gets index of first empty input in initial guess row.
     * @param  {number} val1 Value of first input in row.
     * @param  {number} val2 Value of second input in row.
     * @param  {number} val3 Value of third input in row.
     * @param  {number} val4 Value of fourth input in row.
     * @param  {number} val5 Value of fifth input in row.
     * @return {number}      Index of first empty input.
     */
    function(val1, val2, val3, val4, val5) {
        let vals = [val1, val2, val3, val4, val5];
        let currentIndex = vals.indexOf(undefined);
        if (currentIndex === -1) {
            return vals.length - 1;
        }
        return currentIndex
    }
"""


getPreviousIndex = """
    /**
     * Gets index of last non-empty input in inital guess guess row
     * based on value returned by getCurrentIndex.
     * @param  {number} indexValue Index of first empty input in row.
     * @return {number}            Index of last non-empty input.
     */
    function(indexValue) {
        if (indexValue === 0) {
            return null;
        } else {
            return indexValue - 1;
        }
    }
"""


printIndex = """
    /**
     * Prints value to console.
     * @param {number} indexValue Value to be printed to console.
     */
    function(indexValue) {
        console.log(indexValue);
    }
"""


focusIndex = """
    /**
     * Focuses on input at given index and blurs all other inputs.
     * @param {number} indexValue Index corresponding to input to focus on.
     */
    function(indexValue) {
        %s
        boxIds.forEach((boxId, i) => {
            if (i === indexValue) {
                document.getElementById(boxId).focus();
            } else {
                document.getElementById(boxId).blur();
            }
        })
    }
""" % boxIds


startEventListener = """
    /**
     * Spawns event listeners for handling backspace events in initial guess row.
     * @param {number} currentIndex  Index corresponding to focused input.
     * @param {number} previousIndex Index corresponding to input before focused input.
     */
    function(currentIndex, previousIndex) {
        %s
        let currentBox = document.getElementById(boxIds[currentIndex]);
        let previousBox = document.getElementById(boxIds[previousIndex]);
        currentBox.addEventListener('keydown', (event) => {
            if (event.key === 'Backspace' || event.key === 'Delete') {
                if (currentBox.value === '') {
                    previousBox.value = '';
                }
            }
        })
    }
""" % boxIds
