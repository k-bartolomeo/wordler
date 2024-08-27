"""JavaScript functions used in clientside callbacks"""


keyListener = """
    /**
     * Adds global 'keydown' listener for updating dcc.Store(id='last-key')
     * @param {String} id Arbitrary input value for Dash callback.
     */
    function(id) {
        document.addEventListener('keydown', (event) => {
            let letters = 'abcdefghijklmnopqrstuvwxyz'.split('');
            ['Backspace', 'Delete'].map((letter) => letters.push(letter));
            if (letters.includes(event.key)) {
                dash_clientside.set_props('last-key', {data: event.key});
            }
        })
        return dash_clientside.no_update;
    }
    """
