(function() {
    function findIframe(frameElement) {
        var iframeList = document.querySelectorAll('iframe');

        for (var i = 0; i < iframeList.length; ++i) {
            if (iframeList[i].contentWindow === frameElement) {
                return iframeList[i];
            }
        }
    }

    function receiveMessage(e) {
        try {
            var data = JSON.parse(e.data);
            var height = data['iframe-height'];
            var iframe;

            if (height && (iframe = findIframe(e.source))) {
                iframe.style.height = height + 'px';
            }
        } catch (err) {
        }
    }

    window.addEventListener('message', receiveMessage, false);
})();
